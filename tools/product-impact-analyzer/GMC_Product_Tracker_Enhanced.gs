// ============================================
// ENHANCED VERSION - Now Tracks Price Changes!
// ============================================

// Key Changes from Original:
// 1. Added price tracking to product snapshots
// 2. Enhanced detectChanges() to detect PRICE_CHANGE events
// 3. Updated sheet structures to include price columns
// 4. Enhanced Outliers Report with price change data
// 5. Added price change summary to email reports

const CONFIG = {
  clients: [
    {
      name: "Tree2mydoor",
      merchantId: "107469209",
      currentSheet: "Tree2mydoor - Current",
      previousSheet: "Tree2mydoor - Previous",
      changesSheet: "Tree2mydoor - Changes"
    },
    {
      name: "Smythson UK",
      merchantId: "102535465",
      currentSheet: "Smythson UK - Current",
      previousSheet: "Smythson UK - Previous",
      changesSheet: "Smythson UK - Changes"
    },
    {
      name: "BrightMinds",
      merchantId: "5291988198",
      currentSheet: "BrightMinds - Current",
      previousSheet: "BrightMinds - Previous",
      changesSheet: "BrightMinds - Changes"
    },
    {
      name: "Accessories for the Home",
      merchantId: "117443871",
      currentSheet: "Accessories for the Home - Current",
      previousSheet: "Accessories for the Home - Previous",
      changesSheet: "Accessories for the Home - Changes"
    },
    {
      name: "Go Glean UK",
      merchantId: "5320484948",
      currentSheet: "Go Glean UK - Current",
      previousSheet: "Go Glean UK - Previous",
      changesSheet: "Go Glean UK - Changes"
    },
    {
      name: "Superspace UK",
      merchantId: "645236311",
      currentSheet: "Superspace - Current",
      previousSheet: "Superspace - Previous",
      changesSheet: "Superspace - Changes"
    },
    {
      name: "Uno Lights",
      merchantId: "513812383",
      currentSheet: "Uno Lights - Current",
      previousSheet: "Uno Lights - Previous",
      changesSheet: "Uno Lights - Changes"
    },
    {
      name: "WheatyBags",
      merchantId: "7481286",
      currentSheet: "WheatyBags - Current",
      previousSheet: "WheatyBags - Previous",
      changesSheet: "WheatyBags - Changes"
    },
    {
      name: "HappySnapGifts",
      merchantId: "7481296",
      currentSheet: "HappySnapGifts - Current",
      previousSheet: "HappySnapGifts - Previous",
      changesSheet: "HappySnapGifts - Changes"
    },
    {
      name: "BMPM",
      merchantId: "7522326",
      currentSheet: "BMPM - Current",
      previousSheet: "BMPM - Previous",
      changesSheet: "BMPM - Changes"
    },
    {
      name: "Camera Manuals",
      merchantId: "7253170",
      currentSheet: "Camera Manuals - Current",
      previousSheet: "Camera Manuals - Previous",
      changesSheet: "Camera Manuals - Changes"
    }
  ],
  dashboardSheet: "Dashboard",

  // Google Ads Account Mapping
  googleAdsAccounts: {
    "107469209": {  // Tree2mydoor
      customerId: "4941701449",
      managerId: "2569949686"
    },
    "102535465": {  // Smythson UK
      customerId: "8573235780",
      managerId: "2569949686"
    },
    "5291988198": {  // BrightMinds
      customerId: "1404868570",
      managerId: "2569949686"
    },
    "117443871": {  // Accessories for the Home
      customerId: "7972994730",
      managerId: null
    },
    "5320484948": {  // Go Glean UK
      customerId: "8492163737",
      managerId: "2569949686"
    },
    "645236311": {  // Superspace UK
      customerId: "7482100090",
      managerId: null
    },
    "513812383": {  // Uno Lights
      customerId: "6413338364",
      managerId: null
    },
    "7481286": {  // WheatyBags
      customerId: "6281395727",
      managerId: "2569949686"
    },
    "7481296": {  // HappySnapGifts
      customerId: "6281395727",
      managerId: "2569949686"
    },
    "7522326": {  // BMPM
      customerId: "6281395727",
      managerId: "2569949686"
    },
    "7253170": {  // Camera Manuals
      customerId: null,
      managerId: null
    }
  }
};

