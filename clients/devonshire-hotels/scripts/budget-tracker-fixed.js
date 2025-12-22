const SHEET_URL = 'https://docs.google.com/spreadsheets/d/1hfshBOXryp0LYuU40kE9HKHQocoinfpXZH8TL6Me7Yc/edit?gid=0#gid=0';

function main() {
  try {
    // Get current date for comparison
    const currentDate = new Date();
    const yesterday = new Date(currentDate);
    yesterday.setDate(yesterday.getDate() - 1);

    // Force all dates to GMT/UTC
    const timezone = 'GMT';

    // Get the spreadsheet
    const ss = SpreadsheetApp.openByUrl(SHEET_URL);
    const sheet = ss.getSheets()[0];

    // Clear all background colors first
    const dataRange = sheet.getDataRange();
    dataRange.setBackground(null);

    // Get all data from the sheet
    const data = sheet.getDataRange().getValues();
    const headers = data[0].map(header => header.trim());

    // Find the column indices
    const startPeriodCol = headers.indexOf('Start Date');
    const endPeriodCol = headers.indexOf('End Date');
    const budgetCol = headers.indexOf('Budget');

    if (startPeriodCol === -1 || endPeriodCol === -1 || budgetCol === -1) {
      Logger.log('ERROR: Required columns not found in spreadsheet');
      return;
    }

    // Check if "Daily Pace" exists and rename it to "Req Daily Budget"
    const dailyPaceCol = headers.indexOf('Daily Pace');
    if (dailyPaceCol !== -1) {
      sheet.getRange(1, dailyPaceCol + 1).setValue('Req Daily Budget');
    }

    // Add new headers if they don't exist
    const newHeaders = [
      'Total Days',
      'Days Elapsed',
      'Days Remaining',
      'Spend',
      'Expected Spend',
      'Remaining Budget',
      'Req Daily Budget',
      'Pacing Percentage',
      'Predicted Spend',
      'Yesterday Spend'
    ];

    // Check which new headers need to be added
    const existingNewHeaders = newHeaders.filter(header => headers.includes(header));
    const headersToAdd = newHeaders.filter(header => !headers.includes(header));

    if (headersToAdd.length > 0) {
      // Add new headers
      const lastCol = sheet.getLastColumn();
      sheet.getRange(1, lastCol + 1, 1, headersToAdd.length).setValues([headersToAdd]);
    }

    // Get updated headers after adding new ones
    const updatedHeaders = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];

    // Find column indices for new columns
    const totalDaysCol = updatedHeaders.indexOf('Total Days');
    const daysElapsedCol = updatedHeaders.indexOf('Days Elapsed');
    const daysRemainingCol = updatedHeaders.indexOf('Days Remaining');
    const spendCol = updatedHeaders.indexOf('Spend');
    const expectedSpendCol = updatedHeaders.indexOf('Expected Spend');
    const remainingBudgetCol = updatedHeaders.indexOf('Remaining Budget');
    const reqDailyBudgetCol = updatedHeaders.indexOf('Req Daily Budget');
    const pacingPercentageCol = updatedHeaders.indexOf('Pacing Percentage');
    const predictedSpendCol = updatedHeaders.indexOf('Predicted Spend');
    const yesterdaySpendCol = updatedHeaders.indexOf('Yesterday Spend');

    // Process each row (skip header row)
    for (let i = 1; i < data.length; i++) {
      const row = data[i];
      const budget = Number(row[budgetCol]);

      // Skip if budget is 0 or invalid
      if (!budget || isNaN(budget)) {
        Logger.log(`Skipping row ${i + 1}: Invalid budget`);
        continue;
      }

      // Convert dates to local timezone and ensure correct date handling
      const startPeriod = new Date(row[startPeriodCol]);
      const endPeriod = new Date(row[endPeriodCol]);

      // Validate dates
      if (isNaN(startPeriod.getTime()) || isNaN(endPeriod.getTime()) ||
          startPeriod.getFullYear() < 2000 || endPeriod.getFullYear() < 2000) {
        Logger.log(`Skipping row ${i + 1}: Invalid dates`);
        continue;
      }

      // Adjust for timezone offset in the spreadsheet values
      const localStartPeriod = new Date(startPeriod);
      localStartPeriod.setDate(localStartPeriod.getDate() + 1);

      const localEndPeriod = new Date(endPeriod);
      localEndPeriod.setDate(localEndPeriod.getDate() + 1);

      Logger.log(`\nProcessing row ${i + 1}:`);
      Logger.log(`Start Period: ${Utilities.formatDate(localStartPeriod, timezone, 'yyyy-MM-dd')}`);
      Logger.log(`End Period: ${Utilities.formatDate(localEndPeriod, timezone, 'yyyy-MM-dd')}`);
      Logger.log(`Budget: ${budget}`);

      // Check if date range is in the future
      if (localStartPeriod > currentDate) {
        Logger.log(`Skipping row ${i + 1}: Start date is in the future`);
        continue;
      }

      // Check if period has expired
      if (localEndPeriod < currentDate) {
        Logger.log(`Period has expired for row ${i + 1}, using end date for calculations`);
        // Use end date instead of current date for expired periods
        const endDateMidnight = new Date(Date.UTC(localEndPeriod.getFullYear(), localEndPeriod.getMonth(), localEndPeriod.getDate()));
        const startDateMidnight = new Date(Date.UTC(localStartPeriod.getFullYear(), localStartPeriod.getMonth(), localStartPeriod.getDate()));

        // For expired periods, days elapsed is the total days
        const expiredTotalDays = Math.floor((endDateMidnight - startDateMidnight) / (1000 * 60 * 60 * 24)) + 1;
        const expiredDaysElapsed = expiredTotalDays;
        const expiredDaysRemaining = 0;

        // Get spend for the entire period - FIXED: Now uses GAQL
        const formattedStartDate = Utilities.formatDate(localStartPeriod, timezone, 'yyyy-MM-dd');
        const formattedEndDate = Utilities.formatDate(localEndPeriod, timezone, 'yyyy-MM-dd');

        let expiredTotalSpend = getSpendForPeriod(formattedStartDate, formattedEndDate);

        // For expired periods, expected spend equals budget
        const expiredExpectedSpend = budget;
        const expiredRemainingBudget = budget - expiredTotalSpend;
        const expiredDailyPace = 0;
        const expiredPredictedSpend = expiredTotalSpend;

        // Calculate pacing percentage for expired period
        const expiredPacingPercentage = budget > 0 ? (expiredTotalSpend / budget) * 100 : 0;

        // Update each calculated column individually
        sheet.getRange(i + 1, totalDaysCol + 1, 1, 1).setValue(expiredTotalDays);
        sheet.getRange(i + 1, daysElapsedCol + 1, 1, 1).setValue(expiredDaysElapsed);
        sheet.getRange(i + 1, daysRemainingCol + 1, 1, 1).setValue(expiredDaysRemaining);
        sheet.getRange(i + 1, spendCol + 1, 1, 1).setValue(expiredTotalSpend);
        sheet.getRange(i + 1, expectedSpendCol + 1, 1, 1).setValue(expiredExpectedSpend);
        sheet.getRange(i + 1, remainingBudgetCol + 1, 1, 1).setValue(expiredRemainingBudget);
        sheet.getRange(i + 1, reqDailyBudgetCol + 1, 1, 1).setValue(expiredDailyPace);
        sheet.getRange(i + 1, pacingPercentageCol + 1, 1, 1).setValue(expiredPacingPercentage / 100);
        sheet.getRange(i + 1, predictedSpendCol + 1, 1, 1).setValue(expiredPredictedSpend);
        sheet.getRange(i + 1, yesterdaySpendCol + 1, 1, 1).setValue(0);

        continue;
      }

      // Create dates at midnight in GMT for accurate day counting
      const startDate = new Date(Date.UTC(localStartPeriod.getFullYear(), localStartPeriod.getMonth(), localStartPeriod.getDate()));
      const yesterdayDate = new Date(Date.UTC(yesterday.getFullYear(), yesterday.getMonth(), yesterday.getDate()));
      const endDate = new Date(Date.UTC(localEndPeriod.getFullYear(), localEndPeriod.getMonth(), localEndPeriod.getDate()));

      // Calculate period metrics
      const totalDays = Math.floor((endDate - startDate) / (1000 * 60 * 60 * 24)) + 1;
      const daysElapsed = Math.max(0, Math.floor((yesterdayDate - startDate) / (1000 * 60 * 60 * 24)) + 1);
      const daysRemaining = Math.max(0, totalDays - daysElapsed);

      // Get spend for the period - FIXED: Now uses GAQL
      const formattedStartDate = Utilities.formatDate(localStartPeriod, timezone, 'yyyy-MM-dd');
      const formattedEndDate = Utilities.formatDate(yesterday, timezone, 'yyyy-MM-dd');

      let totalSpend = getSpendForPeriod(formattedStartDate, formattedEndDate);

      // Calculate pacing metrics
      const dailyBudget = budget / totalDays;
      const expectedSpend = dailyBudget * daysElapsed;
      const remainingBudget = budget - totalSpend;
      const dailyPace = daysRemaining > 0 ? remainingBudget / daysRemaining : 0;

      // Get yesterday's spend
      const yesterdayFormatted = Utilities.formatDate(yesterday, timezone, 'yyyy-MM-dd');
      let yesterdaySpend = getSpendForDate(yesterdayFormatted);

      Logger.log(`Current Period Calculations:`);
      Logger.log(`1. Budget Distribution:`);
      Logger.log(`   Total Budget: £${budget.toFixed(2)}`);
      Logger.log(`   Total Days: ${totalDays} days`);
      Logger.log(`   Daily Budget: £${dailyBudget.toFixed(2)}`);
      Logger.log(`2. Expected Spend:`);
      Logger.log(`   Days Elapsed: ${daysElapsed} days`);
      Logger.log(`   Expected Spend: £${expectedSpend.toFixed(2)}`);
      Logger.log(`3. Actual Spend:`);
      Logger.log(`   Total Spend: £${totalSpend.toFixed(2)}`);
      Logger.log(`   Remaining Budget: £${remainingBudget.toFixed(2)}`);
      Logger.log(`4. Yesterday's Spend: £${yesterdaySpend.toFixed(2)}`);

      // Calculate predicted spend
      let predictedSpend = 0;
      if (daysRemaining > 0) {
        predictedSpend = totalSpend + (yesterdaySpend * daysRemaining);
      } else {
        predictedSpend = totalSpend;
      }

      Logger.log(`5. Final Prediction:`);
      Logger.log(`   Predicted Spend: £${predictedSpend.toFixed(2)}`);
      Logger.log(`   Budget Variance: £${(predictedSpend - budget).toFixed(2)}`);

      // Calculate pacing percentage
      const pacingPercentage = expectedSpend > 0 ? (totalSpend / expectedSpend) * 100 : 0;

      // Update spreadsheet
      sheet.getRange(i + 1, totalDaysCol + 1, 1, 1).setValue(totalDays);
      sheet.getRange(i + 1, daysElapsedCol + 1, 1, 1).setValue(daysElapsed);
      sheet.getRange(i + 1, daysRemainingCol + 1, 1, 1).setValue(daysRemaining);
      sheet.getRange(i + 1, spendCol + 1, 1, 1).setValue(totalSpend);
      sheet.getRange(i + 1, expectedSpendCol + 1, 1, 1).setValue(expectedSpend);
      sheet.getRange(i + 1, remainingBudgetCol + 1, 1, 1).setValue(remainingBudget);
      sheet.getRange(i + 1, reqDailyBudgetCol + 1, 1, 1).setValue(dailyPace);
      sheet.getRange(i + 1, pacingPercentageCol + 1, 1, 1).setValue(pacingPercentage / 100);
      sheet.getRange(i + 1, predictedSpendCol + 1, 1, 1).setValue(predictedSpend);
      sheet.getRange(i + 1, yesterdaySpendCol + 1, 1, 1).setValue(yesterdaySpend);

      // Highlight row based on pacing
      const rowRange = sheet.getRange(i + 1, 1, 1, sheet.getLastColumn());
      if (pacingPercentage > 100) {
        rowRange.setBackground('#ffebee'); // Light red for over pacing
      } else {
        rowRange.setBackground('#e8f5e9'); // Light green for under pacing
      }
    }

    // Format the sheet
    formatSheet(sheet, updatedHeaders);

    // Create daily spend graph
    createDailySpendGraph(ss, currentDate, yesterday, timezone);

    Logger.log('Budget pacing calculations completed successfully.');

  } catch (error) {
    Logger.log('Error: ' + error.message);
    Logger.log('Stack trace: ' + error.stack);
    throw error;
  }
}

