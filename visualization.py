# -*- coding: utf-8 -*-
"""Visualization.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1BBAAc2q1GyvOGPBrka6oT2x-9hJCwiIr
"""

!pip install nibabel SimpleITK pyradiomics

import SimpleITK as sitk
import numpy as np
import matplotlib.pyplot as plt
from radiomics import featureextractor
import nibabel as nib
import six

from google.colab import drive
drive.mount('/content/drive')

template = '/content/drive/My Drive/nifti/ProstateX-0000/'
data1 = '/content/drive/My Drive/nifti/ProstateX-0001/'

# Load images for the ProstateX-0001 dataset
T2W_t1 = nib.load(template + 'T2W.nii.gz').get_fdata()
CM_t1 = nib.load(template + 'LS1.nii.gz').get_fdata()
T2W_s1 = nib.load(data1 + 'T2W.nii.gz').get_fdata()
CM_s1 = nib.load(data1 + 'LS1.nii.gz').get_fdata()
ADC_s1 = nib.load(data1 + 'ADC.nii.gz').get_fdata()
ADC_t1 = nib.load(template + 'ADC.nii.gz').get_fdata()

# Standardize T2W_s1 using T2W_t
mean_t2w1 = np.mean(T2W_t1)
std_t2w1 = np.std(T2W_t1) + 1e-8
T2W_s1_standardized = (T2W_s1 - np.mean(T2W_s1)) / np.std(T2W_s1) * std_t2w1 + mean_t2w1

# Standardize ADC_s1 using ADC_t
mean_ADC1 = np.mean(ADC_t1)
std_ADC1 = np.std(ADC_t1) + 1e-8
ADC_s1_standardized = (ADC_s1 - np.mean(ADC_s1)) / np.std(ADC_s1) * std_ADC1 + mean_ADC1

# Get the middle slice index for both volumes
middle_slice_index_T2W = T2W_t1.shape[2] // 2
middle_slice_index_ADC = ADC_t1.shape[2] // 2

# Get the middle slices
T2W_slice_t = T2W_t1[:, :, middle_slice_index_T2W].astype(np.float32)
T2W_slice_s = T2W_s1_standardized[:, :, middle_slice_index_T2W].astype(np.float32)

# Get the middle slices
ADC_slice_t = ADC_t1[:, :, middle_slice_index_ADC].astype(np.float32)
ADC_slice_s = ADC_s1_standardized[:, :, middle_slice_index_ADC].astype(np.float32)

T2W_slice_t_rotated = np.rot90(T2W_slice_t)
T2W_slice_s_rotated = np.rot90(T2W_slice_s)
ADC_slice_t_rotated = np.rot90(ADC_slice_t)
ADC_slice_s_rotated = np.rot90(ADC_slice_s)

# Display the slices with a 2x2 grid
fig, axes = plt.subplots(2, 2, figsize=(20, 20))

# T2W original slice
axes[0, 0].imshow(T2W_slice_t_rotated, cmap='gray', origin='lower')
axes[0, 0].set_title('T2W from ProstateX-0000 (Middle Slice)')
axes[0, 0].axis('off')

# T2W standardized slice
axes[0, 1].imshow(T2W_slice_s_rotated, cmap='gray', origin='lower')
axes[0, 1].set_title('Standardized T2W from ProstateX-0001 (Middle Slice)')
axes[0, 1].axis('off')

# ADC original slice
axes[1, 0].imshow(ADC_slice_t_rotated, cmap='gray', origin='lower')
axes[1, 0].set_title('ADC from ProstateX-0000 (Middle Slice)')
axes[1, 0].axis('off')

# ADC standardized slice
axes[1, 1].imshow(ADC_slice_s_rotated, cmap='gray', origin='lower')
axes[1, 1].set_title('Standardized ADC from ProstateX-0001 (Middle Slice)')
axes[1, 1].axis('off')

plt.tight_layout()
plt.show()

# Convert to SimpleITK images
T2W_s1_sitk = sitk.GetImageFromArray(T2W_s1_standardized)
ADC_s1_sitk = sitk.GetImageFromArray(ADC_s1_standardized)
CM_s1_sitk = sitk.GetImageFromArray(CM_s1)

from google.colab import files

# Upload the params.yaml file
uploaded = files.upload()

# Set up Radiomics extractor with config file
extractor = featureextractor.RadiomicsFeatureExtractor('params.yaml')

