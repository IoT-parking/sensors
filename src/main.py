import argparse
import sys
from logging import Logger

from logger import get_logger
from utils.cli import (
    cli_info_handler,
    perform_healthcheck,
    start_simulation,
)

logger: Logger = get_logger()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mock", action="store_true", help="Enable mock mode")
    args = parser.parse_args()

    cli_info_handler()
    if args.mock:
        print("NOTE: Application running in MOCK MODE")

    while True:
        try:
            command = input("iot-parking> ").strip().lower()

            if command == "start":
                start_simulation(args.mock)
            elif command == "healthcheck":
                perform_healthcheck()
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