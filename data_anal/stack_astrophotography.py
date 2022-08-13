import cv2
import numpy as np
import argparse
import os
parser = argparse.ArgumentParser()
parser.add_argument("--images", "-i", nargs="+")

base_dir = os.getcwd()

args = parser.parse_args()

image_filenames = args.images
N_images = len(image_filenames)

target_filename = image_filenames[0]
target_image = cv2.imread(target_filename) 
width, height = target_image.shape
print(f"Found {N_images} matching the glob, will create a final stacked image stacked_{target_filename}")

transformed_images = [target_image]

# cv2 objects
orb_detector = cv2.ORB_create(5000)
matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True)

target_kp, target_d = orb_detector.detectAndCompute(target_image, None)

for index, image_name in enumerate(image_filenames[1:]):
    source_image = cv2.imread(os.path.join(base_dir, image_name))
    source_kp, source_d = orb_detector.detectAndCompute(source_image, None)

    matches = matcher.match(source_d, target_d)
    matches.sort(key = lambda x: x.distance)
    matches = matches[:int(len(matches)*0.9)]
    no_of_matches = len(matches)
     
    p1 = np.zeros((no_of_matches, 2))
    p2 = np.zeros((no_of_matches, 2))
     
    for i in range(len(matches)):
        p1[i, :] = source_kp[matches[i].queryIdx].pt
        p2[i, :] = target_kp[matches[i].trainIdx].pt
     
    homography, mask = cv2.findHomography(p1, p2, cv2.RANSAC)
     
    transformed_img = cv2.warpPerspective(source_image, homography, (width, height))
    transformed_images.append(transformed_img)
    print(f"Progress: {100*index/(N_images - 1):.2f}")

stack = np.stack(transformed_images)
print(stack.shape)

final_image_data = np.median(stack, axis=3)
final_image_data = final_image_data.astype(np.uint16)
final_image = cv2.imwrite(f"stacked_moon.jpg", final_image_data) 

# # -----
# img1_color = cv2.imread("align.jpg")  # Image to be aligned.
# img2_color = cv2.imread("ref.jpg")    # Reference image.
 
# # Convert to grayscale.
# img1 = cv2.cvtColor(img1_color, cv2.COLOR_BGR2GRAY)
# img2 = cv2.cvtColor(img2_color, cv2.COLOR_BGR2GRAY)
# height, width = img2.shape
 
# # Create ORB detector with 5000 features.
# orb_detector = cv2.ORB_create(5000)
 
# # Find keypoints and descriptors.
# # The first arg is the image, second arg is the mask
# #  (which is not required in this case).
# kp1, d1 = orb_detector.detectAndCompute(img1, None)
# kp2, d2 = orb_detector.detectAndCompute(img2, None)
 
# # Match features between the two images.
# # We create a Brute Force matcher with
# # Hamming distance as measurement mode.
# matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True)
 
# # Match the two sets of descriptors.
# matches = matcher.match(d1, d2)
 
# # Sort matches on the basis of their Hamming distance.
# matches.sort(key = lambda x: x.distance)
 
# # Take the top 90 % matches forward.
# matches = matches[:int(len(matches)*0.9)]
# no_of_matches = len(matches)
 
# # Define empty matrices of shape no_of_matches * 2.
# p1 = np.zeros((no_of_matches, 2))
# p2 = np.zeros((no_of_matches, 2))
 
# for i in range(len(matches)):
#   p1[i, :] = kp1[matches[i].queryIdx].pt
#   p2[i, :] = kp2[matches[i].trainIdx].pt
 
# # Find the homography matrix.
# homography, mask = cv2.findHomography(p1, p2, cv2.RANSAC)
 
# # Use this matrix to transform the
# # colored image wrt the reference image.
# transformed_img = cv2.warpPerspective(img1_color,
#                     homography, (width, height))
 
# # Save the output.
# cv2.imwrite('output.jpg', transformed_img)
