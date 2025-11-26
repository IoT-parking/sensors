from .sensor import Sensor
from constants import (
    OCCUPANCY_SENSOR_TYPE,
    OCCUPANCY_VALUES,
    OCCUPANCY_MESSAGES_PER_MIN,
    TEMPERATURE_SENSOR_TYPE,
    TEMPERATURE_VALUES_RANGE,
    TEMPERATURE_MESSAGES_PER_MIN,
    CO_SENSOR_TYPE,
    CO_VALUES_RANGE,
    CO_MESSAGES_PER_MIN,
    ENERGY_SENSOR_TYPE,
    ENERGY_VALUES_RANGE,
    ENERGY_MESSAGES_PER_MIN,
)


class OccupancySensor(Sensor):
    def __init__(self, name: str) -> None:
        super().__init__(
            name=name,
            type=OCCUPANCY_SENSOR_TYPE,
            value_range=OCCUPANCY_VALUES,
            messages_per_min=OCCUPANCY_MESSAGES_PER_MIN,
        )

    def _generate_value(self) -> int:
        pass


class CarbonMonoxideSensor(Sensor):
    def __init__(self, name: str) -> None:
        super().__init__(
            name=name,
            type=CO_SENSOR_TYPE,
            value_range=CO_VALUES_RANGE,
            messages_per_min=CO_MESSAGES_PER_MIN,
        )

    def _generate_value(self) -> int:
        return 2


class TemperatureSensor(Sensor):
    def __init__(self, name: str) -> None:
        super().__init__(
            name=name,
            type=TEMPERATURE_SENSOR_TYPE,
            value_range=TEMPERATURE_VALUES_RANGE,
            messages_per_min=TEMPERATURE_MESSAGES_PER_MIN,
        )

    def _generate_value(self) -> int:
        pass


class EnergyConsumptionSensor(Sensor):
    def __init__(self, name: str) -> None:
        super().__init__(
            name=name,
            type=ENERGY_SENSOR_TYPE,
            value_range=ENERGY_VALUES_RANGE,
            messages_per_min=ENERGY_MESSAGES_PER_MIN,
        )

    def _generate_value(self) -> int:
        return 2
