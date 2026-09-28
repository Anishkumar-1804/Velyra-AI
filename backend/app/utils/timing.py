import time
from contextlib import contextmanager
import logging

logger = logging.getLogger("angiyam.timing")


@contextmanager
def timed_block(name: str):
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        logger.info(f"[{name}] took {elapsed * 1000:.1f}ms")
