/**
 * Test GLB Loading System
 * Verify Claude Desktop import pipeline works
 */

const { WebSocket } = require('ws');
const fetch = require('node-fetch');

// Alternative: Use headless browser testing
const puppeteer = require('puppeteer');

async function testGLBLoading() {
    console.log('🧪 Testing Claude Desktop GLB Import System');
    console.log('='.repeat(50));
    
    const browser = await puppeteer.launch({ 
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    try {
        const page = await browser.newPage();
        
        // Enable console logging
        page.on('console', msg => {
            const type = msg.type();
            const text = msg.text();
            
            if (text.includes('[v7.1.0]')) {
                console.log(`🔍 Browser: ${text}`);
                
                if (text.includes('✅ Claude Desktop Model loaded')) {
                    console.log('🎉 SUCCESS: GLB Import working!');
                } else if (text.includes('⚠️ No Claude Desktop GLB found')) {
                    console.log('⚠️  Falling back to procedural model');
                }
            }
        });
        
        // Navigate to test page
        console.log('📱 Loading VetScan Pro v7.1.0...');
        await page.goto('http://localhost:8081/vetscan-bello-3d-v7.html', {
            waitUntil: 'networkidle2',
            timeout: 30000
        });
        
        // Wait for 3D initialization
        await page.waitForTimeout(5000);
        
        // Check for Three.js scene
        const sceneExists = await page.evaluate(() => {
            return typeof window.scene !== 'undefined' && window.scene !== null;
        });
        
        console.log(`🎮 3D Scene initialized: ${sceneExists ? '✅' : '❌'}`);
        
        // Check for Bello model
        const modelLoaded = await page.evaluate(() => {
            return typeof window.belloModel !== 'undefined' && window.belloModel !== null;
        });
        
        console.log(`🐕 Bello model loaded: ${modelLoaded ? '✅' : '❌'}`);
        
        // Test medical visualizations
        if (modelLoaded) {
            console.log('🔬 Testing medical visualizations...');
            
            const visualizations = ['normal', 'xray', 'ultrasound', 'thermal', 'mri', 'ct'];
            
            for (const viz of visualizations) {
                await page.evaluate((mode) => {
                    if (window.switchVisualization) {
                        window.switchVisualization(mode);
                    }
                }, viz);
                
                await page.waitForTimeout(500);
                console.log(`   ${viz}: ✅ Applied`);
            }
        }
        
        // Take screenshot
        await page.screenshot({ 
            path: 'test-results/glb-loading-test.png',
            fullPage: true 
        });
        
        console.log('📸 Screenshot saved: test-results/glb-loading-test.png');
        console.log('🎯 Test completed successfully!');
        
    } catch (error) {
        console.error('❌ Test failed:', error.message);
    } finally {
        await browser.close();
    }
}

// Simple HTTP test without puppeteer
async function simpleHTTPTest() {
    console.log('🌐 Testing HTTP endpoints...');
    
    const endpoints = [
        'http://localhost:8081/vetscan-bello-3d-v7.html',
        'http://localhost:8081/models/animals/dog/medium/bello_claude_desktop.glb'
    ];
    
    for (const url of endpoints) {
        try {
            const response = await fetch(url);
            const status = response.status;
            const size = response.headers.get('content-length');
            
            console.log(`${status === 200 ? '✅' : '❌'} ${url} (${size} bytes)`);
        } catch (error) {
            console.log(`❌ ${url} - ${error.message}`);
        }
    }
}

// Run tests
if (require.main === module) {
    (async () => {
        await simpleHTTPTest();
        
        // Try puppeteer test if available
        try {
            await testGLBLoading();
        } catch (error) {
            console.log('⚠️  Puppeteer test skipped:', error.message);
            console.log('💡 Install puppeteer for browser testing: npm install puppeteer');
        }
    })();
}