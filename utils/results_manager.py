"""
Results Manager for Battery Test

This module handles organized storage of battery test results with automatic
system info collection and result calculation.
"""

import os
import json
import csv
import platform
import psutil
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import logging


@dataclass
class SystemInfo:
    """System information for battery test."""
    cpu: str
    cpu_cores: int
    ram_gb: float
    os_name: str
    os_version: str
    architecture: str
    hostname: str
    python_version: str
    battery_present: bool
    battery_design_capacity: Optional[str] = None
    gpu_info: Optional[str] = None
    serial_number: Optional[str] = None
    system_model: Optional[str] = None


@dataclass
class BatteryReading:
    """Single battery level reading."""
    timestamp: str
    battery_percent: int
    plugged: bool
    cycle_number: int
    test_phase: str  # 'browser', 'office', 'youtube'


@dataclass
class TestSummary:
    """Final test results summary."""
    test_id: str
    start_time: str
    end_time: Optional[str]
    duration_hours: Optional[float]
    total_cycles: int
    final_battery_percent: Optional[int]
    average_cycle_time_minutes: Optional[float]
    test_status: str  # 'running', 'completed', 'interrupted'


class ResultsManager:
    """Manages organized storage of battery test results."""
    
    def __init__(self, base_results_dir: str = "battery_test_results"):
        self.base_results_dir = base_results_dir
        self.current_test_dir: Optional[str] = None
        self.test_id: Optional[str] = None
        self.system_info: Optional[SystemInfo] = None
        self.battery_readings: List[BatteryReading] = []
        self.start_time: Optional[datetime] = None
        self.cycle_count = 0
        self.logger = logging.getLogger(__name__)
        
        # Ensure base results directory exists
        os.makedirs(self.base_results_dir, exist_ok=True)
    
    def start_new_test(self, test_name_suffix: str = "") -> str:
        """
        Start a new battery test session.
        
        Args:
            test_name_suffix: Optional suffix for test folder name
            
        Returns:
            Test ID string
        """
        # Generate test ID with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        
        # Add system info to folder name
        hostname = platform.node().replace(' ', '-')
        if test_name_suffix:
            self.test_id = f"{timestamp}_{hostname}_{test_name_suffix}"
        else:
            self.test_id = f"{timestamp}_{hostname}"
        
        # Create test directory
        self.current_test_dir = os.path.join(self.base_results_dir, self.test_id)
        os.makedirs(self.current_test_dir, exist_ok=True)
        
        # Record start time
        self.start_time = datetime.now()
        
        # Collect and save system info
        self.system_info = self._collect_system_info()
        self._save_system_info()
        
        # Initialize test log
        self._setup_test_logging()
        
        # Create empty CSV file with headers
        self._initialize_battery_csv()
        
        self.logger.info(f"Started new battery test: {self.test_id}")
        self.logger.info(f"Results directory: {self.current_test_dir}")
        
        return self.test_id
    
    def record_battery_reading(self, test_id: str, battery_info, test_phase: str = "general") -> None:
        """Record a battery level reading.
        
        Args:
            test_id: Test session ID
            battery_info: Dictionary with 'percentage', 'is_plugged' keys OR individual values
            test_phase: Phase of test (general, browser, office, youtube)
        """
        if not self.test_id:
            raise ValueError("No active test session. Call start_new_test() first.")
        
        # Handle dictionary input from battery_utils.get_battery_level()
        if isinstance(battery_info, dict):
            battery_percent = battery_info.get('percentage', 0)
            plugged = battery_info.get('is_plugged', False)
        else:
            # Handle legacy direct value input
            battery_percent = battery_info
            plugged = False  # Default fallback
        
        # Use shorter timestamp format (YYYY-MM-DDTHH:MM)
        timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M")
        reading = BatteryReading(
            timestamp=timestamp,
            battery_percent=battery_percent,
            plugged=plugged,
            cycle_number=self.cycle_count,
            test_phase=test_phase
        )
        
        self.battery_readings.append(reading)
        self._append_to_battery_csv(reading)
        
        self.logger.info(f"Battery: {battery_percent}% ({'plugged' if plugged else 'unplugged'}) - {test_phase}")
    
    def increment_cycle(self) -> None:
        """Increment the test cycle counter."""
        self.cycle_count += 1
        self.logger.info(f"Completed test cycle {self.cycle_count}")
    
    def finish_test(self, final_battery_percent: Optional[int] = None) -> Dict:
        """
        Finish the current test and generate summary.
        
        Args:
            final_battery_percent: Final battery level when test ended
            
        Returns:
            Test summary dictionary
        """
        if not self.test_id or not self.start_time:
            raise ValueError("No active test session.")
        
        end_time = datetime.now()
        duration = end_time - self.start_time
        
        # Create summary
        summary = TestSummary(
            test_id=self.test_id,
            start_time=self.start_time.strftime("%Y-%m-%dT%H:%M"),
            end_time=end_time.strftime("%Y-%m-%dT%H:%M"),
            duration_hours=round(duration.total_seconds() / 3600, 2),
            total_cycles=self.cycle_count,
            final_battery_percent=final_battery_percent,
            average_cycle_time_minutes=round((duration.total_seconds() / 60) / max(self.cycle_count, 1), 1),
            test_status='completed'
        )
        
        # Save summary
        self._save_summary(summary)
        
        self.logger.info(f"Test completed: {duration} ({duration.total_seconds()/3600:.1f} hours)")
        self.logger.info(f"Total cycles: {self.cycle_count}")
        
        return asdict(summary)
    
    def get_current_test_dir(self) -> Optional[str]:
        """Get the current test directory path."""
        return self.current_test_dir
    
    def _collect_system_info(self) -> SystemInfo:
        """Collect comprehensive system information."""
        # Basic system info
        cpu_info = platform.processor() or "Unknown CPU"
        memory = psutil.virtual_memory()
        
        # Try to get more detailed CPU info on Windows
        try:
            if platform.system() == "Windows":
                result = subprocess.run(
                    ['wmic', 'cpu', 'get', 'name', '/format:value'], 
                    capture_output=True, text=True, shell=True
                )
                for line in result.stdout.split('\n'):
                    if 'Name=' in line:
                        cpu_info = line.split('=')[1].strip()
                        break
        except:
            pass
        
        # Battery info
        battery_present = False
        battery_design_capacity = None
        try:
            battery = psutil.sensors_battery()
            battery_present = battery is not None
            
            # Try to get battery design capacity on Windows
            if battery_present and platform.system() == "Windows":
                try:
                    result = subprocess.run(
                        ['powershell', '-Command', 
                         'Get-WmiObject -Class Win32_Battery | Select-Object DesignCapacity'],
                        capture_output=True, text=True
                    )
                    if result.stdout:
                        lines = result.stdout.strip().split('\n')
                        for line in lines:
                            if line.strip().isdigit():
                                battery_design_capacity = f"{line.strip()} mWh"
                                break
                except:
                    pass
        except:
            pass
        
        # GPU info
        gpu_info = None
        try:
            if platform.system() == "Windows":
                result = subprocess.run(
                    ['wmic', 'path', 'win32_VideoController', 'get', 'name', '/format:value'],
                    capture_output=True, text=True, shell=True
                )
                for line in result.stdout.split('\n'):
                    if 'Name=' in line and line.split('=')[1].strip():
                        gpu_info = line.split('=')[1].strip()
                        break
        except:
            pass
        
        # System serial number and model
        serial_number = None
        system_model = None
        try:
            if platform.system() == "Windows":
                # Get serial number
                result = subprocess.run(
                    ['wmic', 'bios', 'get', 'serialnumber', '/format:value'],
                    capture_output=True, text=True, shell=True
                )
                for line in result.stdout.split('\n'):
                    if 'SerialNumber=' in line and line.split('=')[1].strip():
                        serial_number = line.split('=')[1].strip()
                        break
                
                # Get system model
                result = subprocess.run(
                    ['wmic', 'computersystem', 'get', 'model', '/format:value'],
                    capture_output=True, text=True, shell=True
                )
                for line in result.stdout.split('\n'):
                    if 'Model=' in line and line.split('=')[1].strip():
                        system_model = line.split('=')[1].strip()
                        break
        except:
            pass
        
        return SystemInfo(
            cpu=cpu_info,
            cpu_cores=psutil.cpu_count(logical=False),
            ram_gb=round(memory.total / (1024**3), 1),
            os_name=platform.system(),
            os_version=platform.release(),
            architecture=platform.architecture()[0],
            hostname=platform.node(),
            python_version=platform.python_version(),
            battery_present=battery_present,
            battery_design_capacity=battery_design_capacity,
            gpu_info=gpu_info,
            serial_number=serial_number,
            system_model=system_model
        )
    
    def _save_system_info(self) -> None:
        """Save system information to JSON file."""
        if not self.system_info or not self.current_test_dir:
            return
        
        system_info_path = os.path.join(self.current_test_dir, "system_info.json")
        with open(system_info_path, 'w', encoding='utf-8') as f:
            json.dump(asdict(self.system_info), f, indent=2)
    
    def _setup_test_logging(self) -> None:
        """Setup logging for this specific test."""
        if not self.current_test_dir:
            return
        
        # Import here to avoid circular imports
        from .logger_config import configure_logging
        
        # Configure logging to save to test directory
        test_log_path = os.path.join(self.current_test_dir, "test_log.log")
        configure_logging(log_file=test_log_path, force_reconfigure=True)
        
        self.logger.info("="*60)
        self.logger.info(f"BATTERY TEST SESSION STARTED: {self.test_id}")
        self.logger.info("="*60)
    
    def _initialize_battery_csv(self) -> None:
        """Initialize empty CSV file with headers."""
        if not self.current_test_dir:
            return
        
        csv_path = os.path.join(self.current_test_dir, "battery_timeline.csv")
        
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'timestamp', 'battery_percent', 'plugged', 'cycle_number', 'test_phase'
            ])
            writer.writeheader()
    
    def _append_to_battery_csv(self, reading: BatteryReading) -> None:
        """Append battery reading to CSV file."""
        if not self.current_test_dir:
            return
        
        csv_path = os.path.join(self.current_test_dir, "battery_timeline.csv")
        
        with open(csv_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'timestamp', 'battery_percent', 'plugged', 'cycle_number', 'test_phase'
            ])
            
            writer.writerow(asdict(reading))
    
    def _save_summary(self, summary: TestSummary) -> None:
        """Save test summary to JSON file."""
        if not self.current_test_dir:
            return
        
        summary_path = os.path.join(self.current_test_dir, "summary.json")
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(asdict(summary), f, indent=2)


# Global results manager instance
results_manager = ResultsManager()