#!/bin/bash
#SBATCH --gres=gpu:1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH -N 1

#SBATCH --job-name=hmd_example
#SBATCH --output=%x-%j.out                                                                                            #SBATCH --error=%x-%j.err

#SBATCH --partition edu-20h
##SBATCH -t 0:5:0

# /data/hmd_2024/run llama3 "I would like a pizza."
/data/hmd_2024/run "$@"

