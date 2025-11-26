from sensor import CarbonMonoxideSensor


def main():
    sensor = CarbonMonoxideSensor(name="co_sensor_1")
    print(sensor.topic)


if __name__ == "__main__":
    main()
