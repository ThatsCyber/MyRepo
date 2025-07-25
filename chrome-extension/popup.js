// QuickSight Auto Downloader - Popup Script
console.log('🎯 Popup script loaded!');

// DOM elements
let autoToggle, autoStatus, autoIndicator, nextDownload, downloadsToday;
let scheduleContainer, logContainer, manualDownload, resetSchedule;
let startRecording, testDownload;

// Initialize popup
document.addEventListener('DOMContentLoaded', async () => {
  console.log('📱 Popup DOM loaded, initializing...');
  
  // Get DOM elements
  autoToggle = document.getElementById('autoToggle');
  autoStatus = document.getElementById('autoStatus');
  autoIndicator = document.getElementById('autoIndicator');
  nextDownload = document.getElementById('nextDownload');
  downloadsToday = document.getElementById('downloadsToday');
  scheduleContainer = document.getElementById('scheduleContainer');
  logContainer = document.getElementById('logContainer');
  manualDownload = document.getElementById('manualDownload');
  resetSchedule = document.getElementById('resetSchedule');
  startRecording = document.getElementById('startRecording');
  testDownload = document.getElementById('testDownload');
  
  // Set up event listeners
  setupEventListeners();
  
  // Load initial data
  await loadPopupData();
  
  // Set up periodic updates
  setInterval(loadPopupData, 30000); // Update every 30 seconds
});

function setupEventListeners() {
  // Auto download toggle
  autoToggle.addEventListener('change', async (e) => {
    const enabled = e.target.checked;
    console.log(`🔄 Toggling auto download: ${enabled}`);
    
    try {
      const response = await chrome.runtime.sendMessage({
        action: 'toggleAutoDownload',
        enabled: enabled
      });
      
      if (response.success) {
        updateAutoStatus(enabled);
      } else {
        // Revert toggle if failed
        autoToggle.checked = !enabled;
      }
    } catch (error) {
      console.error('❌ Error toggling auto download:', error);
      autoToggle.checked = !enabled;
    }
  });
  
  // Manual download button
  manualDownload.addEventListener('click', async () => {
    console.log('📥 Manual download requested');
    
    manualDownload.disabled = true;
    manualDownload.textContent = '⏳ Downloading...';
    
    try {
      // Check if we're on a QuickSight tab
      const tabs = await chrome.tabs.query({ 
        active: true, 
        currentWindow: true,
        url: ['https://us-east-1.quicksight.aws.amazon.com/*', 'https://*.quicksight.aws.amazon.com/*']
      });
      
      if (tabs.length === 0) {
        showTemporaryMessage('⚠️ Please open QuickSight first', 'error');
        return;
      }
      
      const response = await chrome.runtime.sendMessage({
        action: 'manualDownload'
      });
      
      if (response.success) {
        showTemporaryMessage('✅ Download started!', 'success');
        await loadLogData(); // Refresh log
      } else {
        showTemporaryMessage(`❌ Download failed: ${response.error}`, 'error');
      }
      
    } catch (error) {
      console.error('❌ Error with manual download:', error);
      showTemporaryMessage('❌ Download error', 'error');
    } finally {
      manualDownload.disabled = false;
      manualDownload.textContent = '📥 Download Now';
    }
  });
  
  // Reset schedule button
  resetSchedule.addEventListener('click', async () => {
    console.log('🔄 Reset schedule requested');
    
    resetSchedule.disabled = true;
    resetSchedule.textContent = '⏳ Resetting...';
    
    try {
      const response = await chrome.runtime.sendMessage({
        action: 'resetSchedule'
      });
      
      if (response.success) {
        showTemporaryMessage('✅ Schedule reset!', 'success');
        await loadPopupData(); // Refresh all data
      } else {
        showTemporaryMessage('❌ Reset failed', 'error');
      }
      
    } catch (error) {
      console.error('❌ Error resetting schedule:', error);
      showTemporaryMessage('❌ Reset error', 'error');
    } finally {
      resetSchedule.disabled = false;
      resetSchedule.textContent = '🔄 Reset Schedule';
    }
  });
  
  // Simple recording button
  startRecording.addEventListener('click', async () => {
    console.log('🔴 Simple recording requested');
    
    startRecording.disabled = true;
    startRecording.textContent = '🔴 Recording...';
    
    try {
      // Check if we're on a QuickSight tab
      const tabs = await chrome.tabs.query({ 
        active: true, 
        currentWindow: true,
        url: ['https://us-east-1.quicksight.aws.amazon.com/*', 'https://*.quicksight.aws.amazon.com/*']
      });
      
      if (tabs.length === 0) {
        showTemporaryMessage('⚠️ Please open QuickSight first', 'error');
        return;
      }
      
      const response = await chrome.runtime.sendMessage({
        action: 'startSimpleRecording'
      });
      
      if (response.success) {
        showTemporaryMessage('🔴 Recording started! Click 3-dots, then Export CSV', 'success');
      } else {
        showTemporaryMessage('❌ Recording failed', 'error');
      }
      
    } catch (error) {
      console.error('❌ Error starting recording:', error);
      showTemporaryMessage('❌ Recording error', 'error');
    } finally {
      // Keep the button disabled for a few seconds to prevent multiple clicks
      setTimeout(() => {
        startRecording.disabled = false;
        startRecording.textContent = '🔴 Start Recording';
      }, 3000);
    }
  });
  
  // Test download button
  testDownload.addEventListener('click', async () => {
    console.log('⚡ Test download requested');
    
    testDownload.disabled = true;
    testDownload.textContent = '⚡ Testing...';
    
    try {
      // Check if we're on a QuickSight tab
      const tabs = await chrome.tabs.query({ 
        active: true, 
        currentWindow: true,
        url: ['https://us-east-1.quicksight.aws.amazon.com/*', 'https://*.quicksight.aws.amazon.com/*']
      });
      
      if (tabs.length === 0) {
        showTemporaryMessage('⚠️ Please open QuickSight first', 'error');
        return;
      }
      
      const response = await chrome.runtime.sendMessage({
        action: 'performSimpleDownload'
      });
      
      if (response.success) {
        showTemporaryMessage('⚡ Test download started!', 'success');
      } else {
        showTemporaryMessage('❌ Test failed', 'error');
      }
      
    } catch (error) {
      console.error('❌ Error with test download:', error);
      showTemporaryMessage('❌ Test error', 'error');
    } finally {
      testDownload.disabled = false;
      testDownload.textContent = '⚡ Test Download';
    }
  });
}

