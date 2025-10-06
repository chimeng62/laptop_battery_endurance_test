"""
Centralized Logging Configuration for Battery Test

This module provides a single point of configuration for all logging throughout
the battery testing application. It ensures consistent formatting and prevents
duplicate logging configuration issues.
"""

import logging
import os
from datetime import datetime
from typing import Optional


class BatteryTestLogger:
    """Centralized logging configuration for battery test application."""
    
    _configured = False
    _log_file = None
    _console_level = logging.INFO
    _file_level = logging.INFO
    
    @classmethod
    def configure(cls, 
                  log_file: Optional[str] = None,
                  console_level: int = logging.INFO,
                  file_level: int = logging.INFO,
                  force_reconfigure: bool = False) -> None:
        """
        Configure logging for the entire application.
        
        Args:
            log_file: Path to log file. If None, uses default 'logfilename.log'
            console_level: Logging level for console output
            file_level: Logging level for file output  
            force_reconfigure: Force reconfiguration even if already configured
        """
        if cls._configured and not force_reconfigure:
            return
            
        # Set default log file if not provided
        if log_file is None:
            log_file = 'logfilename.log'
        
        cls._log_file = log_file
        cls._console_level = console_level
        cls._file_level = file_level
        
        # Clear any existing handlers
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        
        # Create formatters
        file_formatter = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)s | %(message)s'
        )
        
        console_formatter = logging.Formatter(
            '%(levelname)s | %(name)s | %(message)s'
        )
        
        # Create file handler
        try:
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(file_level)
            file_handler.setFormatter(file_formatter)
            root_logger.addHandler(file_handler)
        except Exception as e:
            print(f"Warning: Could not create file handler for {log_file}: {e}")
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(console_level)
        console_handler.setFormatter(console_formatter)
        root_logger.addHandler(console_handler)
        
        # Set root logger level to the minimum of console and file levels
        root_logger.setLevel(min(console_level, file_level))
        
        cls._configured = True
        
        # Log configuration success
        config_logger = logging.getLogger('battery_test.config')
        config_logger.info(f"Logging configured - File: {log_file}, Console Level: {logging.getLevelName(console_level)}, File Level: {logging.getLevelName(file_level)}")
    
    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        """
        Get a logger for a specific module or component.
        
        Args:
            name: Logger name (typically __name__ of the calling module)
            
        Returns:
            Configured logger instance
        """
        # Auto-configure if not already done
        if not cls._configured:
            cls.configure()
        
        # Create hierarchical logger name
        if not name.startswith('battery_test.'):
            name = f'battery_test.{name}'
        
        return logging.getLogger(name)
    
    @classmethod
    def is_configured(cls) -> bool:
        """Check if logging has been configured."""
        return cls._configured
    
    @classmethod
    def get_log_file(cls) -> Optional[str]:
        """Get the current log file path."""
        return cls._log_file


# Convenience function for easy import
def get_logger(name: str) -> logging.Logger:
    """
    Get a configured logger for the given name.
    
    Args:
        name: Logger name (use __name__ from calling module)
        
    Returns:
        Configured logger instance
        
    Example:
        from utils.logger_config import get_logger
        logger = get_logger(__name__)
        logger.info("This is a test message")
    """
    return BatteryTestLogger.get_logger(name)


def configure_logging(**kwargs) -> None:
    """
    Configure application logging with custom settings.
    
    Args:
        **kwargs: Arguments passed to BatteryTestLogger.configure()
        
    Example:
        configure_logging(log_file='battery_test_custom.log', console_level=logging.DEBUG)
    """
    BatteryTestLogger.configure(**kwargs)


# Auto-configure with defaults when module is imported
BatteryTestLogger.configure()