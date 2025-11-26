from logging import Logger

from constants import INSTANCES_PER_DEVICE_TYPE, MQTT_BROKER_HOST, MQTT_BROKER_PORT
from logger import get_logger
from utils.setup import (
    generate_sensor_devices,
    is_broker_available,
    start_all_sensors_simulation,
)

logger: Logger = get_logger()


def cli_info_handler() -> None:
    print("\n--- IoT-parking Sensor Simulation ---")
    print(f"MQTT Broker Hostname: {MQTT_BROKER_HOST}:{MQTT_BROKER_PORT}")
    print(f"Number of sensor instances per type: {INSTANCES_PER_DEVICE_TYPE}")
    print("-------------------------------------")
    print("Available Commands:")
    print("  start       - Start the sensor simulation (Blocking)")
    print("  healthcheck - Check connectivity to MQTT Broker")
    print("  help        - Show this menu")
    print("  exit        - Quit the application")
    print(" ")


def perform_healthcheck(*, mock_mode: bool) -> bool:
    logger.info("Performing healthcheck...")
    if mock_mode:
        logger.warning("Mock mode enabled: Skipping healthcheck.")
        return True

    if MQTT_BROKER_HOST is None or MQTT_BROKER_PORT is None:
        msg = (
            "MQTT_BROKER_HOST and MQTT_BROKER_PORT must be set as environment variables"
        )
        raise ValueError(msg)

    if is_broker_available(MQTT_BROKER_HOST, int(MQTT_BROKER_PORT)):
        logger.info(
            "Healthcheck PASSED: MQTT Broker is reachable at %s:%s",
            MQTT_BROKER_HOST,
            MQTT_BROKER_PORT,
        )
        return True

    logger.error(
        "Healthcheck FAILED: Unable to reach MQTT Broker at %s:%s",
        MQTT_BROKER_HOST,
        MQTT_BROKER_PORT,
    )
    return False


def start_simulation(*, mock_mode: bool) -> None:
    logger.info("Initializing Sensors...")

    if mock_mode:
        logger.warning("Mock mode enabled: Skipping healthcheck.")
    elif not perform_healthcheck(mock_mode=mock_mode):
        logger.info("Please check if your Docker container 'mosquitto' is running")
        return

    sensors = generate_sensor_devices()

    if not sensors:
        logger.error("No sensors generated. Check INSTANCES_PER_DEVICE_TYPE")
        return

    try:
        start_all_sensors_simulation(sensors, mock_mode=mock_mode)
    except Exception:
        logger.exception("Failed to start sensor simulations")
        return

    logger.info("Started %d sensors. Press Ctrl+C to stop.", len(sensors))

    try:
        while True:
            pass
    except KeyboardInterrupt:
        logger.info("\nStopping all sensors...")
        for sensor in sensors:
            sensor.stop()
        logger.info("Stopped. Returning to menu...")
