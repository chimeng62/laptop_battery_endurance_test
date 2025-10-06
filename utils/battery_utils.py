import psutil
import time
from .logger_config import get_logger

logger = get_logger(__name__)

def get_battery_level():

    battery = psutil.sensors_battery()
    plugged = battery.power_plugged
    percent = battery.percent
    plugged_status = "Plugged In" if plugged else "Not Plugged In"

    log_string = f'Battery level: {percent}% ({plugged_status})'
    print(log_string)

    logger.info(log_string)
    
    # Return battery info for results manager
    return {
        'percentage': percent,
        'is_plugged': plugged,
        'status': plugged_status
    }
    