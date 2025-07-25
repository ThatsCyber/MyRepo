// QuickSight Auto Downloader - Background Service Worker
console.log('🚀 QuickSight Auto Downloader - Background Script Loaded!');

// Configuration
const CONFIG = {
  START_HOUR: 7,        // 7 AM
  END_HOUR: 17,         // 5 PM (exclusive)
  INTERVAL_HOURS: 1.5,  // Every 1.5 hours
  TIMEZONE: Intl.DateTimeFormat().resolvedOptions().timeZone
};

// Calculate download times for the day
function calculateDownloadTimes() {
  const times = [];
  const now = new Date();
  const startTime = new Date(now);
  startTime.setHours(CONFIG.START_HOUR, 0, 0, 0);
  
  let currentTime = new Date(startTime);
  
  while (currentTime.getHours() < CONFIG.END_HOUR) {
    times.push({
      hour: currentTime.getHours(),
      minute: currentTime.getMinutes(),
      time: currentTime.toLocaleTimeString()
    });
    
    // Add 1.5 hours (90 minutes)
    currentTime.setMinutes(currentTime.getMinutes() + (CONFIG.INTERVAL_HOURS * 60));
  }
  
  return times;
}

// Set up all alarms for the day
async function setupDailyAlarms() {
  try {
    // Clear existing alarms
    await chrome.alarms.clearAll();
    
    const downloadTimes = calculateDownloadTimes();
    const now = new Date();
    
    console.log('📅 Setting up download schedule:', downloadTimes);
    
    for (const timeSlot of downloadTimes) {
      const alarmTime = new Date(now);
      alarmTime.setHours(timeSlot.hour, timeSlot.minute, 0, 0);
      
      // If the time has already passed today, schedule for tomorrow
      if (alarmTime <= now) {
        alarmTime.setDate(alarmTime.getDate() + 1);
      }
      
      const alarmName = `download-${timeSlot.hour}-${timeSlot.minute}`;
      
      await chrome.alarms.create(alarmName, {
        when: alarmTime.getTime()
      });
      
      console.log(`⏰ Scheduled download: ${timeSlot.time} (${alarmName})`);
    }
    
    // Set up daily reset alarm for midnight
    const midnight = new Date(now);
    midnight.setHours(24, 0, 0, 0); // Next midnight
    
    await chrome.alarms.create('daily-reset', {
      when: midnight.getTime()
    });
    
    console.log('🔄 Daily reset scheduled for midnight');
    
    // Store schedule in storage
    await chrome.storage.local.set({
      downloadSchedule: downloadTimes,
      lastScheduleUpdate: now.toISOString()
    });
    
  } catch (error) {
    console.error('❌ Error setting up alarms:', error);
  }
}

// Handle alarm events
chrome.alarms.onAlarm.addListener(async (alarm) => {
  console.log('🔔 Alarm triggered:', alarm.name);
  
  if (alarm.name === 'daily-reset') {
    console.log('🔄 Daily reset - setting up new schedule');
    await setupDailyAlarms();
    return;
  }
  
  if (alarm.name.startsWith('download-')) {
    console.log('📥 Triggering automatic download');
    await triggerAutoDownload();
  }
});

// Trigger automatic download
async function triggerAutoDownload() {
  try {
    // Check if extension is enabled
    const { autoDownloadEnabled = true } = await chrome.storage.local.get('autoDownloadEnabled');
    
    if (!autoDownloadEnabled) {
      console.log('⏸️ Auto download is disabled');
      return;
    }
    
    // Get QuickSight tabs (try active first, then any QuickSight tab)
    let tabs = await chrome.tabs.query({
      active: true,
      currentWindow: true,
      url: ['https://us-east-1.quicksight.aws.amazon.com/*', 'https://*.quicksight.aws.amazon.com/*']
    });
    
    // If no active QuickSight tab, look for any QuickSight tab
    if (tabs.length === 0) {
      tabs = await chrome.tabs.query({
        url: ['https://us-east-1.quicksight.aws.amazon.com/*', 'https://*.quicksight.aws.amazon.com/*']
      });
    }
    
    if (tabs.length === 0) {
      console.log('⚠️ No QuickSight tabs found');
      throw new Error('No QuickSight tab found. Please open QuickSight first.');
    }
    
    // Send message to content script to perform download
    let downloadSuccessful = false;
    
    for (const tab of tabs) {
      try {
        console.log(`🎯 Attempting to send download message to tab ${tab.id} (${tab.url})`);
        
        const response = await chrome.tabs.sendMessage(tab.id, {
          action: 'performSimpleDownload',
          timestamp: new Date().toISOString()
        });
        
        if (response && response.success) {
          console.log(`✅ Simple download started successfully in tab ${tab.id}`);
          downloadSuccessful = true;
          await logDownloadAttempt('manual', true);
          break; // Stop after first successful download
        } else {
          console.log(`⚠️ Download response from tab ${tab.id}:`, response);
        }
        
      } catch (error) {
        console.error(`❌ Error sending message to tab ${tab.id}:`, error.message);
        
        // If it's a "Receiving end does not exist" error, the content script isn't loaded
        if (error.message.includes('Receiving end does not exist')) {
          console.log(`💡 Content script not loaded in tab ${tab.id}, trying to inject...`);
          try {
            // Try to inject the content script
            await chrome.scripting.executeScript({
              target: { tabId: tab.id },
              files: ['content.js']
            });
            console.log(`✅ Content script injected into tab ${tab.id}`);
            
            // Wait a moment for script to initialize
            await new Promise(resolve => setTimeout(resolve, 1000));
            
            // Try the download again
            const retryResponse = await chrome.tabs.sendMessage(tab.id, {
              action: 'performSimpleDownload',
              timestamp: new Date().toISOString()
            });
            
            if (retryResponse && retryResponse.success) {
              console.log(`✅ Simple download started after injection in tab ${tab.id}`);
              downloadSuccessful = true;
              await logDownloadAttempt('manual', true);
              break;
            }
            
          } catch (injectionError) {
            console.error(`❌ Failed to inject content script:`, injectionError);
          }
        }
      }
    }
    
    if (!downloadSuccessful) {
      await logDownloadAttempt('manual', false, 'Could not connect to any QuickSight tab');
      throw new Error('Could not establish connection to QuickSight. Please refresh the QuickSight page and try again.');
    }
    
  } catch (error) {
    console.error('❌ Error in triggerAutoDownload:', error);
    await logDownloadAttempt('auto', false, error.message);
  }
}

