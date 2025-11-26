from abc import ABC, abstractmethod
from threading import Thread, Event
from constants import (
    MAIN_TOPIC,
    MQTT_BROKER_HOST,
    MQTT_BROKER_PORT,
    SECONDS_IN_A_MINUTE,
)
import paho.mqtt.client as mqtt


class Sensor(ABC):
    def __init__(
        self,
        name: str,
        type: str,
        value_range: tuple[float, float] | tuple[int, int],
        messages_per_min: int,
        mqtt_host: str | None = MQTT_BROKER_HOST,
        mqtt_port: str | None = MQTT_BROKER_PORT,
    ) -> None:
        if mqtt_host is None or mqtt_port is None:
            raise ValueError(
                "MQTT host and port must be provided as environment variables."
            )

        self.name: str = name
        self.type: str = type

        self.interval: float = SECONDS_IN_A_MINUTE / messages_per_min
        self.value_range: tuple[float, float] | tuple[int, int] = value_range

        self.topic: str = f"{MAIN_TOPIC}/{self.type}/{self.name}"

        self._stop_event = Event()
        self._pause_event = Event()

        self._pause_event.set()

        self.thread: Thread = Thread(
            target=self._simulation_loop,
            name=f"{self.type}_{self.name}_thread",
            daemon=True,
        )

        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.mqtt_host: str = str(mqtt_host)
        self.mqtt_port: int = int(mqtt_port)

    @abstractmethod
    def _generate_value(self) -> float | int:
        raise NotImplementedError

    def start(self) -> None:
        if not self.thread.is_alive():
            print(f"[{self.name}] Starting...")
            self.thread.start()

    def stop(self) -> None:
        self._stop_event.set()

        self._pause_event.set()
        if self.thread.is_alive():
            print(f"[{self.name}] Stopping...")
            self.thread.join(timeout=1.0)

            self.client.loop_stop()
            self.client.disconnect()

    def pause(self) -> None:
        print(f"[{self.name}] Pausing...")
        self._pause_event.clear()

    def resume(self) -> None:
        print(f"[{self.name}] Resuming...")
        self._pause_event.set()

    def _simulation_loop(self) -> None:
        try:
            self.client.connect(self.mqtt_host, self.mqtt_port, 60)
            self.client.loop_start()
            print(f"[{self.name}] Connected to MQTT and started simulation.")

            while not self._stop_event.is_set():
                is_resumed = self._pause_event.wait(timeout=1.0)

                if not is_resumed:
                    continue

                value = self._generate_value()
                print(f"[{self.name}] Publishing value: {value} to topic: {self.topic}")

                self.client.publish(self.topic, value)

                self._stop_event.wait(self.interval)

        except Exception as e:
            print(f"[{self.name}] Error in simulation loop: {e}")
