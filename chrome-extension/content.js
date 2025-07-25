// QuickSight Auto Downloader - Content Script
console.log('🎯 QuickSight Auto Downloader - Content Script Loaded!');

try {
  console.log('🔧 Starting content script initialization...');

  // Simple recording system
  let isSimpleRecording = false;
  let recordedMenuButton = null;
  let recordedExportButton = null;
  
  console.log('✅ Variables initialized');

// SIMPLE RECORDING FUNCTION - Just record what user clicks
function startSimpleRecording() {
  console.log('🔴 SIMPLE RECORDING STARTED!');
  console.log('📝 Step 1: Click the 3-dots menu button on Supply & Demand chart');
  console.log('📝 Step 2: Then click "Export to CSV"');
  
  // Check if already recording
  if (isSimpleRecording) {
    console.log('⚠️ Already recording, stopping previous recording');
    stopSimpleRecording();
  }
  
  isSimpleRecording = true;
  recordedMenuButton = null;
  recordedExportButton = null;
  
  console.log('🎯 Recording state set to:', isSimpleRecording);
  
  // Show indicator
  try {
    showRecordingIndicator('Click 3-dots menu, then Export to CSV');
    console.log('✅ Recording indicator shown');
  } catch (error) {
    console.error('❌ Error showing recording indicator:', error);
  }
  
  // Add click listener
  try {
    document.addEventListener('click', handleRecordingClick, true);
    console.log('✅ Click listener added for recording');
  } catch (error) {
    console.error('❌ Error adding click listener:', error);
    throw error;
  }
}

function handleRecordingClick(event) {
  console.log('🖱️ Click detected during recording, isSimpleRecording:', isSimpleRecording);
  
  if (!isSimpleRecording) {
    console.log('⚠️ Not recording, ignoring click');
    return;
  }
  
  const element = event.target;
  console.log('🎯 Recording click on element:', element);
  console.log('   - tagName:', element.tagName);
  console.log('   - className:', element.className);
  console.log('   - data-automation-id:', element.getAttribute('data-automation-id'));
  console.log('   - aria-label:', element.getAttribute('aria-label'));
  console.log('   - textContent:', element.textContent?.trim());
  
  // If we haven't recorded menu button yet
  if (!recordedMenuButton) {
    console.log('✅ Recording as MENU button');
    recordedMenuButton = {
      selector: createSimpleSelector(element),
      ariaLabel: element.getAttribute('aria-label') || '',
      dataId: element.getAttribute('data-automation-id') || '',
      className: element.className || ''
    };
    
    console.log('📋 Menu button details:', recordedMenuButton);
    showRecordingIndicator('Great! Now click Export to CSV');
    
    // Don't prevent this click - let menu open
    return;
  }
  
    // If we have menu button but not export button
  if (recordedMenuButton && !recordedExportButton) {
    console.log('✅ Recording as EXPORT button');
    
    // Prevent this click since we're just recording
    event.preventDefault();
    event.stopPropagation();
    
    recordedExportButton = {
      selector: createSimpleSelector(element),
      textContent: element.textContent?.trim() || '',
      dataId: element.getAttribute('data-automation-id') || '',
      className: element.className || ''
    };
    
    console.log('📋 Export button details:', recordedExportButton);
    
    // Save and complete
    try {
      saveSimpleRecording();
      console.log('✅ Recording saved successfully');
      showRecordingIndicator('Recording complete! Ready for automation.', 'success');
      
      setTimeout(() => {
        stopSimpleRecording();
      }, 3000);
    } catch (error) {
      console.error('❌ Error saving recording:', error);
      showRecordingIndicator('Error saving recording!', 'error');
    }
  }
}

function createSimpleSelector(element) {
  const selectors = [];
  
  // 1. data-automation-id (most reliable for this app)
  const dataId = element.getAttribute('data-automation-id');
  if (dataId) {
    selectors.push(`[data-automation-id="${dataId}"]`);
  }
  
  // 2. aria-label for menu button
  const ariaLabel = element.getAttribute('aria-label');
  if (ariaLabel) {
    selectors.push(`[aria-label="${ariaLabel}"]`);
  }
  
  // 3. For export button, use text content if it's specific
  const text = element.textContent?.trim();
  if (text === 'Export to CSV') {
    selectors.push('li[role="menuitem"]:contains("Export to CSV")');
  }
  
  // 4. Class-based fallback
  if (element.className) {
    const mainClasses = element.className.split(' ').slice(0, 2);
    if (mainClasses.length > 0) {
      selectors.push(`.${mainClasses.join('.')}`);
    }
  }
  
  return selectors;
}

function saveSimpleRecording() {
  const recordingData = {
    menuButton: recordedMenuButton,
    exportButton: recordedExportButton,
    timestamp: new Date().toISOString()
  };
  
  try {
    localStorage.setItem('quicksight_simple_recording', JSON.stringify(recordingData));
    console.log('✅ Recording saved successfully!');
  } catch (error) {
    console.error('❌ Error saving recording:', error);
  }
}

function stopSimpleRecording() {
  console.log('⏹️ Simple recording stopped');
  isSimpleRecording = false;
  document.removeEventListener('click', handleRecordingClick, true);
  hideRecordingIndicator();
}

// AUTOMATED DOWNLOAD using simple recording
function performSimpleDownload() {
  console.log('🚀 Starting simple automated download...');
  
  // Load recording
  let recordingData;
  try {
    console.log('📂 Loading recording from localStorage...');
    const stored = localStorage.getItem('quicksight_simple_recording');
    if (!stored) {
      console.log('❌ No recording found! Please record first with startSimpleRecording()');
      alert('❌ No recording found! Please record first by clicking "Start Recording" and following the steps.');
      return;
    }
    recordingData = JSON.parse(stored);
    console.log('✅ Recording loaded successfully:', recordingData);
  } catch (error) {
    console.error('❌ Error loading recording:', error);
    alert('❌ Error loading recording: ' + error.message);
    return;
  }
  
  console.log('📋 Using recorded data:', recordingData);
  
  // Step 1: Find and click menu button
  console.log('🔍 Step 1: Finding menu button...');
  
  let menuButton = null;
  
  // Try each selector for menu button
  for (const selector of recordingData.menuButton.selector) {
    try {
      if (selector.includes(':contains')) {
        // Handle text-based selectors manually
        continue;
      }
      
      const element = document.querySelector(selector);
      if (element && element.offsetParent !== null) {
        console.log(`✅ Found menu button with: ${selector}`);
        menuButton = element;
        break;
      }
    } catch (e) {
      console.log(`⚠️ Selector failed: ${selector}`);
    }
  }
  
  // Fallback: look for exact data-automation-id we know works
  if (!menuButton) {
    console.log('🔍 Fallback: Looking for analysis_visual_dropdown_menu_button...');
    menuButton = document.querySelector('[data-automation-id="analysis_visual_dropdown_menu_button"]');
  }
  
  if (!menuButton) {
    console.log('❌ Could not find menu button');
    return;
  }
  
  // Click menu button
  console.log('🖱️ Clicking menu button...');
  menuButton.click();
  
  // Step 2: Wait and find export button
  setTimeout(() => {
    console.log('🔍 Step 2: Finding export button...');
    
    let exportButton = null;
    
    // Try recorded selectors for export button
    for (const selector of recordingData.exportButton.selector) {
      try {
        if (selector.includes(':contains')) {
          // Find by text content manually
          const menuItems = document.querySelectorAll('li[role="menuitem"]');
          for (const item of menuItems) {
            if (item.textContent?.trim() === 'Export to CSV') {
              exportButton = item;
              break;
            }
          }
        } else {
          const element = document.querySelector(selector);
          if (element && element.offsetParent !== null) {
            console.log(`✅ Found export button with: ${selector}`);
            exportButton = element;
            break;
          }
        }
      } catch (e) {
        console.log(`⚠️ Export selector failed: ${selector}`);
      }
      
      if (exportButton) break;
    }
    
    // Fallback: look for dashboard_visual_dropdown_export
    if (!exportButton) {
      console.log('🔍 Fallback: Looking for dashboard_visual_dropdown_export...');
      exportButton = document.querySelector('[data-automation-id="dashboard_visual_dropdown_export"]');
    }
    
    // Final fallback: text search
    if (!exportButton) {
      console.log('🔍 Final fallback: Text search for Export to CSV...');
      const allElements = document.querySelectorAll('*');
      for (const element of allElements) {
        if (element.textContent?.trim() === 'Export to CSV' && element.offsetParent) {
          exportButton = element;
          break;
        }
      }
    }
    
    if (!exportButton) {
      console.log('❌ Could not find export button');
      return;
    }
    
    // Click export button
    console.log('🖱️ Clicking export button...');
    exportButton.click();
    
    console.log('🎉 Simple download completed!');
    console.log('📁 Check your Downloads folder for the CSV file');
    
  }, 1500);
}

// Visual indicator functions
function showRecordingIndicator(message, type = 'recording') {
  hideRecordingIndicator();
  
  const indicator = document.createElement('div');
  indicator.id = 'recording-indicator';
  indicator.style.cssText = `
    position: fixed;
    top: 20px;
    left: 20px;
    background: ${type === 'success' ? '#4CAF50' : '#ff4444'};
    color: white;
    padding: 15px 20px;
    border-radius: 8px;
    z-index: 999999;
    font-family: Arial, sans-serif;
    font-size: 16px;
    font-weight: bold;
    box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    border: 3px solid ${type === 'success' ? '#2E7D32' : '#cc0000'};
    max-width: 300px;
  `;
  indicator.textContent = `🔴 ${message}`;
  
  document.body.appendChild(indicator);
}

function hideRecordingIndicator() {
  const existing = document.getElementById('recording-indicator');
  if (existing) {
    existing.remove();
  }
}

// OLD: Main download function using recorded selectors (keeping for compatibility)
function performAutoDownload() {
  console.log('🚀 Starting auto download process...');
  
  // First, try to close any open menus to reset state
  console.log('🔄 Resetting menu state...');
  
  // Click elsewhere to close any open menus
  try {
    const bodyClick = new MouseEvent('click', { bubbles: true });
    document.body.dispatchEvent(bodyClick);
    
    // Wait a moment for any menus to close
    setTimeout(() => {
      continueDownload();
    }, 500);
  } catch (error) {
    console.log('⚠️ Could not reset menu state, continuing anyway...');
    continueDownload();
  }
}

function continueDownload() {
  // First try to load recorded selectors
  loadRecordedSelectors((hasRecorded) => {
    if (!hasRecorded) {
      console.log('❌ No recorded selectors found!');
      console.log('💡 Use startRecording() to record the button locations first');
      return;
    }
    
    console.log('✅ Using recorded selectors for automation');
    
    // Step 1: Find menu button using recorded selector
    console.log('🔍 Step 1: Looking for recorded menu button...');
    
    let menuButton = null;
    
    // Try the recorded selectors first
    for (const selector of recordedSelectors.menuButton.selector) {
      try {
        const element = document.querySelector(selector);
        if (element && element.offsetParent !== null) { // Check if visible
          console.log(`✅ Found menu button with selector: ${selector}`);
          menuButton = element;
          break;
        }
      } catch (e) {
        continue;
      }
    }
    
    // If recorded selectors fail, try to find the Supply & Demand menu button
    if (!menuButton) {
      console.log('🔍 Recorded selectors failed, searching for Supply & Demand menu...');
      
      // Look for buttons with Supply & Demand related attributes
      const allButtons = document.querySelectorAll('button');
      for (let button of allButtons) {
        const ariaLabel = button.getAttribute('aria-label') || '';
        const dataId = button.getAttribute('data-automation-id') || '';
        
        if ((ariaLabel.toLowerCase().includes('supply') && ariaLabel.toLowerCase().includes('demand')) ||
            dataId.includes('analysis_visual_dropdown') ||
            dataId.includes('visual_dropdown_menu')) {
          console.log(`✅ Found menu button by search: ${ariaLabel || dataId}`);
          menuButton = button;
          break;
        }
      }
    }
    
    if (!menuButton) {
      console.log('❌ Could not find menu button with any method');
      console.log('💡 Try recording again with startRecording()');
      return;
    }
    
    // Step 2: Click menu button
    console.log('🖱️ Step 2: Clicking menu button...');
    menuButton.click();
    
    // Step 3: Wait and find export option with improved search
    setTimeout(() => {
      console.log('🔍 Step 3: Looking for export option...');
      
      let exportOption = null;
      
      // First try recorded selectors (but skip generic 'li' selectors)
      if (recordedSelectors.exportOption && recordedSelectors.exportOption.selector) {
        for (const selector of recordedSelectors.exportOption.selector) {
          if (selector !== 'li' && selector !== 'div') { // Skip generic selectors
            try {
              const element = document.querySelector(selector);
              if (element && element.offsetParent !== null) { // Check if visible
                console.log(`✅ Found export option with selector: ${selector}`);
                exportOption = element;
                break;
              }
            } catch (e) {
              continue;
            }
          }
        }
      }
      
      // If recorded selectors fail, search for export text
      if (!exportOption) {
        console.log('🔍 Searching for export option by text...');
        
        const allElements = document.querySelectorAll('*');
        for (let element of allElements) {
          if (element.offsetParent !== null) { // visible
            const text = element.textContent || '';
            const cleanText = text.trim();
            
            // Look for exact export text matches
            if (cleanText === 'Export to CSV' || 
                cleanText === 'Export' ||
                (cleanText.includes('Export') && cleanText.includes('CSV'))) {
              console.log(`✅ Found export option by text: "${cleanText}"`);
              exportOption = element;
              break;
            }
          }
        }
      }
      
      // Final fallback - look for any clickable elements in dropdowns/menus
      if (!exportOption) {
        console.log('🔍 Final fallback: looking in menu containers...');
        
        const menuContainers = document.querySelectorAll('[role="menu"], .MuiMenu-list, .dropdown-menu, ul, ol');
        for (let container of menuContainers) {
          if (container.offsetParent !== null) { // visible
            const clickableElements = container.querySelectorAll('li, [role="menuitem"], button, a');
            for (let element of clickableElements) {
              const text = element.textContent || '';
              if (text.toLowerCase().includes('export') && text.toLowerCase().includes('csv')) {
                console.log(`✅ Found export option in menu: "${text}"`);
                exportOption = element;
                break;
              }
            }
            if (exportOption) break;
          }
        }
      }
      
      if (!exportOption) {
        console.log('❌ Could not find export option anywhere');
        console.log('🔍 Available menu items:');
        
        // Debug: show what's available
        const menuItems = document.querySelectorAll('[role="menuitem"], li');
        for (let item of menuItems) {
          if (item.offsetParent !== null) {
            const text = item.textContent?.trim();
            if (text && text.length < 100) {
              console.log(`  - "${text}"`);
            }
          }
        }
        return;
      }
      
      // Step 4: Click export option
      console.log('🖱️ Step 4: Clicking export option...');
      exportOption.click();
      
      setTimeout(() => {
        console.log('🎉 Download process completed!');
        console.log('📁 Check your Downloads folder for the CSV file');
      }, 2000);
      
    }, 1500);
  });
}

function showDebugInfo() {
  console.log('🔍 Available buttons with menu/dropdown attributes:');
  
  const allButtons = document.querySelectorAll('button');
  for (let button of allButtons) {
    if (!button.offsetParent) continue;
    
    const ariaLabel = button.getAttribute('aria-label') || '';
    const dataId = button.getAttribute('data-automation-id') || '';
    
    if (ariaLabel.toLowerCase().includes('menu') ||
        ariaLabel.toLowerCase().includes('options') ||
        dataId.includes('dropdown') ||
        dataId.includes('menu')) {
      console.log(`  - Button: "${ariaLabel}" (${dataId})`);
    }
  }
}

// Function to debug all buttons on page
function debugAllButtons() {
  console.log('🔍 DEBUG: ALL BUTTONS ON PAGE:');
  
  const allButtons = document.querySelectorAll('button');
  let buttonList = [];
  
  allButtons.forEach((button, index) => {
    if (!button.offsetParent) return; // Skip hidden buttons
    
    const ariaLabel = button.getAttribute('aria-label') || '';
    const dataId = button.getAttribute('data-automation-id') || '';
    const title = button.getAttribute('title') || '';
    const className = button.className || '';
    const text = button.textContent?.trim().substring(0, 30) || '';
    
    // Only show buttons that might be relevant
    if (ariaLabel.toLowerCase().includes('supply') ||
        ariaLabel.toLowerCase().includes('demand') ||
        ariaLabel.toLowerCase().includes('menu') ||
        ariaLabel.toLowerCase().includes('options') ||
        dataId.includes('dropdown') ||
        dataId.includes('menu') ||
        dataId.includes('visual') ||
        dataId.includes('analysis')) {
      
      buttonList.push({
        index: index + 1,
        ariaLabel,
        dataId,
        title,
        className: className.substring(0, 80),
        text,
        element: button
      });
    }
  });
  
  buttonList.forEach((btn, idx) => {
    console.log(`  ${idx + 1}. Button #${btn.index}:`);
    console.log(`     aria-label: "${btn.ariaLabel}"`);
    console.log(`     data-automation-id: "${btn.dataId}"`);
    console.log(`     title: "${btn.title}"`);
    console.log(`     className: "${btn.className}"`);
    console.log(`     text: "${btn.text}"`);
    console.log(`     ────────────────────────────────────────`);
  });
  
  return buttonList;
}

// Save recorded selectors - prioritize localStorage for reliability
function saveRecordedSelectors() {
  const storageKey = 'quicksight_recorded_selectors';
  const dataToSave = JSON.stringify(recordedSelectors);
  
  console.log('💾 Saving recorded selectors...');
  
  // Always save to localStorage first (most reliable)
  try {
    localStorage.setItem(storageKey, dataToSave);
    console.log('✅ Saved to localStorage successfully');
  } catch (error) {
    console.error('❌ Error saving to localStorage:', error);
  }
  
  // Also try chrome.storage as backup (if available)
  try {
    if (typeof chrome !== 'undefined' && chrome.storage && chrome.storage.local && !chrome.runtime.lastError) {
      chrome.storage.local.set({ [storageKey]: recordedSelectors }, () => {
        if (chrome.runtime.lastError) {
          console.log('⚠️ Chrome storage failed, but localStorage worked');
        } else {
          console.log('✅ Also saved to chrome.storage as backup');
        }
      });
    }
  } catch (error) {
    // Ignore chrome.storage errors since localStorage is primary
    console.log('⚠️ Chrome storage not available, but localStorage worked');
  }
  
  console.log('📋 Saved data:', recordedSelectors);
}

// Load recorded selectors - prioritize localStorage
function loadRecordedSelectors(callback) {
  const storageKey = 'quicksight_recorded_selectors';
  
  console.log('📂 Loading recorded selectors...');
  
  // Try localStorage first (most reliable)
  try {
    const stored = localStorage.getItem(storageKey);
    if (stored) {
      recordedSelectors = JSON.parse(stored);
      console.log('✅ Loaded from localStorage:', recordedSelectors);
      callback(true);
      return;
    }
  } catch (error) {
    console.error('❌ Error loading from localStorage:', error);
  }
  
  // Fallback to chrome.storage only if localStorage fails
  try {
    if (typeof chrome !== 'undefined' && chrome.storage && chrome.storage.local) {
      chrome.storage.local.get([storageKey], (result) => {
        if (chrome.runtime.lastError) {
          console.log('❌ Chrome storage also failed');
          callback(false);
        } else if (result[storageKey]) {
          recordedSelectors = result[storageKey];
          console.log('✅ Loaded from chrome.storage fallback:', recordedSelectors);
          callback(true);
        } else {
          console.log('📂 No recorded selectors found in any storage');
          callback(false);
        }
      });
    } else {
      console.log('📂 No storage available');
      callback(false);
    }
  } catch (error) {
    console.error('❌ All storage methods failed:', error);
    callback(false);
  }
}

console.log('🔧 Checkpoint 1: Reached function assignment section');

// Check which functions exist before assigning
console.log('🔧 Function existence check:', {
  performAutoDownload: typeof performAutoDownload,
  startSimpleRecording: typeof startSimpleRecording,
  stopSimpleRecording: typeof stopSimpleRecording,
  performSimpleDownload: typeof performSimpleDownload
});

// Make functions available globally (with error handling for each)
try {
  window.startSimpleRecording = startSimpleRecording;
  console.log('✅ startSimpleRecording assigned');
} catch (e) { console.error('❌ Error assigning startSimpleRecording:', e); }

try {
  window.stopSimpleRecording = stopSimpleRecording;
  console.log('✅ stopSimpleRecording assigned');
} catch (e) { console.error('❌ Error assigning stopSimpleRecording:', e); }

try {
  window.performSimpleDownload = performSimpleDownload;
  console.log('✅ performSimpleDownload assigned');
} catch (e) { console.error('❌ Error assigning performSimpleDownload:', e); }

// Skip the old functions for now to avoid errors
console.log('🔧 Checkpoint 2: Core functions assigned to window');

// Test function to debug the system
window.testSimpleRecordingSystem = function() {
  console.log('🧪 Testing Simple Recording System...');
  console.log('📋 Current recording state:', {
    isSimpleRecording,
    recordedMenuButton,
    recordedExportButton
  });
  
  // Check localStorage
  const stored = localStorage.getItem('quicksight_simple_recording');
  if (stored) {
    console.log('📂 Stored recording data:', JSON.parse(stored));
  } else {
    console.log('📂 No recording data in localStorage');
  }
  
  // Check if functions exist
  console.log('🔧 Function availability:', {
    startSimpleRecording: typeof startSimpleRecording,
    performSimpleDownload: typeof performSimpleDownload,
    stopSimpleRecording: typeof stopSimpleRecording
  });
  
  console.log('✅ Test complete - check console output above');
};

console.log('🔧 Checkpoint 3: Test function created');

// Immediate test that functions are assigned
console.log('🔧 Immediate function assignment check:', {
  testSimpleRecordingSystem: typeof window.testSimpleRecordingSystem,
  startSimpleRecording: typeof window.startSimpleRecording,
  performSimpleDownload: typeof window.performSimpleDownload
});

console.log('🔧 Checkpoint 4: About to add event listeners');

// WORKAROUND: Listen for window messages to trigger functions
window.addEventListener('message', function(event) {
  if (event.data && event.data.action === 'startSimpleRecording') {
    console.log('🎯 Starting simple recording via message!');
    startSimpleRecording();
  } else if (event.data && event.data.action === 'performSimpleDownload') {
    console.log('🎯 Performing simple download via message!');
    performSimpleDownload();
  } else if (event.data && event.data.action === 'debugButtons') {
    console.log('🎯 Debugging all buttons!');
    debugAllButtons();
  }
});

// Listen for messages from background script (with improved error handling)
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  console.log('📨 Content script received message:', request);
  
  try {
    if (request.action === 'downloadSupplyDemand') {
      console.log('🎯 Starting scheduled download...');
      performSimpleDownload(); // Use simple download instead
      sendResponse({ success: true, message: 'Download initiated' });
      return true;
    } else if (request.action === 'startRecording') {
      console.log('🎯 Starting simple recording from popup (legacy action)...');
      startSimpleRecording(); // Use simple recording instead
      sendResponse({ success: true });
      return true;
    } else if (request.action === 'startSimpleRecording') {
      console.log('🎯 Starting simple recording from popup...');
      try {
        startSimpleRecording();
        console.log('✅ Simple recording started successfully');
        sendResponse({ success: true });
      } catch (recordingError) {
        console.error('❌ Error starting simple recording:', recordingError);
        sendResponse({ success: false, error: recordingError.message });
      }
      return true;
    } else if (request.action === 'performSimpleDownload') {
      console.log('🎯 Performing simple download from popup...');
      try {
        performSimpleDownload();
        console.log('✅ Simple download started successfully');
        sendResponse({ success: true });
      } catch (downloadError) {
        console.error('❌ Error performing simple download:', downloadError);
        sendResponse({ success: false, error: downloadError.message });
      }
      return true;
    } else {
      console.log('⚠️ Unknown message action:', request.action);
      sendResponse({ success: false, error: 'Unknown action' });
      return true;
    }
  } catch (error) {
    console.error('❌ Error handling message:', error);
    sendResponse({ success: false, error: error.message });
    return true;
  }
});

