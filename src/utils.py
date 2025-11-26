from __future__ import annotations

import random
from typing import TYPE_CHECKING

from constants import (
    ANOMALY_CHANCE,
    INSTANCES_PER_DEVICE_TYPE,
    LOWER_FACTOR_BOUND,
    UPPER_FACTOR_BOUND,
)
from logger import get_logger
from sensor import (
    CarbonMonoxideSensor,
    EnergyConsumptionSensor,
    OccupancySensor,
    Sensor,
    TemperatureSensor,
)

if TYPE_CHECKING:
    from logging import Logger

logger: Logger = get_logger()


def calculate_measurement(min_value: float, max_value: float) -> float:
    """
    Note:
        There is a 10% chance to generate an anomalous measurement outside the normal range.
        There is equal chance for anomaly to be above max_value or below min_value.

    """
    if random.random() > ANOMALY_CHANCE:
        normal_value: float = random.uniform(min_value, max_value)
        return round(normal_value, 2)

    spike_up: bool = random.choice([True, False])
    factor: float = random.uniform(LOWER_FACTOR_BOUND, UPPER_FACTOR_BOUND)

    if spike_up:
        result_value: float = max_value * factor
    else:
        result_value: float = max(0, min_value / factor)

    logger.info(
        "Anomalous (%s) measurement generated: %.2f",
        "SPIKE UP" if spike_up else "SPIKE DOWN",
        result_value,
    )

    return round(result_value, 2)


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


def start_all_sensors_simulation(sensors: list[Sensor]) -> None:
    for sensor in sensors:
        sensor.start()
