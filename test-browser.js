// Simple browser test script to check for console errors
// Can be run with Node.js if Playwright is installed

const testUrls = [
    'http://localhost:8080/vetscan-ultimate.html',
    'http://localhost:8080/vetscan-story-mode.html'
];

async function testWithFetch() {
    console.log('🔍 Testing HTML files for basic loading...\n');
    
    for (const url of testUrls) {
        try {
            const response = await fetch(url);
            const text = await response.text();
            
            // Check if HTML loads
            if (response.ok && text.includes('<!DOCTYPE html>')) {
                console.log(`✅ ${url} - HTML loads successfully`);
                
                // Check for common JS errors in the code
                const jsErrors = [];
                
                // Check for undefined variables
                if (text.match(/\b(undefined|null)\./g)) {
                    jsErrors.push('Potential undefined variable access');
                }
                
                // Check for missing dependencies
                if (text.includes('three.min.js') && !text.includes('THREE')) {
                    jsErrors.push('Three.js might not be properly loaded');
                }
                
                if (jsErrors.length > 0) {
                    console.log(`⚠️  Potential issues found:`);
                    jsErrors.forEach(err => console.log(`   - ${err}`));
                } else {
                    console.log(`   No obvious JavaScript errors detected in source`);
                }
            } else {
                console.log(`❌ ${url} - Failed to load`);
            }
        } catch (error) {
            console.log(`❌ ${url} - Error: ${error.message}`);
        }
        console.log('');
    }
}

// Manual test instructions
console.log('=================================');
console.log('MANUAL BROWSER TEST INSTRUCTIONS');
console.log('=================================\n');
console.log('1. Open Chrome/Firefox');
console.log('2. Press F12 to open Developer Tools');
console.log('3. Go to Console tab');
console.log('4. Visit each URL:');
testUrls.forEach(url => console.log(`   - ${url}`));
console.log('5. Check for any red error messages in console');
console.log('6. Test basic interactions (click buttons, etc.)');
console.log('\n=================================\n');

// Run basic fetch test
testWithFetch().catch(console.error);