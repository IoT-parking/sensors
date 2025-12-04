import argparse
import sys
from logging import Logger
from typing import TYPE_CHECKING

from logger import get_logger
from utils.cli import (
    cli_info_handler,
    perform_healthcheck,
    start_simulation,
)
from utils.setup import generate_sensor_devices

if TYPE_CHECKING:
    from sensor import Sensor

logger: Logger = get_logger()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mock", action="store_true", help="Enable mock mode")
    args = parser.parse_args()

    cli_info_handler()
    if args.mock:
        print("NOTE: Application running in MOCK MODE")

    logger.info("Initializing Sensors...")
    sensors: list[Sensor] = generate_sensor_devices()
    logger.info("%d Sensors initialized successfully.", len(sensors))

    while True:
        try:
            command = input("iot-parking> ").strip().lower()

            if command == "start":
                start_simulation(sensors=sensors, mock_mode=args.mock)
            elif command == "healthcheck":
                perform_healthcheck(mock_mode=args.mock)
            elif command == "fire":
                sensor_name = input("Enter sensor name: ").strip()
                value_str = input("Enter value to publish: ").strip()
                try:
                    value = float(value_str)
                except ValueError:
                    print("Invalid value. Please enter a numeric value.")
                    continue

                matched_sensors = [s for s in sensors if s.name == sensor_name]
                if not matched_sensors:
                    print(f"No sensor found with name '{sensor_name}'.")
                    continue

                sensor = matched_sensors[0]
                from utils.setup import fire_single_message

                fire_single_message(sensor, value)
                print(f"Published value {value} to sensor '{sensor_name}'.")
            elif command == "help":
                cli_info_handler()
            elif command == "exit":
                logger.info("Exiting application.")
                sys.exit(0)
            elif command == "":
                continue
            else:
                print(f"Unknown command: '{command}'. Type 'help' for options.")

        except KeyboardInterrupt:
            print("\nUse 'exit' to quit.")


if __name__ == "__main__":
    main()
