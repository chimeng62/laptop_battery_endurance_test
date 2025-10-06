"""
Process Management Utility for Battery Test

This module handles reliable process tracking and termination to prevent
hanging on confirmation dialogs during battery testing.
"""

import psutil
import subprocess
import time
import platform
import logging
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class TrackedProcess:
    """Represents a process opened by the battery test."""
    pid: int
    name: str
    command: str
    start_time: float


class ProcessManager:
    """Manages processes opened during battery testing with reliable cleanup."""
    
    def __init__(self):
        self.tracked_processes: Dict[int, TrackedProcess] = {}
        self.platform = platform.system()
        self.logger = logging.getLogger(__name__)
        
    def track_process_by_pid(self, pid: int, name: str = "", command: str = "") -> bool:
        """
        Start tracking a process by its PID.
        
        Args:
            pid: Process ID to track
            name: Human-readable name for the process
            command: Command used to start the process
            
        Returns:
            bool: True if process exists and is now tracked
        """
        try:
            # Verify process exists
            process = psutil.Process(pid)
            
            tracked_proc = TrackedProcess(
                pid=pid,
                name=name or process.name(),
                command=command,
                start_time=time.time()
            )
            
            self.tracked_processes[pid] = tracked_proc
            self.logger.info(f"Now tracking process: {tracked_proc.name} (PID: {pid})")
            return True
            
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            self.logger.error(f"Cannot track process {pid}: {e}")
            return False
    
    def find_and_track_processes(self, process_names: List[str]) -> List[int]:
        """
        Find running processes by name and start tracking them.
        
        Args:
            process_names: List of process names to find and track
            
        Returns:
            List of PIDs that were found and are now being tracked
        """
        found_pids = []
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                proc_name = proc.info['name'].lower()
                
                for target_name in process_names:
                    if target_name.lower() in proc_name:
                        pid = proc.info['pid']
                        if self.track_process_by_pid(pid, proc.info['name'], str(proc.info['cmdline'])):
                            found_pids.append(pid)
                        
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
                
        return found_pids
    
    def launch_and_track(self, command: List[str], name: str = "") -> Optional[int]:
        """
        Launch a process and immediately start tracking it.
        
        Args:
            command: Command to execute as a list (e.g., ['notepad.exe', 'file.txt'])
            name: Human-readable name for the process
            
        Returns:
            PID of launched process if successful, None otherwise
        """
        try:
            process = subprocess.Popen(command)
            pid = process.pid
            
            if self.track_process_by_pid(pid, name or command[0], ' '.join(command)):
                return pid
            else:
                # If tracking failed, try to kill the process we just started
                try:
                    process.terminate()
                except:
                    pass
                return None
                
        except Exception as e:
            self.logger.error(f"Failed to launch process {command}: {e}")
            return None
    
    def terminate_process(self, pid: int, force_kill: bool = False, timeout: float = 5.0) -> bool:
        """
        Terminate a specific tracked process.
        
        Args:
            pid: Process ID to terminate
            force_kill: If True, use kill() instead of terminate()
            timeout: Time to wait before force killing if terminate() fails
            
        Returns:
            bool: True if process was terminated successfully
        """
        if pid not in self.tracked_processes:
            self.logger.warning(f"Process {pid} is not being tracked")
            return False
            
        try:
            process = psutil.Process(pid)
            tracked = self.tracked_processes[pid]
            
            if force_kill:
                process.kill()
                self.logger.info(f"Force killed process: {tracked.name} (PID: {pid})")
            else:
                # Try graceful termination first
                process.terminate()
                
                # Wait for process to terminate
                try:
                    process.wait(timeout=timeout)
                    self.logger.info(f"Gracefully terminated process: {tracked.name} (PID: {pid})")
                except psutil.TimeoutExpired:
                    # Force kill if graceful termination failed
                    process.kill()
                    self.logger.info(f"Force killed process after timeout: {tracked.name} (PID: {pid})")
            
            # Remove from tracking
            del self.tracked_processes[pid]
            return True
            
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            self.logger.error(f"Cannot terminate process {pid}: {e}")
            # Remove from tracking anyway since process doesn't exist
            if pid in self.tracked_processes:
                del self.tracked_processes[pid]
            return False
    
    def terminate_by_name(self, process_names: List[str], force_kill: bool = False) -> int:
        """
        Terminate all processes matching the given names.
        
        Args:
            process_names: List of process names to terminate
            force_kill: If True, use kill() instead of terminate()
            
        Returns:
            int: Number of processes successfully terminated
        """
        terminated_count = 0
        
        if self.platform == "Windows":
            # Use taskkill on Windows for reliability
            for name in process_names:
                try:
                    cmd = ['taskkill', '/f' if force_kill else '/t', '/im', name]
                    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
                    if result.returncode == 0:
                        terminated_count += 1
                        self.logger.info(f"Terminated {name} using taskkill")
                    else:
                        self.logger.warning(f"taskkill failed for {name}: {result.stderr}")
                except Exception as e:
                    self.logger.error(f"Failed to terminate {name} using taskkill: {e}")
        else:
            # Use pkill on macOS/Linux
            for name in process_names:
                try:
                    signal_flag = '-KILL' if force_kill else '-TERM'
                    cmd = ['pkill', signal_flag, '-f', name]
                    result = subprocess.run(cmd, capture_output=True, text=True)
                    if result.returncode == 0:
                        terminated_count += 1
                        self.logger.info(f"Terminated {name} using pkill")
                    else:
                        self.logger.warning(f"pkill failed for {name}: {result.stderr}")
                except Exception as e:
                    self.logger.error(f"Failed to terminate {name} using pkill: {e}")
        
        return terminated_count
    
    def cleanup_all_tracked(self, force_kill: bool = False, timeout: float = 5.0) -> int:
        """
        Terminate all tracked processes.
        
        Args:
            force_kill: If True, use kill() instead of terminate()
            timeout: Time to wait before force killing each process
            
        Returns:
            int: Number of processes successfully terminated
        """
        pids_to_terminate = list(self.tracked_processes.keys())
        terminated_count = 0
        
        for pid in pids_to_terminate:
            if self.terminate_process(pid, force_kill, timeout):
                terminated_count += 1
                
        return terminated_count
    
    def cleanup_common_test_processes(self, force_kill: bool = True) -> int:
        """
        Terminate common processes that might be left running from battery tests.
        This is a safety net for processes that weren't properly tracked.
        
        Args:
            force_kill: If True, use force termination
            
        Returns:
            int: Number of processes terminated
        """
        # Common browser and office processes that battery tests might open
        common_processes = [
            # Browsers
            'msedge.exe', 'chrome.exe', 'firefox.exe', 'safari',
            # Office
            'winword.exe', 'excel.exe', 'powerpnt.exe',
            # Media
            'vlc.exe', 'wmplayer.exe'
        ]
        
        return self.terminate_by_name(common_processes, force_kill)
    
    def get_tracked_processes_info(self) -> List[Dict]:
        """Get information about all tracked processes."""
        info_list = []
        
        for pid, tracked in self.tracked_processes.items():
            try:
                process = psutil.Process(pid)
                info = {
                    'pid': pid,
                    'name': tracked.name,
                    'status': process.status(),
                    'cpu_percent': process.cpu_percent(),
                    'memory_mb': process.memory_info().rss / 1024 / 1024,
                    'runtime_seconds': time.time() - tracked.start_time,
                    'command': tracked.command
                }
                info_list.append(info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                # Process no longer exists, remove from tracking
                del self.tracked_processes[pid]
                
        return info_list
    
    def is_process_running(self, pid: int) -> bool:
        """Check if a tracked process is still running."""
        if pid not in self.tracked_processes:
            return False
            
        try:
            process = psutil.Process(pid)
            return process.is_running()
        except psutil.NoSuchProcess:
            # Remove from tracking if process no longer exists
            del self.tracked_processes[pid]
            return False


# Global process manager instance for easy access
process_manager = ProcessManager()