// ============================================================================
// FIXED: Helper function to get spend for a date range using GAQL (not AWQL)
// ============================================================================
function getSpendForPeriod(startDate, endDate) {
  try {
    Logger.log(`Getting spend for period: ${startDate} to ${endDate}`);

    // GAQL syntax (Google Ads Query Language - replaces deprecated AWQL)
    const query = `
      SELECT
        campaign.name,
        metrics.cost_micros
      FROM campaign
      WHERE segments.date BETWEEN '${startDate}' AND '${endDate}'
        AND campaign.name LIKE '%properties%'
        AND campaign.name NOT LIKE '%Highwayman%'
        AND campaign.name NOT LIKE '%The Hide%'
        AND metrics.cost_micros > 0
    `;

    let totalSpend = 0;
    const report = AdsApp.report(query);
    const rows = report.rows();

    while (rows.hasNext()) {
      const row = rows.next();
      // CRITICAL: In GAQL, cost_micros is in micros (1/1,000,000 of currency)
      // Must divide by 1,000,000 to get actual £ amount
      const cost = parseFloat(row['metrics.cost_micros']) / 1000000;
      totalSpend += cost;
      Logger.log(`  Campaign: ${row['campaign.name']}, Cost: £${cost.toFixed(2)}`);
    }

    Logger.log(`Total spend for period: £${totalSpend.toFixed(2)}`);
    return totalSpend;
  } catch (error) {
    Logger.log('Error getting spend for period ' + startDate + ' to ' + endDate + ': ' + error.message);
    Logger.log('Stack trace: ' + error.stack);
    return 0;
  }
}

