import time
from sensor import EnergyConsumptionSensor


def main():
    sensor = EnergyConsumptionSensor(name="energy_sensor_1")

    sensor.start()
    
    time.sleep(40)
    
    # Pause
    sensor.pause()
    time.sleep(3)
    
    # Resume
    sensor.resume()
    time.sleep(5)
    
    # Stop
    sensor.stop()

    sensor.start()




if __name__ == "__main__":
    main()
