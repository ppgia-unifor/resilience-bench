# 01 main temporal outage 300ms

## Objective
Measure resilience strategy behavior under repeated temporal outages with the selected outage duration.

## Execution
Run from the repository root:

```bash
docker compose -p rb-01-main-temporal-outage-300ms -f docker-compose.yaml -f tests/experiment-execution-plan/01_main_temporal_outage_300ms/docker-compose.yaml up --build --abort-on-container-exit --exit-code-from scheduler scheduler
```

Then run the same command with `down` instead of `up ... scheduler` before the next experiment. Results are written to this folder's `results/` directory.

## Validity checks
- Verify actual outage-window start/completion counts and scenario duration in scheduler output.
- Inspect Envoy access logs to confirm faults occur only in intended windows (or match the Bernoulli percentage for the control).
- Exclude transition errors, incomplete coverage, and fault leakage.
- The DSL stops on `succRequests` or `maxRequests`, not fixed wall-clock time; calibrate `succRequests` and verify temporal coverage before collecting final data.
