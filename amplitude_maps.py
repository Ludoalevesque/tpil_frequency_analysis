# !/usr/bin/env python
# -*- coding: utf-8
#########################################################################################
#
# Compute amplitude maps using specified frequency bands
#
# example:
# python3 "${python_scripts_path}/amplitude_maps.py" \
# -bp '/mnt/d/NeuroImaging/BOLD_data' \
# -bs 'antsed_bold_blur_res-8.nii.gz' \
# -ap '/mnt/d/NeuroImaging/ALFF_test_bash' \
# -mf '/mnt/d/NeuroImaging/binerizedGMmaks-thr4.nii' \
# -si '/mnt/d/NeuroImaging/Data_Felix.xlsx' \
# -v 'V1' 'V2' 'V3' \
# -fb "0.01-0.05" "0.05-0.12" "0.12-0.20" \
# -fblb 'Low' 'Mid' 'High' \
# -ssm 'zscore' 

# ---------------------------------------------------------------------------------------
# Authors:Ludovic Arsenault-Lévesque
#
#########################################################################################

import argparse
import pandas as pd
import nibabel as nib
import numpy as np
import os
from scipy.signal import welch
from nilearn import image
from nilearn.maskers import NiftiMasker

def read_sub_data_file(filename):
    
    if filename.endswith('.csv'):
        # Read CSV file
        df = pd.read_csv(filename)
    elif filename.endswith('.xlsx'):
        # Read Excel file
        df = pd.read_excel(filename)
    else:
        raise ValueError("Unsupported file format. Only CSV and XLSX files are supported.")

    # Remove empty columns and rows
    df = df.dropna(axis='columns', how='all')
    df = df.dropna(axis='index', how='all')

    # Set the header based on the first non-empty row
    df.columns = df.iloc[0]

    # Remove the first row (header row)
    df = df[1:]

    # Reset the index
    df = df.reset_index(drop=True)
    return df

def fband_amplitude(bold_img, fbands, mask_file, standardize):
    
    """
    This function returns a nii image object of the amplitude in every
    frequency band specified for the voxels or ROI in the provided mask

    Parameters
    ----------
    bold_img : nii image file or object
        File or image of the data to compute amplitude map from.
    fbands : Array of float
        Array of the lower and upper boundary of the wanted frequency bands.
        Shape needs to be number of freq bands by 2.
    mask_file : nii image file or object
        Mask used to extract regions.

    Returns
    -------
    None.

    """
          
    n_fbands = len(fbands)
    min_f = min(min(arr) for arr in fbands)
    max_f = max(max(arr) for arr in fbands)
    cutoff_freq= [min_f, max_f]

    # Define the parameters for welch
    TR = nib.load(bold_img).header['pixdim'][4]
    fs = 1 / TR
    
    masker = NiftiMasker(mask_img=mask_file,
                         detrend=True,
                         standardize="zscore_sample",
                         low_pass=cutoff_freq[1],
                         high_pass=cutoff_freq[0],
                         t_r=TR
                         )
    
    # Check if affine are the same 
    if not np.array_equal(nib.load(bold_img).affine,
                       nib.load(mask_file).affine):
        
        # Change the affine of the image
        good_affine = nib.load(mask_file).affine
        img_to_update = nib.load(bold_img)   # Use this image's data
        new_img = nib.Nifti1Image(
            np.asanyarray(img_to_update.dataobj),
            affine=good_affine,
            header=img_to_update.header)  # Keep everything in the header but the affine
        new_img.to_filename(bold_img)
    
    
    
    bold_masked = masker.fit_transform(bold_img)
    
    # Initialize the matrix to store the amplitude
    Amp_mtx = np.zeros((n_fbands, bold_masked.shape[1])) 
    
    # Iterate trough colums of the masked data
    region_signals= zip(*bold_masked)
   
    for i,signal in enumerate(region_signals):
        f, Pxx = welch(signal, fs=fs, nperseg=len(signal),
                       window='hann', scaling='density')
        
        # # Plotting the power spectrum
        # plt.semilogy(f, Pxx)
        # plt.xlim(fbands[0, 0], fbands[2, 1])
        # plt.xlabel('Frequency (Hz)')
        # plt.ylabel('Power Spectral Density')
        # plt.title('Power Spectrum')
        # plt.grid(True)
        # plt.show()
        
        for fband_idx in range(n_fbands):
            # Find the indices of the frequency range in the power spectrum
            idx_frange = np.logical_and(f >= fbands[fband_idx][0], f <= fbands[fband_idx][1])
            
            # Calculate the average amplitude across the frequency band
            mean_amp_fband = np.mean(np.sqrt(Pxx[idx_frange]))
            Amp_mtx[fband_idx,i] = mean_amp_fband
 

    # Standardize according to the specified method
    if standardize:
        regions_mean = np.mean(Amp_mtx,axis=1).reshape(-1,1)
        regions_std = np.mean(Amp_mtx,axis=1).reshape(-1,1)
        
        if standardize=='mean':
            Amp_mtx = Amp_mtx / regions_mean
        elif standardize=='zscore':
            Amp_mtx = (Amp_mtx - regions_mean) / regions_std
        else:
            raise ValueError('Invalid standardization method specified. Supported methods: zscore, mean')


    return masker.inverse_transform(Amp_mtx)
    
