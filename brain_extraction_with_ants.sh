#!/bin/bash

sub='02'
root_dir="/mnt/d/NeuroImaging"
T1="${root_dir}/V1_BIDS/sub-${sub}/anat/sub-${sub}_T1w.nii.gz"
template_with_skull="${root_dir}/Templates/MICCAI2012-Multi-Atlas-Challenge-Data/T_template0.nii.gz"
brain_prob_mask="${root_dir}/Templates/MICCAI2012-Multi-Atlas-Challenge-Data/T_template0_BrainCerebellumProbabilityMask.nii.gz"
output_dir="${root_dir}/V1_BIDS/sub-${sub}/anat"

docker run -it -v ${root_dir}:${root_dir} --entrypoint bash nipreps/fmriprep
export ANTSPATH=/opt/ants/bin
antsBrainExtraction.sh -d 3 -a $T1 -e $template_with_skull -m $brain_prob_mask -o "${output_dir}/sub-{sub}_T1_brain.nii.gz"
