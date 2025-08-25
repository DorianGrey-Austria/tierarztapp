#!/usr/bin/env python3
"""
🔬 Comprehensive Blender Integration Test Suite
Systematischer Test aller Blender-Claude Code Kommunikationsmethoden

Author: Claude Code (Opus 4.1)
Purpose: Lösung des Blender-Integration Problems für Subagent-System
Date: 2025-08-24
"""

import time
import json
import subprocess
import os
import sys
import socket
import threading
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

class BlenderIntegrationTester:
    def __init__(self):
        self.results = {}
        self.start_time = time.time()
        self.test_count = 0
        self.blender_path = "/Applications/Blender.app/Contents/MacOS/Blender"
        
        # Create test directories
        self.test_dir = Path("tests/blender_integration")
        self.test_dir.mkdir(parents=True, exist_ok=True)
        
        # Results storage
        self.results_file = self.test_dir / f"test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        print("🔬 Blender Integration Test Suite initialized")
        print(f"📁 Test directory: {self.test_dir}")
        print(f"📊 Results will be saved to: {self.results_file}")
        print("=" * 60)

    def log_test(self, test_name: str, method: str, success: bool, 
                 latency: float, error: str = "", details: Dict = None):
        """Systematische Test-Dokumentation"""
        self.test_count += 1
        
        result = {
            'test_id': self.test_count,
            'test_name': test_name,
            'method': method,
            'success': success,
            'latency_ms': round(latency * 1000, 2),
            'timestamp': datetime.now().isoformat(),
            'error': error,
            'details': details or {}
        }
        
        # Store result
        if method not in self.results:
            self.results[method] = []
        self.results[method].append(result)
        
        # Live logging
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"{status} | {test_name} | {latency*1000:.1f}ms | {method}")
        if error:
            print(f"    Error: {error}")

    def check_prerequisites(self) -> Dict[str, bool]:
        """Check system prerequisites"""
        print("\n📋 Checking Prerequisites...")
        
        prereqs = {}
        
        # Check Blender installation
        prereqs['blender_installed'] = os.path.exists(self.blender_path)
        
        # Check running Blender processes
        try:
            result = subprocess.run(['pgrep', '-f', 'Blender'], 
                                  capture_output=True, text=True)
            prereqs['blender_running'] = bool(result.stdout.strip())
        except:
            prereqs['blender_running'] = False
        
        # Check MCP tools
        try:
            subprocess.run(['uvx', '--version'], capture_output=True, timeout=5)
            prereqs['uvx_available'] = True
        except:
            prereqs['uvx_available'] = False
            
        try:
            subprocess.run(['npx', '--version'], capture_output=True, timeout=5)
            prereqs['npx_available'] = True
        except:
            prereqs['npx_available'] = False
        
        # Check Python modules
        try:
            import bpy
            prereqs['bpy_available'] = True
        except ImportError:
            prereqs['bpy_available'] = False
            
        # Report prerequisites
        for name, status in prereqs.items():
            status_icon = "✅" if status else "❌"
            print(f"    {status_icon} {name}: {status}")
        
        return prereqs

    def test_suite_1_direct_mcp(self):
        """TEST SUITE 1: Direkte MCP-Kommunikation"""
        print("\n🔬 Test Suite 1: Direct MCP Communication")
        print("-" * 40)
        
        # Test A: Native MCP Functions
        self.test_native_mcp_functions()
        
        # Test B: Environment-based MCP
        self.test_environment_mcp()
        
        # Test C: JSON-RPC MCP
        self.test_json_rpc_mcp()

    def test_native_mcp_functions(self):
        """Test A: Native MCP Functions (expected to fail)"""
        start_time = time.time()
        
        try:
            # This should fail in Claude Code
            scene = get_scene_info()
            self.log_test("Native get_scene_info()", "Direct MCP", 
                         True, time.time() - start_time, 
                         details={'scene_objects': len(scene.objects) if scene else 0})
        except NameError as e:
            self.log_test("Native get_scene_info()", "Direct MCP", 
                         False, time.time() - start_time, 
                         error=f"NameError: {str(e)}")
        except Exception as e:
            self.log_test("Native get_scene_info()", "Direct MCP", 
                         False, time.time() - start_time, 
                         error=f"Exception: {str(e)}")

    def test_environment_mcp(self):
        """Test B: Environment-based MCP"""
        start_time = time.time()
        
        # Check for MCP-related environment variables
        mcp_vars = {}
        for var in os.environ:
            if 'MCP' in var.upper() or 'BLENDER' in var.upper():
                mcp_vars[var] = os.environ[var]
        
        success = len(mcp_vars) > 0
        self.log_test("Environment MCP Variables", "Environment MCP", 
                     success, time.time() - start_time,
                     details={'found_variables': mcp_vars})

    def test_json_rpc_mcp(self):
        """Test C: JSON-RPC WebSocket MCP"""
        start_time = time.time()
        
        # Try to connect to common MCP ports
        ports_to_try = [8765, 3000, 8080, 9000]
        
        for port in ports_to_try:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(1)
                    result = s.connect_ex(('localhost', port))
                    if result == 0:
                        self.log_test(f"WebSocket Connection Port {port}", "JSON-RPC MCP", 
                                     True, time.time() - start_time,
                                     details={'port': port, 'connection': 'established'})
                        return
            except Exception as e:
                continue
        
        self.log_test("WebSocket Connection (all ports)", "JSON-RPC MCP", 
                     False, time.time() - start_time,
                     error="No open ports found", 
                     details={'tried_ports': ports_to_try})

    def test_suite_2_subprocess(self):
        """TEST SUITE 2: Subprocess Communication"""
        print("\n🔬 Test Suite 2: Subprocess Communication")
        print("-" * 40)
        
        # Test D: Blender CLI with --python
        self.test_blender_cli_python()
        
        # Test E: Background job
        self.test_blender_background_job()
        
        # Test F: Named pipes
        self.test_named_pipes()

    def test_blender_cli_python(self):
        """Test D: Blender CLI with --python (this should work)"""
        start_time = time.time()
        
        # Create simple test script
        test_script = self.test_dir / "test_basic.py"
        with open(test_script, 'w') as f:
            f.write('''
import bpy
print("BLENDER_TEST: Script executed successfully")
print(f"BLENDER_TEST: Scene has {len(bpy.data.objects)} objects")

# Create a simple test object
bpy.ops.mesh.primitive_cube_add(location=(1, 1, 1))
test_obj = bpy.context.object
test_obj.name = "Claude_Test_Cube"

print(f"BLENDER_TEST: Created object {test_obj.name}")
print("BLENDER_TEST: Test completed successfully")
''')
        
        try:
            result = subprocess.run([
                self.blender_path, '--background', '--factory-startup',
                '--python', str(test_script)
            ], capture_output=True, text=True, timeout=30)
            
            success = result.returncode == 0 and "Test completed successfully" in result.stdout
            
            # Extract details from output
            objects_count = 0
            if "Scene has" in result.stdout:
                try:
                    line = [l for l in result.stdout.split('\n') if 'Scene has' in l][0]
                    objects_count = int(line.split()[3])
                except:
                    pass
            
            self.log_test("Blender CLI --python", "Subprocess CLI", 
                         success, time.time() - start_time,
                         error=result.stderr if not success else "",
                         details={
                             'return_code': result.returncode,
                             'objects_detected': objects_count,
                             'stdout_length': len(result.stdout)
                         })
        except subprocess.TimeoutExpired:
            self.log_test("Blender CLI --python", "Subprocess CLI", 
                         False, time.time() - start_time,
                         error="Timeout after 30 seconds")
        except Exception as e:
            self.log_test("Blender CLI --python", "Subprocess CLI", 
                         False, time.time() - start_time,
                         error=str(e))

    def test_blender_background_job(self):
        """Test E: Persistent Blender background job"""
        start_time = time.time()
        
        try:
            # Start Blender in background mode that stays open
            # This is tricky - we need to keep it alive somehow
            
            # For now, test if we can determine if Blender is already running
            result = subprocess.run(['pgrep', '-f', 'Blender'], 
                                  capture_output=True, text=True, timeout=5)
            
            blender_pids = result.stdout.strip().split('\n') if result.stdout.strip() else []
            success = len(blender_pids) > 0
            
            self.log_test("Persistent Blender Background", "Background Job", 
                         success, time.time() - start_time,
                         details={
                             'running_processes': len(blender_pids),
                             'pids': blender_pids
                         })
        except Exception as e:
            self.log_test("Persistent Blender Background", "Background Job", 
                         False, time.time() - start_time,
                         error=str(e))

    def test_named_pipes(self):
        """Test F: Named Pipes/FIFO communication"""
        start_time = time.time()
        
        try:
            # Create a named pipe for testing
            pipe_path = self.test_dir / "blender_command_pipe"
            
            # Remove if exists
            if pipe_path.exists():
                pipe_path.unlink()
            
            # Create named pipe (Unix/macOS)
            os.mkfifo(str(pipe_path))
            
            success = pipe_path.exists()
            
            self.log_test("Named Pipe Creation", "Named Pipes", 
                         success, time.time() - start_time,
                         details={'pipe_path': str(pipe_path)})
            
            # Clean up
            if pipe_path.exists():
                pipe_path.unlink()
                
        except Exception as e:
            self.log_test("Named Pipe Creation", "Named Pipes", 
                         False, time.time() - start_time,
                         error=str(e))

    def test_suite_3_file_based(self):
        """TEST SUITE 3: File-based Communication"""
        print("\n🔬 Test Suite 3: File-based Communication")
        print("-" * 40)
        
        # Test G: Watch folder system
        self.test_watch_folder()
        
        # Test H: Blend file manipulation
        self.test_blend_file_access()

    def test_watch_folder(self):
        """Test G: Watch-Folder System"""
        start_time = time.time()
        
        try:
            # Create command and response folders
            cmd_folder = self.test_dir / "commands"
            resp_folder = self.test_dir / "responses"
            cmd_folder.mkdir(exist_ok=True)
            resp_folder.mkdir(exist_ok=True)
            
            # Create test command file
            cmd_file = cmd_folder / "test_command.json"
            with open(cmd_file, 'w') as f:
                json.dump({
                    'command': 'create_cube',
                    'params': {'location': [0, 0, 0]},
                    'timestamp': datetime.now().isoformat()
                }, f)
            
            success = cmd_file.exists()
            
            self.log_test("Watch Folder Setup", "File Watch", 
                         success, time.time() - start_time,
                         details={
                             'command_folder': str(cmd_folder),
                             'response_folder': str(resp_folder)
                         })
        except Exception as e:
            self.log_test("Watch Folder Setup", "File Watch", 
                         False, time.time() - start_time,
                         error=str(e))

    def test_blend_file_access(self):
        """Test H: Direct .blend file access"""
        start_time = time.time()
        
        try:
            # Test if we can create a minimal .blend file
            test_blend = self.test_dir / "test.blend"
            
            # Create simple Blender script that saves a file
            save_script = self.test_dir / "save_test.py"
            with open(save_script, 'w') as f:
                f.write(f'''
import bpy
bpy.ops.wm.save_as_mainfile(filepath="{test_blend}")
print("BLEND_TEST: File saved successfully")
''')
            
            result = subprocess.run([
                self.blender_path, '--background', '--factory-startup',
                '--python', str(save_script)
            ], capture_output=True, text=True, timeout=15)
            
            success = test_blend.exists() and result.returncode == 0
            file_size = test_blend.stat().st_size if success else 0
            
            self.log_test("Blend File Creation", "Blend File", 
                         success, time.time() - start_time,
                         details={
                             'file_path': str(test_blend),
                             'file_size_bytes': file_size
                         })
        except Exception as e:
            self.log_test("Blend File Creation", "Blend File", 
                         False, time.time() - start_time,
                         error=str(e))

    def test_suite_4_applescript(self):
        """TEST SUITE 4: AppleScript/System Integration"""
        print("\n🔬 Test Suite 4: AppleScript/System Integration")
        print("-" * 40)
        
        # Test J: AppleScript control
        self.test_applescript_control()
        
        # Test K: System events
        self.test_system_events()

    def test_applescript_control(self):
        """Test J: AppleScript Blender Control"""
        start_time = time.time()
        
        try:
            # Test basic AppleScript functionality
            applescript = '''
tell application "System Events"
    set processList to name of every process
    set blenderRunning to "Blender" is in processList
end tell

return blenderRunning
'''
            
            result = subprocess.run(['osascript', '-e', applescript], 
                                  capture_output=True, text=True, timeout=10)
            
            success = result.returncode == 0
            blender_running = result.stdout.strip() == 'true' if success else False
            
            self.log_test("AppleScript Process Check", "AppleScript", 
                         success, time.time() - start_time,
                         details={
                             'blender_detected': blender_running,
                             'output': result.stdout.strip()
                         })
        except Exception as e:
            self.log_test("AppleScript Process Check", "AppleScript", 
                         False, time.time() - start_time,
                         error=str(e))

    def test_system_events(self):
        """Test K: System Events"""
        start_time = time.time()
        
        try:
            # Check if we can detect system capabilities
            system_info = {
                'platform': sys.platform,
                'python_version': sys.version,
                'current_user': os.getenv('USER', 'unknown')
            }
            
            success = sys.platform == 'darwin'  # macOS required for AppleScript
            
            self.log_test("System Events Capability", "System Events", 
                         success, time.time() - start_time,
                         details=system_info)
        except Exception as e:
            self.log_test("System Events Capability", "System Events", 
                         False, time.time() - start_time,
                         error=str(e))

    def run_all_tests(self):
        """Execute complete test suite"""
        print("🚀 Starting Complete Blender Integration Test Suite")
        print("=" * 60)
        
        # Check prerequisites
        prereqs = self.check_prerequisites()
        
        # Run all test suites
        self.test_suite_1_direct_mcp()
        self.test_suite_2_subprocess()
        self.test_suite_3_file_based()
        self.test_suite_4_applescript()
        
        # Generate final report
        self.generate_report(prereqs)

    def generate_report(self, prereqs: Dict[str, bool]):
        """Generate comprehensive test report"""
        print("\n📊 Generating Test Report...")
        
        total_time = time.time() - self.start_time
        
        # Save raw results
        report_data = {
            'test_session': {
                'start_time': datetime.fromtimestamp(self.start_time).isoformat(),
                'total_duration_seconds': round(total_time, 2),
                'total_tests': self.test_count,
                'claude_version': 'Opus 4.1',
                'system': sys.platform
            },
            'prerequisites': prereqs,
            'test_results': self.results
        }
        
        with open(self.results_file, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        # Generate summary
        successful_methods = []
        failed_methods = []
        
        for method, tests in self.results.items():
            success_rate = sum(1 for t in tests if t['success']) / len(tests)
            avg_latency = sum(t['latency_ms'] for t in tests) / len(tests)
            
            if success_rate > 0.5:  # More than 50% success
                successful_methods.append((method, success_rate, avg_latency))
            else:
                failed_methods.append((method, success_rate, avg_latency))
        
        # Print summary
        print("\n🎯 TEST RESULTS SUMMARY")
        print("=" * 60)
        print(f"⏱️  Total Test Time: {total_time:.2f}s")
        print(f"🧪 Total Tests: {self.test_count}")
        print(f"📊 Results saved to: {self.results_file}")
        
        if successful_methods:
            print("\n✅ WORKING METHODS:")
            for method, success_rate, latency in successful_methods:
                print(f"    {method}: {success_rate*100:.0f}% success, {latency:.1f}ms avg")
        
        if failed_methods:
            print("\n❌ FAILED METHODS:")
            for method, success_rate, latency in failed_methods:
                print(f"    {method}: {success_rate*100:.0f}% success")
        
        # Recommendations
        print("\n💡 RECOMMENDATIONS:")
        if successful_methods:
            best_method = max(successful_methods, key=lambda x: x[1])
            print(f"    🥇 Best Method: {best_method[0]} ({best_method[1]*100:.0f}% success)")
            print(f"    📈 Use for Subagent System: {best_method[0]}")
        else:
            print("    ⚠️  No fully working methods found")
            print("    🔧 Manual intervention required")
        
        return report_data

# Main execution
if __name__ == "__main__":
    tester = BlenderIntegrationTester()
    results = tester.run_all_tests()
    
    print("\n🎉 Blender Integration Test Suite Complete!")
    print("📋 Use results for Troubleshooting documentation")
    print("🚀 Ready for Subagent implementation planning")