// ============================================
// MAIN FUNCTION - Run this daily
// ============================================

function dailyProductCheck() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();

  CONFIG.clients.forEach(client => {
    try {
      Logger.log(`Processing ${client.name}...`);
      processClient(client, ss);
    } catch (error) {
      Logger.log(`Error processing ${client.name}: ${error}`);
    }
  });

  updateDashboard(ss);
  Logger.log("Daily check complete!");
}

// ============================================
// PROCESS EACH CLIENT
// ============================================

function processClient(client, ss) {
  const currentProducts = getProductsFromGMC(client.merchantId);
  const currentSheet = ss.getSheetByName(client.currentSheet);
  const previousSheet = ss.getSheetByName(client.previousSheet);
  const changesSheet = ss.getSheetByName(client.changesSheet);
  const previousProducts = readSnapshot(previousSheet);
  const changes = detectChanges(previousProducts, currentProducts);

  if (changes.length > 0) {
    logChanges(changesSheet, changes);
    Logger.log(`${client.name}: Found ${changes.length} changes`);
  } else {
    Logger.log(`${client.name}: No changes detected`);
  }

  copyCurrentToPrevious(currentSheet, previousSheet);
  writeSnapshot(currentSheet, currentProducts);
}

// ============================================
// GET PRODUCTS FROM GOOGLE MERCHANT CENTER
// ============================================
// ENHANCED: Now includes price, currency, and availability

function getProductsFromGMC(merchantId) {
  const products = [];
  let pageToken = null;

  do {
    const options = { maxResults: 250 };
    if (pageToken) options.pageToken = pageToken;

    const response = ShoppingContent.Products.list(merchantId, options);

    if (response.resources) {
      response.resources.forEach(product => {
        // Extract status
        let productStatus = "active";
        if (product.status && product.status.destinationStatuses) {
          const shoppingStatus = product.status.destinationStatuses.find(
            dest => dest.destination === "Shopping"
          );
          if (shoppingStatus) {
            productStatus = shoppingStatus.status || "active";
          }
        }

        // Extract price - ENHANCED!
        let price = null;
        let currency = null;
        if (product.price) {
          price = parseFloat(product.price.value);
          currency = product.price.currency;
        }

        // Extract availability
        let availability = product.availability || "unknown";

        products.push({
          id: product.offerId,
          title: product.title || "No Title",
          status: productStatus,
          price: price,           // NEW
          currency: currency,     // NEW
          availability: availability  // NEW
        });
      });
    }

    pageToken = response.nextPageToken;
  } while (pageToken);

  Logger.log(`Retrieved ${products.length} products from GMC ${merchantId}`);
  return products;
}

// ============================================
// READ SNAPSHOT FROM SHEET
// ============================================
// ENHANCED: Now reads price and currency columns

function readSnapshot(sheet) {
  if (sheet.getLastRow() <= 1) {
    return {};
  }

  const data = sheet.getDataRange().getValues();
  const products = {};

  for (let i = 1; i < data.length; i++) {
    if (data[i][0]) {
      // Parse price properly - handle empty/null/string values
      let price = data[i][3];
      if (price === "" || price === null || price === undefined) {
        price = null;
      } else {
        price = parseFloat(price);
        if (isNaN(price)) price = null;
      }

      products[data[i][0]] = {
        id: data[i][0],
        title: data[i][1],
        status: data[i][2],
        price: price,           // Properly parsed as number or null
        currency: data[i][4],   // NEW - Column E
        availability: data[i][5] // NEW - Column F
      };
    }
  }

  return products;
}

