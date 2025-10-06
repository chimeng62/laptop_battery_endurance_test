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
from utils.logger_config import get_logger
from utils.results_manager import ResultsManager
from test_cases.office_test import run_office_test
from test_cases.browser_test import run_browser_test
from test_cases.youtube_test import run_youtube_test

# Disable fail safe mechanism of Pyautogui
pyautogui.FAILSAFE = False

# Configure centralized logging and results management
from utils.logger_config import get_logger
from utils.results_manager import results_manager
logger = get_logger(__name__)

def start_test(no_youtube='0'):
    # Start organized test session
    test_id = results_manager.start_new_test("battery_endurance")
    logger.info(f'Starting new organized test session: {test_id}')
    logger.info('====================== Starting new test... ====================')
    if (no_youtube == '1'):
        youtube_message = 'YouTube test is disabled'
    else:
        youtube_message = 'YouTube test is enable'

    print(youtube_message)
    logger.info(youtube_message)

    os_name = os.name
    platform_name = platform.system()

    print(f'Running on {os_name}, {platform_name}')
    get_battery_level()

    try:
        while True:
            print("Starting new test cycle...")
            
            # Record battery level at start of cycle
            battery_level = get_battery_level()
            results_manager.record_battery_reading(test_id, battery_level)
            
            # Cleanup any processes from previous cycles
            cleanup_count = process_manager.cleanup_common_test_processes(force_kill=True)
            if cleanup_count > 0:
                logger.info(f'Pre-cycle cleanup: terminated {cleanup_count} processes')
            
            # Run tests with error handling
            try:
                run_browser_test()
            except Exception as e:
                logger.error(f'Browser test failed: {e}')
                process_manager.cleanup_common_test_processes(force_kill=True)
            
            try:
                run_office_test()
            except Exception as e:
                logger.error(f'Office test failed: {e}')
                process_manager.cleanup_common_test_processes(force_kill=True)

            if str(no_youtube) != '1':
                try:
                    run_youtube_test()
                except Exception as e:
                    logger.error(f'YouTube test failed: {e}')
                    process_manager.cleanup_common_test_processes(force_kill=True)
            
            print("Test cycle completed. Starting next cycle...")
            
    except KeyboardInterrupt:
        print("Test interrupted by user")
        logger.info('Test interrupted by user')
    except Exception as e:
        print(f"Test failed with error: {e}")
        logger.error(f'Test failed: {e}')
    finally:
        # Final cleanup
        print("Performing final cleanup...")
        final_cleanup = process_manager.cleanup_common_test_processes(force_kill=True)
        logger.info(f'Final cleanup: terminated {final_cleanup} processes')
        
        # Finish the organized test session
        final_battery = get_battery_level()
        results_manager.finish_test(final_battery_percent=final_battery.get('percentage', None))
        logger.info(f'Test completed - Results saved to: {results_manager.current_test_dir}')

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