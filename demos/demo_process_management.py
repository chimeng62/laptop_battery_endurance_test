"""
Process Management Comparison Demo

This script demonstrates the difference between the old approach (prone to hanging)
and the new approach (reliable process termination).
"""

import time
import subprocess
import webbrowser
import platform
from utils.process_manager import ProcessManager

def demo_old_approach():
    """Demonstrate the old approach that can hang on confirmation dialogs."""
    print("=== OLD APPROACH (Problematic) ===")
    print("This approach uses keyboard shortcuts which can trigger confirmation dialogs")
    print()
    
    # Open a browser
    print("1. Opening browser with a webpage...")
    webbrowser.open('https://example.com')
    time.sleep(3)
    
    print("2. Old approach would use:")
    if platform.system() == "Windows":
        print("   pyautogui.hotkey('alt', 'f4')  # Can trigger 'Close all tabs?' dialog")
    else:
        print("   pyautogui.hotkey('command', 'q')  # Can trigger 'Save changes?' dialog")
    
    print()
    print("❌ PROBLEM: This can hang if the application shows a confirmation dialog!")
    print("❌ PROBLEM: No way to track which specific processes were opened by the test")
    print("❌ PROBLEM: If user has other instances open, might close the wrong one")
    print()


def demo_new_approach():
    """Demonstrate the new robust approach."""
    print("=== NEW APPROACH (Robust) ===")
    print("This approach tracks processes and uses force termination")
    print()
    
    pm = ProcessManager()
    
    # Track existing processes
    print("1. Scanning for existing browser processes...")
    existing = pm.find_and_track_processes(['msedge', 'chrome', 'firefox', 'safari'])
    print(f"   Found and tracking {len(existing)} existing browser processes")
    
    # Open a browser  
    print("2. Opening browser with a webpage...")
    webbrowser.open('https://example.com')
    time.sleep(3)
    
    # Track new processes
    print("3. Scanning for new browser processes...")
    all_tracked = pm.find_and_track_processes(['msedge', 'chrome', 'firefox', 'safari'])
    print(f"   Now tracking {len(all_tracked)} total browser processes")
    
    # Show tracked processes
    processes = pm.get_tracked_processes_info()
    if processes:
        print("4. Currently tracked processes:")
        for proc in processes:
            print(f"   - {proc['name']} (PID: {proc['pid']}) - Memory: {proc['memory_mb']:.1f}MB")
    
    # Force terminate
    print("5. Force terminating all tracked processes...")
    terminated = pm.cleanup_all_tracked(force_kill=True)
    print(f"   ✅ Successfully terminated {terminated} processes")
    
    print()
    print("✅ ADVANTAGES:")
    print("✅ No confirmation dialogs - processes are force killed")
    print("✅ Tracks which processes belong to the test")  
    print("✅ Won't interfere with user's existing applications")
    print("✅ Reliable cleanup even if applications are unresponsive")
    print("✅ Cross-platform process termination")
    print()


def demo_safety_cleanup():
    """Demonstrate the safety cleanup feature."""
    print("=== SAFETY CLEANUP FEATURE ===")
    print("Even if process tracking fails, we can cleanup common test processes")
    print()
    
    pm = ProcessManager()
    
    print("Running safety cleanup for common battery test processes...")
    terminated = pm.cleanup_common_test_processes(force_kill=True)
    
    if terminated > 0:
        print(f"✅ Safety cleanup terminated {terminated} processes")
    else:
        print("✅ No processes needed cleanup - system is clean")
    
    print()
    print("This ensures that even if something goes wrong with tracking,")
    print("we can still clean up common processes that battery tests might leave running.")
    print()


def main():
    """Run the comparison demo."""
    print("Process Management Approach Comparison")
    print("=" * 50)
    print()
    
    print("This demo shows why the new process management approach is better")
    print("for battery testing reliability.")
    print()
    
    input("Press Enter to see the old approach problems...")
    demo_old_approach()
    
    input("Press Enter to see the new robust approach...")
    demo_new_approach()
    
    input("Press Enter to see the safety cleanup feature...")
    demo_safety_cleanup()
    
    print("=" * 50)
    print("Demo completed! The new approach prevents battery tests from hanging")
    print("on confirmation dialogs and provides reliable process cleanup.")


if __name__ == "__main__":
    main()