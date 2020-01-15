import numpy as np
import math
import cv2

"""
    All filters should be done.
    Ideal and Gaussian only need 3 inputs: image, cutoff, width.
    Butterworth takes 4: image, cutoff, width, order.
"""
class Band_Filters:

    # ====================== main functions =================

    def Ideal_Band_Reject(self, image, cutoff, width):

        mask = Band_Filters.get_ideal_mask(self, image, cutoff, width)
        filtered_image = Band_Filters.filtering(self, image, mask, False)

        return filtered_image

    def Ideal_Band_Pass(self, image, cutoff, width):

        mask = Band_Filters.get_ideal_mask(self,image, cutoff, width)
        bp_mask = np.ones(image.shape) - mask
        filtered_image = Band_Filters.filtering(self,image, bp_mask, True)

        return filtered_image

    def Gaussian_Band_Reject(self, image, cutoff, width):

        mask = Band_Filters.get_gaussian_mask(self, image, cutoff, width)
        filtered_image = Band_Filters.filtering(self, image, mask, False)

        return filtered_image

    def Gaussian_Band_Pass(self, image, cutoff, width):

        mask = Band_Filters.get_gaussian_mask(self, image, cutoff, width)
        bp_mask = np.ones(image.shape) - mask
        filtered_image = Band_Filters.filtering(self, image, bp_mask, True)

        return filtered_image

    def Butterworth_Band_Reject(self, image, cutoff, width, order):

        mask = Band_Filters.get_butterworth_mask(self, image, cutoff, width, order)
        filtered_image = Band_Filters.filtering(self, image, mask, False)

        return filtered_image

    def Butterworth_Band_Pass(self, image, cutoff, width, order):

        mask = Band_Filters.get_butterworth_mask(self, image, cutoff, width, order)
        bp_mask = np.ones(image.shape) - mask
        filtered_image = Band_Filters.filtering(self, image, bp_mask, True)

        return filtered_image

    # ====================== helper functions =========================

    def get_ideal_mask(self, image, cutoff, width):     # returns mask for ideal band reject
        x = image.shape[0]
        y = image.shape[1]
        inner_bound = cutoff - (width / 2)
        outer_bound = cutoff + (width / 2)
        mask = np.ones([x, y])
        for u in range(x):
            for v in range(y):
                d = Band_Filters.dist(self, u, v, x, y)
                if inner_bound <= d <= outer_bound:
                    mask[u][v] = 0

        return mask

    def get_gaussian_mask(self, image, cutoff, width):
        x = image.shape[0]
        y = image.shape[1]
        mask = np.zeros([x, y])
        for u in range(x):
            for v in range(y):
                d = Band_Filters.dist(self, u, v, x, y)
                if d != 0:
                    mask[u][v] = 1 - np.exp(-((d ** 2 - cutoff ** 2) / (d * width)) ** 2)
                else:
                    mask[u][v] = 1

        return mask

    def get_butterworth_mask(self, image, cutoff, width, order):
        x = image.shape[0]
        y = image.shape[1]
        mask = np.zeros([x, y])
        for u in range(x):
            for v in range(y):
                d = Band_Filters.dist(self, u, v, x, y)
                if d != cutoff:
                    mask[u][v] = 1 / (1 + (d * width / (d ** 2 - cutoff ** 2)) ** (2 * order))

        return mask

    def post_process_image(self, image, is_band_pass):
        """
        this function performs full contrast stretch on filtered image
        and gets negative if a band pass filter is used

        :param image:  the image
        :param is_band_pass: says whether a band pass filter was used
                             if so, then we take the negative of image.
        :return:  the final image, full contrast stretched, possibly negative.
        """

        # full contrast stretch
        x = image.shape[0]
        y = image.shape[1]
        A = np.amin(image)
        B = np.amax(image)
        fcs_image = np.zeros([x, y])
        for i in range(x):
            for j in range(y):
                fcs_image[i, j] = (255 / (B - A)) * (image[i, j] - A)

        # take negative
        if is_band_pass:
            negative = np.ones(image.shape) * 255
            negative = negative - fcs_image
            return negative

        return fcs_image

    def filtering(self, image, mask, is_band_pass):
        """
        This function performs frequency domain filtering using a given mask.

        :param image:   the image to perform filtering on
        :param mask:    the mask with which to filter frequencies with
        :param is_band_pass:    boolean stating if band pass or not. used to
                                tell whether to take negative of image or not.
        :return:        filtered image
        """
        dft = np.fft.fft2(image)   # dft
        sdft = np.fft.fftshift(dft)     # shifted dft
        sdft_masked = np.multiply(sdft, mask)   # shifted dft with mask applied
        isdft_masked = np.fft.ifftshift(sdft_masked)    # revert the shift on the dft
        filtered = np.fft.ifft2(isdft_masked)       # apply inverse dft
        mag = np.abs(filtered)  # get magnitude of inverse dft (aka image)

        filt_image = Band_Filters.post_process_image(self, mag, is_band_pass).astype("uint8")
        dft_mag = (np.log(np.abs(sdft)) * 10).astype("uint8")   # dft before filtering
        filt_dft = np.multiply(dft_mag, mask)

        # cv2.imwrite("lenna_dft.jpg", dft_mag)
        # cv2.imwrite("lenna_dft_filtered.jpg", filt_dft)

        return filt_image

    def dist(self, u, v, P, Q):     # function for D(u,v) as in the slides, returns distance.
        d = math.sqrt((u-P/2)**2 + (v-Q/2)**2)
        return d
