#!/usr/bin/env node
/**
 * VetScan Pro - Automatic Blender Export Watcher
 * Watches for changes in Blender files and automatically exports to GLB
 */

const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

// Configuration
const WATCH_DIR = path.join(__dirname, '..', 'assets', 'models', 'animals', 'bello');
const BLENDER_PATH = '/Applications/Blender.app/Contents/MacOS/Blender';
const EXPORT_SCRIPT = path.join(__dirname, 'direct-bello-export.py');

// Colors for console output
const colors = {
    reset: '\x1b[0m',
    bright: '\x1b[1m',
    green: '\x1b[32m',
    yellow: '\x1b[33m',
    blue: '\x1b[34m',
    red: '\x1b[31m'
};

function log(message, color = '') {
    const timestamp = new Date().toISOString().split('T')[1].split('.')[0];
    console.log(`${color}[${timestamp}] ${message}${colors.reset}`);
}

log('🔍 VetScan Pro - Blender Export Watcher', colors.bright);
log(`📁 Watching directory: ${WATCH_DIR}`, colors.blue);
log(`🔧 Using Blender at: ${BLENDER_PATH}`, colors.blue);
console.log('=' .repeat(60));

// Create watch directory if it doesn't exist
if (!fs.existsSync(WATCH_DIR)) {
    fs.mkdirSync(WATCH_DIR, { recursive: true });
    log('📁 Created watch directory', colors.green);
}

// Track file modification times to prevent duplicate exports
const fileTimestamps = new Map();
let exportInProgress = false;

// Export function
function exportModel(filename) {
    if (exportInProgress) {
        log('⏳ Export already in progress, queuing...', colors.yellow);
        setTimeout(() => exportModel(filename), 5000);
        return;
    }

    exportInProgress = true;
    log(`🚀 Exporting ${filename}...`, colors.green);

    const exportProcess = spawn('python3', [EXPORT_SCRIPT], {
        cwd: path.dirname(EXPORT_SCRIPT)
    });

    exportProcess.stdout.on('data', (data) => {
        const output = data.toString().trim();
        if (output && !output.includes('Blender')) {
            log(`   ${output}`, colors.blue);
        }
    });

    exportProcess.stderr.on('data', (data) => {
        log(`❌ Error: ${data}`, colors.red);
    });

    exportProcess.on('close', (code) => {
        exportInProgress = false;
        if (code === 0) {
            log(`✅ Export completed successfully!`, colors.green);
            notifyBrowser();
        } else {
            log(`❌ Export failed with code ${code}`, colors.red);
        }
    });
}

// Browser notification via WebSocket (optional)
function notifyBrowser() {
    try {
        // Try to notify any connected browsers
        const WebSocket = require('ws');
        const ws = new WebSocket('ws://localhost:8765');
        
        ws.on('open', () => {
            ws.send(JSON.stringify({
                type: 'model_updated',
                path: 'assets/models/animals/bello/bello_high.glb',
                timestamp: Date.now()
            }));
            ws.close();
            log('📱 Browser notified of model update', colors.green);
        });

        ws.on('error', () => {
            // WebSocket server not available, that's okay
        });
    } catch (e) {
        // WebSocket module not available, skip notification
    }
}

// Watch for file changes
log('👀 Watching for changes...', colors.yellow);

// Watch for .blend file changes
fs.watch(WATCH_DIR, { recursive: true }, (eventType, filename) => {
    if (!filename) return;
    
    // Only watch .blend files
    if (!filename.endsWith('.blend')) return;
    
    const fullPath = path.join(WATCH_DIR, filename);
    
    // Check if file exists (might be a delete event)
    if (!fs.existsSync(fullPath)) return;
    
    // Get file stats
    const stats = fs.statSync(fullPath);
    const mtime = stats.mtime.getTime();
    
    // Check if this is a new modification
    const lastMtime = fileTimestamps.get(filename);
    if (lastMtime && mtime - lastMtime < 2000) {
        // Ignore if modified less than 2 seconds ago (duplicate event)
        return;
    }
    
    fileTimestamps.set(filename, mtime);
    
    log(`📝 Detected change in ${filename}`, colors.yellow);
    
    // Wait a moment for file write to complete
    setTimeout(() => {
        exportModel(filename);
    }, 1000);
});

// Also watch for manual trigger file
const triggerFile = path.join(WATCH_DIR, 'export.trigger');
setInterval(() => {
    if (fs.existsSync(triggerFile)) {
        log('🎯 Manual export triggered', colors.bright);
        fs.unlinkSync(triggerFile);
        exportModel('manual');
    }
}, 2000);

// Initial export on startup
log('🚀 Performing initial export...', colors.green);
exportModel('initial');

// Handle exit gracefully
process.on('SIGINT', () => {
    log('\n👋 Stopping watcher...', colors.yellow);
    process.exit(0);
});

// Instructions
console.log('\n' + '='.repeat(60));
log('📖 Instructions:', colors.bright);
log('1. Edit any .blend file in the watch directory', colors.blue);
log('2. The model will automatically export to GLB', colors.blue);
log('3. The browser will reload the model (if connected)', colors.blue);
log('4. Create "export.trigger" file to force export', colors.blue);
log('5. Press Ctrl+C to stop watching', colors.blue);
console.log('='.repeat(60) + '\n');

// Keep process alive
process.stdin.resume();