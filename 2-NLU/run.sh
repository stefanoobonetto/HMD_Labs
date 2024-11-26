#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: sh run.sh <prompt_file>"
    exit 1
fi

PROMPT_FILE=$1

if [ ! -f "$PROMPT_FILE" ]; then
    echo "Error: File '$PROMPT_FILE' not found!"
    exit 1
fi

sbatch example.sbatch --system-prompt "$(cat "$PROMPT_FILE")" llama2 "I want a cheese pizza" --max_seq_length 1000

# --reservation=hmd-2024-wed: This is the reservation name for the HMD cluster. You can change it to your own reservation name.