#!/usr/bin/env bash
#
# Run the ResilienceBench experiment suite sequentially.
# Execute from any working directory; paths are resolved relative to this script.
#
set -uo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
BASE_COMPOSE="$REPO_ROOT/docker-compose.yaml"

KEEP_GOING=0
CURRENT_PROJECT=""
CURRENT_EXP_DIR=""

usage() {
  cat <<'USAGE'
Usage: tests/experiment-execution-plan/run-all.sh [--keep-going] [--help]

Runs all ten experiment configurations in the documented order.
Each experiment gets its own Compose project and results directory.
The script stops at the first failed experiment unless --keep-going is set.

Options:
  --keep-going  Continue with later experiments after a failure.
  --help        Show this help.

Run from any directory. Requires Docker Compose v2.
USAGE
}

while (($#)); do
  case "$1" in
    --keep-going) KEEP_GOING=1 ;;
    --help|-h) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
  shift
done

if ! command -v docker >/dev/null 2>&1; then
  echo "ERROR: docker was not found in PATH." >&2
  exit 127
fi
if ! docker compose version >/dev/null 2>&1; then
  echo "ERROR: Docker Compose v2 ('docker compose') is required." >&2
  exit 127
fi
if [[ ! -f "$BASE_COMPOSE" ]]; then
  echo "ERROR: repository-root docker-compose.yaml was not found at $BASE_COMPOSE" >&2
  exit 2
fi

cleanup_current() {
  if [[ -n "$CURRENT_PROJECT" && -n "$CURRENT_EXP_DIR" ]]; then
    echo "Cleaning up Compose project: $CURRENT_PROJECT"
    docker compose -p "$CURRENT_PROJECT" \
      -f "$BASE_COMPOSE" \
      -f "$CURRENT_EXP_DIR/docker-compose.yaml" \
      down --remove-orphans --volumes || true
    CURRENT_PROJECT=""
    CURRENT_EXP_DIR=""
  fi
}
trap cleanup_current EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

EXPERIMENTS=(
  "00_smoke_and_calibration"
  "05_no_fault_reference"
  "04_legacy_bernoulli_control"
  "02_single_outage_recovery"
  "01_main_temporal_outage_100ms"
  "01_main_temporal_outage_300ms"
  "01_main_temporal_outage_500ms"
  "03_frequency_sensitivity_healthy_300ms"
  "03_frequency_sensitivity_healthy_1000ms"
  "03_frequency_sensitivity_healthy_3000ms"
)

FAILED=()
PASSED=()

run_experiment() {
  local name="$1"
  local exp_dir="$SCRIPT_DIR/$name"
  local project="rb-exp-${name//_/-}"
  local log_file="$exp_dir/results/compose-run.log"
  local status=0

  if [[ ! -f "$exp_dir/config.json" || ! -f "$exp_dir/docker-compose.yaml" ]]; then
    echo "ERROR: $name is missing config.json or docker-compose.yaml"
    return 2
  fi

  mkdir -p "$exp_dir/results"
  CURRENT_PROJECT="$project"
  CURRENT_EXP_DIR="$exp_dir"

  echo
  echo "============================================================"
  echo "Starting experiment: $name"
  echo "Compose project: $project"
  echo "Output log: $log_file"
  echo "============================================================"

  if ! docker compose -p "$project" \
      -f "$BASE_COMPOSE" \
      -f "$exp_dir/docker-compose.yaml" \
      config >/dev/null; then
    echo "ERROR: Compose configuration validation failed for $name"
    cleanup_current
    return 2
  fi

  docker compose -p "$project" \
    -f "$BASE_COMPOSE" \
    -f "$exp_dir/docker-compose.yaml" \
    up --build --abort-on-container-exit --exit-code-from scheduler scheduler \
    2>&1 | tee "$log_file"
  status=${PIPESTATUS[0]}

  # Always tear down before starting another experiment. The result files are
  # bind-mounted, so removing the project-scoped named volumes does not remove
  # the experiment's results directory.
  cleanup_current

  if ((status == 0)); then
    echo "PASS: $name"
    return 0
  fi

  echo "FAIL: $name (docker compose exit code $status)"
  return "$status"
}

for experiment in "${EXPERIMENTS[@]}"; do
  if run_experiment "$experiment"; then
    PASSED+=("$experiment")
  else
    FAILED+=("$experiment")
    if ((KEEP_GOING == 0)); then
      echo "Stopping after first failure. Use --keep-going to run the remaining experiments."
      break
    fi
  fi
done

echo
echo "==================== Experiment summary ===================="
printf 'Passed: %d\n' "${#PASSED[@]}"
for name in "${PASSED[@]}"; do printf '  PASS  %s\n' "$name"; done
printf 'Failed: %d\n' "${#FAILED[@]}"
for name in "${FAILED[@]}"; do printf '  FAIL  %s\n' "$name"; done
echo "Per-experiment Compose logs are saved under each experiment's results/ directory."

if (("${#FAILED[@]}" > 0)); then
  exit 1
fi
