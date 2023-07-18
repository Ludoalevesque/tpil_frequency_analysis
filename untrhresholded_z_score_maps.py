# -*- coding: utf-8 -*-
"""
Created on Fri Jul  7 12:57:51 2023

@author: ludoa
"""


"""
debug and test !

"""
import nibabel as nib
import numpy as np
import os
from nilearn.maskers import NiftiMasker
import time

# Start the timer
start_time = time.time()



def zscore_maps(files_gr1, files_gr2, mask):
    
    masker = NiftiMasker(mask)
    
    gr1_2D= masker.fit_transform(files_gr1)
    gr2_2D= masker.fit_transform(files_gr2)
    
    gr1_mean= np.mean(gr1_2D,axis=0)
    gr2_mean= np.mean(gr2_2D, axis=0)
    gr2_std= np.std(gr2_2D, axis=0)
    
    z_score_2D= (gr1_mean - gr2_mean )/ gr2_std
    
    return masker.inverse_transform(z_score_2D)
    


#### Main


ALFF_path = r"D:/NeuroImaging/ALFF_test_bash"
# visit = 'V1'
# fband_label = "High"
control = "Sain"
clinical= "DC"

for visit in ['V1', 'V2', 'V3']:
    for fband_label in ['High', 'Mid','Low']:
        

        
        # Define the gray matter mask that is going to be used for all subjects
        mask_file='D:/NeuroImaging/binerizedGMmaks-thr4.nii'
        
                
        gr1_dir=f"{ALFF_path}/{visit}/{clinical}/{fband_label}"
        gr2_dir=f"{ALFF_path}/{visit}/{control}/{fband_label}"
        
        files_gr1 = [os.path.join(gr1_dir,file) for file in os.listdir(gr1_dir) if file.endswith('.nii.gz')]
        files_gr2 = [os.path.join(gr2_dir,file) for file in os.listdir(gr2_dir) if file.endswith('.nii.gz')]
                   
        
        zscore_img=zscore_maps(files_gr1, files_gr2, mask_file)
        zscore_filename= f"{ALFF_path}/Stats/unthresh_zscore_maps/{visit}_{fband_label}_zscore_map.nii.gz"
        
        if not os.path.exists(f"{ALFF_path}/Stats/unthresh_zscore_maps"):
            os.makedirs(f"{ALFF_path}/Stats/unthresh_zscore_maps")
        
        nib.save(zscore_img, zscore_filename)

# End the timer
end_time = time.time()

# Calculate the elapsed time
elapsed_time = end_time - start_time

# Print the elapsed time
print(f"Elapsed time: {elapsed_time} seconds")

