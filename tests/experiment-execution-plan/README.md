# ResilienceBench journal experiment execution plan

This bundle contains ten named experiment folders. Each folder contains a ResilienceBench `config.json`, an experiment-specific `README.md`, and a Docker Compose override.

## Recommended execution order
1. `00_smoke_and_calibration`
2. `05_no_fault_reference`
3. `04_legacy_bernoulli_control`
4. `02_single_outage_recovery`
5. `01_main_temporal_outage_100ms`
6. `01_main_temporal_outage_300ms`
7. `01_main_temporal_outage_500ms`
8. `03_frequency_sensitivity_healthy_300ms`
9. `03_frequency_sensitivity_healthy_1000ms`
10. `03_frequency_sensitivity_healthy_3000ms`

## Methodological notes
- The DSL stops on `succRequests` or `maxRequests`, not fixed wall-clock duration. Calibrate `succRequests` and freeze it across comparable runs.
- Verify at least three complete outage/recovery cycles from `scenarioDurationMs`, `faultWindowsStarted`, and `faultWindowsCompleted`.
- The full grid expands to 402 client configurations per duration. With two user levels, five rounds, and three outage durations, that is 12,060 scenario executions.
- Polly and Resilience4j parameter semantics differ; report actual library settings rather than claiming exact equivalence.
- Preserve raw CSVs, scheduler logs, and Envoy access logs. Exclude transition errors, missed windows, incomplete coverage, and fault leakage.

Each Compose file is an override for the repository-root `docker-compose.yaml`; run it from the repository root. It selects that experiment's config and results directory. Run experiments sequentially because the base stack uses fixed container names and shared Envoy fault state. Docker runtime execution has not yet been verified.
