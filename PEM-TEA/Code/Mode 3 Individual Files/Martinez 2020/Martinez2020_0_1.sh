#!/bin/sh
#
# Simple "Martinez2020_0_1" submit script for Slurm.
#
#SBATCH --account=free    # The account name for the job.
#SBATCH --job-name=Martinez2020_0_1 # The job name.
#SBATCH -c 1 # The number of cpu cores to use.
#SBATCH --time=360:00 # The time the job will take to run.
#SBATCH --mem-per-cpu=5gb # The memory the job will use per cpu core.
 
module load anaconda
 
#Command to execute Python program
python Martinez2020_0_1.py
 
#End of script
