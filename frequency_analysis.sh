#!/bin/bash

# This script needs to be run in a virtual environment names frequency_analysis, that has the folowing modules installed : pandas openpyxl nibabel numpy scipy nilearn

# Activate the virtual environment
CONDA_SCRIPT_PATH="$HOME/miniconda3/etc/profile.d/conda.sh"
source "${CONDA_SCRIPT_PATH}"
conda activate frequency_analysis

python_scripts_path="/mnt/c/Users/ludoa/Python_env/test_venv/Scripts"


# Useful variables
ALFF_path='/mnt/d/NeuroImaging/ALFF_test_bash2'
fbands=("0.01-0.05" "0.05-0.12" "0.12-0.20")
visits=('V1' 'V2' 'V3')
fbands_labels=('Low' 'Mid' 'High')
groups=("DC" "Sain")

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


# Running randomise

# Loop over visits
for visit in "${visits[@]}"; do
    # Loop over frequency bands
    for fband_label in "${fband_labels[@]}"; do
	
        echo "Running script for visit: $visit, frequency band: $fband_label"

        ## Running randomise for a Two sample unpaired test:

        # create_randomise_inputs.py creates the inputs to run randomise.
        # Warning! May need to be changed if the wanted comparison is not an Unpaired two sample test
        output=$(python "${python_scripts_path}/create_randomise_inputs_2SampUnp.py" \
            -ap "$ALFF_path" \
            -v "$visit" \
            -fblb "$fband_label" \
            -gr "${groups[@]}" \
            -cp "TwoSampUnpairedT")

        echo "create_randomise_inputs finished"

        # Split the output into individual variables
        IFS=' ' read -ra vars <<< "$output"

        # Access the individual variables
        input4D="${vars[0]}"
        output_prefix="${vars[1]}"
        design_txt="${vars[2]}"
        contrast_txt="${vars[3]}"
        Stats_path="${vars[4]}"

        # Format design and contrast matrix files
        Text2Vest $design_txt "${Stats_path}/design.mat"
        Text2Vest $contrast_txt "${Stats_path}/design.con"

        randomise -i $input4D -o $output_prefix -d "${Stats_path}/design.mat" -t "${Stats_path}/design.con" -x

        echo "Script finished for visit: $visit, frequency band: $fband_label"
        echo
    done
done






