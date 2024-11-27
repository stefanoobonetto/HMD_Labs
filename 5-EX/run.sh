#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: sh run.sh <prompt_file> <input_file>"
    exit 1
fi

PROMPT_FILE=$1
INPUT_FILE=$2

if [ ! -f "$PROMPT_FILE" ]; then
    echo "Error: File '$PROMPT_FILE' not found!"
    exit 1
fi

if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: File '$INPUT_FILE' not found!"
    exit 1
fi

sbatch --account=hmd-2024 example.sbatch --system-prompt "$(cat "$PROMPT_FILE")" llama2  "$(cat "$INPUT_FILE")" --max_seq_length 1000