// ============================================
// DETECT CHANGES
// ============================================
// ENHANCED: Now detects PRICE_CHANGE and TITLE_CHANGE

function detectChanges(previousProducts, currentProducts) {
  const changes = [];
  const today = new Date();
  const currentProductsMap = {};

  currentProducts.forEach(p => {
    currentProductsMap[p.id] = p;
  });

  // Detect REMOVED products
  Object.keys(previousProducts).forEach(id => {
    if (!currentProductsMap[id]) {
      changes.push({
        date: today,
        id: id,
        type: "REMOVED",
        title: previousProducts[id].title,
        status: previousProducts[id].status,
        oldPrice: previousProducts[id].price,
        newPrice: null,
        priceChange: null,
        notes: "Product no longer in feed"
      });
    }
  });

  // Detect NEW products and changes
  Object.keys(currentProductsMap).forEach(id => {
    const current = currentProductsMap[id];
    const previous = previousProducts[id];

    if (!previous) {
      // NEW product
      changes.push({
        date: today,
        id: id,
        type: "NEW",
        title: current.title,
        status: current.status,
        oldPrice: null,
        newPrice: current.price,
        priceChange: null,
        notes: "New product in feed"
      });
    } else {
      // Check for PRICE_CHANGE - ENHANCED!
      if (previous.price !== null && current.price !== null &&
          previous.price !== current.price) {

        const priceChangePercent = ((current.price - previous.price) / previous.price * 100).toFixed(2);

        changes.push({
          date: today,
          id: id,
          type: "PRICE_CHANGE",
          title: current.title,
          status: current.status,
          oldPrice: previous.price,
          newPrice: current.price,
          priceChange: priceChangePercent,
          notes: `Price changed from ${current.currency || '£'}${Number(previous.price).toFixed(2)} to ${current.currency || '£'}${Number(current.price).toFixed(2)} (${priceChangePercent > 0 ? '+' : ''}${priceChangePercent}%)`
        });
      }

      // Check for TITLE_CHANGE
      if (previous.title !== current.title) {
        changes.push({
          date: today,
          id: id,
          type: "TITLE_CHANGE",
          title: current.title,
          status: current.status,
          oldPrice: current.price,
          newPrice: current.price,
          priceChange: null,
          notes: `Title changed from "${previous.title}" to "${current.title}"`
        });
      }

      // Check for AVAILABILITY_CHANGE
      if (previous.availability !== current.availability) {
        changes.push({
          date: today,
          id: id,
          type: "AVAILABILITY_CHANGE",
          title: current.title,
          status: current.status,
          oldPrice: current.price,
          newPrice: current.price,
          priceChange: null,
          notes: `Availability changed from "${previous.availability}" to "${current.availability}"`
        });
      }
    }
  });

  return changes;
}

// ============================================
// LOG CHANGES TO SHEET
// ============================================
// ENHANCED: Now includes price columns

function logChanges(changesSheet, changes) {
  const rows = changes.map(change => [
    change.date,
    change.id,
    change.type,
    change.title,
    change.status,
    change.oldPrice || "",          // NEW - Column F
    change.newPrice || "",          // NEW - Column G
    change.priceChange || "",       // NEW - Column H
    change.notes
  ]);

  if (rows.length > 0) {
    changesSheet.getRange(changesSheet.getLastRow() + 1, 1, rows.length, 9).setValues(rows);
  }
}

// ============================================
// WRITE SNAPSHOT TO SHEET
// ============================================
// ENHANCED: Now includes price, currency, availability columns

function writeSnapshot(sheet, products) {
  if (sheet.getLastRow() > 1) {
    sheet.getRange(2, 1, sheet.getLastRow() - 1, 7).clearContent();
  }

  if (products.length === 0) return;

  const timestamp = new Date();
  const rows = products.map(p => [
    p.id,
    p.title,
    p.status,
    p.price || "",              // NEW - Column D
    p.currency || "",           // NEW - Column E
    p.availability || "",       // NEW - Column F
    timestamp
  ]);

  sheet.getRange(2, 1, rows.length, 7).setValues(rows);
}

