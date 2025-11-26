from __future__ import annotations

import random

from constants import (
    CO_MESSAGES_PER_MIN,
    CO_SENSOR_TYPE,
    CO_VALUES_RANGE,
    ENERGY_MESSAGES_PER_MIN,
    ENERGY_SENSOR_TYPE,
    ENERGY_VALUES_RANGE,
    OCCUPANCY_MESSAGES_PER_MIN,
    OCCUPANCY_SENSOR_TYPE,
    OCCUPANCY_VALUES,
    TEMPERATURE_MESSAGES_PER_MIN,
    TEMPERATURE_SENSOR_TYPE,
    TEMPERATURE_VALUES_RANGE,
)
from utils.measurement import calculate_measurement

from .sensor import Sensor


class OccupancySensor(Sensor):
    def __init__(self, name: str) -> None:
        super().__init__(
            name=name,
            device_type=OCCUPANCY_SENSOR_TYPE,
            value_range=OCCUPANCY_VALUES,
            messages_per_min=OCCUPANCY_MESSAGES_PER_MIN,
        )

    def _generate_value(self) -> int:
        min_value, max_value = self._value_range
        return random.randint(min_value, max_value)


class CarbonMonoxideSensor(Sensor):
    def __init__(self, name: str) -> None:
        super().__init__(
            name=name,
            device_type=CO_SENSOR_TYPE,
            value_range=CO_VALUES_RANGE,
            messages_per_min=CO_MESSAGES_PER_MIN,
        )

    def _generate_value(self) -> float:
        min_value, max_value = self._value_range
        return calculate_measurement(min_value=min_value, max_value=max_value)


class TemperatureSensor(Sensor):
    def __init__(self, name: str) -> None:
        super().__init__(
            name=name,
            device_type=TEMPERATURE_SENSOR_TYPE,
            value_range=TEMPERATURE_VALUES_RANGE,
            messages_per_min=TEMPERATURE_MESSAGES_PER_MIN,
        )

    def _generate_value(self) -> float:
        min_value, max_value = self._value_range
        return calculate_measurement(min_value=min_value, max_value=max_value)


class EnergyConsumptionSensor(Sensor):
    def __init__(self, name: str) -> None:
        super().__init__(
            name=name,
            device_type=ENERGY_SENSOR_TYPE,
            value_range=ENERGY_VALUES_RANGE,
            messages_per_min=ENERGY_MESSAGES_PER_MIN,
        )

    def _generate_value(self) -> float:
        min_value, max_value = self._value_range
        return calculate_measurement(min_value=min_value, max_value=max_value)
