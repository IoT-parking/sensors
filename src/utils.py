import random
from constants import ANOMALY_CHANCE, LOWER_FACTOR_BOUND, UPPER_FACTOR_BOUND
from logger import get_logger
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

    logger.info("Anomalous (%s) measurement generated: %.2f", "SPIKE UP" if spike_up else "SPIKE DOWN", result_value)

    return round(result_value, 2)