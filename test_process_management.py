"""
Test Script for Process Management Functionality

This script tests the process management system without running the full battery test.
It simulates opening applications and verifies that they can be properly tracked and terminated.
"""

import time
import subprocess
import logging
import os
from utils.process_manager import ProcessManager

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)

logger = logging.getLogger(__name__)


def test_process_tracking():
    """Test basic process tracking functionality."""
    logger.info("=== Testing Process Tracking ===")
    
    pm = ProcessManager()
    
    # Test 1: Launch and track notepad (Windows) or TextEdit (macOS)
    logger.info("Test 1: Launch and track a simple application")
    
    import platform
    if platform.system() == "Windows":
        # Launch notepad
        pid = pm.launch_and_track(['notepad.exe'], 'Test Notepad')
        if pid:
            logger.info(f"✅ Successfully launched and tracked notepad (PID: {pid})")
            
            # Wait a bit then terminate
            time.sleep(2)
            if pm.terminate_process(pid):
                logger.info("✅ Successfully terminated notepad")
            else:
                logger.error("❌ Failed to terminate notepad")
        else:
            logger.error("❌ Failed to launch notepad")
    else:
        # Launch TextEdit on macOS
        pid = pm.launch_and_track(['open', '-a', 'TextEdit'], 'Test TextEdit')
        if pid:
            logger.info(f"✅ Successfully launched and tracked TextEdit (PID: {pid})")
            
            # Wait a bit then terminate
            time.sleep(2)
            if pm.terminate_process(pid):
                logger.info("✅ Successfully terminated TextEdit")
            else:
                logger.error("❌ Failed to terminate TextEdit")
        else:
            logger.error("❌ Failed to launch TextEdit")


def test_browser_simulation():
    """Test opening a browser and tracking it."""
    logger.info("=== Testing Browser Process Management ===")
    
    pm = ProcessManager()
    
    # Find existing browser processes before we start
    initial_browsers = pm.find_and_track_processes(['msedge', 'chrome', 'firefox', 'safari'])
    logger.info(f"Found {len(initial_browsers)} existing browser processes")
    
    # Open a webpage using default browser
    import webbrowser
    
    logger.info("Opening a webpage in default browser...")
    webbrowser.open('https://www.example.com')
    
    # Wait for browser to start
    time.sleep(3)
    
    # Find new browser processes
    new_browsers = pm.find_and_track_processes(['msedge', 'chrome', 'firefox', 'safari'])
    logger.info(f"Now tracking {len(new_browsers)} browser processes")
    
    # Show process info
    processes_info = pm.get_tracked_processes_info()
    for info in processes_info:
        logger.info(f"  Process: {info['name']} (PID: {info['pid']}) - CPU: {info['cpu_percent']:.1f}% - Memory: {info['memory_mb']:.1f}MB")
    
    # Wait a bit then cleanup
    time.sleep(5)
    
    logger.info("Cleaning up browser processes...")
    terminated = pm.cleanup_all_tracked(force_kill=True)
    logger.info(f"✅ Terminated {terminated} tracked browser processes")


def test_office_simulation():
    """Test opening Office applications (if available)."""
    logger.info("=== Testing Office Process Management ===")
    
    pm = ProcessManager()
    
    import platform
    if platform.system() == "Windows":
        # Try to open Word
        try:
            logger.info("Attempting to launch Word...")
            pid = pm.launch_and_track(['winword.exe'], 'Test Word')
            if pid:
                logger.info(f"✅ Successfully launched Word (PID: {pid})")
                
                # Wait then terminate
                time.sleep(3)
                if pm.terminate_process(pid, force_kill=True):
                    logger.info("✅ Successfully terminated Word")
                else:
                    logger.error("❌ Failed to terminate Word")
            else:
                logger.info("⚠️  Word not available or failed to launch")
        except Exception as e:
            logger.info(f"⚠️  Word test failed: {e}")
    
    # Test creating a simple text file and opening it
    logger.info("Testing file opening simulation...")
    
    # Create a test file
    test_file = 'test_document.txt'
    with open(test_file, 'w') as f:
        f.write("This is a test document for process management testing.")
    
    try:
        if platform.system() == "Windows":
            # Open with default application
            import os
            os.startfile(test_file)
        else:
            subprocess.run(['open', test_file])
        
        logger.info("Opened test file with default application")
        
        # Wait then cleanup any text editor processes
        time.sleep(3)
        
        # Find and terminate common text editors
        terminated = pm.terminate_by_name(['notepad.exe', 'TextEdit', 'gedit'], force_kill=True)
        logger.info(f"Terminated {terminated} text editor processes")
        
    except Exception as e:
        logger.error(f"File opening test failed: {e}")
    finally:
        # Cleanup test file
        try:
            os.remove(test_file)
        except:
            pass


def test_force_kill_scenarios():
    """Test force kill functionality for stubborn processes."""
    logger.info("=== Testing Force Kill Scenarios ===")
    
    pm = ProcessManager()
    
    # Launch multiple instances of a simple application
    pids = []
    
    import platform
    if platform.system() == "Windows":
        app_cmd = ['notepad.exe']
        app_name = 'Notepad'
    else:
        app_cmd = ['open', '-a', 'Calculator']
        app_name = 'Calculator'
    
    logger.info(f"Launching multiple {app_name} instances...")
    
    for i in range(3):
        pid = pm.launch_and_track(app_cmd, f'{app_name} Instance {i+1}')
        if pid:
            pids.append(pid)
            logger.info(f"Launched {app_name} instance {i+1} (PID: {pid})")
    
    logger.info(f"Launched {len(pids)} {app_name} instances")
    
    # Wait a bit
    time.sleep(2)
    
    # Show all tracked processes
    processes_info = pm.get_tracked_processes_info()
    logger.info("Currently tracked processes:")
    for info in processes_info:
        logger.info(f"  {info['name']} (PID: {info['pid']}) - Runtime: {info['runtime_seconds']:.1f}s")
    
    # Test force kill all
    logger.info("Force killing all tracked processes...")
    terminated = pm.cleanup_all_tracked(force_kill=True)
    logger.info(f"✅ Force killed {terminated} processes")


def test_cleanup_common_processes():
    """Test the safety net cleanup function."""
    logger.info("=== Testing Common Process Cleanup ===")
    
    pm = ProcessManager()
    
    logger.info("Running safety cleanup for common test processes...")
    terminated = pm.cleanup_common_test_processes(force_kill=True)
    logger.info(f"Cleaned up {terminated} common test processes")


def main():
    """Run all process management tests."""
    logger.info("Starting Process Management Test Suite")
    logger.info("=" * 50)
    
    try:
        # Basic tests
        test_process_tracking()
        time.sleep(1)
        
        # Browser simulation
        test_browser_simulation()
        time.sleep(1)
        
        # Office simulation
        test_office_simulation()
        time.sleep(1)
        
        # Force kill scenarios
        test_force_kill_scenarios()
        time.sleep(1)
        
        # Cleanup test
        test_cleanup_common_processes()
        
        logger.info("=" * 50)
        logger.info("✅ All process management tests completed!")
        
    except Exception as e:
        logger.error(f"❌ Test suite failed: {e}")
        
    finally:
        # Final cleanup to make sure no test processes are left running
        pm = ProcessManager()
        pm.cleanup_common_test_processes(force_kill=True)
        logger.info("Final cleanup completed")


if __name__ == "__main__":
    main()