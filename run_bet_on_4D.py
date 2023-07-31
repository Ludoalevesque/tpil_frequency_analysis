
import nibabel as nib
from nilearn import image
import os
import subprocess
import time
from copy_header import copy_header
import sys
import argparse

def remove_files(file_list):
    for file_path in file_list:
        try:
            os.remove(file_path)
            # print(f"File '{file_path}' removed successfully.")
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
        except Exception as e:
            print(f"Error removing file '{file_path}': {e}")


def skull_strip_4D(og_img, temp_path, bet_filepath):
    count=0
    file_list = [];
    for img in image.iter_img(og_img):

        # Create one file per volume
        vol_file_path= os.path.join(temp_path, f"vol_{count}.nii.gz")
        nib.save(img, vol_file_path)
        out_filepath= os.path.join(temp_path, f"vol_{count}_brain.nii.gz")
        
        # Create the fsl command line string
        fsl_command = ["bet", vol_file_path, out_filepath]

        # run bet
        result = subprocess.run(fsl_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode == 0:
            print("FSL command executed successfully.")
        else:
            print("Error executing FSL command.")
            print("Error message:", result.stderr.decode())
            sys.exit(1) 

        file_list.append(out_filepath)

        count += 1 

    # Create the new 4D image of the brain extracted data
    bet_img = image.concat_imgs(file_list)
    
    bet_path=os.path.dirname(bet_filepath)
    if not os.path.exists(os.path.dirname(bet_path)):
        os.makedirs(bet_path)
    nib.save(bet_img, bet_filepath)

    # copy the header of the original file
    copy_header(og_img, bet_filepath)

    # Clear the temp folder
    remove_files(file_list)


def main():
        
    # start timer
    start_time = time.time()

    parser = argparse.ArgumentParser(description="Skull-strip 4D NIfTI images.")
    parser.add_argument("--BIDS_path", type=str, help="Path to the BIDS dataset.")
    parser.add_argument("--bet_path", type=str, help="Path to the output directory for the brain-extracted images.")
    parser.add_argument("--folder", type=str, help="Folder within each subject containing 4D NIfTI images.")
    parser.add_argument("--temp_path", type=str, help="Temporary path for intermediate files.")

    args = parser.parse_args()
    BIDS_path = args.BIDS_path
    bet_path = args.bet_path
    folder = args.folder
    temp_path = args.temp_path

    # BIDS_path='/mnt/d/NeuroImaging/V1_BIDS'
    # bet_path='/mnt/d/NeuroImaging/V1_BIDS_bet'
    # folder="func"
    # temp_path='/mnt/d/NeuroImaging/temp'

    if not os.path.exists(temp_path):
        os.makedirs(temp_path)

        
    for sub_dir in os.listdir(BIDS_path):
        if not os.path.isdir(BIDS_path+'/'+sub_dir):
            continue

        og_pattern = os.path.join(BIDS_path,sub_dir,folder)
        for file in os.listdir(og_pattern):
            if file.endswith('nii.gz'):
                og_img = os.path.join(og_pattern,file)

        if og_img != os.path.join(og_pattern,file):
            print("No file found with the 'nii.gz' extension in ", og_pattern)

        bet_pattern = os.path.join(bet_path,sub_dir,folder)
        for file in os.listdir(bet_pattern):
            if file.endswith('nii.gz'):
                bet_filepath = os.path.join(bet_pattern,file)
        
        if bet_filepath !=os.path.join(bet_pattern,file):
            print("No file found with the 'nii.gz' extension in ", bet_pattern)
        
        skull_strip_4D(og_img, temp_path, bet_filepath)
        print(sub_dir, ' finished')


    end_time= time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.6f} seconds")

if __name__ == '__main__':
    main()