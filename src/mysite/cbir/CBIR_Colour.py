import numpy as np

def max(a, b):
    return np.maximum(a, b)

def min(a, b):
    return np.minimum(a, b)

def rgb_to_hsv(img):
    img = img / 255.0
    r, g, b = img[:, :, 0], img[:, :, 1], img[:, :, 2]

    cmax = np.maximum(np.maximum(r, g), b)
    cmin = np.minimum(np.minimum(r, g), b)
    delta = cmax - cmin

    h = np.zeros_like(r)
    mask = (delta != 0)
    h[mask & (cmax == r)] = ((g[mask & (cmax == r)] - b[mask & (cmax == r)]) / delta[mask & (cmax == r)] % 6) / 6
    h[mask & (cmax == g)] = ((b[mask & (cmax == g)] - r[mask & (cmax == g)]) / delta[mask & (cmax == g)] + 2) / 6
    h[mask & (cmax == b)] = ((r[mask & (cmax == b)] - g[mask & (cmax == b)]) / delta[mask & (cmax == b)] + 4) / 6
    h[~mask] = 0  # Kondisi jika delta delta = 0

    s = np.zeros_like(r)
    s[cmax == 0] = 0  # Kondisi jika cmax = 0
    s[cmax != 0] = delta[cmax != 0] / cmax[cmax != 0]

    v = cmax

    hsv_matrix = []
    for i in range(h.shape[0]):
        row = []
        for j in range(h.shape[1]):
            row.append({'h': h[i, j], 's': s[i, j], 'v': v[i, j]})
        hsv_matrix.append(row)

    return hsv_matrix

def display_matrix(mat):
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            print("[{:.2f}, {:.2f}, {:.2f}], ".format(mat[i][j]['h'], mat[i][j]['s'], mat[i][j]['v']), end="")
        print()

def compare(A, B):
    dot_product = np.dot(A, B)
    norm_A = np.linalg.norm(A)
    norm_B = np.linalg.norm(B)

    if norm_A == 0 or norm_B == 0:
        return 0
    else:
        return dot_product / (norm_A * norm_B)

def average_hsv_block(mat, i, j, size):
    avg_h = 0.0
    avg_s = 0.0
    avg_v = 0.0

    count = 0
    for k in range(i, min(i + size, len(mat))):
        for l in range(j, min(j + size, len(mat[0]))):
            if k < len(mat) and l < len(mat[0]):
                avg_h += mat[k][l]['h']
                avg_s += mat[k][l]['s']
                avg_v += mat[k][l]['v']
                count += 1

    if count > 0:
        avg_h /= count
        avg_s /= count
        avg_v /= count

    return {'h': avg_h, 's': avg_s, 'v': avg_v}

def compute_histogram(block, histogram, bins):
    histogram[int(block['h'] / (360.0 / bins))] += 1
    histogram[min(int(block['s'] * 100 / (100.0 / bins)), bins * 3 - 1)] += 1
    histogram[min(int(block['v'] * 100 / (100.0 / bins)), bins * 3 - 1)] += 1

def cosine_similarity_block(mat1, mat2, bins, size):
    sum_similarity = 0.0
    step = 0

    histogram1 = np.zeros(bins * 3, dtype=int)
    histogram2 = np.zeros(bins * 3, dtype=int)

    for i in range(0, len(mat1), size):
        for j in range(0, len(mat1[0]), size):
            histogram1.fill(0)
            histogram2.fill(0)

            avg_block1 = average_hsv_block(mat1, i, j, size)
            avg_block2 = average_hsv_block(mat2, i, j, size)

            compute_histogram(avg_block1, histogram1, bins)
            compute_histogram(avg_block2, histogram2, bins)

            step += 1
            similarity = compare(histogram1, histogram2)
            sum_similarity += similarity

            if i + size >= len(mat1) and j + size >= len(mat1[0]):
                break

    average_similarity = sum_similarity / step
    return average_similarity*100