import numpy as np

def to_gray(img):
    r, g, b = img[..., 0], img[..., 1], img[..., 2]
    return 0.299 * r + 0.587 * g + 0.114 * b

def process_chedec(image):
    gray_img = to_gray(image)

    c = np.zeros((256, 256), dtype=np.uint32)

    i_values = gray_img[:, :-1].astype(np.uint8)
    j_values = gray_img[:, 1:].astype(np.uint8)

    np.add.at(c, (i_values, j_values), 1)

    c_transpose = c.T
    c_symmetric = c + c_transpose

    val = np.sum(c)
    normalized = c_symmetric / val

    i, j = np.indices((256, 256))

    contrast = np.sum(normalized * (i - j) ** 2)
    dissimilarity = np.sum(normalized * np.abs(i - j))
    homogeneity = np.sum(normalized / (1 + (i - j) ** 2))

    entropy_mask = normalized > 0
    entropy = -np.sum(normalized[entropy_mask] * np.log10(normalized[entropy_mask]))

    asm = np.sum(normalized ** 2)
    energy = np.sqrt(asm)

    miui = np.sum(normalized * i)
    miuj = np.sum(normalized * j)

    mean_i = np.mean(i)
    mean_j = np.mean(j)

    sigma_i = np.sum(normalized * (i - mean_i) ** 2)
    sigma_j = np.sum(normalized * (j - mean_j) ** 2)

    correlation = np.sum(normalized * (i - miui) * (j - miuj) / (sigma_i ** 2 * sigma_j ** 2) ** 0.5)

    diff = [contrast, homogeneity, entropy, dissimilarity, energy, correlation]
    return diff

def compare(chedec1, chedec2):
    numerator = np.dot(chedec1, chedec2)
    denominator = np.linalg.norm(chedec1) * np.linalg.norm(chedec2)
    similarity = (numerator / denominator)*100
    return similarity

def cbir_texture(img1, img2):
    chedec1 = process_chedec(img1)
    chedec2 = process_chedec(img2)
    similarity = compare(chedec1, chedec2)
    return similarity