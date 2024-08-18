import cv2
import numpy as np


def distance_l1(x, y):
    return abs(x - y)


def distance_l2(x, y):
    return (x - y) ** 2


def pixel_wise_matching(left_img, right_img, disparity_range, cost_method, cost_method_name, save_result=True):
    # Read left, right images then convert to grayscale
    left = cv2.imread(left_img, 0)
    right = cv2.imread(right_img, 0)

    left = left.astype(np.float32)
    right = right.astype(np.float32)

    height, width = left.shape[:2]

    # Create blank disparity map
    depth = np.zeros((height, width), np.uint8)
    scale = 100
    max_value = 255

    for y in range(height):
        for x in range(width):
            # Find j where cost has minimum value
            disparity = 0
            cost_min = max_value

            for j in range(disparity_range):
                cost = max_value if (
                    x - j) < 0 else cost_method(int(left[y, x]), int(right[y, x - j]))
                if cost < cost_min:
                    cost_min = cost
                    disparity = j
            # Let depth at (y, x) = j (disparity)
            # Multiply by a scale factor for visualization purpose
            depth[y, x] = disparity * scale

    if save_result == True:
        print('Saving result ...')
        # save results
        cv2.imwrite(f'pixel_wise_{cost_method_name}.png', depth)
        cv2.imwrite(f'pixel_wise_{cost_method_name}_color.png',
                    cv2.applyColorMap(depth, cv2.COLORMAP_JET))
    print('Done.')
    return depth


left_img_path = './data/tsukuba/left.png'
right_img_path = './data/tsukuba/right.png'
disparity_range = 16

pixel_wise_result_l1 = pixel_wise_matching(
    left_img_path, right_img_path, disparity_range, distance_l1, "l1", save_result=True)

pixel_wise_result_l2 = pixel_wise_matching(
    left_img_path, right_img_path, disparity_range, distance_l2, "l2", save_result=True)
