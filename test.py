import pyautogui
import time
import multiprocessing
import os
import platform
import logging
import argparse
from datetime import datetime

from utils.battery_utils import get_battery_level
from utils.process_manager import process_manager
from test_cases.office_test import run_office_test
from test_cases.browser_test import run_browser_test
from test_cases.youtube_test import run_youtube_test

# Disable fail safe mechanism of Pyautogui
pyautogui.FAILSAFE = False

logging.basicConfig(
    filename=f'logfilename.log',
    encoding='utf-8',
    level=logging.INFO,
    format='%(asctime)s | %(message)s'
)

def start_test(no_youtube='0'):
    logging.info('====================== Starting new test... ====================')
    if (no_youtube == '1'):
        youtube_message = 'YouTube test is disabled'
    else:
        youtube_message = 'YouTube test is enable'

    print(youtube_message)
    logging.info(youtube_message)

    os_name = os.name
    platform_name = platform.system()

    print(f'Running on {os_name}, {platform_name}')
    get_battery_level()

    try:
        while True:
            print("Starting new test cycle...")
            
            # Cleanup any processes from previous cycles
            cleanup_count = process_manager.cleanup_common_test_processes(force_kill=True)
            if cleanup_count > 0:
                logging.info(f'Pre-cycle cleanup: terminated {cleanup_count} processes')
            
            # Run tests with error handling
            try:
                run_browser_test()
            except Exception as e:
                logging.error(f'Browser test failed: {e}')
                process_manager.cleanup_common_test_processes(force_kill=True)
            
            try:
                run_office_test()
            except Exception as e:
                logging.error(f'Office test failed: {e}')
                process_manager.cleanup_common_test_processes(force_kill=True)

            if str(no_youtube) != '1':
                try:
                    run_youtube_test()
                except Exception as e:
                    logging.error(f'YouTube test failed: {e}')
                    process_manager.cleanup_common_test_processes(force_kill=True)
            
            print("Test cycle completed. Starting next cycle...")
            
    except KeyboardInterrupt:
        print("Test interrupted by user")
        logging.info('Test interrupted by user')
    except Exception as e:
        print(f"Test failed with error: {e}")
        logging.error(f'Test failed: {e}')
    finally:
        # Final cleanup
        print("Performing final cleanup...")
        final_cleanup = process_manager.cleanup_common_test_processes(force_kill=True)
        logging.info(f'Final cleanup: terminated {final_cleanup} processes')

def calculate_elapsed_time(start_time):
    elapsed_time = datetime.now() - start_time
    print(f'Elapsed time: {elapsed_time}')

def information_process():
    start_time = datetime.now()
    while True:
        get_battery_level()
        calculate_elapsed_time(start_time=start_time)
        time.sleep(3)

if __name__ == "__main__":
    parser=argparse.ArgumentParser(description="Run a script and measure battery life")
    parser.add_argument("no_youtube", nargs='?', choices=['1', '0'], default='0')

    args = parser.parse_args()

    p1 = multiprocessing.Process(target=start_test, args=(args.no_youtube))
    p2 = multiprocessing.Process(target=information_process)
    p1.start()
    p2.start()