async function loadPopupData() {
  console.log('📊 Loading popup data...');
  
  try {
    // Load all data in parallel
    await Promise.all([
      loadScheduleData(),
      loadStatusData(),
      loadLogData()
    ]);
    
  } catch (error) {
    console.error('❌ Error loading popup data:', error);
  }
}

async function loadScheduleData() {
  try {
    const response = await chrome.runtime.sendMessage({ action: 'getSchedule' });
    
    if (response && response.downloadSchedule) {
      displaySchedule(response.downloadSchedule);
      updateNextDownload(response.downloadSchedule);
    } else {
      scheduleContainer.innerHTML = '<div class="loading">No schedule found</div>';
    }
    
  } catch (error) {
    console.error('❌ Error loading schedule:', error);
    scheduleContainer.innerHTML = '<div class="loading">Error loading schedule</div>';
  }
}

async function loadStatusData() {
  try {
    // Get auto download status
    const { autoDownloadEnabled = true } = await chrome.storage.local.get('autoDownloadEnabled');
    
    autoToggle.checked = autoDownloadEnabled;
    updateAutoStatus(autoDownloadEnabled);
    
  } catch (error) {
    console.error('❌ Error loading status:', error);
    autoStatus.textContent = 'Error';
    autoIndicator.className = 'status-indicator inactive';
  }
}

