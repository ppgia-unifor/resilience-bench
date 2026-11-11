import threading
import time
from logger import get_logger

logger = get_logger('timeline')

def validate_windows(windows, repeat=False):
    """
    Checks that fault windows are a non-empty list of {start, duration} (ms) and that repeat is a boolean.
    Each start is relative to the end of the previous window (the first one, to the scenario start), so any order is valid.
    """
    if not isinstance(windows, list) or not windows:
        raise ValueError('fault.windows must be a non-empty list')
    for idx, window in enumerate(windows):
        if not isinstance(window, dict) or 'start' not in window or 'duration' not in window:
            raise ValueError(f'fault.windows[{idx}] must have start and duration')
        start, duration = window['start'], window['duration']
        if isinstance(start, bool) or not isinstance(start, (int, float)) or start < 0:
            raise ValueError(f'fault.windows[{idx}].start must be >= 0')
        if isinstance(duration, bool) or not isinstance(duration, (int, float)) or duration <= 0:
            raise ValueError(f'fault.windows[{idx}].duration must be > 0')
    if not isinstance(repeat, bool):
        raise ValueError('fault.repeat must be true or false')
    if repeat and all(window['start'] == 0 for window in windows):
        raise ValueError('fault.repeat needs at least one window with start > 0, otherwise the fault never turns off')

class FaultTimeline:
    """
    Turns the fault on during each window and off between them.

    Each window starts `start` ms after the previous window ends (the first one, after start()).
    With repeat, the list starts over after its last window until the timeline is stopped.
    """

    def __init__(self, envoy, fault_spec, percentage, windows, repeat=False):
        self._envoy = envoy
        self._fault_spec = fault_spec
        self._percentage = percentage
        self._windows = windows
        self._repeat = repeat
        self._stop_event = threading.Event()
        self._thread = None
        self._start_time = None
        self.windows_started = 0
        self.windows_completed = 0
        self.duration_ms = None

    def start(self):
        self._set_fault(0)
        self._start_time = time.monotonic()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self):
        self.duration_ms = round((time.monotonic() - self._start_time) * 1000)
        self._stop_event.set()
        self._thread.join()
        self._set_fault(0)
        if self.windows_completed < len(self._windows):
            logger.warning(f'scenario ended after {self.duration_ms} ms, before the list of fault windows finished once: '
                           f'{self.windows_completed}/{len(self._windows)} completed, {self.windows_started} started')

    def _schedule(self):
        """Yields (list position, on offset, off offset) in ms from start(), forever when repeating."""
        offset = 0
        while True:
            for idx, window in enumerate(self._windows):
                on = offset + window['start']
                offset = on + window['duration']
                yield idx, on, offset
            if not self._repeat:
                return

    def _run(self):
        total = len(self._windows)
        for idx, on, off in self._schedule():
            if self._wait_until(on):
                return
            self._set_fault(self._percentage)
            self.windows_started += 1
            logger.info(f'fault window {self.windows_started} ({idx + 1}/{total} in the list) on at {self._elapsed_ms()} ms')
            if self._wait_until(off):
                return
            self._set_fault(0)
            self.windows_completed += 1
            logger.info(f'fault window {self.windows_completed} ({idx + 1}/{total} in the list) off at {self._elapsed_ms()} ms')

    def _wait_until(self, offset_ms):
        """Waits until offset_ms after start; returns True if stopped first."""
        remaining = self._start_time + offset_ms / 1000 - time.monotonic()
        return self._stop_event.wait(max(remaining, 0))

    def _elapsed_ms(self):
        return round((time.monotonic() - self._start_time) * 1000)

    def _set_fault(self, percentage):
        try:
            self._envoy.set_fault(self._fault_spec, percentage)
        except Exception as e:
            logger.error(f'Failed to set fault to {percentage}% in envoy! {e}')