# Convert them to numpy arrays for plotting.
T2W_array = sitk.GetArrayFromImage(T2W_s1_sitk)
ADC_array = sitk.GetArrayFromImage(ADC_s1_sitk)
CM_array = sitk.GetArrayFromImage(CM_s1_sitk)

# Display the middle slice of the CM image
slice_index = CM_array.shape[2] // 2  # Choose the middle slice

plt.figure(figsize=(5, 5))  #

# Plot the middle slice of the contrast-enhanced image
plt.imshow(CM_array[:, :, slice_index], cmap='gray')
plt.title('CM')
plt.axis('off')  # Hide the axes
plt.show()

# Extract features using the same extractor
features_P1_T2W = extractor.execute(T2W_s1_sitk, CM_s1_sitk, label=1, voxelBased=True)
features_P1_ADC = extractor.execute(ADC_s1_sitk, CM_s1_sitk, label=1, voxelBased=True)

import SimpleITK as sitk
import numpy as np
import matplotlib.pyplot as plt
import six

# Visualize all feature maps
for key, val in six.iteritems(features_P1_T2W):
    if isinstance(val, sitk.Image):
        # Extract the volume as a NumPy array
        volume = sitk.GetArrayViewFromImage(val)

        # Choose a specific slice to display (the second slice)
        img = np.reshape(volume[:, :, 1], (volume.shape[1], volume.shape[0]))

        # Display the image with a color map
        plt.imshow(img, cmap='turbo', alpha=0.7)
        plt.title(key)
        plt.colorbar()

        # Show the plot
        plt.show()

from scipy.ndimage import zoom



# Count the number of non-zero pixels in the image slice
non_zero_pixel_count = np.count_nonzero(img)
print(f"Feature map has {non_zero_pixel_count} non-zero pixels.")

# Convert the mask to a NumPy array and select the middle slice
cm_slice = CM_array[:, :, slice_index]

# Count the number of pixels greater than 0 in the middle slice
non_zero_pixels = np.count_nonzero(cm_slice > 0)
print(f"Number of pixels greater than 0 in the middle slice of the CM image: {non_zero_pixels}")

# Resize 'img' to match the shape of cm_slice
img_resized = zoom(img, (cm_slice.shape[0] / img.shape[0], cm_slice.shape[1] / img.shape[1]))

# Now replace the image in CM_array with 'img_resized' wherever cm_slice is greater than 0
feature_map = np.where(cm_slice > 0, img_resized, cm_slice)

# Update CM_array with the modified middle slice
CM_array[:, :, slice_index] = feature_map

# Display the updated CM_array with the feature map
plt.figure(figsize=(5, 5))
plt.imshow(CM_array[:, :, slice_index], cmap='gray')
plt.title('Updated CM with Feature Map')
plt.axis('off')  # Hide the axes
plt.show()

from scipy import ndimage
import matplotlib.pyplot as plt
import numpy as np
import SimpleITK as sitk

def overlay_heatmap_with_specific_rotation(original, feature_map, mask, alpha=0.5, angle=270):
    """
    Overlay feature map values within a cancer mask region on the original image and rotate by a specific angle.

    Parameters:
        original (ndarray): Original grayscale image.
        feature_map (ndarray): Feature map values to overlay (e.g., from PyRadiomics).
        mask (ndarray): Binary mask where overlay is to be applied.
        alpha (float): Opacity of the feature map.
        angle (int): Rotation angle (e.g., 270 for a 270-degree rotation).
    """
    # Create an overlay by keeping feature map values only within the mask region
    overlay = np.zeros_like(original)
    overlay[mask > 0] = feature_map[mask > 0]

    # Rotate the original image and overlay by the specified angle
    rotated_original = ndimage.rotate(original, angle, reshape=False)
    rotated_overlay = ndimage.rotate(overlay, angle, reshape=False)

    # Plot the rotated original image with the overlay
    plt.figure(figsize=(6, 6))
    plt.imshow(rotated_original, cmap='gray', interpolation='nearest')
    plt.imshow(rotated_overlay, cmap='hot', interpolation='nearest', alpha=alpha)
    plt.title(f'Rotated by {angle}° with Overlay')
    plt.colorbar(label='Feature Map Intensity')
    plt.axis('off')
    plt.show()

# Load data from SimpleITK images
T2W_array = sitk.GetArrayFromImage(T2W_s1_sitk)  # Original T2W image
CM_array = sitk.GetArrayFromImage(CM_s1_sitk)    # Cancer mask

