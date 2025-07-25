// Debug Content Script - Test QuickSight Element Detection
console.log('🔍 DEBUG: QuickSight Element Detection Test');

function debugQuickSightElements() {
  console.log('📊 Current page URL:', window.location.href);
  console.log('📊 Page title:', document.title);
  
  // Check if we're on QuickSight
  if (!window.location.href.includes('quicksight')) {
    console.log('❌ Not on QuickSight page');
    return;
  }
  
  console.log('✅ On QuickSight page');
  
  // Look for any Supply & Demand elements
  console.log('\n🔍 Looking for Supply & Demand content...');
  
  const allElements = document.querySelectorAll('*');
  let supplyDemandElements = [];
  
  for (const element of allElements) {
    const text = element.textContent?.toLowerCase() || '';
    if (text.includes('supply') && text.includes('demand')) {
      supplyDemandElements.push({
        element: element,
        text: text.substring(0, 100),
        tagName: element.tagName,
        className: element.className,
        id: element.id
      });
    }
  }
  
  console.log(`📋 Found ${supplyDemandElements.length} elements with 'Supply & Demand':`);
  supplyDemandElements.forEach((item, index) => {
    console.log(`  ${index + 1}. ${item.tagName} - "${item.text.substring(0, 50)}..."`);
    console.log(`     Class: ${item.className}`);
    console.log(`     ID: ${item.id}`);
  });
  
  // Look for visual containers
  console.log('\n🔍 Looking for visual containers...');
  const visualSelectors = [
    '[class*="visual"]',
    '[data-testid*="visual"]', 
    '[data-automation-id*="visual"]'
  ];
  
  let visualContainers = [];
  visualSelectors.forEach(selector => {
    const elements = document.querySelectorAll(selector);
    console.log(`📊 Found ${elements.length} elements with selector: ${selector}`);
    
    elements.forEach((element, index) => {
      if (element.textContent?.toLowerCase().includes('supply') || 
          element.textContent?.toLowerCase().includes('demand')) {
        visualContainers.push({
          selector: selector,
          element: element,
          text: element.textContent.substring(0, 100)
        });
      }
    });
  });
  
  console.log(`📊 Found ${visualContainers.length} visual containers with Supply/Demand content`);
  
  // Look for menu buttons
  console.log('\n🔍 Looking for menu buttons...');
  const menuSelectors = [
    'button[data-automation-id*="dropdown_menu"]',
    'button[data-automation-id*="visual_dropdown"]', 
    'button[data-automation-id*="menu"]',
    'button[aria-label*="menu"]',
    'button[aria-label*="options"]'
  ];
  
  let menuButtons = [];
  menuSelectors.forEach(selector => {
    const buttons = document.querySelectorAll(selector);
    console.log(`🔘 Found ${buttons.length} buttons with selector: ${selector}`);
    
    buttons.forEach(button => {
      if (button.offsetWidth > 0 && button.offsetHeight > 0) { // Visible check
        menuButtons.push({
          selector: selector,
          button: button,
          ariaLabel: button.getAttribute('aria-label'),
          dataId: button.getAttribute('data-automation-id'),
          visible: true
        });
      }
    });
  });
  
  console.log(`🔘 Found ${menuButtons.length} visible menu buttons`);
  menuButtons.forEach((item, index) => {
    console.log(`  ${index + 1}. aria-label: "${item.ariaLabel}"`);
    console.log(`     data-automation-id: "${item.dataId}"`);
  });
  
  // Summary
  console.log('\n📋 SUMMARY:');
  console.log(`✅ Supply & Demand elements: ${supplyDemandElements.length}`);
  console.log(`✅ Visual containers: ${visualContainers.length}`);
  console.log(`✅ Menu buttons: ${menuButtons.length}`);
  
  if (supplyDemandElements.length === 0) {
    console.log('⚠️ No Supply & Demand elements found. Make sure you\'re on the right dashboard.');
  }
  
  if (menuButtons.length === 0) {
    console.log('⚠️ No menu buttons found. The page might not be fully loaded.');
  }
  
  return {
    supplyDemandElements,
    visualContainers, 
    menuButtons
  };
}

// Auto-run debug after page loads
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    setTimeout(debugQuickSightElements, 3000);
  });
} else {
  setTimeout(debugQuickSightElements, 1000);
}

// Make function available globally for manual testing
window.debugQuickSight = debugQuickSightElements; 