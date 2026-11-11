# 05 No Fault Reference

## Objective
Measure baseline performance without injected faults, providing a reference for the cost of resilience mechanisms and the workload environment.

## Rationale and design
This reference uses 0% abort probability and representative baseline, Retry, and Circuit Breaker configurations. It helps separate overhead introduced by resilience mechanisms from effects caused by outages.

## Run with Docker Compose
Copy this folder into the repository at `tests/experiment-execution-plan/05_no_fault_reference/`. From the repository root, run:

```bash
docker compose -p rb-05-no-fault-reference -f docker-compose.yaml -f tests/experiment-execution-plan/05_no_fault_reference/docker-compose.yaml up --build --abort-on-container-exit --exit-code-from scheduler scheduler
```

After the scheduler exits, stop and remove the stack with the same two `-f` arguments and `down`.

## Execution procedure
Run in a clean environment, verify no injected 503 responses, and check that workload and runtime settings match the other experiments.

## Validity checks
- Confirm `faultWindowsStarted` and `faultWindowsCompleted` agree with the schedule.
- Check `scenarioDurationMs` for every strategy, library, user level, and round.
- Inspect raw Envoy access logs for unexpected injected 503s.
- Verify fault state does not leak into the next scenario.
- Exclude transition errors, missing windows, unexpected faults, or incomplete coverage.

## Analysis
Compare strategy/library overhead without faults. Treat this as a reference point, not a substitute for the Bernoulli 0% control.

## Important limitation
The DSL ends a scenario when `succRequests` or `maxRequests` is reached; it does not specify fixed wall-clock duration. Pilot, inspect `scenarioDurationMs`, and increase `succRequests` if needed. Keep the stopping rule consistent across compared configurations.
