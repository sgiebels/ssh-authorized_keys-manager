#!/bin/sh
# Name: run_latest_py_in_poetry.sh
# Description: Script that finds the most recent Python script in the current directory and runs it using Poetry
# Author: Sebastiaan Giebels, sgiebels_run_latest_py_in_poetry_sh@pcprobleemloos.nl


# Enable to debug this shell script:
# set -ex

# bash find the most recent file with a specific extension
#extension='*.py'
newest_file=$(find . -type f -name '*.py' -printf '%T@ %p\n' | sort -n | cut -d' ' -f 2- | tail -n 1)
echo "The newest file is: $newest_file"
poetry run python3 "${newest_file}"
