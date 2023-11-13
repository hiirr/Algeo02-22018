import os
import cv2
import concurrent.futures
import time
from Colour import rgb_to_hsv
from Colour import cosine_similarity_block

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

def sort_path_cos(paths, images):
        v = []
        for image in images:
            processed_image = rgb_to_hsv(image)
            v.append(processed_image)
        
        cos = []
        path_cos = []
        for i in range(0, len(v)):
            cos.append(cosine_similarity_block(v[0], v[i], 10, 4)*100)
            path_cos.append([paths[i], cos[i]])
        print(path_cos)

        #urut sesuai similarity terbesar
        path_cos.sort(key=lambda x: x[1], reverse=True)
        path_sort = [item[0] for item in path_cos]
        cos_sort = [item[1] for item in path_cos]

        return path_sort, cos_sort

if __name__ == "__main__":
    folder_path = os.path.abspath("testing")
    
    if os.path.exists(folder_path):
        # Read images from the folder in parallel
        paths, images = read_images_from_folder_parallel(folder_path)

        path_sort, cos_sort = sort_path_cos(paths, images)

    else:
        print(f"The folder '{folder_path}' does not exist.")

end = time.time()
print(end - start)