// ============================================================================
// FIXED: Helper function to get spend for a single date using GAQL (not AWQL)
// ============================================================================
function getSpendForDate(date) {
  try {
    Logger.log(`Getting spend for date: ${date}`);

    // GAQL syntax - for a single date, use = instead of BETWEEN
    const query = `
      SELECT
        campaign.name,
        metrics.cost_micros
      FROM campaign
      WHERE segments.date = '${date}'
        AND campaign.name LIKE '%properties%'
        AND campaign.name NOT LIKE '%Highwayman%'
        AND campaign.name NOT LIKE '%The Hide%'
        AND metrics.cost_micros > 0
    `;

    let totalSpend = 0;
    const report = AdsApp.report(query);
    const rows = report.rows();

    while (rows.hasNext()) {
      const row = rows.next();
      // CRITICAL: Divide by 1,000,000 to convert micros to £
      const cost = parseFloat(row['metrics.cost_micros']) / 1000000;
      totalSpend += cost;
    }

    Logger.log(`Total spend for date: £${totalSpend.toFixed(2)}`);
    return totalSpend;
  } catch (error) {
    Logger.log('Error getting spend for date ' + date + ': ' + error.message);
    Logger.log('Stack trace: ' + error.stack);
    return 0;
  }
}

function createDailySpendGraph(ss, mainCurrentDate, yesterday, timezone) {
  try {
    // Create or get the graph sheet
    let graphSheet = ss.getSheetByName('Daily Spend Graph');
    if (!graphSheet) {
      graphSheet = ss.insertSheet('Daily Spend Graph');
    } else {
      graphSheet.clear();
    }

    // Set up headers
    graphSheet.getRange('A1:C1').setValues([['Date', 'Cumulative Expected Spend', 'Cumulative Actual Spend']]);
    graphSheet.getRange('A1:C1').setFontWeight('bold');

    // Get the main sheet data
    const mainSheet = ss.getSheets()[0];
    const data = mainSheet.getDataRange().getValues();
    const headers = data[0].map(header => header.trim());

    // Find the current period
    const startPeriodCol = headers.indexOf('Start Date');
    const endPeriodCol = headers.indexOf('End Date');
    const budgetCol = headers.indexOf('Budget');

    let currentPeriodStart = null;
    let currentPeriodEnd = null;
    let currentPeriodBudget = null;

    // Find the current period
    for (let i = 1; i < data.length; i++) {
      const row = data[i];
      const startDate = new Date(row[startPeriodCol]);
      const endDate = new Date(row[endPeriodCol]);
      const budget = Number(row[budgetCol]);

      if (startDate <= mainCurrentDate && endDate >= mainCurrentDate) {
        currentPeriodStart = new Date(startDate);
        currentPeriodEnd = new Date(endDate);
        currentPeriodBudget = budget;
        break;
      }
    }

    if (!currentPeriodStart || !currentPeriodEnd || !currentPeriodBudget) {
      Logger.log('No current period found for graph');
      return;
    }

    // Calculate daily budget
    const totalDays = Math.floor((currentPeriodEnd - currentPeriodStart) / (1000 * 60 * 60 * 24)) + 1;
    const dailyBudget = currentPeriodBudget / totalDays;

    // Prepare data for the graph
    const graphData = [];
    let graphDate = new Date(currentPeriodStart);
    const endDate = new Date(Math.min(currentPeriodEnd, yesterday));
    let cumulativeActualSpend = 0;

    while (graphDate <= endDate) {
      const formattedDate = Utilities.formatDate(graphDate, timezone, 'yyyy-MM-dd');
      const daysElapsed = Math.floor((graphDate - currentPeriodStart) / (1000 * 60 * 60 * 24)) + 1;
      const expectedSpend = dailyBudget * daysElapsed;

      // Get actual spend for this day using helper function
      const dailySpend = getSpendForDate(formattedDate);
      cumulativeActualSpend += dailySpend;

      graphData.push([
        Utilities.formatDate(graphDate, timezone, 'yyyy-MM-dd'),
        expectedSpend,
        cumulativeActualSpend
      ]);

      graphDate.setDate(graphDate.getDate() + 1);
    }

    // Add data to sheet
    if (graphData.length > 0) {
      graphSheet.getRange(2, 1, graphData.length, 3).setValues(graphData);

      // Format the data
      graphSheet.getRange(2, 1, graphData.length, 1).setNumberFormat('yyyy-mm-dd');
      graphSheet.getRange(2, 2, graphData.length, 2).setNumberFormat('£#,##0.00');

      // Create the chart
      const chart = graphSheet.newChart()
        .setChartType(Charts.ChartType.LINE)
        .addRange(graphSheet.getRange(1, 1, graphData.length + 1, 3))
        .setPosition(5, 5, 0, 0)
        .setOption('title', 'Cumulative Expected vs Actual Spend')
        .setOption('legend', {
          position: 'bottom',
          textStyle: {
            fontSize: 12,
            bold: true
          }
        })
        .setOption('series', {
          0: {
            color: '#4285f4',
            lineWidth: 2,
            labelInLegend: 'Expected Spend (Target)',
            targetAxisIndex: 0
          },
          1: {
            color: '#ea4335',
            lineWidth: 2,
            labelInLegend: 'Actual Spend',
            targetAxisIndex: 0
          }
        })
        .setOption('vAxis', {
          title: 'Cumulative Spend (£)',
          format: '£#,##0.00',
          titleTextStyle: {
            fontSize: 12,
            bold: true
          }
        })
        .setOption('hAxis', {
          title: 'Date',
          format: 'yyyy-MM-dd',
          titleTextStyle: {
            fontSize: 12,
            bold: true
          }
        })
        .build();

      graphSheet.insertChart(chart);
      graphSheet.autoResizeColumns(1, 3);
    }

  } catch (error) {
    Logger.log('Error creating graph: ' + error.message);
  }
}