async function loadLogData() {
  try {
    const response = await chrome.runtime.sendMessage({ action: 'getDownloadLog' });
    
    if (response && response.downloadLog) {
      displayLog(response.downloadLog);
      updateDownloadsToday(response.downloadLog);
    } else {
      logContainer.innerHTML = '<div class="loading">No log entries</div>';
    }
    
  } catch (error) {
    console.error('❌ Error loading log:', error);
    logContainer.innerHTML = '<div class="loading">Error loading log</div>';
  }
}

function displaySchedule(schedule) {
  if (!schedule || schedule.length === 0) {
    scheduleContainer.innerHTML = '<div class="loading">No scheduled downloads</div>';
    return;
  }
  
  scheduleContainer.innerHTML = '';
  
  schedule.forEach(timeSlot => {
    const timeDiv = document.createElement('div');
    timeDiv.className = 'schedule-time';
    timeDiv.textContent = timeSlot.time;
    scheduleContainer.appendChild(timeDiv);
  });
}

function displayLog(log) {
  if (!log || log.length === 0) {
    logContainer.innerHTML = '<div class="loading">No recent activity</div>';
    return;
  }
  
  logContainer.innerHTML = '';
  
  // Show last 5 entries
  const recentEntries = log.slice(0, 5);
  
  recentEntries.forEach(entry => {
    const entryDiv = document.createElement('div');
    entryDiv.className = 'log-entry';
    
    const time = new Date(entry.timestamp).toLocaleTimeString();
    const status = entry.success ? 'Success' : 'Failed';
    const statusClass = entry.success ? 'success' : 'error';
    
    entryDiv.innerHTML = `
      <div>
        <span class="log-status ${statusClass}">${status}</span>
        ${entry.error ? `<br><small>${entry.error}</small>` : ''}
      </div>
      <div class="log-time">${time}</div>
    `;
    
    logContainer.appendChild(entryDiv);
  });
}

function updateAutoStatus(enabled) {
  autoStatus.textContent = enabled ? 'Enabled' : 'Disabled';
  autoIndicator.className = `status-indicator ${enabled ? 'active' : 'inactive'}`;
}

function updateNextDownload(schedule) {
  if (!schedule || schedule.length === 0) {
    nextDownload.textContent = 'No schedule';
    return;
  }
  
  const now = new Date();
  const currentHour = now.getHours();
  const currentMinute = now.getMinutes();
  
  // Find next download time
  let nextTime = null;
  
  for (const timeSlot of schedule) {
    if (timeSlot.hour > currentHour || 
        (timeSlot.hour === currentHour && timeSlot.minute > currentMinute)) {
      nextTime = timeSlot;
      break;
    }
  }
  
  if (nextTime) {
    nextDownload.textContent = nextTime.time;
  } else {
    // Next download is tomorrow
    nextDownload.textContent = 'Tomorrow 7:00 AM';
  }
}

function updateDownloadsToday(log) {
  if (!log) {
    downloadsToday.textContent = '0';
    return;
  }
  
  const today = new Date().toDateString();
  const todayDownloads = log.filter(entry => {
    const entryDate = new Date(entry.timestamp).toDateString();
    return entryDate === today && entry.success;
  });
  
  downloadsToday.textContent = todayDownloads.length.toString();
}

function showTemporaryMessage(message, type = 'info') {
  // Create temporary message element
  const messageDiv = document.createElement('div');
  messageDiv.style.cssText = `
    position: fixed;
    top: 10px;
    left: 10px;
    right: 10px;
    background: ${type === 'success' ? '#d4edda' : type === 'error' ? '#f8d7da' : '#d1ecf1'};
    color: ${type === 'success' ? '#155724' : type === 'error' ? '#721c24' : '#0c5460'};
    padding: 8px 12px;
    border-radius: 4px;
    font-size: 12px;
    z-index: 1000;
    border: 1px solid ${type === 'success' ? '#c3e6cb' : type === 'error' ? '#f5c6cb' : '#bee5eb'};
  `;
  messageDiv.textContent = message;
  
  document.body.appendChild(messageDiv);
  
  // Remove after 3 seconds
  setTimeout(() => {
    if (messageDiv.parentNode) {
      messageDiv.parentNode.removeChild(messageDiv);
    }
  }, 3000);
} 