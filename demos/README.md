# Demos Directory

This directory contains demonstration scripts that showcase the battery test system functionality.

## Demo Files

### System Demonstrations
- **demo_organized_storage.py** - Complete demonstration of the organized storage system
- **demo_process_management.py** - Shows process tracking and cleanup in action
- **demo_centralized_logging.py** - Demonstrates the hierarchical logging system

## Usage

Run any demo to see the system in action:
```bash
python demos/demo_organized_storage.py
python demos/demo_process_management.py
python demos/demo_centralized_logging.py
```

## What Demos Show

### Organized Storage Demo
- Creates sample test session with organized folder structure
- Demonstrates system info collection (CPU, RAM, serial number, model)
- Shows battery timeline CSV creation with timestamps
- Generates test summary with metrics calculation

### Process Management Demo
- Launches and tracks test applications
- Demonstrates force-kill capabilities across platforms
- Shows cleanup of all tracked processes

### Logging Demo
- Shows centralized logger configuration
- Demonstrates hierarchical logger naming
- Tests file and console logging integration

## Demo Safety

All demos are designed to be:
- ✅ **Safe to run** - No destructive operations
- ✅ **Quick execution** - Complete in under 1 minute
- ✅ **Self-contained** - Create temporary files only
- ✅ **Informative** - Clear output showing system functionality