// Show notification
async function showNotification(title, message) {
  try {
    await chrome.notifications.create({
      type: 'basic',
      iconUrl: 'icons/icon48.png',
      title: title,
      message: message
    });
  } catch (error) {
    console.error('❌ Error showing notification:', error);
  }
}

// Log download attempts
async function logDownloadAttempt(type, success, error = null) {
  try {
    const { downloadLog = [] } = await chrome.storage.local.get('downloadLog');
    
    const logEntry = {
      timestamp: new Date().toISOString(),
      type: type, // 'auto' or 'manual'
      success: success,
      error: error
    };
    
    downloadLog.unshift(logEntry); // Add to beginning
    
    // Keep only last 50 entries
    if (downloadLog.length > 50) {
      downloadLog.splice(50);
    }
    
    await chrome.storage.local.set({ downloadLog });
    
  } catch (error) {
    console.error('❌ Error logging download attempt:', error);
  }
}

// Handle messages from popup or content script
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  console.log('📨 Background received message:', message);
  
  switch (message.action) {
    case 'getSchedule':
      chrome.storage.local.get(['downloadSchedule', 'lastScheduleUpdate']).then(sendResponse);
      return true; // Will respond asynchronously
      
    case 'toggleAutoDownload':
      chrome.storage.local.set({ autoDownloadEnabled: message.enabled }).then(() => {
        console.log(`🔄 Auto download ${message.enabled ? 'enabled' : 'disabled'}`);
        sendResponse({ success: true });
      });
      return true;
      
    case 'getDownloadLog':
      chrome.storage.local.get('downloadLog').then(sendResponse);
      return true;
      
    case 'manualDownload':
      triggerAutoDownload().then(() => {
        sendResponse({ success: true });
      }).catch(error => {
        sendResponse({ success: false, error: error.message });
      });
      return true;
      
    case 'resetSchedule':
      setupDailyAlarms().then(() => {
        sendResponse({ success: true });
      }).catch(error => {
        sendResponse({ success: false, error: error.message });
      });
      return true;
      
    case 'startSimpleRecording':
      // Forward to content script
      chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        if (tabs[0]) {
          chrome.tabs.sendMessage(tabs[0].id, { action: 'startSimpleRecording' }, (response) => {
            if (chrome.runtime.lastError) {
              sendResponse({ success: false, error: chrome.runtime.lastError.message });
            } else {
              sendResponse({ success: true });
            }
          });
        } else {
          sendResponse({ success: false, error: 'No active tab' });
        }
      });
      return true;
      
    case 'performSimpleDownload':
      // Forward to content script
      chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        if (tabs[0]) {
          chrome.tabs.sendMessage(tabs[0].id, { action: 'performSimpleDownload' }, (response) => {
            if (chrome.runtime.lastError) {
              sendResponse({ success: false, error: chrome.runtime.lastError.message });
            } else {
              sendResponse({ success: true });
            }
          });
        } else {
          sendResponse({ success: false, error: 'No active tab' });
        }
      });
      return true;
  }
});

// Extension startup
chrome.runtime.onStartup.addListener(async () => {
  console.log('🔄 Extension startup - setting up schedule');
  await setupDailyAlarms();
});

chrome.runtime.onInstalled.addListener(async () => {
  console.log('📦 Extension installed - initial setup');
  await setupDailyAlarms();
  
  // Set default settings
  await chrome.storage.local.set({
    autoDownloadEnabled: true,
    downloadLog: []
  });
  
  await showNotification(
    'QuickSight Auto Downloader Installed!',
    'Automatic downloads will run every 1.5 hours from 7 AM to 5 PM. Open QuickSight and check the extension popup for status.'
  );
}); 