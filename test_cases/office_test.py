import pyautogui
import os
import platform
from utils.battery_utils import get_battery_level
from utils import start_file, close_window
from utils import custom_scroll
from utils.process_manager import process_manager
from utils.smart_wait import wait_for_application_ready, smart_sleep
import time

text_to_write = """
    Activity Requirements
    Each team in the class will be assigned one of the topics from the below list. The students will research and write a 700 word reflection report about it:
    1.	Identify a government initiative on IT, describe it and explain its impact on IT strategy.
    2.	Identify an economic factor (such as AEC - Asean Economic Community or TPP), describe it and explain its impact on IT strategy.
    3.	Identify a technology that will be soon commercialized, describe it and explain its impact on IT strategy.
"""

def run_office_test():
    base_path = os.path.join('test_files', 'office')

    file_paths = [
        os.path.join(base_path, 'word_test_1.docx'),
        os.path.join(base_path, 'word_test_2.docx'),
        os.path.join(base_path, 'word_test_3.docx'),
        os.path.join(base_path, 'excel_test_1.xlsx'),
    ]

    os_name = os.name
    platform_name = platform.system()

    print(f'Running Office Test on {os_name}, {platform_name}')
    get_battery_level()

    screenWidth, screenHeight = pyautogui.size() # Get the size of the primary monitor
    print(f'Screen size: {screenWidth}, {screenHeight}')

    # Track Office processes before starting
    office_processes = ['winword', 'excel', 'powerpnt', 'Word', 'Excel', 'PowerPoint']
    initial_office = process_manager.find_and_track_processes(office_processes)
    print(f'Initially tracking {len(initial_office)} Office processes')

    for path in file_paths:
        print(f'Opening file: {path}')
        
        start_file(path)
        
        # Smart wait for application to be ready (max 15 seconds)
        if wait_for_application_ready(timeout=15):
            print("  Application ready")
        else:
            print("  Application timeout - continuing anyway")
            
        process_manager.find_and_track_processes(office_processes)
        
        pyautogui.moveTo(screenWidth/2, screenHeight/2, duration=1)
        pyautogui.click(clicks=1)

        custom_scroll(times=10, direction="down")

        # Smart sleep instead of hardcoded delay
        smart_sleep(10)

        custom_scroll(times=10, direction="up")

        # Smart sleep instead of hardcoded delay
        smart_sleep(10)

        custom_scroll(times=10, direction="down")

        # Force close to avoid "Do you want to save?" dialogs
        print("Force closing Office application...")
        terminated = process_manager.cleanup_all_tracked(force_kill=True)
        print(f'Force terminated {terminated} Office processes')

        # Brief pause before next file
        smart_sleep(2)
    
    # Final cleanup of any remaining Office processes
    print("Final Office cleanup...")
    final_cleanup = process_manager.terminate_by_name(
        ['winword.exe', 'excel.exe', 'powerpnt.exe'], 
        force_kill=True
    )
    if final_cleanup > 0:
        print(f'Final cleanup terminated {final_cleanup} additional Office processes')