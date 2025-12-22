/**
 * P9 Budget Management Script for Smythson
 * December 22-28, 2025
 *
 * This script automatically adjusts campaign budgets based on date and time.
 * Schedule to run hourly from Dec 22-28.
 */

function main() {
  // Define budget schedules for each account
  const budgetSchedule = {
    '8573235780': { // UK Account
      '2025-12-22': 650,
      '2025-12-23': 860,
      '2025-12-24-morning': 860,
      '2025-12-24-evening': 1505, // Sale launch at 6pm
      '2025-12-25': 2900,
      '2025-12-26': 5000, // Boxing Day
      '2025-12-27': 5880,
      '2025-12-28': 5670
    },
    '7808690871': { // USA Account
      '2025-12-22': 465,
      '2025-12-23': 620,
      '2025-12-24-morning': 620,
      '2025-12-24-evening': 1085,
      '2025-12-25': 2089,
      '2025-12-26': 3800,
      '2025-12-27': 4480,
      '2025-12-28': 4320
    },
    '7679616761': { // EUR Account
      '2025-12-22': 270,
      '2025-12-23': 360,
      '2025-12-24-morning': 360,
      '2025-12-24-evening': 630,
      '2025-12-25': 1213,
      '2025-12-26': 2500, // Highest Boxing Day potential
      '2025-12-27': 2940,
      '2025-12-28': 2835
    },
    '5556710725': { // ROW Account
      '2025-12-22': 115,
      '2025-12-23': 160,
      '2025-12-24-morning': 160,
      '2025-12-24-evening': 280,
      '2025-12-25': 537,
      '2025-12-26': 700,
      '2025-12-27': 700,
      '2025-12-28': 675
    }
  };

  // Get current date and hour
  const now = new Date();
  const currentDate = Utilities.formatDate(now, 'Europe/London', 'yyyy-MM-dd');
  const currentHour = now.getHours();

  Logger.log('Current date/time: ' + currentDate + ' ' + currentHour + ':00');

  // Determine which budget to use
  let dateKey = currentDate;
  if (currentDate === '2025-12-24') {
    dateKey = currentHour >= 18 ? '2025-12-24-evening' : '2025-12-24-morning';
    Logger.log('December 24 - Using ' + (currentHour >= 18 ? 'evening' : 'morning') + ' budget');
  }

  // Process each account
  const accountIds = Object.keys(budgetSchedule);

  accountIds.forEach(function(accountId) {
    try {
      // Get the target budget for this account and date
      const targetBudget = budgetSchedule[accountId][dateKey];

      if (!targetBudget) {
        Logger.log('No budget defined for account ' + accountId + ' on ' + dateKey);
        return;
      }

      Logger.log('Processing account ' + accountId + ' - Target budget: £' + targetBudget);

      // Select the account
      const accounts = AdsManagerApp.accounts()
        .withCondition('customer.id = "' + accountId + '"')
        .get();

      if (accounts.hasNext()) {
        const account = accounts.next();
        AdsManagerApp.select(account);

        // Update all enabled campaigns in this account
        const campaigns = AdsApp.campaigns()
          .withCondition('campaign.status = "ENABLED"')
          .get();

        let campaignCount = 0;
        while (campaigns.hasNext()) {
          const campaign = campaigns.next();
          const currentBudget = campaign.getBudget().getAmount();

          // Only update if budget is different
          if (Math.abs(currentBudget - targetBudget) > 0.01) {
            campaign.getBudget().setAmount(targetBudget);
            Logger.log('Updated campaign "' + campaign.getName() +
                      '" from £' + currentBudget + ' to £' + targetBudget);
            campaignCount++;
          }
        }

        Logger.log('Account ' + accountId + ': Updated ' + campaignCount + ' campaigns');

        // Send notification for critical changes
        if (dateKey === '2025-12-24-evening' || dateKey === '2025-12-26') {
          sendNotification(accountId, targetBudget, dateKey);
        }
      }
    } catch (e) {
      Logger.log('Error processing account ' + accountId + ': ' + e.message);
    }
  });
}

/**
 * Send email notification for critical budget changes
 */
function sendNotification(accountId, budget, dateKey) {
  const accountNames = {
    '8573235780': 'UK',
    '7808690871': 'USA',
    '7679616761': 'EUR',
    '5556710725': 'ROW'
  };

  const eventNames = {
    '2025-12-24-evening': 'Sale Launch (6pm)',
    '2025-12-26': 'Boxing Day'
  };

  const subject = 'P9 Budget Update: ' + accountNames[accountId] + ' - ' + eventNames[dateKey];
  const body = 'Successfully updated ' + accountNames[accountId] + ' account (' + accountId + ')' +
               ' to £' + budget + ' for ' + eventNames[dateKey] + '.' +
               '\n\nTime: ' + new Date().toString();

  // Send to your email
  MailApp.sendEmail('petere@roksys.co.uk', subject, body);
}

/**
 * Test function - run this first to verify script works
 */
function testScript() {
  Logger.log('Test run at: ' + new Date().toString());

  // Test account access
  const accounts = AdsManagerApp.accounts().get();
  while (accounts.hasNext()) {
    const account = accounts.next();
    Logger.log('Found account: ' + account.getName() + ' (' + account.getCustomerId() + ')');
  }

  Logger.log('Test complete - script has access to accounts');
}

/**
 * Setup function - creates hourly trigger
 */
function setupTrigger() {
  // Delete existing triggers
  const triggers = ScriptApp.getProjectTriggers();
  triggers.forEach(function(trigger) {
    ScriptApp.deleteTrigger(trigger);
  });

  // Create new hourly trigger
  ScriptApp.newTrigger('main')
    .timeBased()
    .everyHours(1)
    .create();

  Logger.log('Hourly trigger created - script will run every hour');
}

/**
 * Manual override function for emergency adjustments
 */
function manualOverride() {
  // Example: Force Boxing Day budgets
  const boxingDayBudgets = {
    '8573235780': 5000,  // UK
    '7808690871': 3800,  // USA
    '7679616761': 2500,  // EUR
    '5556710725': 700    // ROW
  };

  Object.keys(boxingDayBudgets).forEach(function(accountId) {
    const accounts = AdsManagerApp.accounts()
      .withCondition('customer.id = "' + accountId + '"')
      .get();

    if (accounts.hasNext()) {
      const account = accounts.next();
      AdsManagerApp.select(account);

      const campaigns = AdsApp.campaigns()
        .withCondition('campaign.status = "ENABLED"')
        .get();

      while (campaigns.hasNext()) {
        const campaign = campaigns.next();
        campaign.getBudget().setAmount(boxingDayBudgets[accountId]);
      }

      Logger.log('Manually set account ' + accountId + ' to £' + boxingDayBudgets[accountId]);
    }
  });
}