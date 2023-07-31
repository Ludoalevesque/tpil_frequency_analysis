#!/bin/bash
#SBATCH --time=01:00:00
#SBATCH --job-name=atlas_to_T1_space
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem-per-cpu=10G
#SBATCH --mail-user=ludo.a.levesque@gmail.com
#SBATCH --mail-type=FAIL,END

root=$HOME/scratch
atlas="${root}/Atlases/BN_Atlas_246_1mm.nii.gz"
bet_T1="${root}/BIDS_data/sub-02/anat/sub-02_T1w_brain.nii.gz"

# 2- Registering the atlas to T1 space using antsRegistration

module load StdEnv/2020 gcc/9.3.0 ants/2.4.4

antsRegistration \
  --dimensionality 3 \
  --output '${root}/test/atlas_in_mni' \
  --interpolation 'Linear' \
  --transform Syn[0.25,3,0] \
  --metric CC \
  --convergence [100x100x70x20, 1e-6, 10] \
  --shrink-factors 4x2x1 \
  --smoothing-sigmas 3x2x1 \
  --use-histogram-matching 1 \
  --fixed $bet_T1 \
  --moving $atlas