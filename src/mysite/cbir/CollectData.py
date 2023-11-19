import os
import cv2
import time
import numpy as np
from .CBIR_Texture import process_chedec
from .CBIR_Colour import rgb_to_hsv


def read_image(img_path):
    img = cv2.imread(img_path)
    return img

def read_to_collect_vector(image_path):
    if os.path.exists(image_path) and image_path.endswith(('.jpg', '.jpeg', '.png')):
        colours_vector = rgb_to_hsv(read_image(image_path))
        texture_vector = process_chedec(read_image(image_path))

    return texture_vector, colours_vector