
import nibabel as nib
from nilearn import image
import os
import subprocess


img_name = "sub-02_acq-rest_dir-AP_epi.nii.gz"
folder="fmap"
og_path='/mnt/d/NeuroImaging/V1_BIDS/sub-02_test'
og_img= os.path.join(og_path, folder, img_name)

bet_filepath=f'/mnt/d/NeuroImaging/V1_BIDS/sub-02_bet/{folder}/{img_name}'

temp_path='/mnt/d/NeuroImaging/temp'
if not os.path.exists(temp_path):
    os.mkdir(temp_path)

count=0
file_list = [];
for img in image.iter_img(og_img):
    volume= f"vol_{count}"
    in_filepath= os.path.join(temp_path, f"{volume}.nii.gz")
    nib.save(img, in_filepath)

    out_filepath= os.path.join(temp_path, f"{volume}_brain.nii.gz")
    
    fsl_command = ["bet", in_filepath, out_filepath]

    result = subprocess.run(fsl_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode == 0:
        print("FSL command executed successfully.")
    else:
        print("Error executing FSL command.")
        print("Error message:", result.stderr.decode())

    file_list.append(out_filepath)

    count += 1 

bet_img = image.concat_imgs(file_list)
nib.save(bet_img, bet_filepath)



