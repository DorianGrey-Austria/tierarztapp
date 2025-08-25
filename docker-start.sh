#!/bin/bash
# VetScan Pro 3000 - Docker Blender MCP Startup Script

set -e

echo "🎯 Starting VetScan Pro Blender MCP Pipeline..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check Docker installation
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed or not in PATH${NC}"
    echo "Please install Docker Desktop: https://www.docker.com/products/docker-desktop"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ docker-compose is not installed or not in PATH${NC}"
    echo "Please install docker-compose"
    exit 1
fi

echo -e "${GREEN}✅ Docker and docker-compose found${NC}"

# Create necessary directories
echo -e "${BLUE}📁 Creating project directories...${NC}"
mkdir -p assets/models/animals/bello
mkdir -p blender-projects
mkdir -p scripts/temp
mkdir -p logs

# Check if blender-projects directory has content
if [ ! -f "blender-projects/bello-base.blend" ]; then
    echo -e "${YELLOW}⚠️  No Bello base project found - will be created at runtime${NC}"
fi

# Stop any existing containers
echo -e "${BLUE}🛑 Stopping existing containers...${NC}"
docker-compose down || true

# Build and start containers
echo -e "${BLUE}🏗️  Building Blender MCP container...${NC}"
docker-compose build --no-cache

echo -e "${BLUE}🚀 Starting Blender MCP services...${NC}"
docker-compose up -d

# Wait for services to start
echo -e "${BLUE}⏳ Waiting for services to initialize...${NC}"
sleep 10

# Check health
echo -e "${BLUE}🔍 Checking service health...${NC}"

# Check if container is running
if docker-compose ps | grep -q "vetscan_blender_mcp.*Up"; then
    echo -e "${GREEN}✅ Blender MCP container is running${NC}"
else
    echo -e "${RED}❌ Blender MCP container failed to start${NC}"
    echo "Logs:"
    docker-compose logs blender-mcp
    exit 1
fi

# Test health endpoint
echo -e "${BLUE}🏥 Testing health endpoint...${NC}"
for i in {1..10}; do
    if curl -f http://localhost:8080/health &>/dev/null; then
        echo -e "${GREEN}✅ Health endpoint responding${NC}"
        break
    fi
    if [ $i -eq 10 ]; then
        echo -e "${RED}❌ Health endpoint not responding after 10 attempts${NC}"
        docker-compose logs blender-mcp
        exit 1
    fi
    echo -e "${YELLOW}⏳ Waiting for health endpoint... (attempt $i/10)${NC}"
    sleep 5
done

# Test MCP WebSocket
echo -e "${BLUE}🔌 Testing MCP WebSocket connection...${NC}"
timeout 10 bash -c 'until nc -z localhost 8765; do sleep 1; done' || {
    echo -e "${RED}❌ MCP WebSocket port 8765 not responding${NC}"
    docker-compose logs blender-mcp
    exit 1
}

echo -e "${GREEN}✅ MCP WebSocket port 8765 is open${NC}"

# Create test script to verify Blender MCP functionality
echo -e "${BLUE}🧪 Creating MCP test script...${NC}"
cat > test-docker-mcp.js << 'EOF'
#!/usr/bin/env node
/**
 * Test Docker-based Blender MCP Connection
 */

const WebSocket = require('ws');

async function testBlenderMCP() {
    return new Promise((resolve, reject) => {
        const ws = new WebSocket('ws://localhost:8765');
        
        ws.on('open', function open() {
            console.log('✅ Connected to Blender MCP WebSocket');
            
            // Test get_scene_info
            const request = {
                id: 1,
                method: 'get_scene_info',
                params: {}
            };
            
            ws.send(JSON.stringify(request));
        });
        
        ws.on('message', function message(data) {
            try {
                const response = JSON.parse(data.toString());
                console.log('📊 Scene Info Response:', JSON.stringify(response, null, 2));
                
                if (response.result && response.result.objects) {
                    console.log(`✅ Found ${response.result.objects.length} objects in Blender scene`);
                    
                    if (response.result.objects.includes('Bello')) {
                        console.log('🐕 Bello model detected in scene!');
                    } else {
                        console.log('⚠️  Bello model not found, will be created on first use');
                    }
                    
                    resolve(true);
                } else {
                    console.log('⚠️  Unexpected response format');
                    resolve(false);
                }
            } catch (e) {
                console.error('❌ Error parsing response:', e);
                resolve(false);
            }
            
            ws.close();
        });
        
        ws.on('error', function error(err) {
            console.error('❌ WebSocket error:', err.message);
            reject(err);
        });
        
        ws.on('close', function close() {
            console.log('🔌 WebSocket connection closed');
        });
        
        // Timeout after 10 seconds
        setTimeout(() => {
            if (ws.readyState === WebSocket.OPEN) {
                ws.close();
            }
            reject(new Error('Connection timeout'));
        }, 10000);
    });
}

// Run test
testBlenderMCP()
    .then(success => {
        if (success) {
            console.log('\n🚀 Blender MCP Docker setup is fully operational!');
            console.log('🌐 WebSocket: ws://localhost:8765');
            console.log('🏥 Health: http://localhost:8080/health');
            console.log('📋 Logs: docker-compose logs -f blender-mcp');
            process.exit(0);
        } else {
            console.log('\n⚠️  Blender MCP setup has issues - check logs');
            process.exit(1);
        }
    })
    .catch(error => {
        console.error('\n❌ Blender MCP test failed:', error.message);
        process.exit(1);
    });
EOF

# Run the test (if Node.js is available)
if command -v node &> /dev/null; then
    echo -e "${BLUE}🧪 Running MCP functionality test...${NC}"
    if npm list -g ws &>/dev/null || npm install -g ws; then
        chmod +x test-docker-mcp.js
        node test-docker-mcp.js
    else
        echo -e "${YELLOW}⚠️  Node.js WebSocket library not available - skipping functionality test${NC}"
        echo -e "${GREEN}✅ Basic health checks passed${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  Node.js not available - skipping functionality test${NC}"
    echo -e "${GREEN}✅ Basic health checks passed${NC}"
fi

echo ""
echo -e "${GREEN}🎯 VetScan Pro Blender MCP is now running!${NC}"
echo ""
echo "🔗 Access Points:"
echo "   WebSocket MCP: ws://localhost:8765"
echo "   Health Check:  http://localhost:8080/health"
echo ""
echo "📋 Useful Commands:"
echo "   View logs:     docker-compose logs -f blender-mcp"
echo "   Stop services: docker-compose down"
echo "   Restart:       docker-compose restart"
echo "   Shell access:  docker-compose exec blender-mcp bash"
echo ""
echo "🐕 Next: Test with Claude Code MCP integration!"

# Clean up test file
rm -f test-docker-mcp.js