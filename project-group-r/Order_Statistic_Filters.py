import cv2
import numpy as np
import math
from cv2.cv2 import CV_8U


class Order_Statistic_Filters:

    def Max_Filter(self, image, window_size):
        row, col = image.shape[:2]
        max_filter_image = np.copy(image)
        for i in range(int(window_size/2), row-int(window_size/2)):
            for j in range(int(window_size/2), col-int(window_size/2)):
                max_val = 0
                for k in range(i-int(window_size/2), i+int(window_size/2)):
                    for l in range(j-int(window_size/2), j+int(window_size/2)):
                                if max_val < image[k][l]:
                                    max_val = image[k][l]
                max_filter_image[i, j] = max_val

        return max_filter_image

    def Min_Filter(self, image, window_size):
        row, col = image.shape[:2]
        min_filter_image = np.copy(image)
        for i in range(int(window_size / 2), row - int(window_size / 2)):
            for j in range(int(window_size / 2), col - int(window_size / 2)):
                min_val = 255
                for k in range(i - int(window_size / 2), i + int(window_size / 2)):
                    for l in range(j - int(window_size / 2), j + int(window_size / 2)):
                        if min_val > image[k][l]:
                            min_val = image[k][l]
                min_filter_image[i, j] = min_val

        return min_filter_image

    def Median_Filter(self, image, window_size):
        x = image.shape[0]
        y = image.shape[1]
        filtered_image = np.copy(image)
        window = window_size
        for i in range(0, x - math.floor(window / 2)):
            for j in range(0, y - math.floor(window / 2)):
                neighbors = []
                for k in range(0 - math.floor(window / 2), math.ceil(window / 2)):
                    for l in range(0 - math.floor(window / 2), math.ceil(window / 2)):
                        n = image[i + k, j + l]
                        neighbors.append(n)
                neighbors.sort()
                median = neighbors[4]
                filtered_image[i, j] = median

        return filtered_image

    def Midpoint_Filter(self, image, window_size):
        row, col = image.shape[:2]
        midpoint_filter_image = np.copy(image)
        for i in range(int(window_size / 2), row - int(window_size / 2)):
            for j in range(int(window_size / 2), col - int(window_size / 2)):
                min_val = 255
                max_val = 0
                for k in range(i - int(window_size / 2), i + int(window_size / 2)):
                    for l in range(j - int(window_size / 2), j + int(window_size / 2)):
                        if min_val > image[k][l]:
                            min_val = image[k][l]
                        if max_val < image[k][l]:
                            max_val = image[k][l]
                midpoint_filter_image[i, j] = (max_val + min_val)/2

        return midpoint_filter_image


    def Alpha_Trimmed_Mean_Filter(self, image, window_size):
        row, col = image.shape[:2]
        alpha_trimmed_image = np.copy(image)

        for i in range(0, image.shape[0]):
            i_max = int(max(i - ((window_size - 1) / 2), 0))
            i_min = int(min(i + ((window_size - 1) / 2) + 1, row))

            for j in range(0, image.shape[1]):
                j_max = int(max(j - ((window_size - 1) / 2), 0))
                j_min = int(min(j + ((window_size - 1) / 2) + 1, col))

                block = image[i_max:i_min, j_max:j_min]
                flattened_block = block.flatten()
                flattened_block = np.sort(flattened_block)
                length = flattened_block.size

                if int((math.pow(window_size, 2)) * 0.5) != 0:
                    flattened_block = flattened_block[int((math.pow(window_size, 2)) * 0.5):(length - (int((math.pow(window_size, 2)) * 0.5)))]

                trim_mean = flattened_block.mean()
                if trim_mean > 0:
                    alpha_trimmed_image[i][j] = int(trim_mean)

        return alpha_trimmed_image

    def Adaptive_Filter(self, image, window_size):
        x = image.shape[0]
        y = image.shape[1]
        NewImg = np.copy(image)
        window = window_size
        # % Pad the  matrix with zeros on all sides
        C = np.pad(image, [math.floor(window_size / 2), math.floor(window_size / 2)])
        #Initialize local variance array
        lvar = np.zeros((x,y))
        #Initialize local mean array
        lmean = np.zeros((x,y))
        #Initialize window array
        temp = np.zeros((window, window))
        #Initialize local mean variable
        lm = 0

        for i in range(0, x):
            for j in range(0, y):
                lm = 0
                for k in range(0 - math.floor(window / 2), math.ceil(window / 2)):
                    for l in range(0 - math.floor(window / 2), math.ceil(window / 2)):
                        n = C[i + k, j + l]
                        lm = lm + n
                        temp[k,l] = n
            #Calculating local mean and local variance
            lmean[i,j] = lm/(window**2)
            lvar[i,j] = np.mean(temp**2)-(np.mean(temp)**2)
        #Calculate overall variance
        nvar = np.mean(lvar)

        for i in range(0, x):
            for j in range(0, y):
                if(nvar > lvar[i, j]):
                    lvar[i,j] = nvar

        for i in range(0, x):
            for j in range(0, y):
                NewImg[i,j] = NewImg[i,j] * (255-(nvar / lvar[i,j])) + ((nvar / lvar[i,j]) *lmean[i,j])

        return NewImg
