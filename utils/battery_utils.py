import psutil
import time
from .logger_config import get_logger

logger = get_logger(__name__)

def get_battery_level():

    battery = psutil.sensors_battery()
    plugged = battery.power_plugged
    percent = str(battery.percent)
    plugged = "Plugged In" if plugged else "Not Plugged In"

    log_string = f'Battery level: {percent}'
    print(log_string)

    logger.info(log_string)
    