// ============================================
// COPY CURRENT TO PREVIOUS
// ============================================
// ENHANCED: Now copies 7 columns instead of 4

function copyCurrentToPrevious(currentSheet, previousSheet) {
  if (previousSheet.getLastRow() > 1) {
    previousSheet.getRange(2, 1, previousSheet.getLastRow() - 1, 7).clearContent();
  }

  if (currentSheet.getLastRow() > 1) {
    const data = currentSheet.getRange(2, 1, currentSheet.getLastRow() - 1, 7).getValues();
    if (data.length > 0) {
      previousSheet.getRange(2, 1, data.length, 7).setValues(data);
    }
  }
}

// ============================================
// UPDATE DASHBOARD
// ============================================

function updateDashboard(ss) {
  const dashboard = ss.getSheetByName(CONFIG.dashboardSheet);
  const now = new Date();
  const sevenDaysAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
  const thirtyDaysAgo = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000);

  CONFIG.clients.forEach((client, index) => {
    const row = index + 2;

    try {
      const currentSheet = ss.getSheetByName(client.currentSheet);
      const totalProducts = currentSheet.getLastRow() - 1;
      const changesSheet = ss.getSheetByName(client.changesSheet);
      const changesData = changesSheet.getDataRange().getValues();

      let changes7Days = 0;
      let changes30Days = 0;

      for (let i = 1; i < changesData.length; i++) {
        const changeDate = new Date(changesData[i][0]);
        if (changeDate >= sevenDaysAgo) changes7Days++;
        if (changeDate >= thirtyDaysAgo) changes30Days++;
      }

      dashboard.getRange(row, 3, 1, 5).setValues([[
        now,
        totalProducts,
        changes7Days,
        changes30Days,
        "Active"
      ]]);

    } catch (error) {
      dashboard.getRange(row, 7).setValue("Error: " + error.message);
    }
  });
}

// ============================================
// ONE-TIME SETUP: CREATE ALL TABS
// ============================================
// ENHANCED: Now creates sheets with price columns

function createAllTabs() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();

  // Create Dashboard
  let dashboard = ss.getSheetByName(CONFIG.dashboardSheet);
  if (!dashboard) {
    dashboard = ss.insertSheet(CONFIG.dashboardSheet, 0);
  }

  dashboard.getRange(1, 1, 1, 7).setValues([[
    "Client Name",
    "Merchant ID",
    "Last Check",
    "Total Products",
    "Changes (Last 7 Days)",
    "Changes (Last 30 Days)",
    "Status"
  ]]);
  dashboard.getRange(1, 1, 1, 7).setFontWeight("bold").setBackground("#4285f4").setFontColor("white");

  const dashboardData = CONFIG.clients.map(client => [
    client.name,
    client.merchantId,
    "",
    "",
    "",
    "",
    "Not Yet Run"
  ]);

  dashboard.getRange(2, 1, dashboardData.length, 7).setValues(dashboardData);

  for (let i = 1; i <= 7; i++) {
    dashboard.autoResizeColumn(i);
  }

  Logger.log("Dashboard created with " + CONFIG.clients.length + " clients");

  // Create client sheets - ENHANCED with price columns
  CONFIG.clients.forEach(client => {
    // Current sheet
    let sheet = ss.getSheetByName(client.currentSheet);
    if (!sheet) {
      sheet = ss.insertSheet(client.currentSheet);
    }
    sheet.getRange(1, 1, 1, 7).setValues([[
      "Product ID", "Title", "Status", "Price", "Currency", "Availability", "Last Updated"
    ]]);
    sheet.getRange(1, 1, 1, 7).setFontWeight("bold").setBackground("#34a853").setFontColor("white");
    sheet.autoResizeColumns(1, 7);

    // Previous sheet
    sheet = ss.getSheetByName(client.previousSheet);
    if (!sheet) {
      sheet = ss.insertSheet(client.previousSheet);
    }
    sheet.getRange(1, 1, 1, 7).setValues([[
      "Product ID", "Title", "Status", "Price", "Currency", "Availability", "Last Updated"
    ]]);
    sheet.getRange(1, 1, 1, 7).setFontWeight("bold").setBackground("#fbbc04").setFontColor("white");
    sheet.autoResizeColumns(1, 7);

    // Changes sheet - ENHANCED with price columns
    sheet = ss.getSheetByName(client.changesSheet);
    if (!sheet) {
      sheet = ss.insertSheet(client.changesSheet);
    }
    sheet.getRange(1, 1, 1, 9).setValues([[
      "Date Detected", "Product ID", "Change Type", "Product Title",
      "Status", "Old Price", "New Price", "Price Change %", "Notes"
    ]]);
    sheet.getRange(1, 1, 1, 9).setFontWeight("bold").setBackground("#ea4335").setFontColor("white");
    sheet.autoResizeColumns(1, 9);

    Logger.log("Created tabs for: " + client.name);
  });

  Logger.log("All tabs created successfully!");
}

