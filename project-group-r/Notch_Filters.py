import numpy as np
import math
import cv2

"""
    Trying to add notch filters.

"""

class Notch_Filters:
    # main functions

    def Ideal_Notch_Reject(self, image, r, s, cutoff):
        mask = Notch_Filters.get_ideal_mask(self, image, r, s, cutoff)
        filtered_image = Notch_Filters.filtering(self, image, mask, False)

        return filtered_image

    def Butterworth_Notch_Reject(self, image, r, s, cutoff, order):
        mask = Notch_Filters.get_butterworth_mask(self, image, r, s, cutoff, order)
        filtered_image = Notch_Filters.filtering(self, image, mask, False)

        return filtered_image

    def Gaussian_Notch_Reject(self, image, r, s, cutoff):
        mask = Notch_Filters.get_gaussian_mask(self, image, r, s, cutoff)
        filtered_image = Notch_Filters.filtering(self, image, mask, False)

        return filtered_image

    def Ideal_Notch_Pass(self, image, r, s, cutoff):
        mask = Notch_Filters.get_ideal_mask(self, image, r, s, cutoff)
        np_mask = np.ones(image.shape) - mask
        filtered_image = Notch_Filters.filtering(self, image, np_mask, True)

        return filtered_image

    def Butterworth_Notch_Pass(self, image, r, s, cutoff, order):
        mask = Notch_Filters.get_butterworth_mask(self, image, r, s, cutoff, order)
        np_mask = np.ones(image.shape) - mask
        filtered_image = Notch_Filters.filtering(self, image, np_mask, True)

        return filtered_image

    def Gaussian_Notch_Pass(self, image, r, s, cutoff):
        mask = Notch_Filters.get_gaussian_mask(self, image, r, s, cutoff)
        np_mask = np.ones(image.shape) - mask
        filtered_image = Notch_Filters.filtering(self, image, np_mask, True)

        return filtered_image

    # helper functions

    def get_ideal_mask(self, image, r, s, cutoff):

        x = image.shape[0]
        y = image.shape[1]
        R = x/2 - r
        S = y/2 - s
        R2 = x/2 + r
        S2 = y/2 + s
        mask = np.ones([x, y])
        for u in range(x):
            for v in range(y):
                d1 = Notch_Filters.dist_notch(self, u, v, R, S)
                d2 = Notch_Filters.dist_notch(self, u, v, R2, S2)
                if d1 <= cutoff or d2 <= cutoff:
                    mask[u][v] = 0

        return mask

    def get_butterworth_mask(self, image, r, s, cutoff, order):
        x = image.shape[0]
        y = image.shape[1]
        R = x / 2 - r
        S = y / 2 - s
        R2 = x / 2 + r
        S2 = y / 2 + s
        mask = np.zeros([x, y])
        for u in range(x):
            for v in range(y):
                d1 = Notch_Filters.dist_notch(self, u, v, R, S)
                d2 = Notch_Filters.dist_notch(self, u, v, R2, S2)
                if d1 and d2 != 0:
                    mask[u][v] = 1 / (1 + (cutoff ** 2 / (d1 * d2)) ** order)

        return mask

    def get_gaussian_mask(self, image, r, s, cutoff):
        x = image.shape[0]
        y = image.shape[1]
        R = x / 2 - r
        S = y / 2 - s
        R2 = x / 2 + r
        S2 = y / 2 + s
        mask = np.zeros([x, y])
        for u in range(x):
            for v in range(y):
                d1 = Notch_Filters.dist_notch(self, u, v, R, S)
                d2 = Notch_Filters.dist_notch(self, u, v, R2, S2)
                mask[u][v] = 1 - math.e**((-1/2) * ((d1 * d2) / cutoff**2))

        return mask

    def post_process_image(self, image, is_notch_pass):
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
        if is_notch_pass:
            negative = np.ones(image.shape) * 255
            negative = negative - fcs_image
            return negative

        return fcs_image

    def filtering(self, image, mask, is_notch_pass):
        """
        This function performs frequency domain filtering using a given mask.

        :param image:   the image to perform filtering on
        :param mask:    the mask with which to filter frequencies with
        :param is_notch_pass:    boolean stating if notch pass or not. used to
                                tell whether to take negative of image or not.
        :return:        filtered image
        """
        dft = np.fft.fft2(image)   # dft
        sdft = np.fft.fftshift(dft)     # shifted dft
        sdft_masked = np.multiply(sdft, mask)   # shifted dft with mask applied
        isdft_masked = np.fft.ifftshift(sdft_masked)    # revert the shift on the dft
        filtered = np.fft.ifft2(isdft_masked)       # apply inverse dft
        mag = np.abs(filtered)  # get magnitude of inverse dft (aka image)

        filt_image = Notch_Filters.post_process_image(self, mag, is_notch_pass).astype("uint8")
        dft_mag = Notch_Filters.post_process_image(self, np.log(np.abs(sdft)), False).astype("uint8")   # dft before filtering
        filt_dft = np.multiply(dft_mag, mask)

        # cv2.imwrite("lenna_dft.jpg", dft_mag)
        # cv2.imwrite("lenna_dft_filtered.jpg", filt_dft)

        return filt_image

    def dist_notch(self, u, v, r, s):
        d = math.sqrt((u - r) ** 2 + (v - s) ** 2)
        return d
