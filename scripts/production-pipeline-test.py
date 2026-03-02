#!/usr/bin/env python3
"""
VetScan Pro v8.0.0 - Production Pipeline Test
=============================================
Complete integration test for Blender MCP → Web Pipeline

Tests:
1. Blender MCP connectivity (6/6 health checks)
2. Model generation and export
3. Web deployment verification
4. Loading pipeline robustness
5. Fallback system validation

Run: python3 scripts/production-pipeline-test.py
"""

import json
import subprocess
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime

class ProductionPipelineTest:
    def __init__(self):
        self.base_url = "https://vibecoding.company"
        self.local_url = "http://localhost:8081"
        self.test_results = []
        print("🚀 VetScan Pro v8.0.0 - Production Pipeline Test")
        print("=" * 60)

    def log_test(self, name, status, details=""):
        result = {
            "test": name,
            "status": status,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        status_icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{status_icon} {name}: {status}")
        if details:
            print(f"   {details}")

    def test_blender_mcp_health(self):
        """Test 1: Blender MCP Health Check"""
        try:
            result = subprocess.run([
                'python3', 'scripts/blender-mcp-health-check.py'
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0 and "6/6 Checks bestanden" in result.stdout:
                self.log_test("Blender MCP Health", "PASS", "All 6 checks passed")
                return True
            else:
                self.log_test("Blender MCP Health", "FAIL", f"Health check failed: {result.stderr}")
                return False
        except Exception as e:
            self.log_test("Blender MCP Health", "FAIL", f"Error: {e}")
            return False

    def test_model_generation(self):
        """Test 2: Fresh Model Generation"""
        try:
            result = subprocess.run([
                'python3', 'scripts/transform-dog-creative.py'
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0 and "TRANSFORMATION ABGESCHLOSSEN" in result.stdout:
                # Check if fresh model file exists
                import os
                model_path = "assets/models/animals/dog/dog_from_blender.glb"
                if os.path.exists(model_path):
                    size_kb = os.path.getsize(model_path) // 1024
                    self.log_test("Model Generation", "PASS", f"Fresh model: {size_kb}KB")
                    return True
                else:
                    self.log_test("Model Generation", "FAIL", "Model file not created")
                    return False
            else:
                self.log_test("Model Generation", "FAIL", f"Generation failed: {result.stderr}")
                return False
        except Exception as e:
            self.log_test("Model Generation", "FAIL", f"Error: {e}")
            return False

    def test_production_deployment(self):
        """Test 3: Production Deployment"""
        try:
            url = f"{self.base_url}/vetscan-bello-3d-v7.html"
            with urllib.request.urlopen(url, timeout=10) as response:
                if response.status == 200:
                    content = response.read().decode('utf-8')
                    
                    # Check for v8.0.0 markers
                    if "Version 8.0.0" in content and "Production Pipeline" in content:
                        self.log_test("Production Deployment", "PASS", f"v8.0.0 deployed, {len(content)} chars")
                        return True
                    else:
                        self.log_test("Production Deployment", "WARN", "Old version detected")
                        return False
                else:
                    self.log_test("Production Deployment", "FAIL", f"HTTP {response.status}")
                    return False
        except Exception as e:
            self.log_test("Production Deployment", "FAIL", f"Error: {e}")
            return False

    def test_model_assets(self):
        """Test 4: Model Assets Availability"""
        test_urls = [
            f"{self.base_url}/assets/models/animals/dog/dog_from_blender.glb",
            f"{self.base_url}/assets/models/animals/dog/dog_high.glb",
            f"{self.base_url}/assets/models/animals/bello/bello_high.glb"
        ]
        
        available_models = 0
        total_size = 0
        
        for url in test_urls:
            try:
                req = urllib.request.Request(url, method='HEAD')
                with urllib.request.urlopen(req, timeout=5) as response:
                    if response.status == 200:
                        available_models += 1
                        content_length = response.headers.get('content-length')
                        if content_length:
                            total_size += int(content_length)
            except:
                pass
        
        if available_models > 0:
            size_mb = total_size / (1024 * 1024)
            self.log_test("Model Assets", "PASS", f"{available_models}/3 models available, {size_mb:.1f}MB total")
            return True
        else:
            self.log_test("Model Assets", "FAIL", "No models accessible")
            return False

    def test_three_js_libraries(self):
        """Test 5: Three.js Libraries"""
        try:
            # Test external CDN dependencies
            libs = [
                "https://unpkg.com/three@0.128.0/build/three.min.js",
                "https://unpkg.com/three@0.128.0/examples/js/controls/OrbitControls.js",
                "https://unpkg.com/three@0.128.0/examples/js/loaders/GLTFLoader.js",
                "https://unpkg.com/three@0.128.0/examples/js/loaders/DRACOLoader.js"
            ]
            
            available_libs = 0
            for lib_url in libs:
                try:
                    req = urllib.request.Request(lib_url, method='HEAD')
                    with urllib.request.urlopen(req, timeout=5) as response:
                        if response.status == 200:
                            available_libs += 1
                except:
                    pass
            
            if available_libs == len(libs):
                self.log_test("Three.js Libraries", "PASS", "All CDN libraries accessible")
                return True
            else:
                self.log_test("Three.js Libraries", "WARN", f"{available_libs}/{len(libs)} libraries available")
                return available_libs > 2
        except Exception as e:
            self.log_test("Three.js Libraries", "FAIL", f"Error: {e}")
            return False

    def test_fallback_system(self):
        """Test 6: Fallback System Logic"""
        try:
            # Read the HTML file to check fallback implementation
            with open("vetscan-bello-3d-v7.html", "r") as f:
                content = f.read()
            
            fallback_indicators = [
                "createProceduralDog",
                "FALLBACK:",
                "All model URLs exhausted",
                "procedural fallback"
            ]
            
            found_indicators = sum(1 for indicator in fallback_indicators if indicator in content)
            
            if found_indicators >= 3:
                self.log_test("Fallback System", "PASS", "Robust fallback implementation detected")
                return True
            else:
                self.log_test("Fallback System", "WARN", "Limited fallback implementation")
                return False
        except Exception as e:
            self.log_test("Fallback System", "FAIL", f"Error: {e}")
            return False

    def generate_report(self):
        """Generate final test report"""
        print("\n" + "=" * 60)
        print("📊 PRODUCTION PIPELINE TEST REPORT")
        print("=" * 60)
        
        passed = sum(1 for result in self.test_results if result["status"] == "PASS")
        total = len(self.test_results)
        success_rate = (passed / total) * 100 if total > 0 else 0
        
        print(f"Tests Passed: {passed}/{total} ({success_rate:.1f}%)")
        print(f"Timestamp: {datetime.now().isoformat()}")
        
        if success_rate >= 80:
            print("🎉 PRODUCTION READY - Pipeline functioning well!")
        elif success_rate >= 60:
            print("⚠️  MOSTLY READY - Minor issues detected")
        else:
            print("❌ NOT READY - Major issues require attention")
        
        # Save detailed report
        report_file = f"production_pipeline_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, "w") as f:
            json.dump({
                "summary": {
                    "passed": passed,
                    "total": total,
                    "success_rate": success_rate,
                    "status": "READY" if success_rate >= 80 else "NOT_READY"
                },
                "tests": self.test_results
            }, f, indent=2)
        
        print(f"📝 Detailed report saved: {report_file}")
        return success_rate >= 80

    def run_all_tests(self):
        """Run complete test suite"""
        print("Starting comprehensive pipeline test...\n")
        
        tests = [
            self.test_blender_mcp_health,
            self.test_model_generation,
            self.test_production_deployment,
            self.test_model_assets,
            self.test_three_js_libraries,
            self.test_fallback_system
        ]
        
        for test in tests:
            test()
            time.sleep(0.5)  # Brief pause between tests
        
        return self.generate_report()

if __name__ == "__main__":
    tester = ProductionPipelineTest()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)