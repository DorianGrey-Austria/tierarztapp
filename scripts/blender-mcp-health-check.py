#!/usr/bin/env python3
"""
Blender MCP Health Check Script
Testet die Verbindung zwischen Cursor/Claude Code und Blender
"""

import socket
import json
import time
import subprocess
import os
from datetime import datetime

class BlenderMCPHealthCheck:
    def __init__(self):
        self.port = 9876
        self.host = 'localhost'
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'checks': {}
        }
    
    def check_blender_process(self):
        """Prüft ob Blender läuft"""
        try:
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            blender_running = 'Blender.app' in result.stdout
            
            if blender_running:
                # PID extrahieren
                for line in result.stdout.split('\n'):
                    if 'Blender.app' in line and 'grep' not in line:
                        pid = line.split()[1]
                        self.results['checks']['blender_process'] = {
                            'status': 'running',
                            'pid': pid,
                            'message': f'Blender läuft (PID: {pid})'
                        }
                        return True
            
            self.results['checks']['blender_process'] = {
                'status': 'not_running',
                'message': 'Blender ist nicht gestartet'
            }
            return False
            
        except Exception as e:
            self.results['checks']['blender_process'] = {
                'status': 'error',
                'message': str(e)
            }
            return False
    
    def check_mcp_port(self):
        """Prüft ob Port 9876 offen ist"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((self.host, self.port))
            sock.close()
            
            if result == 0:
                self.results['checks']['mcp_port'] = {
                    'status': 'open',
                    'port': self.port,
                    'message': f'Port {self.port} ist offen'
                }
                return True
            else:
                self.results['checks']['mcp_port'] = {
                    'status': 'closed',
                    'port': self.port,
                    'message': f'Port {self.port} ist geschlossen'
                }
                return False
                
        except Exception as e:
            self.results['checks']['mcp_port'] = {
                'status': 'error',
                'message': str(e)
            }
            return False
    
    def check_uvx_installation(self):
        """Prüft ob uvx installiert ist"""
        try:
            result = subprocess.run(['which', 'uvx'], capture_output=True, text=True)
            if result.returncode == 0:
                uvx_path = result.stdout.strip()
                
                # Version prüfen
                version_result = subprocess.run(['uvx', '--version'], capture_output=True, text=True)
                version = version_result.stdout.strip() if version_result.returncode == 0 else 'unknown'
                
                self.results['checks']['uvx_installation'] = {
                    'status': 'installed',
                    'path': uvx_path,
                    'version': version,
                    'message': f'uvx ist installiert: {uvx_path}'
                }
                return True
            else:
                self.results['checks']['uvx_installation'] = {
                    'status': 'not_installed',
                    'message': 'uvx ist nicht installiert'
                }
                return False
                
        except Exception as e:
            self.results['checks']['uvx_installation'] = {
                'status': 'error',
                'message': str(e)
            }
            return False
    
    def check_blender_mcp_processes(self):
        """Prüft ob blender-mcp Prozesse laufen"""
        try:
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            processes = [line for line in result.stdout.split('\n') if 'blender-mcp' in line and 'grep' not in line]
            
            if processes:
                self.results['checks']['blender_mcp_processes'] = {
                    'status': 'running',
                    'count': len(processes),
                    'message': f'{len(processes)} blender-mcp Prozesse gefunden'
                }
                return True
            else:
                self.results['checks']['blender_mcp_processes'] = {
                    'status': 'not_running',
                    'message': 'Keine blender-mcp Prozesse gefunden'
                }
                return False
                
        except Exception as e:
            self.results['checks']['blender_mcp_processes'] = {
                'status': 'error',
                'message': str(e)
            }
            return False
    
    def check_cursor_config(self):
        """Prüft ob .cursor/mcp.json existiert und korrekt ist"""
        config_path = '.cursor/mcp.json'
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = json.load(f)
                
                # Prüfe ob blender-mcp konfiguriert ist
                if 'mcpServers' in config and 'blender-mcp' in config['mcpServers']:
                    blender_config = config['mcpServers']['blender-mcp']
                    
                    # Prüfe ob uvx verwendet wird (kritisch!)
                    if blender_config.get('command') == 'uvx':
                        self.results['checks']['cursor_config'] = {
                            'status': 'correct',
                            'command': 'uvx',
                            'message': '✅ Cursor Config korrekt (uvx wird verwendet)'
                        }
                        return True
                    else:
                        self.results['checks']['cursor_config'] = {
                            'status': 'incorrect',
                            'command': blender_config.get('command', 'unknown'),
                            'message': f'❌ Falscher command: {blender_config.get("command")} (sollte uvx sein)'
                        }
                        return False
                else:
                    self.results['checks']['cursor_config'] = {
                        'status': 'incomplete',
                        'message': 'blender-mcp nicht in Config gefunden'
                    }
                    return False
            else:
                self.results['checks']['cursor_config'] = {
                    'status': 'missing',
                    'message': f'{config_path} existiert nicht'
                }
                return False
                
        except Exception as e:
            self.results['checks']['cursor_config'] = {
                'status': 'error',
                'message': str(e)
            }
            return False
    
    def send_test_command(self):
        """Sendet ein Test-Command an Blender MCP"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((self.host, self.port))
            
            # Test-Command senden
            test_command = {
                "method": "get_scene_info",
                "params": {}
            }
            
            message = json.dumps(test_command) + '\n'
            sock.send(message.encode())
            
            # Auf Antwort warten
            response = sock.recv(4096).decode()
            sock.close()
            
            if response:
                self.results['checks']['test_command'] = {
                    'status': 'success',
                    'response_length': len(response),
                    'message': 'Test-Command erfolgreich gesendet und Antwort erhalten'
                }
                return True
            else:
                self.results['checks']['test_command'] = {
                    'status': 'no_response',
                    'message': 'Keine Antwort vom Server erhalten'
                }
                return False
                
        except Exception as e:
            self.results['checks']['test_command'] = {
                'status': 'failed',
                'message': str(e)
            }
            return False
    
    def run_all_checks(self):
        """Führt alle Health Checks aus"""
        print("🔍 Blender MCP Health Check wird ausgeführt...\n")
        
        checks = [
            ("Blender Prozess", self.check_blender_process),
            ("uvx Installation", self.check_uvx_installation),
            ("Cursor Config", self.check_cursor_config),
            ("MCP Port 9876", self.check_mcp_port),
            ("Blender-MCP Prozesse", self.check_blender_mcp_processes),
            ("Test Command", self.send_test_command)
        ]
        
        total_checks = len(checks)
        passed_checks = 0
        
        for name, check_func in checks:
            print(f"Prüfe {name}...", end=" ")
            if check_func():
                print("✅")
                passed_checks += 1
            else:
                print("❌")
        
        # Zusammenfassung
        print("\n" + "="*50)
        print(f"ERGEBNIS: {passed_checks}/{total_checks} Checks bestanden")
        print("="*50 + "\n")
        
        # Details ausgeben
        for check_name, check_data in self.results['checks'].items():
            status_icon = "✅" if check_data['status'] in ['running', 'open', 'installed', 'correct', 'success'] else "❌"
            print(f"{status_icon} {check_name}: {check_data['message']}")
        
        # Empfehlungen
        print("\n📋 EMPFEHLUNGEN:")
        if self.results['checks'].get('blender_process', {}).get('status') != 'running':
            print("- Starte Blender: /Applications/Blender.app")
        
        if self.results['checks'].get('mcp_port', {}).get('status') != 'open':
            print("- Aktiviere Blender MCP Addon in Blender (N-Key → BlenderMCP → Start Server)")
        
        if self.results['checks'].get('cursor_config', {}).get('command') != 'uvx':
            print("- ⚠️ KRITISCH: Ändere command in .cursor/mcp.json von npx zu uvx!")
        
        if self.results['checks'].get('blender_mcp_processes', {}).get('status') != 'running':
            print("- Starte blender-mcp: uvx blender-mcp")
        
        # JSON Export
        output_file = f'blender_mcp_health_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(output_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"\n💾 Detaillierte Ergebnisse gespeichert in: {output_file}")
        
        return passed_checks == total_checks

if __name__ == "__main__":
    health_check = BlenderMCPHealthCheck()
    success = health_check.run_all_checks()
    
    if success:
        print("\n🎉 Alle Checks bestanden! Blender MCP ist bereit!")
    else:
        print("\n⚠️ Einige Checks sind fehlgeschlagen. Bitte Empfehlungen beachten.")
    
    exit(0 if success else 1)