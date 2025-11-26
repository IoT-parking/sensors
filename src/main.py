from typing import TYPE_CHECKING

from utils.setup import generate_sensor_devices, start_all_sensors_simulation

if TYPE_CHECKING:
    from sensor import Sensor


def main():
    all_sensors: list[Sensor] = generate_sensor_devices()
    start_all_sensors_simulation(all_sensors)




if __name__ == "__main__":
    main()