# Select the middle slice for visualization
slice_index = CM_array.shape[2] // 2
T2W_slice = T2W_array[:, :, slice_index]
CM_slice = CM_array[:, :, slice_index]


feature_map = np.random.random(CM_slice.shape)

# Call the function to overlay the feature map on the T2W image
overlay_heatmap_with_specific_rotation(T2W_slice, feature_map, CM_slice, alpha=0.6, angle=270)

import SimpleITK as sitk
import numpy as np
import matplotlib.pyplot as plt
import six

# Visualize all feature maps
for key, val in six.iteritems(features_P1_ADC):
    if isinstance(val, sitk.Image):
        # Extract the volume as a NumPy array
        volume = sitk.GetArrayViewFromImage(val)

        # Choose a specific slice to display (the second slice)
        img_ADC1 = np.reshape(volume[:, :, 1], (volume.shape[1], volume.shape[0]))

        # Display the image with a color map
        plt.imshow(img, cmap='turbo', alpha=0.7)
        plt.title(key)
        plt.colorbar()

        # Show the plot
        plt.show()

from scipy.ndimage import zoom



# Count the number of non-zero pixels in the image slice
non_zero_pixel_count = np.count_nonzero(img_ADC1)
print(f"Feature map has {non_zero_pixel_count} non-zero pixels.")

# Convert the mask to a NumPy array and select the middle slice
cm_slice = CM_array[:, :, slice_index]

# Count the number of pixels greater than 0 in the middle slice
non_zero_pixels = np.count_nonzero(cm_slice > 0)
print(f"Number of pixels greater than 0 in the middle slice of the CM image: {non_zero_pixels}")

# Resize 'img' to match the shape of cm_slice
img_ADC1_resized = zoom(img_ADC1, (cm_slice.shape[0] / img_ADC1.shape[0], cm_slice.shape[1] / img_ADC1.shape[1]))

# Now replace the image in CM_array with 'img_resized' wherever cm_slice is greater than 0
feature_map_ADC1 = np.where(cm_slice > 0, img_ADC1_resized, cm_slice)

# Update CM_array with the modified middle slice
CM_array[:, :, slice_index] = feature_map_ADC1

# Display the updated CM_array with the feature map
plt.figure(figsize=(5, 5))
plt.imshow(CM_array[:, :, slice_index], cmap='gray')
plt.title('Updated CM with Feature Map')
plt.axis('off')  # Hide the axes
plt.show()

import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
import SimpleITK as sitk

def overlay_heatmap_with_specific_rotation(original, heatmap, mask, alpha=0.5, angle=270):
    """
    Overlay heatmap (feature map) within a cancer mask region on the original image and rotate by a specific angle.

    Parameters:
        original (ndarray): Original grayscale image.
        heatmap (ndarray): Feature map to overlay.
        mask (ndarray): Binary mask where overlay is to be applied.
        alpha (float): Opacity of the heatmap.
        angle (int): Rotation angle (e.g., 270 for a 270-degree rotation).
    """
    # Ensure the feature map aligns with the mask
    heatmap_resized = np.zeros_like(original)
    heatmap_resized[mask > 0] = heatmap[mask > 0]  # Assign feature map values only to masked areas

    # Rotate the original image and heatmap by the specified angle
    rotated_original = ndimage.rotate(original, angle, reshape=False)
    rotated_heatmap = ndimage.rotate(heatmap_resized, angle, reshape=False)

    # Plot the rotated images
    plt.imshow(rotated_original, cmap='gray', interpolation='nearest')
    plt.imshow(rotated_heatmap, cmap='hot', interpolation='nearest', alpha=alpha)
    plt.title(f'Rotated by {angle}°')
    plt.colorbar(label='Heatmap Intensity')
    plt.axis('off')
    plt.show()

# Load data from SimpleITK images
ADC_array = sitk.GetArrayFromImage(ADC_s1_sitk)  # Original T2W image
CM_array = sitk.GetArrayFromImage(CM_s1_sitk)    # Cancer mask

# Select the middle slice for visualization
slice_index = CM_array.shape[2] // 2
ADC_slice = ADC_array[:, :, slice_index]
CM_slice = CM_array[:, :, slice_index]

img_ADC1 = np.random.rand(*CM_slice.shape)

