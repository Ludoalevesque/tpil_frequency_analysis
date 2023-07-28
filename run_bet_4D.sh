#!/bin/bash
#SBATCH --time=15:00:00
#SBATCH --job-name=bet_func
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem-per-cpu=4G
#SBATCH --mail-user=ludo.a.levesque@gmail.com
#SBATCH --mail-type=FAIL,END


BIDS_path='/home/ludoal/scratch/BIDS_data/V1_BIDS_bet'
bet_path='/home/ludoal/scratch/BIDS_data/V1_BIDS_bet'
folder='func'
temp_path='/home/ludoal/scratch'

# Call the Python script with the arguments
python run_bet_on_4D.py "$BIDS_path" "$bet_path" "$folder" "$temp_path"