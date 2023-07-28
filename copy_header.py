import nibabel as nib
from nilearn import image
import os
import time




def copy_header(source_image_path, target_image_path):
    # Load the source NIfTI image
    source_img = nib.load(source_image_path)

    # Load the target NIfTI image (to be modified)
    target_img = nib.load(target_image_path)

    # start_time=time.time()
    # Get the image data from the target image
    target_data = target_img.get_fdata()
    # end_time= time.time()
    # elapsed_time = end_time - start_time

    # print(f"Elapsed time: {elapsed_time:.6f} seconds")

    # Create a new NIfTI image with the same data and the header from the source image
    target_img_with_header = nib.Nifti1Image(target_data, source_img.affine, header=source_img.header)

    # Save the modified target image with the same header
    nib.save(target_img_with_header, target_image_path)

if __name__ == "__main__":

    # Func
    source_image_path = "/mnt/d/NeuroImaging/V1_BIDS/sub-10/func/sub-10_task-rest_bold.nii.gz"
    target_image_path = "/mnt/d/NeuroImaging/V1_BIDS/sub-10_bet/func/sub-10_task-rest_bold.nii.gz"
    copy_header(source_image_path, target_image_path)

    # fmap
    source_image_path = "/mnt/d/NeuroImaging/V1_BIDS/sub-10/fmap/sub-10_acq-rest_dir-AP_epi.nii.gz"
    target_image_path = "/mnt/d/NeuroImaging/V1_BIDS/sub-10_bet/fmap/sub-10_acq-rest_dir-AP_epi.nii.gz"
    copy_header(source_image_path, target_image_path)   