# Ensure the feature map is applied only within the mask region
feature_map_ADC1 = np.zeros_like(CM_slice)
feature_map_ADC1[CM_slice > 0] = img_ADC1[CM_slice > 0]

# Call the function to overlay and rotate by 270 degrees
overlay_heatmap_with_specific_rotation(ADC_slice, feature_map_ADC1, CM_slice, alpha=0.6, angle=270)

"""Paitent 2

"""

data2 = '/content/drive/My Drive/nifti/ProstateX-0002/'

T2W_t2 = nib.load(template + 'T2W.nii.gz').get_fdata()
CM_t2 = nib.load(template + 'LS1.nii.gz').get_fdata()
T2W_s2 = nib.load(data2 + 'T2W.nii.gz').get_fdata()
CM_s2 = nib.load(data2 + 'LS1.nii.gz').get_fdata()
ADC_s2 = nib.load(data2 + 'ADC.nii.gz').get_fdata()
ADC_t2 = nib.load(template + 'ADC.nii.gz').get_fdata()

mean_t2w2 = np.mean(T2W_t2)
std_t2w2 = np.std(T2W_t2) + 1e-8
T2W_s2_standardized = (T2W_s2 - np.mean(T2W_s2)) / np.std(T2W_s2) * std_t2w2 + mean_t2w2


mean_ADC2 = np.mean(ADC_t2)
std_ADC2 = np.std(ADC_t2) + 1e-8
ADC_s2_standardized = (ADC_s2 - np.mean(ADC_s2)) / np.std(ADC_s2) * std_ADC2 + mean_ADC2

middle_slice_index_T2W_2 = T2W_t2.shape[2] // 2
middle_slice_index_ADC_2 = ADC_t2.shape[2] // 2

# Get the middle slices
T2W_slice_t_2 = T2W_t2[:, :, middle_slice_index_T2W_2].astype(np.float32)
T2W_slice_s_2 = T2W_s2_standardized[:, :, middle_slice_index_T2W_2].astype(np.float32)

# Get the middle slices
ADC_slice2_t = ADC_t2[:, :, middle_slice_index_ADC_2].astype(np.float32)
ADC_slice2_s = ADC_s2_standardized[:, :, middle_slice_index_ADC_2].astype(np.float32)


T2W_slice_t_rotated_2 = np.rot90(T2W_slice_t_2)
T2W_slice_s_rotated_2 = np.rot90(T2W_slice_s_2)
ADC_slice_t_rotated_2 = np.rot90(ADC_slice2_t)
ADC_slice_s_rotated_2 = np.rot90(ADC_slice2_s)

# Display the slices with a 2x2 grid
fig, axes = plt.subplots(2, 2, figsize=(20, 20))

# T2W original slice
axes[0, 0].imshow(T2W_slice_t_rotated_2, cmap='gray', origin='lower')
axes[0, 0].set_title('T2W from ProstateX-0000 (Middle Slice)')
axes[0, 0].axis('off')

# T2W standardized slice
axes[0, 1].imshow(T2W_slice_s_rotated_2, cmap='gray', origin='lower')
axes[0, 1].set_title('Standardized T2W from ProstateX-0002 (Middle Slice)')
axes[0, 1].axis('off')

# ADC original slice
axes[1, 0].imshow(ADC_slice_t_rotated_2, cmap='gray', origin='lower')
axes[1, 0].set_title('ADC from ProstateX-0000 (Middle Slice)')
axes[1, 0].axis('off')

# ADC standardized slice
axes[1, 1].imshow(ADC_slice_s_rotated_2, cmap='gray', origin='lower')
axes[1, 1].set_title('Standardized ADC from ProstateX-0002 (Middle Slice)')
axes[1, 1].axis('off')

plt.tight_layout()
plt.show()

# Convert to SimpleITK images
T2W_s2_sitk = sitk.GetImageFromArray(T2W_s2_standardized)
ADC_s2_sitk = sitk.GetImageFromArray(ADC_s2_standardized)
CM_s1_sitk = sitk.GetImageFromArray(CM_s1)

# Extract features using the same extractor
features_P2_T2W = extractor.execute(T2W_s2_sitk, CM_s1_sitk, label=1, voxelBased=True)
features_P2_ADC = extractor.execute(ADC_s2_sitk, CM_s1_sitk, label=1, voxelBased=True)

# Import necessary libraries
import matplotlib.pyplot as plt
import numpy as np
import SimpleITK as sitk
import six

