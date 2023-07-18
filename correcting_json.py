# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 14:29:46 2023

@author: ludoa
"""

import json
import os
import glob



def process_json_file(file_path, fields_to_add, fields_to_remove):
    with open(file_path, "r+") as file:
        data = json.load(file)

        # Removing fields
        for field in fields_to_remove:
            data.pop(field, None)
            
        # Adding fields
        for field, value in fields_to_add.items():
            data[field] = value
            
        # Renaming field if "EstimatedTotalReadoutTime" exists
        if "EstimatedTotalReadoutTime" in data:
            data["TotalReadoutTime"] = data.pop("EstimatedTotalReadoutTime")
            



        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()


root_path= "E:\IRM\V1_BIDS"
for sub in os.listdir(root_path):
# for sub in ['sub-08']:
    if os.path.isdir(f"{root_path}/{sub}"):
        
        
        func_path= os.path.join(root_path, sub,'func')
        fmap_path= os.path.join(root_path,sub, 'fmap')

        # Fields to remove to func
        fields_to_remove = ["PhaseEncodingAxis"]
        
        # Fields to add to func
        fields_to_add = {
            "PhaseEncodingDirection": "j",
            "PhaseEncodingAxis": "j",
            "TaskName": 'rest',
            "B0FieldSource": "pepolar_fmap0"
        }
        
        for file in os.listdir(func_path):
            if file.endswith(".nii.gz") and file.startswith("sub"):
                new_name=f"{func_path}/{sub}_task-rest_bold.nii.gz"
                os.rename(f"{func_path}/{file}",new_name)
                
            if file.endswith(".json") and file.startswith("sub"):
                new_name=f"{func_path}/{sub}_task-rest_bold.json"
                os.rename(f"{func_path}/{file}",new_name)
                process_json_file(f"{func_path}/{file}",fields_to_add, fields_to_remove)

       


        
        # Fields to remove to fmap
        fields_to_remove = ["PhaseEncodingAxis", "IntendedFor"]
        
        # Fields to add to fmap
        fields_to_add = {
            "PhaseEncodingDirection": "j-",
            "PhaseEncodingAxis": "j",
            "B0FieldSource": "pepolar_fmap0",
            "B0FieldIdentifier": "pepolar_fmap0",
            "IntendedFor": f"func/{sub}_task-rest_bold.nii.gz"
        }
        
        
        for file in os.listdir(fmap_path):
            if file.endswith(".nii.gz") and file.startswith("sub"):
                new_name=f"{fmap_path}/{sub}_acq-rest_dir-PA_epi.nii.gz"
                os.rename(f"{fmap_path}/{file}",new_name)
            
            if file.endswith(".json") and file.startswith("sub"):
                new_name=f"{fmap_path}/{sub}_acq-rest_dir-PA_epi.json"
                os.rename(f"{fmap_path}/{file}",new_name)
                process_json_file(new_name,fields_to_add, fields_to_remove)

