#!/bin/bash
#SBATCH --time=00:30:00
#SBATCH --job-name=test_bet
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=10G
#SBATCH --mail-user=ludo.a.levesque@gmail.com
#SBATCH --mail-type=FAIL,END

root=$HOME/scratch
native_T1="${root}/BIDS_data/sub-02/anat/sub-02_T1w.nii.gz"
bet_T1="${root}/BIDS_data/sub-02/anat/sub-02_T1w_brain.nii.gz"


# 1- brain extraction using bet

module load StdEnv/2020  gcc/9.3.0  cuda/11.0 fsl/6.0.4
echo $native_T1
bet -i $native_T1 -o $bet_T1


