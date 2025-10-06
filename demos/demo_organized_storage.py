#!/usr/bin/env python3
"""
Quick Demo: Battery Test with Organized Storage

This script demonstrates the integrated battery test with organized storage.
It runs a short version of the actual battery test to show the organized storage in action.
"""

import os
import time
from datetime import datetime

from utils.process_manager import process_manager
from utils.logger_config import get_logger
from utils.results_manager import results_manager
from utils.battery_utils import get_battery_level

# Setup
logger = get_logger(__name__)
print("🔋 Battery Test with Organized Storage - Demo")
print("=" * 50)

def demo_battery_test():
    """Run a short demo version of the battery test."""
    
    # Start organized test session
    test_id = results_manager.start_new_test("demo_test")
    logger.info(f'Starting demo battery test session: {test_id}')
    print(f"📁 Test folder created: {results_manager.current_test_dir}")
    
    try:
        # Simulate a few test cycles with battery readings
        for cycle in range(1, 4):  # 3 short cycles
            print(f"\n🔄 Test Cycle {cycle}")
            
            # Record battery level at start of cycle
            battery_info = get_battery_level()
            results_manager.record_battery_reading(test_id, battery_info, test_phase=f"cycle_{cycle}")
            
            # Simulate some brief work (instead of opening browsers/apps)
            print("   📊 Simulating browser test...")
            time.sleep(2)
            
            print("   📄 Simulating office test...")
            time.sleep(2)
            
            print("   📺 Simulating youtube test...")
            time.sleep(2)
            
            # Record another battery reading mid-cycle
            battery_info = get_battery_level()
            results_manager.record_battery_reading(test_id, battery_info, test_phase=f"cycle_{cycle}_mid")
            
            print(f"   ✅ Cycle {cycle} completed")
            
        print(f"\n✨ Demo completed! Check results in: {results_manager.current_test_dir}")
        
    except KeyboardInterrupt:
        print("\n⏹️  Demo interrupted by user")
        logger.info('Demo interrupted by user')
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        logger.error(f'Demo failed: {e}')
    finally:
        # Clean up any processes
        process_manager.cleanup_all_tracked()
        
        # Finish the organized test session
        final_battery = get_battery_level()
        summary = results_manager.finish_test(final_battery_percent=final_battery.get('percentage'))
        
        print(f"\n📋 Test Summary:")
        print(f"   - Duration: {summary['duration_hours']:.3f} hours ({summary['duration_hours']*60:.1f} minutes)")
        print(f"   - Test Status: {summary['test_status']}")
        print(f"   - Results saved in: {results_manager.current_test_dir}")
        
        # Show what files were created
        print(f"\n📁 Files created:")
        for file in os.listdir(results_manager.current_test_dir):
            file_path = os.path.join(results_manager.current_test_dir, file)
            if os.path.isfile(file_path):
                size = os.path.getsize(file_path)
                print(f"   📄 {file} ({size} bytes)")

def main():
    """Run the demo."""
    print("This demo shows the organized storage system in action.")
    print("It will create a test folder with system info, logs, battery readings, and summary.\n")
    
    try:
        response = input("🚀 Run battery test demo? (Y/n): ").lower().strip()
        if response in ('', 'y', 'yes'):
            demo_battery_test()
        else:
            print("Demo cancelled.")
    except KeyboardInterrupt:
        print("\nDemo cancelled.")

if __name__ == "__main__":
    main()