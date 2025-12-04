import socket
from logging import Logger

from constants import INSTANCES_PER_DEVICE_TYPE
from logger import get_logger
from sensor import (
    CarbonMonoxideSensor,
    EnergyConsumptionSensor,
    OccupancySensor,
    Sensor,
    TemperatureSensor,
)

logger: Logger = get_logger()


def generate_sensor_devices() -> list[Sensor]:
    sensors: list[Sensor] = []

    for i in range(INSTANCES_PER_DEVICE_TYPE):
        occupancy_sensor = OccupancySensor(name=f"occ_sensor_{i + 1}")
        sensors.append(occupancy_sensor)

        co_sensor = CarbonMonoxideSensor(name=f"co_sensor_{i + 1}")
        sensors.append(co_sensor)

        temperature_sensor = TemperatureSensor(name=f"temp_sensor_{i + 1}")
        sensors.append(temperature_sensor)

        energy_sensor = EnergyConsumptionSensor(name=f"energy_sensor_{i + 1}")
        sensors.append(energy_sensor)

    return sensors


def start_all_sensors_simulation(
    sensors: list[Sensor], *, mock_mode: bool = False
) -> None:
    for sensor in sensors:
        sensor.start(mock_mode=mock_mode)


def is_broker_available(host: str, port: int, timeout: int = 3) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False


def fire_single_message(sensor: Sensor, value: float) -> None:
    sensor._client.publish(sensor.topic, value)