// Auto-announce we're ready
setTimeout(() => {
  console.log('🎯 QuickSight Auto Downloader - Ready!');
  
  // Verify functions are available
  console.log('🔧 Function check:', {
    testSimpleRecordingSystem: typeof window.testSimpleRecordingSystem,
    startSimpleRecording: typeof window.startSimpleRecording,
    performSimpleDownload: typeof window.performSimpleDownload
  });
  
  console.log('💡 SIMPLE RECORDING: startSimpleRecording()');
  console.log('💡 SIMPLE DOWNLOAD: performSimpleDownload()');
  console.log('💡 TEST SYSTEM: testSimpleRecordingSystem()');
  console.log('💡 Or via messages:');
  console.log('   window.postMessage({action: "startSimpleRecording"}, "*")');
  console.log('   window.postMessage({action: "performSimpleDownload"}, "*")');
  console.log('📅 Scheduled downloads will run automatically every 1.5 hours (7 AM - 5 PM)');
  
  // Double-check function availability
  if (typeof window.testSimpleRecordingSystem === 'undefined') {
    console.error('❌ testSimpleRecordingSystem not available!');
    console.log('🔄 Re-creating functions...');
    
    // Re-create the test function
    window.testSimpleRecordingSystem = function() {
      console.log('🧪 Testing Simple Recording System...');
      console.log('📋 Current recording state:', {
        isSimpleRecording,
        recordedMenuButton,
        recordedExportButton
      });
      
      const stored = localStorage.getItem('quicksight_simple_recording');
      if (stored) {
        console.log('📂 Stored recording data:', JSON.parse(stored));
      } else {
        console.log('📂 No recording data in localStorage');
      }
      
      console.log('🔧 Function availability:', {
        startSimpleRecording: typeof startSimpleRecording,
        performSimpleDownload: typeof performSimpleDownload,
        stopSimpleRecording: typeof stopSimpleRecording
      });
      
      console.log('✅ Test complete - check console output above');
    };
    
    window.startSimpleRecording = startSimpleRecording;
    window.performSimpleDownload = performSimpleDownload;
    window.stopSimpleRecording = stopSimpleRecording;
    
    console.log('✅ Functions re-created');
  } else {
    console.log('✅ All functions available');
  }
}, 1000);

} catch (globalError) {
  console.error('❌ CRITICAL ERROR in content script:', globalError);
  console.error('❌ Stack trace:', globalError.stack);
  console.log('🔧 Content script failed to initialize properly');
} 