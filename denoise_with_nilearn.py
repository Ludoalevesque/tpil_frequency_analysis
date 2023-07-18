# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 09:59:48 2023

@author: ludoa
"""

# derivatives_root="D:/NeuroImaging/BIDS_Test/derivatives/sub-02"
# subject_id = '02'
# from timeseries_extraction import extract_brain_timeseries
# time_series= extract_brain_timeseries(subject_id, derivatives_root)


import os
import nibabel as nib
import subprocess
from nilearn.maskers import NiftiMasker
from nilearn.interfaces.fmriprep import load_confounds_strategy


derivatives_root="D:/NeuroImaging/BIDS_Test/derivatives/sub-02"
anat_path =os.path.join(derivatives_root, 'anat')
func_path =os.path.join(derivatives_root, 'func')
fmri_filenames= "sub-02_task-rest_space-MNI152NLin6Asym_desc-preproc_bold.nii.gz"
fmri_file_path = os.path.join(func_path, fmri_filenames)
output_filename = "sub-02_task-rest_space-MNI152NLin6Asym_desc-preproc_bold_denoised.nii.gz"
output_path = os.path.join(func_path, output_filename)


# Getting the confouds to remove
confounds_simple, sample_mask = load_confounds_strategy(fmri_file_path, denoise_strategy="simple" )

# Getting the brain mask computed by fmriprep for that run
brain_mask_filename = "sub-02_task-rest_space-MNI152NLin6Asym_desc-brain_mask.nii.gz"
brain_mask_path = os.path.join(func_path,brain_mask_filename)

# Creating the masker object for time series extraction
brain_masker = NiftiMasker(
    mask_img=brain_mask_path,
    detrend=True,
    standardize="zscore_sample",
    low_pass=0.201,
    high_pass=0.009,
    t_r=1.075,  # hard coded
    memory="nilearn_cache",
    memory_level=1,
    verbose=0 )

time_series = brain_masker.fit_transform(fmri_file_path, confounds=confounds_simple)

nii_data = brain_masker.inverse_transform(time_series)
nib.save(nii_data, output_path)

##
# import nibabel as nib
# from nilearn.signal import clean

# # Load the fMRI data
# fmri_file_path = "input.nii.gz"
# fmri_img = nib.load(fmri_file_path)
# fmri_data = fmri_img.get_fdata()

# # Load the confounds
# confounds_file_path = "confounds.txt"
# confounds = np.loadtxt(confounds_file_path)

# # Regress out confounds, detrend, and standardize the data
# cleaned_data = clean(fmri_data, confounds=confounds, detrend=False, standardize=True)

# # Create a new NIfTI image using the cleaned data and the affine transformation matrix from the input image
# cleaned_img = nib.Nifti1Image(cleaned_data, fmri_img.affine, header=fmri_img.header)

# # Save the cleaned fMRI data as a NIfTI file
# output_filename = "output.nii.gz"
# cleaned_img.to_filename(output_filename)


# def open_with_fsl(file_path):
#     fslview_cmd = ['fslview', file_path]
#     subprocess.run(fslview_cmd)


# # Open the output file with FSL
# open_with_fsl(output_path)
