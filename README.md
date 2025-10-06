# Laptop Battery Endurance Test

🔋 **Enterprise-Grade Battery Testing Suite** - Simulate realistic office workloads to measure laptop battery performance with comprehensive result tracking and analysis.

This test runs continuous cycles of web browsing, Microsoft Office tasks, and YouTube video playback to provide standardized, reproducible battery performance measurements.

## ✨ **Key Features (Phase 1 Complete)**

- 📊 **Organized Results Storage** - Automatic folder creation with timestamped results
- 🖥️ **Complete System Identification** - CPU, RAM, OS, serial number, and model detection
- ⚡ **Robust Process Management** - Force-kill system prevents hanging applications
- 📈 **Battery Timeline Tracking** - CSV format with minute-precision timestamps
- 🔧 **Smart Error Handling** - Comprehensive recovery from application failures
- 📋 **Automatic Test Summaries** - JSON reports with duration and performance metrics
- 🌐 **Cross-Platform Support** - Enhanced Windows 11 and macOS 12+ compatibility

# Supported OS

- Windows 11 x86 / x64
- Windows 11 ARM 64-bit
- macOS 12 ARM 64-bit

The author has tested this program on several laptops running a wide variety of CPUs, including Intel Core Ultra, Snapdragon X Elite, Apple M-Series

# Required third party software

- Python: to run the script
- A default browser: Edge, Safari, or any default browser of your choice. Edge and Safari are recommended since they are default browser for most Windows and Mac machine
- Microsoft Office: Word, Excel, PowerPoint

# 🎯 Test Workflow

The program runs continuous cycles of realistic office tasks:
1. **Web Browsing** - Opens 5 websites with scrolling and interaction
2. **Office Tasks** - Opens 3 Word files and 1 Excel file with navigation
3. **Video Playback** - YouTube videos for media consumption testing

Each cycle includes mouse movement, scrolling, and realistic user interaction patterns.

## 📊 **Results & Output** 

### Organized Storage Structure
Each test automatically creates a comprehensive results folder:
```
battery_test_results/
└── YYYY-MM-DD_HH-MM-SS_HOSTNAME_testname/
    ├── system_info.json      # Complete hardware specifications
    ├── battery_timeline.csv  # Timestamped battery readings
    ├── summary.json          # Test duration and performance metrics
    └── test_log.log         # Detailed execution logs
```

### System Information Collected
- **Hardware**: CPU model, cores, RAM, serial number, system model
- **Software**: OS version, Python version, architecture
- **Battery**: Design capacity, current status, plugged state
- **Performance**: Test duration, cycles completed, battery drain rate

# ✅ **Pre-Test Setup Checklist**

**Complete this checklist before running any test to ensure consistent and accurate results:**

### Power & Performance Settings
- [ ] Set laptop power mode to **"Balance"** (Windows) or disable **"High Performance Mode"** (macOS)
- [ ] Set screen brightness to **75%** (on macOS: ask Siri "Set screen brightness to 75%")
- [ ] Leave all refresh rate settings at **default configuration**
- [ ] Turn **off** automatic screen turn-off on battery power
- [ ] Set battery saver mode to activate at **30%** (if available)

### Display & Audio Settings  
- [ ] Turn **off** "lower screen brightness on low battery"
- [ ] Disable auto-dim and lock screen when user is away
- [ ] Set volume to **0%** (muted)

### Network & Connectivity
- [ ] Connect laptop to **Wi-Fi network**  
- [ ] Turn **on** Bluetooth

### Battery Preparation
- [ ] Charge laptop battery to **100%**
- [ ] Disconnect charger before starting test (run on battery only)

# How to run

## Installation

1. Install Python https://www.python.org/downloads/
2. Download this code by click on the Code (green button) > Download ZIP, or you can use `git clone` this repo to your machine.
3. Unzip the ZIP file you have just download
4. Open Command Prompt (cmd) and navigate to your extracted folder (e.g: `cd C:\Users\Duyluan\Downloads\laptop_battery_test`)

## Run the program

**Always navigate to project folder first**

### Windows:

Note: You must run the following commands in Command Prompt (CMD), do not run on PowerShell

```cmd
python -m venv battery_test_env
battery_test_env\Scripts\activate.bat
python.exe -m pip install --upgrade pip
pip install -r requirements.txt
python test.py
```

**You only need to do it once, on the first time**. For the following runs, you only need to run these code

```cmd
battery_test_env\Scripts\activate.bat
python test.py
```

### macOS:

Open Terminal and run the following commands

```sh
python3 -m venv battery_test_env
source battery_test_env/bin/activate
pip3 install --upgrade pip
pip3 install -r requirements.txt
python3 test.py
```

**You only need to do it once, on the first time**. For the following runs, you only need to run these code

```sh
source battery_test_env/bin/activate
python3 test.py
```

> [!NOTE]
**Note for Windows ARM**: You may need to install C++ Builds Tools (especially on Windows ARM devices) if the error show when building wheels. Check the error message to see if you need to do so. Download [Visual Studio](https://visualstudio.microsoft.com/downloads/) and install **Desktop Development with C++**, then run the installation commands again.

## 🎬 **Disable YouTube Test**

By default, the script includes YouTube playback testing. To disable YouTube playback:

```sh
# Windows
python test.py 1

# macOS  
python3 test.py 1
```

## 📁 **Project Structure**

```
laptop_battery_endurance_test/
├── test.py                 # Main battery test runner
├── utils/                  # Core system modules
│   ├── battery_utils.py    # Battery monitoring
│   ├── process_manager.py  # Process management
│   ├── logger_config.py    # Centralized logging
│   ├── smart_wait.py       # Intelligent delays
│   └── results_manager.py  # Organized storage
├── test_cases/            # Test modules
│   ├── browser_test.py    # Web browsing simulation
│   ├── office_test.py     # Office applications
│   └── youtube_test.py    # Video playback
├── test_files/           # Test assets
└── battery_test_results/ # Generated results (auto-created)
```

## 🔧 **Advanced Features**

### Robust Process Management
- **Force-kill system** prevents hanging on confirmation dialogs
- **Cross-platform support** (Windows taskkill, macOS pkill)
- **Process tracking** for reliable cleanup between test cycles

### Smart Error Handling
- **Comprehensive try-catch blocks** around all test operations
- **Graceful failure recovery** - continues testing even if components fail
- **Detailed error logging** for troubleshooting

### Intelligent System Monitoring
- **CPU-based smart waiting** replaces hardcoded delays
- **Real-time battery monitoring** with timeline tracking
- **System resource awareness** for optimal test execution

## 📈 **Result Analysis**

After test completion, analyze results from the generated files:

1. **system_info.json** - Hardware specifications and test environment
2. **battery_timeline.csv** - Import into Excel/Google Sheets for graphing
3. **summary.json** - Key metrics including duration and battery drain rate
4. **test_log.log** - Detailed execution log for troubleshooting

## 🐛 **Troubleshooting**

### Common Issues  
- **Applications hang on save dialogs** → ✅ Resolved with force-kill system
- **Inconsistent timing** → ✅ Resolved with smart waiting
- **Lost test results** → ✅ Resolved with organized storage
- **Process cleanup failures** → ✅ Resolved with robust process management

### Getting Help
- Check `test_log.log` in your results folder for detailed error information
- Review `claude.md` for technical implementation details
- Ensure all pre-test checklist items are completed for consistent results