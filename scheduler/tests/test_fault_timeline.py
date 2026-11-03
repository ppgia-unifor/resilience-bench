import os
import sys
import time
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fault_timeline import FaultTimeline, validate_windows

TOLERANCE_MS = 30

class FakeEnvoy:

    def __init__(self):
        self.calls = []
        self._start = time.monotonic()

    def set_fault(self, fault_spec, percentage):
        self.calls.append((round((time.monotonic() - self._start) * 1000), percentage))

class FaultTimelineTest(unittest.TestCase):

    def run_timeline(self, windows, scenario_ms, percentage=100, repeat=False):
        envoy = FakeEnvoy()
        timeline = FaultTimeline(envoy, {'type': 'abort', 'status': 503}, percentage, windows, repeat)
        timeline.start()
        time.sleep(scenario_ms / 1000)
        timeline.stop()
        return envoy.calls, timeline

    def assertAt(self, actual_ms, expected_ms):
        self.assertLessEqual(abs(actual_ms - expected_ms), TOLERANCE_MS, f'{actual_ms} ms is not ~{expected_ms} ms')

    def test_toggles_fault_at_window_edges(self):
        windows = [{'start': 100, 'duration': 200}, {'start': 100, 'duration': 100}]
        calls, timeline = self.run_timeline(windows, 600, percentage=75)

        self.assertEqual([pct for _, pct in calls], [0, 75, 0, 75, 0, 0])
        for (actual, _), expected in zip(calls[1:5], [100, 300, 400, 500]):
            self.assertAt(actual, expected)
        self.assertEqual(timeline.windows_started, 2)
        self.assertEqual(timeline.windows_completed, 2)
        self.assertAt(timeline.duration_ms, 600)

    def test_window_starting_at_zero(self):
        calls, _ = self.run_timeline([{'start': 0, 'duration': 100}], 200)

        self.assertEqual([pct for _, pct in calls], [0, 100, 0, 0])
        self.assertAt(calls[1][0], 0)
        self.assertAt(calls[2][0], 100)

    def test_stop_during_window_turns_fault_off(self):
        windows = [{'start': 50, 'duration': 1000}, {'start': 2000, 'duration': 100}]
        calls, timeline = self.run_timeline(windows, 200)

        self.assertEqual([pct for _, pct in calls], [0, 100, 0])
        self.assertAt(calls[-1][0], 200)
        self.assertEqual(timeline.windows_started, 1)
        self.assertEqual(timeline.windows_completed, 0)

    def test_start_counts_from_end_of_previous_window(self):
        windows = [{'start': 300, 'duration': 100}, {'start': 50, 'duration': 100}]
        calls, timeline = self.run_timeline(windows, 650)

        self.assertEqual([pct for _, pct in calls], [0, 100, 0, 100, 0, 0])
        for (actual, _), expected in zip(calls[1:5], [300, 400, 450, 550]):
            self.assertAt(actual, expected)
        self.assertEqual(timeline.windows_completed, 2)

    def test_runs_list_once_without_repeat(self):
        calls, timeline = self.run_timeline([{'start': 50, 'duration': 50}], 400)

        self.assertEqual([pct for _, pct in calls], [0, 100, 0, 0])
        self.assertEqual(timeline.windows_started, 1)
        self.assertEqual(timeline.windows_completed, 1)

    def test_repeat_cycles_until_stopped(self):
        # up 100, down 50: on at 100, 250, 400; off at 150, 300, 450; stopped at 520
        calls, timeline = self.run_timeline([{'start': 100, 'duration': 50}], 520, repeat=True)

        self.assertEqual([pct for _, pct in calls], [0, 100, 0, 100, 0, 100, 0, 0])
        for (actual, _), expected in zip(calls[1:7], [100, 150, 250, 300, 400, 450]):
            self.assertAt(actual, expected)
        self.assertEqual(timeline.windows_started, 3)
        self.assertEqual(timeline.windows_completed, 3)

    def test_repeat_restarts_list_after_last_window(self):
        # on 50-100, on 150-250, then the list again: on 300-350, stopped at 380
        windows = [{'start': 50, 'duration': 50}, {'start': 50, 'duration': 100}]
        calls, timeline = self.run_timeline(windows, 380, repeat=True)

        self.assertEqual([pct for _, pct in calls], [0, 100, 0, 100, 0, 100, 0, 0])
        for (actual, _), expected in zip(calls[1:7], [50, 100, 150, 250, 300, 350]):
            self.assertAt(actual, expected)
        self.assertEqual(timeline.windows_started, 3)
        self.assertEqual(timeline.windows_completed, 3)

    def test_stop_before_any_window(self):
        calls, timeline = self.run_timeline([{'start': 1000, 'duration': 100}], 50)

        self.assertEqual([pct for _, pct in calls], [0, 0])
        self.assertEqual(timeline.windows_started, 0)
        self.assertEqual(timeline.windows_completed, 0)

class ValidateWindowsTest(unittest.TestCase):

    def test_accepts_relative_windows(self):
        validate_windows([{'start': 0, 'duration': 5000}, {'start': 5000, 'duration': 1000}])
        validate_windows([{'start': 2000, 'duration': 100}, {'start': 0, 'duration': 100}])
        validate_windows([{'start': 10000, 'duration': 5000}], repeat=True)
        validate_windows([{'start': 0, 'duration': 100}, {'start': 50, 'duration': 100}], repeat=True)

    def test_rejects_invalid_repeat(self):
        with self.assertRaises(ValueError):
            validate_windows([{'start': 100, 'duration': 100}], repeat='yes')
        with self.assertRaises(ValueError):
            validate_windows([{'start': 0, 'duration': 100}], repeat=True)

    def test_rejects_invalid_windows(self):
        invalid = [
            [],
            {'start': 0, 'duration': 1},
            [{'start': 0}],
            [{'start': -1, 'duration': 1}],
            [{'start': 0, 'duration': 0}],
            [{'start': True, 'duration': 1}],
        ]
        for windows in invalid:
            with self.subTest(windows=windows):
                with self.assertRaises(ValueError):
                    validate_windows(windows)

if __name__ == '__main__':
    unittest.main()
