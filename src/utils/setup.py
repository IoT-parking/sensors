from constants import INSTANCES_PER_DEVICE_TYPE
from sensor import (
    CarbonMonoxideSensor,
    EnergyConsumptionSensor,
    OccupancySensor,
    Sensor,
    TemperatureSensor,
)


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
