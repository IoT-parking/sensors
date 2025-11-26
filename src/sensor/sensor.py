from __future__ import annotations

from abc import ABC, abstractmethod
from threading import Event, Thread
from typing import TYPE_CHECKING

import paho.mqtt.client as mqtt

from constants import (
    MAIN_TOPIC,
    MQTT_BROKER_HOST,
    MQTT_BROKER_PORT,
    SECONDS_IN_A_MINUTE,
)
from logger import get_logger

if TYPE_CHECKING:
    from logging import Logger

logger: Logger = get_logger()


class Sensor(ABC):
    def __init__(
        self,
        name: str,
        device_type: str,
        value_range: tuple[float, float] | tuple[int, int],
        messages_per_min: int,
    ) -> None:
        if MQTT_BROKER_HOST is None or MQTT_BROKER_PORT is None:
            msg = "MQTT_BROKER_HOST and MQTT_BROKER_PORT must be set as environment variables"
            raise ValueError(msg)

        self.name: str = name
        self.device_type: str = device_type
        self.messages_sent: int = 0

        self._interval: float = SECONDS_IN_A_MINUTE / messages_per_min
        self._value_range: tuple[float, float] | tuple[int, int] = value_range

        self.topic: str = f"{MAIN_TOPIC}/{self.device_type}/{self.name}"
        self._thread_name: str = f"{self.name}_thread"

        self._stop_event: Event = Event()
        self._pause_event: Event = Event()

        self._pause_event.set()

        self._thread: Thread = Thread(
            target=self._simulation_loop,
            name=self._thread_name,
            daemon=True,
        )

        self._client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self._mqtt_host: str = str(MQTT_BROKER_HOST)
        self._mqtt_port: int = int(MQTT_BROKER_PORT)

    @property
    def status_label(self) -> str:
        if not self._thread.is_alive():
            return "STOPPED"
        if not self._pause_event.is_set():
            return "PAUSED"
        return "RUNNING"

    @abstractmethod
    def _generate_value(self) -> float | int:
        raise NotImplementedError

    def start(self) -> None:
        if self._thread.is_alive():
            logger.warning("Sensor is already running.")
            return

        self.messages_sent = 0
        self._stop_event.clear()
        self._pause_event.set()

        self._thread = Thread(
            target=self._simulation_loop,
            name=self._thread_name,
            daemon=True,
        )

        self._thread.start()
        logger.info("Sensor started.")

    def stop(self) -> None:
        self._stop_event.set()

        self._pause_event.set()
        if self._thread.is_alive():
            logger.debug("Stopping...")
            self._thread.join(timeout=1.0)

            self._client.loop_stop()
            self._client.disconnect()
            logger.info("Sensor stopped.")

    def pause(self) -> None:
        logger.debug("Pausing...")
        self._pause_event.clear()
        logger.info("Sensor paused.")

    def resume(self) -> None:
        logger.debug("Resuming...")
        self._pause_event.set()
        logger.info("Sensor resumed.")

    def _simulation_loop(self) -> None:
        try:
            logger.debug(
                "Connecting to MQTT broker at %s:%s", self._mqtt_host, self._mqtt_port
            )
            self._client.connect(self._mqtt_host, self._mqtt_port, 60)
            self._client.loop_start()
            logger.info("Connected to MQTT and started simulation.")
        except Exception as e:
            logger.warning("Could not connect to MQTT broker: %s", e)
            self._stop_event.set()
            return

        while not self._stop_event.is_set():
            try:
                is_resumed = self._pause_event.wait(timeout=1.0)

                if not is_resumed:
                    logger.debug("Simulation loop is paused.")
                    continue

                value = self._generate_value()

                self._client.publish(self.topic, value)

                self._stop_event.wait(self._interval)
            except Exception as e:
                logger.warning("Error occured in simulation loop: %s", e)
            else:
                self.messages_sent += 1
                logger.debug("Published value: %s to topic: %s", value, self.topic)

    def _mock_local_simulation(self) -> None:
        while not self._stop_event.is_set():
            try:
                is_resumed = self._pause_event.wait(timeout=1.0)

                if not is_resumed:
                    continue

                value = self._generate_value()
                logger.debug("Generated value %s", value)

                self._stop_event.wait(self._interval)
            except Exception as e:
                logger.warning("Error occured in simulation loop: %s", e)
            else:
                self.messages_sent += 1
                logger.debug("Generated value: %s", value)