// ============================================
// OUTLIERS REPORT
// ============================================
// ENHANCED: Now includes price change columns

function generateOutliersReport() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();

  let outliersSheet = ss.getSheetByName("Outliers Report");
  if (!outliersSheet) {
    outliersSheet = ss.insertSheet("Outliers Report", 1);
  } else {
    outliersSheet.clear();
  }

  // ENHANCED: Added price columns
  outliersSheet.getRange(1, 1, 1, 10).setValues([[
    "Client",
    "Product ID",
    "Change Type",
    "Date Changed",
    "Product Title",
    "Days Since Change",
    "Old Price",      // NEW
    "New Price",      // NEW
    "Price Change %", // NEW
    "Flag"
  ]]);
  outliersSheet.getRange(1, 1, 1, 10).setFontWeight("bold").setBackground("#9900ff").setFontColor("white");

  const today = new Date();
  const outliers = [];

  CONFIG.clients.forEach(client => {
    const changesSheet = ss.getSheetByName(client.changesSheet);
    if (!changesSheet || changesSheet.getLastRow() <= 1) return;

    const changesData = changesSheet.getRange(2, 1, changesSheet.getLastRow() - 1, 9).getValues();

    changesData.forEach(row => {
      const changeDate = new Date(row[0]);
      const productId = row[1];
      const changeType = row[2];
      const productTitle = row[3];
      const oldPrice = row[5];
      const newPrice = row[6];
      const priceChange = row[7];

      const daysSince = Math.floor((today - changeDate) / (1000 * 60 * 60 * 24));

      let flag = "";

      if (daysSince <= 7) {
        flag = "🔴 Recent Change";
      } else if (changeType === "REMOVED") {
        flag = "⚠️ Product Removed";
      } else if (changeType === "PRICE_CHANGE") {
        // ENHANCED: Special flags for price changes
        if (Math.abs(parseFloat(priceChange)) >= 15) {
          flag = "💰 Significant Price Change";
        } else if (daysSince >= 28 && daysSince <= 56) {
          flag = "📊 Ready to Analyze";
        }
      } else if (daysSince >= 28 && daysSince <= 56) {
        flag = "📊 Ready to Analyze";
      }

      if (flag) {
        outliers.push([
          client.name,
          productId,
          changeType,
          changeDate,
          productTitle,
          daysSince,
          oldPrice || "",
          newPrice || "",
          priceChange || "",
          flag
        ]);
      }
    });
  });

  outliers.sort((a, b) => a[5] - b[5]);

  if (outliers.length > 0) {
    outliersSheet.getRange(2, 1, outliers.length, 10).setValues(outliers);
    for (let i = 1; i <= 10; i++) {
      outliersSheet.autoResizeColumn(i);
    }
  } else {
    outliersSheet.getRange(2, 1, 1, 10).setValues([["No flagged changes found", "", "", "", "", "", "", "", "", ""]]);
  }

  Logger.log(`Outliers report generated: ${outliers.length} flagged changes`);
  sendOutliersEmail(outliers, ss.getUrl());
}

