# 03 Frequency Sensitivity — 3000 ms

Measures repeated 300 ms outages with a 3000 ms interval. Run from repository root using this folder's Compose override, inspect scheduler and Envoy logs, and validate complete repeated-window coverage. The DSL stops by request count, not wall-clock duration; calibrate `succRequests` before final collection.
