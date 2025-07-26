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
  console.log('📋 Using recorded selectors from user session');

  // Step 0: First, activate the Supply & Demand chart to make menu buttons visible
  console.log('🎯 Step 0: Activating Supply & Demand chart to reveal menu buttons...');
  
  // Find the Supply & Demand chart container/title
  let chartElement = null;
  
  // Method 1: Look for the visual title container with "Supply & Demand" text
  const titleContainers = document.querySelectorAll('.visual-title-container');
  for (const container of titleContainers) {
    const text = container.textContent?.trim();
    if (text === 'Supply & Demand') {
      chartElement = container;
      console.log('✅ Found Supply & Demand chart by title container');
      break;
    }
  }
  
  // Method 2: If not found, look for any element with aria-label="visual title" containing Supply & Demand
  if (!chartElement) {
    const visualTitles = document.querySelectorAll('[aria-label="visual title"]');
    for (const title of visualTitles) {
      const text = title.textContent?.trim();
      if (text === 'Supply & Demand') {
        chartElement = title;
        console.log('✅ Found Supply & Demand chart by aria-label');
        break;
      }
    }
  }
  
  // Method 3: Broader search - look for any element containing "Supply & Demand" text
  if (!chartElement) {
    console.log('🔍 Broader search for Supply & Demand chart...');
    const allElements = document.querySelectorAll('*');
    for (const element of allElements) {
      const text = element.textContent?.trim();
      if (text === 'Supply & Demand' && element.offsetParent !== null) {
        // Make sure it's a reasonable container (has some size)
        const rect = element.getBoundingClientRect();
        if (rect.width > 50 && rect.height > 20) {
          chartElement = element;
          console.log('✅ Found Supply & Demand chart by text search');
          break;
        }
      }
    }
  }
  
  if (!chartElement) {
    console.error('❌ CRITICAL: Could not find the Supply & Demand chart to activate');
    console.log('💡 Make sure you are on the QuickSight dashboard with the Supply & Demand chart visible');
    return false;
  }
  
  // Activate the chart by simulating hover and focus
  console.log('🖱️ Activating chart with hover and focus events...');
  try {
    // Create and dispatch mouse events to simulate hover
    const mouseEnterEvent = new MouseEvent('mouseenter', {
      bubbles: true,
      cancelable: true,
      view: window
    });
    
    const mouseOverEvent = new MouseEvent('mouseover', {
      bubbles: true,
      cancelable: true,
      view: window
    });
    
    // Dispatch hover events
    chartElement.dispatchEvent(mouseEnterEvent);
    chartElement.dispatchEvent(mouseOverEvent);
    
    // Also try focus if the element can be focused
    if (chartElement.focus && typeof chartElement.focus === 'function') {
      chartElement.focus();
    }
    
    // Try clicking on the chart area (but not the menu button yet)
    const clickEvent = new MouseEvent('click', {
      bubbles: true,
      cancelable: true,
      view: window
    });
    chartElement.dispatchEvent(clickEvent);
    
    console.log('✅ Chart activation events dispatched');
    
  } catch (error) {
    console.error('❌ Error activating chart:', error);
    // Continue anyway, maybe the buttons are already visible
  }
  
  // Wait a moment for the UI to update and show the menu buttons
  console.log('⏳ Waiting for menu buttons to become visible...');
  
  setTimeout(() => {
    proceedWithDownload();
  }, 500); // Give it 500ms for the buttons to appear
}

