import os
import cv2
import time
from Texture import process_chedec
from Colour import rgb_to_hsv

start = time.time()

def read_image(img_path):
    img = cv2.imread(img_path)
    return img

def read_to_collect_vector(image_path):

    if os.path.exists(image_path) and image_path.endswith(('.jpg', '.jpeg', '.png')):
        texture_vector = process_chedec(image_path)
        colours_vector = rgb_to_hsv(image_path)

    return (texture_vector, colours_vector)