// ============================================
// EMAIL OUTLIERS SUMMARY
// ============================================
// ENHANCED: Now includes price change summary

function sendOutliersEmail(outliers, sheetUrl) {
  const recipient = "petere@roksys.co.uk";
  const subject = `GMC Product ID Changes - Weekly Outliers Report (${new Date().toLocaleDateString()})`;

  let recentChanges = 0;
  let removedProducts = 0;
  let readyToAnalyze = 0;
  let significantPriceChanges = 0;  // NEW

  outliers.forEach(row => {
    const flag = row[9];
    if (flag.includes("Recent Change")) recentChanges++;
    else if (flag.includes("Product Removed")) removedProducts++;
    else if (flag.includes("Ready to Analyze")) readyToAnalyze++;
    else if (flag.includes("Significant Price Change")) significantPriceChanges++;
  });

  let htmlBody = `
    <html>
      <body style="font-family: Arial, sans-serif;">
        <h2 style="color: #4285f4;">GMC Product ID Change Report</h2>
        <p>Weekly summary of flagged product ID changes across all clients.</p>

        <div style="background: #f1f3f4; padding: 15px; border-radius: 5px; margin: 20px 0;">
          <h3 style="margin-top: 0;">Summary</h3>
          <p><strong>🔴 Recent Changes (Last 7 Days):</strong> ${recentChanges}</p>
          <p><strong>⚠️ Products Removed:</strong> ${removedProducts}</p>
          <p><strong>💰 Significant Price Changes (±15%+):</strong> ${significantPriceChanges}</p>
          <p><strong>📊 Ready to Analyze (4-8 weeks old):</strong> ${readyToAnalyze}</p>
          <p><strong>Total Flagged Changes:</strong> ${outliers.length}</p>
        </div>
  `;

  if (outliers.length > 0) {
    const byClient = {};
    outliers.forEach(row => {
      const client = row[0];
      if (!byClient[client]) byClient[client] = [];
      byClient[client].push(row);
    });

    htmlBody += `<h3>Changes by Client</h3>`;

    Object.keys(byClient).forEach(client => {
      htmlBody += `
        <h4 style="color: #34a853; margin-top: 20px;">${client} (${byClient[client].length} changes)</h4>
        <table style="border-collapse: collapse; width: 100%; margin-bottom: 20px;">
          <tr style="background: #f1f3f4;">
            <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Product ID</th>
            <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Change Type</th>
            <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Price Change</th>
            <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Days Since</th>
            <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Flag</th>
          </tr>
      `;

      byClient[client].slice(0, 10).forEach(row => {
        const priceChangeText = row[8] ? `${row[8] > 0 ? '+' : ''}${row[8]}%` : '-';
        htmlBody += `
          <tr>
            <td style="border: 1px solid #ddd; padding: 8px;">${row[1]}</td>
            <td style="border: 1px solid #ddd; padding: 8px;">${row[2]}</td>
            <td style="border: 1px solid #ddd; padding: 8px;">${priceChangeText}</td>
            <td style="border: 1px solid #ddd; padding: 8px;">${row[5]}</td>
            <td style="border: 1px solid #ddd; padding: 8px;">${row[9]}</td>
          </tr>
        `;
      });

      if (byClient[client].length > 10) {
        htmlBody += `
          <tr>
            <td colspan="5" style="border: 1px solid #ddd; padding: 8px; text-align: center; font-style: italic;">
              + ${byClient[client].length - 10} more changes...
            </td>
          </tr>
        `;
      }

      htmlBody += `</table>`;
    });
  } else {
    htmlBody += `<p style="color: #34a853; font-weight: bold;">✓ No flagged changes this week - all clear!</p>`;
  }

  htmlBody += `
        <p style="margin-top: 30px;">
          <a href="${sheetUrl}" style="background: #4285f4; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
            View Full Report in Google Sheets
          </a>
        </p>

        <p style="color: #666; font-size: 12px; margin-top: 30px;">
          This is an automated report from your GMC Product ID Tracker.<br>
          Generated on ${new Date().toLocaleString()}
        </p>
      </body>
    </html>
  `;

  MailApp.sendEmail({
    to: recipient,
    subject: subject,
    htmlBody: htmlBody
  });

  Logger.log(`Email sent to ${recipient}`);
}

