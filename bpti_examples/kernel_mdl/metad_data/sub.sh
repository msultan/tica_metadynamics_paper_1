#!/bin/bash
#SBATCH --job-nam=bpti_multi_0
#SBATCH -o /scratch/test/log.out
#SBATCH -p pande
#SBATCH -n 5
#SBATCH --gres=gpu:5
#SBATCH -t 23:59:00


source ~/.bash_profile
echo $CUDA_VISIBLE_DEVICES


sbatch --dependency=afterany:$SLURM_JOB_ID sub.sh
srun python multi_tic.py
