#!/usr/bin/env python3
"""
Test script to verify organized storage functionality for Battery Endurance Test

This script validates:
1. Results folder creation wit    folder_contents = list(Path(results_manager.current_test_dir).iterdir())proper structure
2. System information collection
3. Battery reading recording
4. CSV timeline generation 
5. JSON summary creation
6. Automatic result calculation

Expected behavior: Creates organized test folders with all required files
"""

import os
import json
import csv
import shutil
from datetime import datetime, timedelta
from pathlib import Path

# Import our modules
from utils.results_manager import ResultsManager
from utils.battery_utils import get_battery_level
from utils.logger_config import get_logger

# Setup
logger = get_logger(__name__)
print("🧪 Testing Organized Storage System")
print("=" * 50)

def test_results_manager():
    """Test all aspects of the results manager"""
    
    # Initialize results manager
    results_manager = ResultsManager()
    
    # Test 1: Start new test session
    print("📁 Test 1: Starting new test session...")
    test_id = results_manager.start_new_test("storage_test")
    
    if not test_id:
        print("❌ FAILED: Could not start test session")
        return False
        
    print(f"✅ SUCCESS: Started test session {test_id}")
    print(f"   Results folder: {results_manager.current_test_dir}")
    
    # Verify folder structure exists
    expected_files = [
        Path(results_manager.current_test_dir) / "system_info.json",
        Path(results_manager.current_test_dir) / "test_log.log",
        Path(results_manager.current_test_dir) / "battery_timeline.csv"
    ]
    
    for file_path in expected_files:
        if file_path.exists():
            print(f"   ✅ Created: {file_path.name}")
        else:
            print(f"   ❌ Missing: {file_path.name}")
            return False
    
    # Test 2: System information collection
    print("\n🖥️  Test 2: System information collection...")
    system_info_path = Path(results_manager.current_test_dir) / "system_info.json"
    
    try:
        with open(system_info_path, 'r') as f:
            system_info = json.load(f)
        
        required_fields = ['hostname', 'os_name', 'os_version', 'cpu', 'ram_gb', 'battery_present']
        missing_fields = [field for field in required_fields if field not in system_info]
        
        if missing_fields:
            print(f"   ❌ Missing system info fields: {missing_fields}")
            return False
            
        print("   ✅ System info complete with all required fields:")
        print(f"      - Hostname: {system_info['hostname']}")
        print(f"      - OS: {system_info['os_name']} {system_info['os_version']}")
        print(f"      - CPU: {system_info['cpu'][:50]}...")
        print(f"      - RAM: {system_info['ram_gb']} GB")
        print(f"      - Battery: {'Present' if system_info['battery_present'] else 'Not found'}")
        if system_info.get('battery_design_capacity'):
            print(f"      - Battery capacity: {system_info['battery_design_capacity']}")
        
    except Exception as e:
        print(f"   ❌ Error reading system info: {e}")
        return False
    
    # Test 3: Battery reading recording
    print("\n🔋 Test 3: Battery reading recording...")
    
    # Simulate multiple battery readings
    test_readings = [
        {'percentage': 100.0, 'is_plugged': False, 'status': 'Not Plugged In'},
        {'percentage': 98.5, 'is_plugged': False, 'status': 'Not Plugged In'},
        {'percentage': 97.2, 'is_plugged': False, 'status': 'Not Plugged In'},
        {'percentage': 95.8, 'is_plugged': False, 'status': 'Not Plugged In'},
    ]
    
    for i, reading in enumerate(test_readings):
        results_manager.record_battery_reading(test_id, reading)
        print(f"   📊 Recorded reading {i+1}: {reading['percentage']}%")
    
    # Verify CSV timeline
    csv_path = Path(results_manager.current_test_dir) / "battery_timeline.csv"
    try:
        with open(csv_path, 'r', newline='') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        if len(rows) != len(test_readings):
            print(f"   ❌ CSV has {len(rows)} rows, expected {len(test_readings)}")
            return False
            
        print(f"   ✅ CSV timeline recorded {len(rows)} readings correctly")
        
        # Check CSV structure
        expected_columns = ['timestamp', 'battery_percent', 'plugged', 'cycle_number', 'test_phase']
        if not all(col in rows[0].keys() for col in expected_columns):
            print(f"   ❌ CSV missing columns. Expected: {expected_columns}, Got: {list(rows[0].keys())}")
            return False
            
        print("   ✅ CSV has all required columns")
        
    except Exception as e:
        print(f"   ❌ Error reading CSV: {e}")
        return False
    
    # Test 4: Test completion and summary
    print("\n📋 Test 4: Test completion and summary...")
    
    summary_result = results_manager.finish_test(final_battery_percent=95)
    if not summary_result:
        print("   ❌ Failed to finish test")
        return False
    
    # Verify test summary
    summary_path = Path(results_manager.current_test_dir) / "summary.json"
    
    try:
        with open(summary_path, 'r') as f:
            summary = json.load(f)
        
        required_summary_fields = ['test_id', 'start_time', 'end_time', 'duration_hours', 
                                 'total_cycles', 'test_status']
        
        missing_fields = [field for field in required_summary_fields if field not in summary]
        if missing_fields:
            print(f"   ❌ Missing summary fields: {missing_fields}")
            return False
        
        print("   ✅ Test summary complete:")
        print(f"      - Duration: {summary['duration_hours']:.2f} hours")
        print(f"      - Cycles: {summary['total_cycles']}")
        print(f"      - Average cycle time: {summary.get('average_cycle_time_minutes', 0):.1f} minutes")
        print(f"      - Status: {summary['test_status']}")
        
    except Exception as e:
        print(f"   ❌ Error reading summary: {e}")
        return False
    
    # Test 5: Folder cleanup verification
    print("\n🗂️  Test 5: Folder structure verification...")
    
    folder_contents = list(Path(results_manager.current_test_dir).iterdir())
    expected_files = ['system_info.json', 'test_log.log', 'battery_timeline.csv', 'test_summary.json']
    
    expected_files = ['system_info.json', 'test_log.log', 'battery_timeline.csv', 'summary.json']
    
    actual_files = [f.name for f in folder_contents if f.is_file()]
    missing_files = [f for f in expected_files if f not in actual_files]
    
    if missing_files:
        print(f"   ❌ Missing files: {missing_files}")
        return False
        
    print(f"   ✅ All expected files present: {actual_files}")
    
    print(f"\n📁 Complete test folder: {results_manager.current_test_dir}")
    
    return True

