# 02 single outage recovery

## Objective
Measure degradation and recovery around one isolated 500 ms outage.

## Execution
Run from the repository root:

```bash
docker compose -p rb-02-single-outage-recovery -f docker-compose.yaml -f tests/experiment-execution-plan/02_single_outage_recovery/docker-compose.yaml up --build --abort-on-container-exit --exit-code-from scheduler scheduler
```

Then run the same command with `down` instead of `up ... scheduler` before the next experiment. Results are written to this folder's `results/` directory.

## Validity checks
- Verify actual outage-window start/completion counts and scenario duration in scheduler output.
- Inspect Envoy access logs to confirm faults occur only in intended windows (or match the Bernoulli percentage for the control).
- Exclude transition errors, incomplete coverage, and fault leakage.
- The DSL stops on `succRequests` or `maxRequests`, not fixed wall-clock time; calibrate `succRequests` and verify temporal coverage before collecting final data.
