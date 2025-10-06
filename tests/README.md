# Tests Directory

This directory contains all verification and test scripts for the battery endurance test system.

## Test Files

### Core System Tests
- **test_organized_storage.py** - Comprehensive test suite for the results storage system
- **test_process_management.py** - Tests for process tracking and cleanup functionality  
- **test_logging_integration.py** - Verification of centralized logging system
- **test_smart_waiting.py** - Tests for intelligent waiting functions

### Legacy/Development Tests
- **test_fixes.py** - General fixes testing
- **test_logging.py** - Basic logging tests
- **quick_test.py** - Quick verification script
- **run_process_tests.py** - Process management test runner

## Usage

Run individual tests:
```bash
python tests/test_organized_storage.py
python tests/test_process_management.py
```

Run all verification tests to ensure system integrity before battery testing.

## Test Coverage

These tests verify:
- ✅ Organized storage creation and structure
- ✅ Process tracking and force-kill functionality  
- ✅ Centralized logging configuration
- ✅ Smart waiting and CPU monitoring
- ✅ System information collection
- ✅ Battery reading integration
- ✅ Error handling and recovery