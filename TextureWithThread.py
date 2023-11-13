import os
import cv2
import numpy as np
import concurrent.futures
import time
from Texture import process_hce
from Texture import compare

start = time.time()

def read_image(img_path):
    img = cv2.imread(img_path)
    return img

def read_images_from_folder_parallel(folder_path):
    images = []
    img_paths = [os.path.join(folder_path, filename) for filename in os.listdir(folder_path)
                 if filename.endswith(('.jpg', '.jpeg', '.png', '.gif'))]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Use executor.map to apply read_image to each image path in parallel
        images = list(executor.map(read_image, img_paths))

    return (img_paths, images)

if __name__ == "__main__":
    folder_path = os.path.abspath("testing")
    
    if os.path.exists(folder_path):
        # Read images from the folder in parallel
        paths, images = read_images_from_folder_parallel(folder_path)

        print(paths[0])

        v = []
        for image in images:
            processed_image = process_hce(image)
            v.append(processed_image)
            
        for i in range(0, len(v)):
            cos = compare(v[0], v[i])
        
            
            
        
    else:
        print(f"The folder '{folder_path}' does not exist.")

end = time.time()
print(end - start)