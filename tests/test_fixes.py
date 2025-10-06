"""
Quick test for Word launching and Brave browser detection
"""

from utils.process_manager import ProcessManager
import subprocess
import time

def test_word_launch():
    print("Testing Word launch methods...")
    pm = ProcessManager()
    
    # Test different Word launch methods
    word_commands = [
        ['cmd', '/c', 'start', 'winword'],
        ['winword.exe'],
        [r'C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE'],
        [r'C:\Program Files (x86)\Microsoft Office\root\Office16\WINWORD.EXE'],
    ]
    
    for i, cmd in enumerate(word_commands):
        try:
            print(f"Trying method {i+1}: {' '.join(cmd)}")
            pid = pm.launch_and_track(cmd, f'Word Test {i+1}')
            if pid:
                print(f"  ✅ Success! Word launched with PID {pid}")
                time.sleep(2)
                if pm.terminate_process(pid, force_kill=True):
                    print(f"  ✅ Successfully terminated Word")
                return True
            else:
                print(f"  ❌ Failed to launch")
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    print("❌ All Word launch methods failed")
    return False

def test_brave_detection():
    print("\nTesting Brave browser detection...")
    pm = ProcessManager()
    
    # Check if Brave is already running
    brave_processes = pm.find_and_track_processes(['brave'])
    print(f"Found {len(brave_processes)} existing Brave processes")
    
    # Test opening a page with default browser (should be Brave)
    import webbrowser
    print("Opening test page in default browser...")
    webbrowser.open('https://httpbin.org/html')  # Simple test page
    
    time.sleep(3)
    
    # Check for new Brave processes
    new_brave = pm.find_and_track_processes(['brave'])
    print(f"Now tracking {len(new_brave)} Brave processes")
    
    processes = pm.get_tracked_processes_info()
    for proc in processes:
        if 'brave' in proc['name'].lower():
            print(f"  Found Brave: {proc['name']} (PID: {proc['pid']}) - Memory: {proc['memory_mb']:.1f}MB")
    
    # Cleanup
    if len(new_brave) > 0:
        terminated = pm.cleanup_all_tracked(force_kill=True)
        print(f"✅ Terminated {terminated} Brave processes")
        return True
    else:
        print("❌ No Brave processes detected")
        return False

if __name__ == "__main__":
    print("Quick Fix Test")
    print("=" * 30)
    
    word_ok = test_word_launch()
    brave_ok = test_brave_detection()
    
    print("\n" + "=" * 30)
    if word_ok and brave_ok:
        print("✅ All tests passed!")
    else:
        print("⚠️  Some issues detected:")
        if not word_ok:
            print("  - Word launching needs investigation")
        if not brave_ok:
            print("  - Brave browser detection needs investigation")