function formatSheet(sheet, headers) {
  try {
    // Format headers
    sheet.getRange(1, 1, 1, headers.length).setFontWeight('bold');

    // Get the data range
    const dataRange = sheet.getDataRange();
    const numRows = dataRange.getNumRows() - 1;

    // Format currency columns
    const currencyColumns = [
      headers.indexOf('Budget'),
      headers.indexOf('Spend'),
      headers.indexOf('Expected Spend'),
      headers.indexOf('Remaining Budget'),
      headers.indexOf('Req Daily Budget'),
      headers.indexOf('Predicted Spend'),
      headers.indexOf('Yesterday Spend')
    ].filter(col => col !== -1);

    currencyColumns.forEach(col => {
      sheet.getRange(2, col + 1, numRows, 1).setNumberFormat('£#,##0.00');
    });

    // Format percentage column
    const percentageCol = headers.indexOf('Pacing Percentage');
    if (percentageCol !== -1) {
      sheet.getRange(2, percentageCol + 1, numRows, 1).setNumberFormat('0.00%');
    }

    // Format date columns
    const dateColumns = [
      headers.indexOf('Start Date'),
      headers.indexOf('End Date')
    ].filter(col => col !== -1);

    dateColumns.forEach(col => {
      sheet.getRange(2, col + 1, numRows, 1).setNumberFormat('yyyy-mm-dd');
    });

    // Format number columns
    const numberColumns = [
      headers.indexOf('Total Days'),
      headers.indexOf('Days Elapsed'),
      headers.indexOf('Days Remaining')
    ].filter(col => col !== -1);

    numberColumns.forEach(col => {
      sheet.getRange(2, col + 1, numRows, 1).setNumberFormat('#,##0');
    });
  } catch (error) {
    Logger.log('Error formatting sheet: ' + error.message);
  }
}
