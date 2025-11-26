import datetime
import logging
from pathlib import Path
from dotenv import load_dotenv
import os

ROOT_PROJECT_PATH: Path = Path(__file__).parent.parent

GLOBAL_LOGGER_NAME: str = "global_logger"

LOGGER_DEFAULT_LEVEL: int = logging.DEBUG

LOGS_DIRPATH: Path = ROOT_PROJECT_PATH / "logs"

DEFAULT_TIMEZONE: datetime.tzinfo = datetime.UTC 


load_dotenv(ROOT_PROJECT_PATH / ".env")

MQTT_BROKER_HOST: str | None = str(os.getenv("MQTT_BROKER_HOST"))
MQTT_BROKER_PORT: str | None = str(os.getenv("MQTT_BROKER_PORT"))

INSTANCES_PER_DEVICE_TYPE: int = 4

SECONDS_IN_A_MINUTE: int = 60

MAIN_TOPIC: str = "parking/sensor"

OCCUPANCY_SENSOR_TYPE: str = "occupancy"
OCCUPANCY_VALUES: tuple[int, int] = (0, 1)
OCCUPANCY_MESSAGES_PER_MIN: int = 12

CO_SENSOR_TYPE: str = "carbon_monoxide"
CO_VALUES_RANGE: tuple[int, int] = (10, 150)
CO_MESSAGES_PER_MIN: int = 10

TEMPERATURE_SENSOR_TYPE: str = "temperature"
TEMPERATURE_VALUES_RANGE: tuple[float, float] = (12.0, 28.0)
TEMPERATURE_MESSAGES_PER_MIN: int = 6

ENERGY_SENSOR_TYPE: str = "energy_consumption"
ENERGY_VALUES_RANGE: tuple[float, float] = (0.0, 22.0)
ENERGY_MESSAGES_PER_MIN: int = 60