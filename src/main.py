import sys
from logging import Logger

from constants import MQTT_BROKER_HOST, MQTT_BROKER_PORT
from logger import get_logger
from utils.setup import (
    generate_sensor_devices,
    is_broker_available,
    start_all_sensors_simulation,
)

logger: Logger = get_logger()


def main():
    logger.info("Initializing Sensors...")

    if not is_broker_available(MQTT_BROKER_HOST, int(MQTT_BROKER_PORT)):
        logger.critical(
            "Critical Error: Unable to reach MQTT Broker at %s:%s.",
            MQTT_BROKER_HOST,
            MQTT_BROKER_PORT,
        )
        logger.info("Please check if your Docker container 'mosquitto' is running")
        sys.exit(1)

    sensors = generate_sensor_devices()

    if not sensors:
        logger.error("No sensors generated. Check INSTANCES_PER_DEVICE_TYPE")
        sys.exit(1)

    try:
        start_all_sensors_simulation(sensors)
    except Exception:
        logger.exception("Failed to start sensor simulations")
        sys.exit(1)

    logger.info("Started %d sensors", len(sensors))

    try:
        while True:
            pass
    except KeyboardInterrupt:
        logger.info("\nStopping all sensors...")
        for sensor in sensors:
            sensor.stop()
        logger.info("Stopped")


if __name__ == "__main__":
    main()
