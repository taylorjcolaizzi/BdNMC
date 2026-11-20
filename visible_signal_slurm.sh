#!/bin/bash

#SBATCH --time=1:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --partition=standard
#SBATCH --mem=1G
#SBATCH --job-name=VisibleDM
#SBATCH --output=%x_%A_%a.out
#SBATCH --error=%x_%A_%a.err
#SBATCH --account=ldmxuva
#SBATCH --array=0-332%16

set -euo pipefail

TASK_ID="${SLURM_ARRAY_TASK_ID:-0}"
if [[ ! "$TASK_ID" =~ ^[0-9]+$ ]] || (( TASK_ID >= 333 )); then
    echo "SLURM_ARRAY_TASK_ID must be between 0 and 332." >&2
    exit 1
fi

EPSILON2_VALUES=(
    1e-16
    3.162277660168379e-16
    1e-15
    3.162277660168379e-15
    1e-14
    3.162277660168379e-14
    1e-13
    3.162277660168379e-13
    1e-12
)

MASS_INDEX=$((TASK_ID / 9))
EPSILON_INDEX=$((TASK_ID % 9))
MASS_MEV=$((100 + 25 * MASS_INDEX))
EPSILON2="${EPSILON2_VALUES[$EPSILON_INDEX]}"
printf -v TASK_TAG "%03d" "$TASK_ID"
OUTPUT_DIR="Events/visible_signal_array/task_${TASK_TAG}"

if [[ "${DRY_RUN:-0}" == "1" ]]; then
    printf 'task=%s mDP=%s MeV epsilon^2=%s output=%s\n' \
        "$TASK_ID" "$MASS_MEV" "$EPSILON2" "$OUTPUT_DIR"
    exit 0
fi

if [[ -z "${SLURM_SUBMIT_DIR:-}" ]]; then
    echo "Submit this script with sbatch from the repository root." >&2
    exit 1
fi

cd "$SLURM_SUBMIT_DIR"

if [[ ! -x build/main ]]; then
    echo "build/main is missing; build it once in a Rivanna compute session before submission." >&2
    exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
    echo "python3 is not available in the job environment." >&2
    exit 1
fi

export BDNMC_EXECUTABLE="$PWD/build/main"
python3 visible_signal_scan.py \
    --point "$MASS_MEV" "$EPSILON2" \
    --output-dir "$OUTPUT_DIR" \
    --no-plot
