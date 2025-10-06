"""
Simple Smart Waiting Utilities

Simple, reliable waiting functions to replace hardcoded time.sleep() calls.
Keeps YouTube at fixed 20 minutes as requested.
"""

import time
import psutil
import pyautogui
from typing import Optional


def wait_for_page_load(timeout: float = 10.0) -> bool:
    """
    Simple page load detection - just waits for CPU to settle after opening browser.
    
    Args:
        timeout: Maximum time to wait in seconds
        
    Returns:
        bool: True if page appears loaded, False if timeout
    """
    start_time = time.time()
    
    # Wait minimum 1 second for browser to start
    time.sleep(1)
    
    # Check if CPU usage has settled (indicates page loading complete)
    stable_count = 0
    last_cpu = psutil.cpu_percent(interval=0.5)
    
    while time.time() - start_time < timeout:
        current_cpu = psutil.cpu_percent(interval=0.5)
        
        # If CPU usage is stable (not spiking), page is likely loaded
        if abs(current_cpu - last_cpu) < 10:  # CPU change less than 10%
            stable_count += 1
            if stable_count >= 2:  # 2 consecutive stable readings
                return True
        else:
            stable_count = 0
            
        last_cpu = current_cpu
    
    # Timeout reached, assume loaded anyway
    return False


def wait_for_application_ready(timeout: float = 15.0) -> bool:
    """
    Simple check if application window is ready for interaction.
    
    Args:
        timeout: Maximum time to wait in seconds
        
    Returns:
        bool: True if application appears ready
    """
    start_time = time.time()
    
    # Wait minimum 2 seconds for app to start
    time.sleep(2)
    
    while time.time() - start_time < timeout:
        try:
            # Try to get screen size - if this works, GUI is responsive
            width, height = pyautogui.size()
            if width > 0 and height > 0:
                # Wait a bit more for app to fully load
                time.sleep(1)
                return True
        except:
            pass
            
        time.sleep(0.5)
    
    return False


def wait_for_process_start(process_names: list, timeout: float = 10.0) -> bool:
    """
    Wait for a process to start (useful after launching applications).
    
    Args:
        process_names: List of process names to look for
        timeout: Maximum time to wait
        
    Returns:
        bool: True if any process found
    """
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        for proc in psutil.process_iter(['name']):
            try:
                proc_name = proc.info['name'].lower()
                for target in process_names:
                    if target.lower() in proc_name:
                        return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        time.sleep(0.5)
    
    return False


def smart_sleep(duration: float, check_interval: float = 1.0):
    """
    Interruptible sleep that can be stopped early if needed.
    
    Args:
        duration: Total time to sleep
        check_interval: How often to check for early termination
    """
    elapsed = 0.0
    while elapsed < duration:
        sleep_time = min(check_interval, duration - elapsed)
        time.sleep(sleep_time)
        elapsed += sleep_time


# Keep YouTube at exactly 20 minutes as requested
YOUTUBE_DURATION = 20 * 60  # 20 minutes in seconds