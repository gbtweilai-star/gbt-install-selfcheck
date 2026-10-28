#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
PYTHONPATH=src python -m gbt_install_selfcheck info
PYTHONPATH=src python -m gbt_install_selfcheck check --payload '{}'
PYTHONPATH=src python -m gbt_install_selfcheck run   --payload '{}'
