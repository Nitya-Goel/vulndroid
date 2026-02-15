#!/usr/bin/env python3
"""
Test script to verify VulnDroid setup and androguard installation
"""

import sys
import os

def test_imports():
    """Test if all required libraries are installed"""
    print("=" * 60)
    print("Testing Python Dependencies")
    print("=" * 60)
    
    required = [
        ('flask', 'Flask'),
        ('androguard', 'Androguard'),
    ]
    
    all_ok = True
    for module_name, display_name in required:
        try:
            __import__(module_name)
            print(f"✓ {display_name} is installed")
        except ImportError:
            print(f"✗ {display_name} is NOT installed")
            print(f"  Install with: pip install {module_name}")
            all_ok = False
    
    print()
    return all_ok

def test_androguard():
    """Test androguard functionality"""
    print("=" * 60)
    print("Testing Androguard Functionality")
    print("=" * 60)
    
    try:
        from androguard.misc import AnalyzeAPK
        print("✓ Androguard AnalyzeAPK imported successfully")
        print()
        return True
    except Exception as e:
        print(f"✗ Androguard import failed: {e}")
        print()
        return False

def test_apk_file(apk_path):
    """Test loading an actual APK file"""
    print("=" * 60)
    print(f"Testing APK File: {apk_path}")
    print("=" * 60)
    
    if not os.path.exists(apk_path):
        print(f"✗ APK file not found: {apk_path}")
        return False
    
    print(f"✓ APK file exists")
    print(f"  Size: {os.path.getsize(apk_path)} bytes")
    
    try:
        from androguard.misc import AnalyzeAPK
        
        print("  Loading APK...")
        apk, dex, analysis = AnalyzeAPK(apk_path)
        
        print("✓ APK loaded successfully!")
        print()
        print("APK Information:")
        print(f"  Package: {apk.get_package()}")
        print(f"  Version: {apk.get_androidversion_name()}")
        print(f"  Min SDK: {apk.get_min_sdk_version()}")
        print(f"  Target SDK: {apk.get_target_sdk_version()}")
        print(f"  Permissions: {len(apk.get_permissions())}")
        print(f"  Activities: {len(apk.get_activities())}")
        print(f"  Services: {len(apk.get_services())}")
        print(f"  Receivers: {len(apk.get_receivers())}")
        print()
        return True
        
    except Exception as e:
        print(f"✗ Failed to load APK: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_vulndroid_structure():
    """Test if VulnDroid project structure is correct"""
    print("=" * 60)
    print("Testing VulnDroid Project Structure")
    print("=" * 60)
    
    required_files = [
        'app.py',
        'templates/upload.html',
        'templates/result.html',
        'core/apk_loader.py',
        'core/manifest_analyzer.py',
        'core/code_analyzer.py',
    ]
    
    all_ok = True
    for filepath in required_files:
        if os.path.exists(filepath):
            print(f"✓ {filepath}")
        else:
            print(f"✗ {filepath} - MISSING")
            all_ok = False
    
    print()
    return all_ok

if __name__ == "__main__":
    print()
    print("🔍 VulnDroid Setup Verification")
    print()
    
    # Test imports
    imports_ok = test_imports()
    
    # Test androguard
    androguard_ok = test_androguard()
    
    # Test project structure
    structure_ok = test_vulndroid_structure()
    
    # Test APK if provided
    if len(sys.argv) > 1:
        apk_path = sys.argv[1]
        apk_ok = test_apk_file(apk_path)
    else:
        print("=" * 60)
        print("APK File Test")
        print("=" * 60)
        print("No APK file provided for testing")
        print("Usage: python test_setup.py path/to/test.apk")
        print()
        apk_ok = True  # Don't fail if no APK provided
    
    # Summary
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    if imports_ok and androguard_ok and structure_ok and apk_ok:
        print("✓ All tests passed! VulnDroid is ready to use.")
        print()
        print("Start the server with:")
        print("  python app.py")
        print()
        sys.exit(0)
    else:
        print("✗ Some tests failed. Please fix the issues above.")
        print()
        if not imports_ok:
            print("Install dependencies with:")
            print("  pip install flask androguard")
        print()
        sys.exit(1)