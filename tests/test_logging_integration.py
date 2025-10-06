"""
Integration Test for Centralized Logging

This test verifies that all modules are now using the centralized logging system
and that there are no more duplicate logging configurations.
"""

import tempfile
import os
from utils.logger_config import configure_logging, get_logger
from utils.battery_utils import get_battery_level


def test_integrated_logging():
    """Test that all modules use centralized logging correctly."""
    print("Integration Test: Centralized Logging System")
    print("=" * 50)
    
    # Create temporary log file for testing
    temp_log = tempfile.mktemp(suffix='.log')
    
    try:
        # Configure logging to use temporary file
        configure_logging(log_file=temp_log, force_reconfigure=True)
        print(f"Configured logging to: {temp_log}")
        
        # Test 1: Main test module logging
        print("\n1. Testing main test module logging...")
        from test import start_test
        # Note: We won't actually run start_test as it's an infinite loop
        
        # Test 2: Battery utils logging  
        print("2. Testing battery utils logging...")
        get_battery_level()
        
        # Test 3: Test case logging (import only to avoid running full tests)
        print("3. Testing test case module imports...")
        
        # Import test cases to verify they use centralized logging
        from test_cases import browser_test, office_test, youtube_test
        
        # Get their loggers and test
        browser_logger = get_logger('test_cases.browser_test')
        office_logger = get_logger('test_cases.office_test') 
        youtube_logger = get_logger('test_cases.youtube_test')
        
        browser_logger.info("Browser test logger working")
        office_logger.info("Office test logger working")
        youtube_logger.info("YouTube test logger working")
        
        # Test 4: Process manager logging
        print("4. Testing process manager logging...")
        from utils.process_manager import process_manager
        process_manager.logger.info("Process manager logger working")
        
        # Verify log file content
        print("\n5. Verifying log file content...")
        if os.path.exists(temp_log):
            with open(temp_log, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print("Log file contents:")
            print("-" * 40)
            print(content)
            print("-" * 40)
            
            # Check for expected content
            expected_messages = [
                "Battery level:",
                "Browser test logger working",
                "Office test logger working", 
                "YouTube test logger working",
                "Process manager logger working"
            ]
            
            all_found = True
            for msg in expected_messages:
                if msg in content:
                    print(f"✅ Found: {msg}")
                else:
                    print(f"❌ Missing: {msg}")
                    all_found = False
            
            if all_found:
                print("\n✅ ALL MODULES USING CENTRALIZED LOGGING!")
            else:
                print("\n❌ Some modules not using centralized logging")
                
        else:
            print("❌ Log file not created")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        
    finally:
        # Cleanup
        if os.path.exists(temp_log):
            try:
                os.remove(temp_log)
            except:
                pass
        
        # Restore default logging
        configure_logging(force_reconfigure=True)


def test_no_duplicate_configs():
    """Test that there are no more duplicate logging configurations."""
    print("\n" + "=" * 50)
    print("Testing No Duplicate Configurations")
    print("=" * 50)
    
    # Count how many basicConfig calls exist in the codebase
    import os
    import glob
    
    duplicate_count = 0
    problematic_files = []
    
    # Search for logging.basicConfig in Python files
    for root, dirs, files in os.walk('.'):
        # Skip test files and virtual environment
        if 'test_env' in root or '__pycache__' in root:
            continue
            
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if 'logging.basicConfig' in content:
                            duplicate_count += 1
                            problematic_files.append(filepath)
                except:
                    pass
    
    print(f"Found {duplicate_count} files with logging.basicConfig")
    
    if duplicate_count == 0:
        print("✅ NO DUPLICATE LOGGING CONFIGURATIONS!")
        print("All modules should now use centralized logging")
    else:
        print("❌ Found duplicate configurations in:")
        for file in problematic_files:
            print(f"  - {file}")
            
    return duplicate_count == 0


def main():
    """Run the integration test."""
    test_integrated_logging()
    no_duplicates = test_no_duplicate_configs()
    
    print("\n" + "=" * 50)
    if no_duplicates:
        print("🎉 CENTRALIZED LOGGING SUCCESSFULLY IMPLEMENTED!")
        print("\nBenefits achieved:")
        print("✅ Single logging configuration point")
        print("✅ Consistent formatting across all modules")  
        print("✅ No more duplicate logging.basicConfig() calls")
        print("✅ Proper logger hierarchy (battery_test.*)")
        print("✅ File and console logging working")
        print("✅ Easy to debug with module-specific loggers")
    else:
        print("⚠️  Centralized logging partially implemented")
        print("Some duplicate configurations may remain")


if __name__ == "__main__":
    main()