# Loop through all features and visualize them
for key, val in six.iteritems(features_P2_T2W):
    if isinstance(val, sitk.Image):
        # Extract the volume as a NumPy array
        volume = sitk.GetArrayViewFromImage(val)

        # Choose a specific slice to display (the second slice)
        img_T2W2 = np.reshape(volume[:, :, 1], (volume.shape[1], volume.shape[0]))

        # Display the image with a color map
        plt.imshow(img, cmap='turbo', alpha=0.7)
        plt.title(key)
        plt.colorbar()

        # Show the plot
        plt.show()

from scipy.ndimage import zoom



# Count the number of non-zero pixels in the image slice
non_zero_pixel_count = np.count_nonzero(img_T2W2)
print(f"Feature map has {non_zero_pixel_count} non-zero pixels.")

# Convert the mask to a NumPy array and select the middle slice
cm_slice = CM_array[:, :, slice_index]

# Count the number of pixels greater than 0 in the middle slice
non_zero_pixels = np.count_nonzero(cm_slice > 0)
print(f"Number of pixels greater than 0 in the middle slice of the CM image: {non_zero_pixels}")

# Resize 'img' to match the shape of cm_slice
img_T2W2_resized = zoom(img_T2W2, (cm_slice.shape[0] / img_T2W2.shape[0], cm_slice.shape[1] / img_T2W2.shape[1]))

#  replace the image in CM_array with 'img_resized' wherever cm_slice is greater than 0
feature_map_T2W2 = np.where(cm_slice > 0, img_T2W2_resized, cm_slice)

# Update CM_array with the modified middle slice
CM_array[:, :, slice_index] = feature_map_T2W2

# Display the updated CM_array with the feature map
plt.figure(figsize=(5, 5))
plt.imshow(CM_array[:, :, slice_index], cmap='gray')
plt.title('Updated CM with Feature Map')
plt.axis('off')  # Hide the axes
plt.show()

from scipy import ndimage
import matplotlib.pyplot as plt
import numpy as np
import SimpleITK as sitk  # Ensure SimpleITK is imported

def overlay_heatmap_with_specific_rotation(original, heatmap, mask, alpha=0.5, angle=270):
    """
    Overlay heatmap (feature map) within a cancer mask region on the original image and rotate by a specific angle.

    Parameters:
        original (ndarray): Original grayscale image.
        heatmap (ndarray): Feature map to overlay.
        mask (ndarray): Binary mask where overlay is to be applied.
        alpha (float): Opacity of the heatmap.
        angle (int): Rotation angle (e.g., 270 for a 270-degree rotation).
    """
    # Apply mask to the heatmap: Keep only regions within the mask
    heatmap_masked = np.zeros_like(original)
    heatmap_masked[mask > 0] = heatmap[mask > 0]  # Apply the feature map only to mask areas

    # Rotate the original image and the heatmap by the specified angle
    rotated_original = ndimage.rotate(original, angle, reshape=False)
    rotated_heatmap = ndimage.rotate(heatmap_masked, angle, reshape=False)

    # Plot the rotated images
    plt.imshow(rotated_original, cmap='gray', interpolation='nearest')
    plt.imshow(rotated_heatmap, cmap='hot', interpolation='nearest', alpha=alpha)
    plt.title(f'Rotated by {angle}°')
    plt.colorbar(label='Heatmap Intensity')
    plt.axis('off')
    plt.show()

# Load data from SimpleITK images
T2W2_array = sitk.GetArrayFromImage(T2W_s2_sitk)  # Original T2W image
CM_array = sitk.GetArrayFromImage(CM_s1_sitk)    # Cancer mask

# Select the middle slice for visualization
slice_index = CM_array.shape[2] // 2
T2W_slice = T2W2_array[:, :, slice_index]
CM_slice = CM_array[:, :, slice_index]

# Assuming img_T2W2 is the feature map (replace with actual feature map)
img_T2W2 = np.random.rand(*CM_slice.shape)  # Example feature map; replace with actual PyRadiomics feature map


feature_map_T2W2 = np.zeros_like(CM_slice)
feature_map_T2W2[CM_slice > 0] = img_T2W2[CM_slice > 0]

# Call the function to overlay and rotate by 270 degrees
overlay_heatmap_with_specific_rotation(T2W_slice, feature_map_T2W2, CM_slice, alpha=0.6, angle=270)

# Import necessary libraries
import matplotlib.pyplot as plt
import numpy as np
import SimpleITK as sitk
import six

