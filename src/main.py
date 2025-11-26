import sys
from logging import Logger

from logger import get_logger
from utils.dashboard import run_dashboard
from utils.setup import generate_sensor_devices, start_all_sensors_simulation

logger: Logger = get_logger()


def main():
    logger.info("Initializing Sensors...")

    sensors = generate_sensor_devices()

    if not sensors:
        logger.error("No sensors generated. Check INSTANCES_PER_DEVICE_TYPE")
        sys.exit(1)

    start_all_sensors_simulation(sensors)
    logger.info(f"Started {len(sensors)} sensors")

    try:
        run_dashboard(sensors)
    except KeyboardInterrupt:
        pass
    finally:
        logger.info("\nStopping all sensors...")
        for sensor in sensors:
            sensor.stop()
        logger.info("Stopped")


if __name__ == "__main__":
    main()