function proceedWithDownload() {
  // Step 1: Find the correct menu button using exact recorded criteria
  console.log('🔍 Step 1: Searching for Supply & Demand menu button...');
  
  // First try: Find by data-automation-id AND aria-label containing "Supply & Demand"
  let correctMenuButton = null;
  const allMenuButtons = document.querySelectorAll('[data-automation-id="analysis_visual_dropdown_menu_button"]');
  
  console.log(`📊 Found ${allMenuButtons.length} buttons with analysis_visual_dropdown_menu_button`);

  // Look for the specific Supply & Demand button
  for (const button of allMenuButtons) {
    const ariaLabel = button.getAttribute('aria-label') || '';
    console.log(`🔍 Checking button with aria-label: "${ariaLabel}"`);
    
    if (ariaLabel.includes('Supply & Demand')) {
      correctMenuButton = button;
      console.log('✅ Found the correct Supply & Demand menu button!');
      console.log(`   - Full aria-label: "${ariaLabel}"`);
      console.log(`   - Is visible: ${button.offsetParent !== null}`);
      break;
    }
  }

  if (!correctMenuButton) {
    console.error('❌ CRITICAL: Could not find the Supply & Demand menu button after chart activation');
    console.log('🔍 Available buttons with analysis_visual_dropdown_menu_button:');
    allMenuButtons.forEach((btn, index) => {
      const label = btn.getAttribute('aria-label') || 'No aria-label';
      const isVisible = btn.offsetParent !== null;
      console.log(`   ${index + 1}. "${label}" (visible: ${isVisible})`);
    });
    
    // Try to provide helpful guidance
    if (allMenuButtons.length === 0) {
      console.log('💡 No menu buttons found even after activation. Chart may not be fully loaded.');
      console.log('💡 Try waiting a moment and running the script again.');
    } else {
      console.log('💡 Menu buttons exist but none match "Supply & Demand". Is the chart visible on screen?');
    }
    return false;
  }
  
  // Step 2: Click the menu button
  console.log('🖱️ Step 2: Clicking the Supply & Demand menu button...');
  try {
    correctMenuButton.click();
    console.log('✅ Menu button clicked successfully');
  } catch (error) {
    console.error('❌ Error clicking menu button:', error);
    return false;
  }

  // Step 3: Wait for menu to appear and find export button
  console.log('⏳ Step 3: Waiting for dropdown menu to appear...');
  
  // Use a more robust approach with retries
  let attempts = 0;
  const maxAttempts = 10;
  const retryInterval = 200; // Check every 200ms
  
  const findAndClickExport = () => {
    attempts++;
    console.log(`🔍 Attempt ${attempts}/${maxAttempts}: Looking for export button...`);
    
    // Method 1: Try by data-automation-id (most reliable)
    let exportButton = document.querySelector('[data-automation-id="dashboard_visual_dropdown_export"]');
    
    if (exportButton) {
      console.log('✅ Found export button by data-automation-id');
    } else {
      // Method 2: Try by text content within menu items
      console.log('🔍 Fallback: Searching by text content...');
      const menuItems = document.querySelectorAll('li[role="menuitem"]');
      for (const item of menuItems) {
        const text = item.textContent?.trim();
        if (text === 'Export to CSV') {
          exportButton = item;
          console.log('✅ Found export button by text content');
          break;
        }
      }
    }

    if (exportButton) {
      // Check if button is visible and clickable
      if (exportButton.offsetParent !== null) {
        console.log('🖱️ Step 4: Clicking export button...');
        try {
          exportButton.click();
          console.log('🎉 Export button clicked successfully!');
          console.log('📁 Download should start shortly. Check your Downloads folder.');
          return true;
        } catch (error) {
          console.error('❌ Error clicking export button:', error);
          return false;
        }
      } else {
        console.log('⚠️ Export button found but not visible, retrying...');
      }
    } else {
      console.log(`⚠️ Export button not found on attempt ${attempts}`);
      
      // Debug: Show what menu items are available
      if (attempts === 1) {
        const availableItems = document.querySelectorAll('li[role="menuitem"]');
        console.log('🔍 Available menu items:');
        availableItems.forEach((item, index) => {
          const text = item.textContent?.trim();
          const dataId = item.getAttribute('data-automation-id');
          const isVisible = item.offsetParent !== null;
          console.log(`   ${index + 1}. "${text}" (data-id: ${dataId}, visible: ${isVisible})`);
        });
      }
    }
    
    // Retry if we haven't reached max attempts
    if (attempts < maxAttempts) {
      setTimeout(findAndClickExport, retryInterval);
    } else {
      console.error('❌ FAILED: Could not find or click export button after all attempts');
      console.log('💡 The menu may not have opened properly or the export option might not be available');
      return false;
    }
  };
  
  // Start looking for export button after a short delay
  setTimeout(findAndClickExport, 300);
  
  return true;
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
  
  console.log(`🔍 Found ${allButtons.length} total buttons on page`);
  
  allButtons.forEach((button, index) => {
    const ariaLabel = button.getAttribute('aria-label') || '';
    const dataId = button.getAttribute('data-automation-id') || '';
    const title = button.getAttribute('title') || '';
    const className = button.className || '';
    const text = button.textContent?.trim().substring(0, 30) || '';
    const isVisible = button.offsetParent !== null;
    
    // Show ALL buttons, not just filtered ones
    buttonList.push({
      index: index + 1,
      ariaLabel,
      dataId,
      title,
      className: className.substring(0, 80),
      text,
      isVisible,
      element: button
    });
  });
  
  // Show all buttons first
  console.log('📋 ALL BUTTONS (including hidden):');
  buttonList.forEach((btn, idx) => {
    if (btn.dataId.includes('analysis_visual_dropdown_menu_button') || 
        btn.ariaLabel.includes('Supply') || 
        btn.ariaLabel.includes('Demand')) {
      console.log(`  ${idx + 1}. Button #${btn.index}:`);
      console.log(`     visible: ${btn.isVisible}`);
      console.log(`     aria-label: "${btn.ariaLabel}"`);
      console.log(`     data-automation-id: "${btn.dataId}"`);
      console.log(`     title: "${btn.title}"`);
      console.log(`     className: "${btn.className}"`);
      console.log(`     text: "${btn.text}"`);
      console.log(`     ────────────────────────────────────────`);
    }
  });
  
  // Also check for any elements with the specific data-automation-id
  console.log('🎯 SPECIFIC SEARCH:');
  const specificButton = document.querySelector('[data-automation-id="analysis_visual_dropdown_menu_button"]');
  if (specificButton) {
    console.log('✅ Found analysis_visual_dropdown_menu_button!');
    console.log(`   visible: ${specificButton.offsetParent !== null}`);
    console.log(`   aria-label: "${specificButton.getAttribute('aria-label')}"`);
  } else {
    console.log('❌ analysis_visual_dropdown_menu_button NOT FOUND');
  }
  
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