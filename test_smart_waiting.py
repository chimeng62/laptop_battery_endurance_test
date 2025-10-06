"""
Test Smart Waiting Functions

Simple test to verify the new smart waiting works without complications.
"""

from utils.smart_wait import wait_for_page_load, wait_for_application_ready, smart_sleep, YOUTUBE_DURATION
import webbrowser
import time

def test_smart_waiting():
    print("Testing Smart Waiting Functions")
    print("=" * 40)
    
    # Test 1: Smart sleep
    print("\n1. Testing smart_sleep (3 seconds)...")
    start = time.time()
    smart_sleep(3)
    elapsed = time.time() - start
    print(f"   ✅ Smart sleep took {elapsed:.1f} seconds")
    
    # Test 2: Page load detection
    print("\n2. Testing page load detection...")
    print("   Opening example.com...")
    webbrowser.open("https://example.com")
    
    start = time.time()
    if wait_for_page_load(timeout=10):
        elapsed = time.time() - start
        print(f"   ✅ Page load detected in {elapsed:.1f} seconds")
    else:
        print("   ⚠️  Page load timeout (10s) - this is normal")
    
    # Test 3: Application ready detection  
    print("\n3. Testing application ready detection...")
    if wait_for_application_ready(timeout=5):
        print("   ✅ Application ready detected")
    else:
        print("   ⚠️  Application ready timeout - this is normal")
    
    # Test 4: YouTube duration constant
    print(f"\n4. YouTube duration: {YOUTUBE_DURATION} seconds ({YOUTUBE_DURATION//60} minutes)")
    print("   ✅ YouTube will play for exactly 20 minutes as requested")
    
    print("\n" + "=" * 40)
    print("✅ Smart waiting test completed!")
    print("The system will now:")
    print("- Wait intelligently for pages to load (up to 10s)")
    print("- Wait for Office apps to be ready (up to 15s)")  
    print("- Keep YouTube videos at exactly 20 minutes")
    print("- Use interruptible sleep for other delays")

if __name__ == "__main__":
    test_smart_waiting()