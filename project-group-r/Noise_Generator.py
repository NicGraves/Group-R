import numpy as np
class noise:

    def Identify_Noise_Type(self, noise_type, image):
        if noise_type == 'Periodic Noise':
            return self.Add_Periodic_Noise(image)
        elif noise_type == 'Gaussian Noise':
            return self.Add_Gaussian_Noise(image)
        elif noise_type == 'Salt and Pepper Noise':
            return self.Add_SP_Noise(image)
        elif noise_type == 'Salt Noise':
            return self.Add_S_Noise(image)
        elif noise_type == 'Pepper Noise':
            return self.Add_P_Noise(image)

    def Add_SP_Noise(self, image):

        s_vs_p = 0.2
        amount = 0.01
        sp_image = np.copy(image)

        # Salt mode
        num_salt = np.ceil(amount * image.size * s_vs_p)
        coords = [np.random.randint(0, i - 1, int(num_salt)) for i in image.shape]
        sp_image[coords] = 255

        # Pepper mode
        num_pepper = np.ceil(amount * image.size * (1. - s_vs_p))
        coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in image.shape]
        sp_image[coords] = 0
        return sp_image

    def Add_S_Noise(self, image):

        s_image = np.copy(image)
        amount = 0.01

        num_salt = np.ceil(amount * image.size)
        coords = [np.random.randint(0, i - 1, int(num_salt)) for i in image.shape]
        s_image[coords] = 255

        return s_image

    def Add_P_Noise(self, image):

        p_image = np.copy(image)
        amount = 0.01

        num_pepper = np.ceil(amount * image.size)
        coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in image.shape]
        p_image[coords] = 0
        return p_image

        return p_image

    def Add_Gaussian_Noise(self, image):

        row, col = image.shape[:2]
        mean = 0
        variance = 15
        gauss = np.random.normal(mean, variance, (row, col))
        gauss = gauss.reshape(row, col)
        noise_image = np.add(image, gauss)

        return noise_image

    def Add_Periodic_Noise(self, image):

        periodic_image = np.copy(image)
        periodic_image = periodic_image.astype('float64')
        for n in range(image.shape[1]):
            periodic_image[:, n] += 10 * np.sin(0.1 * np.pi * n)

        return periodic_image
