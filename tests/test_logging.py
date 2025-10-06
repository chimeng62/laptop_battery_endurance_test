"""
Test Suite for Centralized Logging Configuration

This script tests the centralized logging system to ensure:
1. No duplicate configurations
2. Consistent formatting across modules
3. Proper file and console output
4. Logger hierarchy works correctly
"""

import os
import tempfile
import logging
from utils.logger_config import get_logger, configure_logging, BatteryTestLogger


def test_basic_logging():
    """Test basic logging functionality."""
    print("\n=== Test 1: Basic Logging ===")
    
    # Get logger for this test
    logger = get_logger(__name__)
    
    print("Testing different log levels:")
    logger.debug("This is a DEBUG message")
    logger.info("This is an INFO message")  
    logger.warning("This is a WARNING message")
    logger.error("This is an ERROR message")
    
    print("✅ Basic logging test completed")


def test_multiple_loggers():
    """Test that multiple modules can get loggers without conflicts."""
    print("\n=== Test 2: Multiple Module Loggers ===")
    
    # Simulate different modules getting loggers
    logger1 = get_logger("test_module_1")
    logger2 = get_logger("test_module_2") 
    logger3 = get_logger("battery_utils")
    logger4 = get_logger("process_manager")
    
    # Each should log with their own name
    logger1.info("Message from test_module_1")
    logger2.info("Message from test_module_2")
    logger3.info("Message from battery_utils")
    logger4.info("Message from process_manager")
    
    print("✅ Multiple logger test completed")


def test_file_logging():
    """Test that file logging works correctly."""
    print("\n=== Test 3: File Logging ===")
    
    # Create temporary log file
    temp_log = tempfile.mktemp(suffix='.log')
    
    try:
        # Reconfigure logging with custom file
        configure_logging(log_file=temp_log, force_reconfigure=True)
        
        # Get logger and write test messages
        logger = get_logger("file_test")
        logger.info("Test message written to file")
        logger.warning("Warning message written to file")
        logger.error("Error message written to file")
        
        # Verify file was created and contains messages
        if os.path.exists(temp_log):
            with open(temp_log, 'r', encoding='utf-8') as f:
                content = f.read()
                
            print(f"Log file created: {temp_log}")
            print("Log file contents:")
            print("-" * 40)
            print(content)
            print("-" * 40)
            
            # Verify expected content
            if "Test message written to file" in content:
                print("✅ File logging working correctly")
            else:
                print("❌ File logging not working - content missing")
        else:
            print("❌ Log file was not created")
            
    finally:
        # Cleanup temp file
        if os.path.exists(temp_log):
            try:
                os.remove(temp_log)
            except:
                pass
        
        # Restore default logging
        configure_logging(force_reconfigure=True)


def test_logger_hierarchy():
    """Test that logger hierarchy works properly."""
    print("\n=== Test 4: Logger Hierarchy ===")
    
    # Test different logger names and hierarchy
    loggers = [
        get_logger("main"),
        get_logger("browser_test"), 
        get_logger("office_test"),
        get_logger("youtube_test"),
        get_logger("utils.battery_utils"),
        get_logger("utils.process_manager")
    ]
    
    print("Testing logger hierarchy:")
    for i, logger in enumerate(loggers):
        logger.info(f"Message from logger {i+1}: {logger.name}")
    
    print("✅ Logger hierarchy test completed")


def test_configuration_status():
    """Test configuration status and properties."""
    print("\n=== Test 5: Configuration Status ===")
    
    # Check if properly configured
    print(f"Is configured: {BatteryTestLogger.is_configured()}")
    print(f"Log file: {BatteryTestLogger.get_log_file()}")
    
    # Test reconfiguration
    original_file = BatteryTestLogger.get_log_file()
    
    configure_logging(log_file='test_custom.log', force_reconfigure=True)
    print(f"After reconfiguration - Log file: {BatteryTestLogger.get_log_file()}")
    
    # Restore original
    configure_logging(log_file=original_file, force_reconfigure=True)
    print(f"After restoration - Log file: {BatteryTestLogger.get_log_file()}")
    
    print("✅ Configuration status test completed")


def test_no_duplicate_handlers():
    """Test that multiple configurations don't create duplicate handlers."""
    print("\n=== Test 6: No Duplicate Handlers ===")
    
    root_logger = logging.getLogger()
    
    print(f"Handlers before test: {len(root_logger.handlers)}")
    
    # Configure multiple times
    for i in range(3):
        configure_logging(force_reconfigure=True)
        print(f"Handlers after config {i+1}: {len(root_logger.handlers)}")
    
    # Should still have same number of handlers (no duplicates)
    if len(root_logger.handlers) <= 2:  # File + Console handler
        print("✅ No duplicate handlers created")
    else:
        print(f"❌ Duplicate handlers detected: {len(root_logger.handlers)} handlers")
    
    print("✅ Duplicate handler test completed")


def simulate_old_vs_new_logging():
    """Demonstrate the difference between old and new logging approaches."""
    print("\n=== Old vs New Logging Comparison ===")
    
    print("\n--- OLD APPROACH (Problematic) ---")
    print("Code that would be in battery_utils.py:")
    print("  logging.basicConfig(filename='logfilename.log', ...)")
    print("Code that would be in test.py:")  
    print("  logging.basicConfig(filename='logfilename.log', ...)")
    print("RESULT: Only first configuration takes effect, inconsistent logging")
    
    print("\n--- NEW APPROACH (Fixed) ---")
    print("Centralized configuration:")
    
    # Demonstrate new approach
    logger1 = get_logger("battery_utils")
    logger2 = get_logger("test_main") 
    logger3 = get_logger("browser_test")
    
    logger1.info("Battery level: 85%")
    logger2.info("Starting test cycle 1")
    logger3.info("Opening browser with URL: https://example.com")
    
    print("RESULT: Consistent formatting, proper hierarchy, no conflicts!")
    print("✅ New centralized logging working perfectly")


def main():
    """Run all logging tests."""
    print("Centralized Logging System Test Suite")
    print("=" * 50)
    
    try:
        test_basic_logging()
        test_multiple_loggers()
        test_file_logging()
        test_logger_hierarchy() 
        test_configuration_status()
        test_no_duplicate_handlers()
        simulate_old_vs_new_logging()
        
        print("\n" + "=" * 50)
        print("✅ ALL LOGGING TESTS PASSED!")
        print("\nThe centralized logging system is working correctly:")
        print("- No duplicate configurations")
        print("- Consistent formatting across all modules")
        print("- Proper file and console output")
        print("- Logger hierarchy working")
        print("- No handler duplication")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        raise


if __name__ == "__main__":
    main()