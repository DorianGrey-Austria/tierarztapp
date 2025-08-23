#!/usr/bin/env python3
"""
Browser Console Error Checker
Tests HTML files for JavaScript errors in the browser console
"""

import time
import sys

def test_manual():
    """Manual testing instructions since Selenium/Playwright may not be installed"""
    
    print("=" * 60)
    print("BROWSER CONSOLE ERROR CHECK")
    print("=" * 60)
    print()
    
    urls = [
        "http://localhost:8080/vetscan-ultimate.html",
        "http://localhost:8080/vetscan-story-mode.html",
        "http://localhost:8080/standalone.html"
    ]
    
    print("🔍 MANUAL TEST CHECKLIST:")
    print("-" * 40)
    
    for i, url in enumerate(urls, 1):
        print(f"\n{i}. Test {url}")
        print("   [ ] Page loads without errors")
        print("   [ ] No red errors in console")
        print("   [ ] 3D visualization works (if applicable)")
        print("   [ ] Buttons are clickable")
        print("   [ ] Forms can be submitted")
        print("   [ ] Animations play smoothly")
    
    print("\n" + "=" * 60)
    print("HOW TO TEST:")
    print("-" * 40)
    print("1. Open Chrome or Firefox")
    print("2. Open Developer Tools (F12)")
    print("3. Click on 'Console' tab")
    print("4. Visit each URL above")
    print("5. Look for any red error messages")
    print("6. Test interactive elements")
    print()
    print("COMMON ERRORS TO LOOK FOR:")
    print("- 'Uncaught ReferenceError' - undefined variable")
    print("- 'TypeError' - wrong data type")
    print("- '404' - missing resource")
    print("- 'CORS' - cross-origin issues")
    print("=" * 60)

    # Quick static analysis
    print("\n📊 STATIC CODE ANALYSIS:")
    print("-" * 40)
    
    import os
    files_to_check = [
        "vetscan-ultimate.html",
        "vetscan-story-mode.html"
    ]
    
    for filename in files_to_check:
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
                
            print(f"\n✅ {filename}:")
            
            # Check for common issues
            issues = []
            
            # Check Three.js usage
            if 'three.min.js' in content:
                if 'new THREE.' in content:
                    print("   ✓ Three.js properly referenced")
                else:
                    issues.append("Three.js loaded but might not be used correctly")
            
            # Check for console.log (debugging left in)
            log_count = content.count('console.log')
            if log_count > 5:
                issues.append(f"Many console.log statements ({log_count}) - consider removing for production")
            
            # Check for proper event listeners
            if 'onclick=' in content:
                onclick_count = content.count('onclick=')
                print(f"   ✓ {onclick_count} onclick handlers found")
            
            # Check for localStorage usage
            if 'localStorage' in content:
                print("   ✓ Uses localStorage for game state")
            
            # Check for proper error handling
            if 'try' in content and 'catch' in content:
                print("   ✓ Has error handling")
            else:
                issues.append("No try-catch blocks found - consider adding error handling")
            
            if issues:
                print("   ⚠️  Potential issues:")
                for issue in issues:
                    print(f"      - {issue}")
            else:
                print("   ✓ No obvious issues found")
        else:
            print(f"\n❌ {filename} not found")
    
    print("\n" + "=" * 60)
    print("✨ Test preparation complete!")
    print("Please manually test the URLs in your browser.")
    print("=" * 60)

if __name__ == "__main__":
    test_manual()