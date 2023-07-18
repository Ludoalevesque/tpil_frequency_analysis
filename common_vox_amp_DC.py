# -*- coding: utf-8 -*-
"""
Created on Fri Jul  7 09:35:28 2023

this code take the resulting images of the statistics on amplitude maps and on 
DC maps, and binerizes them to a specified threshold. Then it multiplies them 
to get a new image that represent common voxels between the two analysis

@author: ludoa
"""
import nibabel as nib
import numpy as np
from nilearn import image
import os



def bin_and_mul_2_img(image1_path, image2_path,threshold1 , threshold2, output_path):
    
    thresholded1=image.threshold_img(image1_path, threshold1, two_sided=True)
    thresholded2=image.threshold_img(image2_path, threshold2, two_sided=True)

    binary1=image.binarize_img(thresholded1)
    binary2=image.binarize_img(thresholded2)
    
    output_data = image.math_img("img1 * img2",
                      img1=binary1, img2=binary2)
    
    os.path.dirname(output_path)
    
    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))
        
    nib.save(output_data, output_path)
    print( output_data.dataobj.max() )
    
    # # Load the images
    # image1 = nib.load(image1_path)
    # image2 = nib.load(image2_path)
    
    # # Get the image data arrays
    # data1 = image1.get_fdata()
    # data2 = image2.get_fdata()
    
    # # Binarize image 1
    # binary1 = np.where(data1 > threshold1, 1, 0)
    
    # # Binarize image 2
    # binary2 = np.where(data2 > threshold2, 1, 0)
    
    # # Multiply the binarized images
    # output_data = binary1 * binary2
    
    # # Create a new NIfTI image with the multiplied data
    # output_image = nib.Nifti1Image(output_data, affine=image1.affine)
    
    # # Save the output image
    # nib.save(output_image, output_path)
    
    # # Print completion message
    # #print("Common voxels image created successfully at:", output_path)
    
    # print("Common voxel ? :", np.logical_and(output_data.max(),1))




fbands_labels = ['Low', 'Mid', 'High']
visits = ['V1', 'V2', 'V3']
tests =['tstat1','tstat2']
ALFF_path=r"D:/NeuroImaging/ALFF_test_bash"

# Thresholds for binarization
threshold_amp = 2
threshold_dc = 2

for fband in fbands_labels:
    for visit in visits:
        for test in tests:
            # Paths to input NIfTI images
            amp_stats_path = f"{ALFF_path}/Stats/TwoSampUnpairedT/{visit}/{fband}/{visit}_{fband}_{test}.nii.gz"
            dc_stats_path = f"D:/NeuroImaging\Stats/TwoSampleUnpairedT_{visit}\{visit}_{test}.nii.gz"
            output_path= f"{ALFF_path}/Stats/CommonVoxFreqDC/{visit}/{fband}/{visit}_{fband}_{test}_DCvsAmp.nii.gz"
            
            print(f"Common vox in {visit} {fband} {test} :")
            bin_and_mul_2_img(amp_stats_path, dc_stats_path, threshold_amp, threshold_dc, output_path)