// ============================================
// ONE-TIME FIX: Fix Old Change Data Column Alignment
// ============================================
// Run this ONCE after migration to move old Notes data to correct column

function fixOldChangeData() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();

  CONFIG.clients.forEach(client => {
    const changesSheet = ss.getSheetByName(client.changesSheet);
    if (!changesSheet || changesSheet.getLastRow() <= 1) return;

    Logger.log(`Fixing ${client.name} Changes sheet...`);

    // Read all data (skip header)
    const lastRow = changesSheet.getLastRow();
    const data = changesSheet.getRange(2, 1, lastRow - 1, 9).getValues();

    const fixedData = data.map(row => {
      // Check if this is old format by seeing if column F has text and column I is empty
      if (row[5] && !row[8]) {
        // Old format: Date, ID, Type, Title, Status, Notes
        // New format: Date, ID, Type, Title, Status, OldPrice, NewPrice, PriceChange%, Notes
        return [
          row[0], // Date
          row[1], // Product ID
          row[2], // Change Type
          row[3], // Product Title
          row[4], // Status
          "",     // Old Price (empty for old data)
          "",     // New Price (empty for old data)
          "",     // Price Change % (empty for old data)
          row[5]  // Notes (moved from column F to column I)
        ];
      }
      // Already in new format, return as-is
      return row;
    });

    // Write fixed data back
    changesSheet.getRange(2, 1, fixedData.length, 9).setValues(fixedData);
    Logger.log(`Fixed ${client.name}`);
  });

  Logger.log("All Changes sheets fixed!");
}

// ============================================
// ONE-TIME FIX: Format Price Columns as Numbers
// ============================================
// Run this ONCE to stop prices displaying as dates

function formatPriceColumns() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();

  CONFIG.clients.forEach(client => {
    // Format Current sheet - column D (Price)
    const currentSheet = ss.getSheetByName(client.currentSheet);
    if (currentSheet) {
      currentSheet.getRange("D:D").setNumberFormat("0.00");
      Logger.log(`Formatted ${client.currentSheet} price column`);
    }

    // Format Previous sheet - column D (Price)
    const previousSheet = ss.getSheetByName(client.previousSheet);
    if (previousSheet) {
      previousSheet.getRange("D:D").setNumberFormat("0.00");
      Logger.log(`Formatted ${client.previousSheet} price column`);
    }

    // Format Changes sheet - columns F, G, H (Old Price, New Price, Price Change %)
    const changesSheet = ss.getSheetByName(client.changesSheet);
    if (changesSheet) {
      changesSheet.getRange("F:F").setNumberFormat("0.00");  // Old Price
      changesSheet.getRange("G:G").setNumberFormat("0.00");  // New Price
      changesSheet.getRange("H:H").setNumberFormat("0.00");  // Price Change %
      Logger.log(`Formatted ${client.changesSheet} price columns`);
    }
  });

  // Format Outliers Report if it exists
  const outliersSheet = ss.getSheetByName("Outliers Report");
  if (outliersSheet) {
    outliersSheet.getRange("G:G").setNumberFormat("0.00");  // Old Price
    outliersSheet.getRange("H:H").setNumberFormat("0.00");  // New Price
    outliersSheet.getRange("I:I").setNumberFormat("0.00");  // Price Change %
    Logger.log("Formatted Outliers Report price columns");
  }

  Logger.log("All price columns formatted!");
}
