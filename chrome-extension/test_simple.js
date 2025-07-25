// Simple test script - just to verify content scripts work
console.log('🧪 TEST SCRIPT LOADED - Extension is working!');

// Try different ways to make function globally available
function testExtension() {
  console.log('✅ Extension content script is working!');
  console.log('📊 Current URL:', window.location.href);
  console.log('📋 Page title:', document.title);
  
  // Test basic element finding
  const allDivs = document.querySelectorAll('div');
  console.log(`📦 Found ${allDivs.length} div elements on page`);
  
  return {
    url: window.location.href,
    title: document.title,
    divCount: allDivs.length,
    working: true
  };
}

// Try multiple ways to expose the function
window.testExtension = testExtension;
globalThis.testExtension = testExtension;

// Also add it to document for easier access
document.testExtension = testExtension;

// Alternative: Create a custom event listener
document.addEventListener('testExtension', function() {
  testExtension();
});

// Auto-announce we're loaded and provide alternative ways to test
setTimeout(() => {
  console.log('🎯 QuickSight Auto Downloader TEST - Ready for testing!');
  console.log('💡 Try these commands:');
  console.log('   1. testExtension()');
  console.log('   2. window.testExtension()');
  console.log('   3. document.testExtension()');
  console.log('   4. document.dispatchEvent(new Event("testExtension"))');
  
  // Auto-run the test to show it works
  console.log('🚀 Auto-running test now:');
  testExtension();
}, 1000); 