def test_real_battery_reading():
    """Test actual battery reading functionality"""
    print("\n🔋 Testing Real Battery Reading...")
    
    try:
        battery_info = get_battery_level()
        
        if not isinstance(battery_info, dict):
            print(f"   ❌ Battery reading returned {type(battery_info)}, expected dict")
            return False
        
        required_keys = ['percentage', 'is_plugged', 'status']
        missing_keys = [key for key in required_keys if key not in battery_info]
        
        if missing_keys:
            print(f"   ❌ Missing battery info keys: {missing_keys}")
            return False
            
        print(f"   ✅ Real battery reading successful:")
        print(f"      - Level: {battery_info['percentage']}%")
        print(f"      - Status: {battery_info['status']}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error reading battery: {e}")
        return False

def cleanup_test_results():
    """Clean up test results folder"""
    print("\n🧹 Cleanup: Removing test results...")
    
    results_base = Path("battery_test_results")
    if results_base.exists():
        # Find storage_test folders
        test_folders = [f for f in results_base.iterdir() 
                       if f.is_dir() and "storage_test" in f.name]
        
        for folder in test_folders:
            try:
                shutil.rmtree(folder)
                print(f"   🗑️  Removed: {folder.name}")
            except Exception as e:
                print(f"   ⚠️  Could not remove {folder.name}: {e}")

def main():
    """Run all tests"""
    print("Starting Battery Endurance Test - Organized Storage Verification")
    print("This will create and test the organized storage system\n")
    
    all_tests_passed = True
    
    try:
        # Test results manager
        if not test_results_manager():
            all_tests_passed = False
        
        # Test real battery reading
        if not test_real_battery_reading():
            all_tests_passed = False
            
    except Exception as e:
        print(f"❌ Test suite failed with error: {e}")
        all_tests_passed = False
    
    # Summary
    print("\n" + "=" * 50)
    if all_tests_passed:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Organized storage system is working correctly")
        print("✅ Ready for battery endurance testing")
    else:
        print("❌ SOME TESTS FAILED!")
        print("🔧 Check the errors above and fix before running battery tests")
    
    print("\n🗂️  Test results are saved in: battery_test_results/")
    
    # Ask about cleanup
    try:
        response = input("\n🧹 Clean up test folders? (y/N): ").lower().strip()
        if response == 'y':
            cleanup_test_results()
    except KeyboardInterrupt:
        print("\nTest completed.")

if __name__ == "__main__":
    main()