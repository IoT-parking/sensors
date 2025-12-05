from __future__ import annotations

import datetime
import logging
import os
from pathlib import Path

from dotenv import load_dotenv

ROOT_PROJECT_PATH: Path = Path(__file__).parent.parent

GLOBAL_LOGGER_NAME: str = "global_logger"

LOGGER_DEFAULT_LEVEL: int = logging.DEBUG

LOGS_DIRPATH: Path = ROOT_PROJECT_PATH / "logs"

DEFAULT_TIMEZONE: datetime.tzinfo = datetime.UTC


load_dotenv(ROOT_PROJECT_PATH / ".env")

MQTT_BROKER_HOST: str | None = os.getenv("MQTT_BROKER_HOST")
MQTT_BROKER_PORT: str | None = os.getenv("MQTT_BROKER_PORT")

INSTANCES_PER_DEVICE_TYPE: int = 4

SECONDS_IN_A_MINUTE: int = 60

ANOMALY_CHANCE: float = 0.1

UPPER_FACTOR_BOUND: float = 1.8
LOWER_FACTOR_BOUND: float = 1.2

MAIN_TOPIC: str = "parking/sensor"

OCCUPANCY_SENSOR_TYPE: str = "occupancy"
OCCUPANCY_VALUES: tuple[int, int] = (0, 1)
OCCUPANCY_MESSAGES_PER_MIN: int = 12

CO_SENSOR_TYPE: str = "carbon_monoxide"
CO_VALUES_RANGE: tuple[float, float] = (10, 150)
CO_MESSAGES_PER_MIN: int = 10

TEMPERATURE_SENSOR_TYPE: str = "temperature"
TEMPERATURE_VALUES_RANGE: tuple[float, float] = (12.0, 28.0)
TEMPERATURE_MESSAGES_PER_MIN: int = 6

ENERGY_SENSOR_TYPE: str = "energy_consumption"
ENERGY_VALUES_RANGE: tuple[float, float] = (3.0, 22.0)
ENERGY_MESSAGES_PER_MIN: int = 8