# Loop through all features and visualize them
for key, val in six.iteritems(features_P2_ADC):
    if isinstance(val, sitk.Image):
        # Extract the volume as a NumPy array
        volume = sitk.GetArrayViewFromImage(val)

        # Choose a specific slice to display (the second slice)
        img_ADC2 = np.reshape(volume[:, :, 1], (volume.shape[1], volume.shape[0]))

        # Display the image with a color map
        plt.imshow(img, cmap='turbo', alpha=0.7)
        plt.title(key)
        plt.colorbar()

        # Show the plot
        plt.show()

from scipy.ndimage import zoom



# Count the number of non-zero pixels in the image slice
non_zero_pixel_count = np.count_nonzero(img_ADC2)
print(f"Feature map has {non_zero_pixel_count} non-zero pixels.")

# Convert the mask to a NumPy array and select the middle slice
cm_slice = CM_array[:, :, slice_index]

# Count the number of pixels greater than 0 in the middle slice
non_zero_pixels = np.count_nonzero(cm_slice > 0)
print(f"Number of pixels greater than 0 in the middle slice of the CM image: {non_zero_pixels}")

# Resize 'img' to match the shape of cm_slice
img_ADC2_resized = zoom(img_ADC2, (cm_slice.shape[0] / img_ADC2.shape[0], cm_slice.shape[1] / img_ADC2.shape[1]))

# Now replace the image in CM_array with 'img_resized' wherever cm_slice is greater than 0
feature_map_ADC2 = np.where(cm_slice > 0, img_ADC2_resized, cm_slice)

# Update CM_array with the modified middle slice
CM_array[:, :, slice_index] = feature_map_ADC2

# Display the updated CM_array with the feature map
plt.figure(figsize=(5, 5))
plt.imshow(CM_array[:, :, slice_index], cmap='gray')
plt.title('Updated CM with Feature Map')
plt.axis('off')  # Hide the axes
plt.show()

from scipy import ndimage
import matplotlib.pyplot as plt
import numpy as np
import SimpleITK as sitk  # Ensure SimpleITK is imported

def overlay_heatmap_with_specific_rotation(original, heatmap, mask, alpha=0.5, angle=270):
    """
    Overlay heatmap (feature map) within a cancer mask region on the original image and rotate by a specific angle.

    Parameters:
        original (ndarray): Original grayscale image.
        heatmap (ndarray): Feature map to overlay.
        mask (ndarray): Binary mask where overlay is to be applied.
        alpha (float): Opacity of the heatmap.
        angle (int): Rotation angle (e.g., 270 for a 270-degree rotation).
    """
    # Apply mask to the heatmap: Keep only regions within the mask
    heatmap_masked = np.zeros_like(original)
    heatmap_masked[mask > 0] = heatmap[mask > 0]  # Apply the feature map only to mask areas

    # Rotate the original image and the heatmap by the specified angle
    rotated_original = ndimage.rotate(original, angle, reshape=False)
    rotated_heatmap = ndimage.rotate(heatmap_masked, angle, reshape=False)

    # Plot the rotated images
    plt.imshow(rotated_original, cmap='gray', interpolation='nearest')
    plt.imshow(rotated_heatmap, cmap='hot', interpolation='nearest', alpha=alpha)
    plt.title(f'Rotated by {angle}°')
    plt.colorbar(label='Heatmap Intensity')
    plt.axis('off')
    plt.show()

# Load data from SimpleITK images
ADC2_array = sitk.GetArrayFromImage(ADC_s2_sitk)  # Original ADC image
CM_array = sitk.GetArrayFromImage(CM_s1_sitk)    # Cancer mask

# Select the middle slice for visualization
slice_index = CM_array.shape[2] // 2
ADC_slice = ADC2_array[:, :, slice_index]
CM_slice = CM_array[:, :, slice_index]

# Feature map: Replace this with your actual feature map (for example)
img_ADC2 = np.random.rand(*CM_slice.shape)  # Example feature map; replace with actual PyRadiomics feature map

feature_map_ADC2 = np.zeros_like(CM_slice)
feature_map_ADC2[CM_slice > 0] = img_ADC2[CM_slice > 0]

# Call the function to overlay and rotate by 270 degrees
overlay_heatmap_with_specific_rotation(ADC_slice, feature_map_ADC2, CM_slice, alpha=0.6, angle=270)