"""Utility helpers."""

import random
import time

from .config import MIN_DELAY, MAX_DELAY


def sleep_random(min_sec: float = MIN_DELAY, max_sec: float = MAX_DELAY) -> None:
    """Sleep for a random duration to mimic human behavior."""
    time.sleep(random.uniform(min_sec, max_sec))
