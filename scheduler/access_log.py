import os
import time
from os import environ
from storage import copy_file
from logger import get_logger

logger = get_logger('access_log')

ENVOY_ACCESS_LOG_PATH = environ.get('ENVOY_ACCESS_LOG_PATH')
# Must be greater than envoy's --file-flush-interval-msec (see server/supervisord.conf)
FLUSH_WAIT_SECONDS = float(environ.get('ENVOY_ACCESS_LOG_FLUSH_WAIT_SECONDS', '1'))

class AccessLog:
    """
    Envoy's raw access log file, shared with the scheduler through a volume.
    Envoy appends to it, so it can be copied and truncated between scenario groups while no requests are in flight.
    """

    def __init__(self, path=ENVOY_ACCESS_LOG_PATH):
        self._path = path
        if not self._path:
            logger.info('ENVOY_ACCESS_LOG_PATH not set, envoy access logs will not be collected')

    def reset(self):
        """Discards what envoy logged before the test started (e.g. warm up requests or previous tests)."""
        if self._is_available():
            self._wait_for_flush()
            os.truncate(self._path, 0)

    def collect(self, destination):
        """Copies the requests logged since the last reset/collect to destination and starts a new log."""
        if self._is_available():
            self._wait_for_flush()
            copy_file(self._path, destination)
            os.truncate(self._path, 0)

    def _is_available(self):
        if not self._path:
            return False
        if not os.path.exists(self._path):
            logger.warning(f'Envoy access log {self._path} not found, skipping')
            return False
        return True

    def _wait_for_flush(self):
        """Envoy buffers access log lines and flushes them periodically; wait until the file stops growing."""
        size = os.path.getsize(self._path)
        while True:
            time.sleep(FLUSH_WAIT_SECONDS)
            new_size = os.path.getsize(self._path)
            if new_size == size:
                return
            size = new_size
