#!/usr/bin/env python3
"""
Download pre-built vulnerable APKs for testing VulnDroid
"""

import os
import sys

def print_instructions():
    print("=" * 60)
    print("  Vulnerable APK Download Guide for VulnDroid Testing")
    print("=" * 60)
    print()
    print("Since building an APK requires Android SDK, here are easier options:")
    print()
    
    print("Option 1: DIVA (Damn Insecure and Vulnerable App)")
    print("-" * 60)
    print("URL: https://github.com/payatu/diva-android/raw/master/diva-beta.apk")
    print("Command:")
    print("  wget https://github.com/payatu/diva-android/raw/master/diva-beta.apk")
    print()
    
    print("Option 2: InsecureBankv2")
    print("-" * 60)
    print("URL: https://github.com/dineshshetty/Android-InsecureBankv2")
    print("Steps:")
    print("  1. git clone https://github.com/dineshshetty/Android-InsecureBankv2.git")
    print("  2. Download APK from releases page")
    print()
    
    print("Option 3: AndroGoat (OWASP)")
    print("-" * 60)
    print("URL: https://github.com/satishpatnayak/AndroGoat")
    print("Command:")
    print("  git clone https://github.com/satishpatnayak/AndroGoat.git")
    print()
    
    print("Option 4: InjuredAndroid")
    print("-" * 60)
    print("URL: https://github.com/B3nac/InjuredAndroid")
    print("Command:")
    print("  wget https://github.com/B3nac/InjuredAndroid/releases/download/v1.0.12/InjuredAndroid-1.0.12-release.apk")
    print()
    
    print("=" * 60)
    print("Quick Test:")
    print("=" * 60)
    print("  python cli.py downloaded-app.apk")
    print()

def download_diva():
    """Attempt to download DIVA APK"""
    try:
        import urllib.request
        
        url = "https://github.com/payatu/diva-android/raw/master/diva-beta.apk"
        output_file = "diva-beta.apk"
        
        print(f"Downloading DIVA APK from {url}...")
        urllib.request.urlretrieve(url, output_file)
        
        if os.path.exists(output_file):
            print(f"✓ Successfully downloaded: {output_file}")
            print(f"  File size: {os.path.getsize(output_file)} bytes")
            print()
            print("Test with VulnDroid:")
            print(f"  python cli.py {output_file}")
            return True
        else:
            print("✗ Download failed")
            return False
    except Exception as e:
        print(f"✗ Error downloading: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--download":
        print("Attempting to download DIVA APK...")
        print()
        if not download_diva():
            print()
            print("Manual download required. See instructions below:")
            print()
            print_instructions()
    else:
        print_instructions()
        print()
        print("To auto-download DIVA APK, run:")
        print("  python download_test_apk.py --download")
        print()
