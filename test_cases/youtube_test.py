import pyautogui
import time
import webbrowser
import os
import platform
from utils.battery_utils import get_battery_level
from utils import close_window
from utils.smart_wait import YOUTUBE_DURATION, wait_for_page_load
from utils.process_manager import process_manager

def run_youtube_test():

    os_name = os.name
    platform_name = platform.system()

    print(f'Running YouTube Test on {os_name}, {platform_name}')
    get_battery_level()

    screenWidth, screenHeight = pyautogui.size() # Get the size of the primary monitor
    print(f'Screen size: {screenWidth}, {screenHeight}')

    # Browsing test
    urls = [
        'https://www.youtube.com/watch?v=MbXLt7OwEXI',
        'https://www.youtube.com/watch?v=w1ucZCmvO5c',
    ]

    # Track browser processes for YouTube (including Brave)
    process_manager.find_and_track_processes(['msedge', 'chrome', 'firefox', 'safari', 'brave'])

    for url in urls:
        get_battery_level()
        print(f"Opening YouTube video: {url}")
        webbrowser.open(url)

        # Brief wait for page load, then fixed 20-minute duration as requested
        wait_for_page_load(timeout=5)
        print(f"Playing video for {YOUTUBE_DURATION//60} minutes...")
        
        time.sleep(YOUTUBE_DURATION)  # Keep exactly 20 minutes as requested

        get_battery_level()

    # Force close browser to avoid confirmation dialogs
    print("Closing YouTube browser...")
    terminated = process_manager.cleanup_all_tracked(force_kill=True)