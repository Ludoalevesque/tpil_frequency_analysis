# !/usr/bin/env python
# -*- coding: utf-8
#########################################################################################
#
# Prepares data for the randomise command of fsl
#
# example:

# python3 /path/to/your/python/script.py \
#     -ap "D:/NeuroImaging/ALFF_test_bash/" \
#     -v "V1" -fblb "High" -gr "DC" "Sain" \
#     -cp "TwoSampUnpairedT"


# ---------------------------------------------------------------------------------------
# Authors:Ludovic Arsenault-Lévesque
#
#########################################################################################


import os
import json
import argparse
from nilearn import image
import nibabel as nib
import numpy as np

def build_arg_parser():
    
    # Create an argument parser
    parser = argparse.ArgumentParser(description='Creates the needed inputs for randomise')
    
    # Add arguments to the parser
    
    parser.add_argument('-ap', '--ALFF_path', type=str, help='Path to amplitude maps', required=True)
    parser.add_argument('-v' ,'--visit', type=str, required=True, help='String of the visit')
    parser.add_argument('-fblb', '--fband_label',type=str, required=True, help='String of the frequency band label')    
    parser.add_argument('-gr', '--groups', type=str, nargs='+', 
                        required=True,
                        help='Strings of the the group labels. Groups will have the same order in the design matrix'
                        )
    parser.add_argument('-cp', '--comparaison',type=str, required=True, help='String of the name of the wanted compairaison or statistical test')
    
    return parser

def merge_same_group_img(ALFF_path,Stats_path, visit, group,fband):
    path=f"{ALFF_path}/{visit}/{group}/{fband}"
    files_paths=[]
    for file in os.listdir(path):
        if file.endswith(".nii.gz") or file.endswith(".nii"):
            files_paths.append( os.path.join(path, file) ) 
            
    n_sub = len(files_paths)
    merged_img = image.concat_imgs(files_paths)
    merged_img_path = f"{Stats_path}/Merged_images"
    if not os.path.exists(merged_img_path):
        os.makedirs(merged_img_path)
        
    merged_img_name = os.path.join(merged_img_path, f'{visit}_{fband}_{group}_merged.nii.gz')
    nib.save(merged_img,merged_img_name)
        
    return merged_img_name, n_sub

def merge_all_groups(files,Stats_path, visit,fband):
    merged_img=image.concat_imgs(files)
    merged_img_path = f"{Stats_path}/Merged_images"
    nib.save(merged_img,os.path.join(merged_img_path, f'{visit}_{fband}_All_groups_merged.nii.gz') )
    return os.path.join(merged_img_path, f'{visit}_{fband}_All_groups_merged.nii.gz')
    

def create_design_and_contrast_matrices(n_sub,visit, fband, Stats_path):
    # Design matrix
    n_col = len(n_sub)
    design_mtx = np.empty((0, n_col))

    for i in range(n_col):
        row = np.zeros((1, n_col))
        for j in range(n_sub[i]):
            row[0, i] = 1
            design_mtx = np.vstack((design_mtx, row))
    
    design_txt_name=f"{Stats_path}/design.txt"
    np.savetxt(design_txt_name, design_mtx, fmt='%d', delimiter=' ')
    
    # Contrast matrix
    # Add options for other comparaison ..
    con_mtx = np.array([[1, -1], [-1, 1]])
    con_txt_name = f"{Stats_path}/contrast.txt"
    np.savetxt(con_txt_name, con_mtx, fmt='%d', delimiter=' ')

    return design_txt_name, con_txt_name


# ### inputs from bash
# ALFF_path ="D:/NeuroImaging/ALFF_test_bash/"
# visit = 'V1'
# fband_label = "High"
# groups = ["DC","Sain"]
# comparaison = "TwoSampUnpairedT"
# ####

def main():
    
    parser = build_arg_parser()
    
    # Parse the command-line arguments
    args = parser.parse_args()
    
    ALFF_path =args.ALFF_path
    visit = args.visit
    fband_label = args.fband_label
    groups =args.groups
    comparaison = args.comparaison
    
    Stats_path= f"{ALFF_path}/Stats/{comparaison}/{visit}/{fband_label}"
    
    #  Merging images of the same group to one 4D image
    merged_groups = []
    n_sub = []
    for group in groups:
        merged_group, n_sub_per_gr = merge_same_group_img(ALFF_path,
                                                             Stats_path,
                                                             visit,
                                                             group,
                                                             fband_label)
        merged_groups.append(merged_group)
        n_sub.append(n_sub_per_gr)
        
    all_groups4D = merge_all_groups(merged_groups, Stats_path, visit,fband_label)
    
    design_txt_name, con_txt_name = create_design_and_contrast_matrices(n_sub,visit, 
                                                                        fband_label,
                                                                        Stats_path)
    output_prefix = f'{Stats_path}/{visit}_{fband_label}'
    randomise_inputs= f"{all_groups4D} {output_prefix} {design_txt_name} {con_txt_name} {Stats_path}"
    
    print(randomise_inputs)
    
    # randomise_inputs = {
    #     'input4D': all_groups4D,
    #     'output_prefix': f'{visit}_{fband_label}',
    #     'design_mtx': design_txt_name,
    #     'contrast_mtx': con_txt_name}
        
    # # Serialize the dictionary as JSON and print it
    # print(json.dumps(randomise_inputs))
        
        
if __name__ == '__main__':
    main()