def save_amp_map(amp_img, group,subLabel,fbands_labels, visit, ALFF_path):
    """
    This function saves the amplitude maps by frequency bands in the right 
    directories and name them accordingly

    Parameters
    ----------
    amp_img : Nii like object
        DESCRIPTION.
    group : TYPE
        DESCRIPTION.
    subLabel : TYPE
        DESCRIPTION.
    fbands_labels : TYPE
        DESCRIPTION.
    visit : TYPE
        DESCRIPTION.
    ALFF_path : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    
    for i, fband in enumerate(fbands_labels):
        fband_amp_img = image.index_img(amp_img, i)
        img_path=f"{ALFF_path}/{visit}/{group}/{fband}"
        img_name =f"{subLabel}_{visit}_{fband}_amp_map.nii.gz"
        
        if not os.path.exists(img_path):
            os.makedirs(img_path)
            
        nib.save(fband_amp_img,os.path.join(img_path, img_name))
    
def build_arg_parser():
    
    # Create an argument parser
    parser = argparse.ArgumentParser(description='Frequency analysis script')
    
    # Add arguments to the parser
    
    parser.add_argument('-bp', '--BOLD_path', type=str, help='Path to BOLD data', required=True)
    parser.add_argument('-bs', '--BOLD_suffix', type=str, help='BOLD data filename suffix', required=True)
    parser.add_argument('-ap', '--ALFF_path', type=str, help='Path to save amplitude maps', required=True)
    parser.add_argument('-mf', '--mask_file', type=str, help='Path to gray matter mask', required=True)
    parser.add_argument('-v' ,'--visits', type=str,nargs='+', required=True, help='Strings of the visits')
    parser.add_argument('-fb','--fbands', type=str, nargs='+',required=True, help='strings representing the lower and upper boundaries of every frequency bands. ex: "0.01-0.05" ')
    parser.add_argument('-fblb', '--fbands_labels',  nargs='+', type=str, required=True, help='Strings of frequency bands labels')
    parser.add_argument('-ssm', '--subject_standardizing_method', 
                        type=str,
                        choices=['zscore', 'mean'],
                        default=None, 
                        help='Method for standardizing subject amplitudes. Default is none.'
                        )
    
    parser.add_argument('-si', '--sub_info_file', type=str, 
                        required=True,
                        help='Path to subject information file. Has to be a xlsx or a csv file containning 3 colums: Group, Sexe, Subject label ending with a 3 digits number'
                        )
    
    
    return parser


def main():
    # Create an argument parser
    parser = build_arg_parser()
    
    # Parse the command-line arguments
    args = parser.parse_args()
       
    # Read the CSV file
    xlData= read_sub_data_file(args.sub_info_file)
    group_col = xlData.columns[0]
    label_col = xlData.columns[2]
    
    # Get fbands  lists
    fbands = [tuple(map(float, fb.split('-'))) for fb in args.fbands]
    
    # Looping over subjects
    for i, row in xlData.iterrows():
        group = row[group_col]
        subLabel =  f"sub-{row[label_col][-3:]}"
    
        # Loop over visits
        for visit in args.visits:
            file_name=f"{args.BOLD_path}/{visit}/{subLabel}/{subLabel}_{args.BOLD_suffix}"
            
            if os.path.exists(file_name):             
    
                # Compute amplitude over fbands
                A = fband_amplitude(file_name, fbands, args.mask_file,standardize=args.subject_standardizing_method)
                
                # Save amplitude map
                save_amp_map(A, group=group,subLabel=subLabel, 
                             fbands_labels=args.fbands_labels,
                             visit=visit,
                             ALFF_path=args.ALFF_path)
            
    
if __name__ == '__main__':
    main()