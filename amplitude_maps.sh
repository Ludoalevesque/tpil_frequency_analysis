#!/bin/bash

# This script needs to be run in a virtual environment names frequency_analysis, that has the folowing modules installed : pandas openpyxl nibabel numpy scipy nilearn

# Activate the virtual environment
CONDA_SCRIPT_PATH="$HOME/miniconda3/etc/profile.d/conda.sh"
source "${CONDA_SCRIPT_PATH}"
conda activate frequency_analysis

python_scripts_path="/mnt/c/Users/ludoa/Python_env/test_venv/Scripts"


# Useful variables
ALFF_path='/mnt/d/NeuroImaging/ALFF_test_bash'
fbands=("0.01,0.05" "0.05,0.12" "0.12,0.20")
visits=('V1' 'V2' 'V3')
fbands_labels=('Low' 'Mid' 'High')

# Computing amplitude maps
python3 "${python_scripts_path}/amplitude_maps.py" \
-bp '/mnt/d/NeuroImaging/BOLD_data' \
-bs 'antsed_bold_blur_res-8.nii.gz' \
-ap '$ALFF_path' \
-mf '/mnt/d/NeuroImaging/binerizedGMmaks-thr4.nii' \
-si '/mnt/d/NeuroImaging/Data_Felix.xlsx' \
-v "${visits[@]}" \
-fb "${fbands[@]}" \
-fblb "${fbands_labels[@]}"
#-ssm 'zscore' 

echo "amplitude_maps.py finished."




# This scripts creates the inputs to run randomise. May need to be changed if the wanted comparaison is not an Unpaired two sample test
python3 "${python_scripts_path}/create_randomise_inputs.py"


TwoSamp4D="$output_4D_path/CLBP_${fband}_HC_4D_amp_maps.nii.gz"
TwoSampT="${Visit}_${fband}"
designMatrx='design.mat'
designContrast='design.con'

randomise -i $TwoSamp4D -o $TwoSampT -d $designMatrx -t $designContrast -x





