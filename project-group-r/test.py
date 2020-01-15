from tkinter import Tk, Label, Entry


class Gui:
   ''' master = Tk()
    master.title('Counting Seconds')
    Label(master, text='First Name').grid(row=0)
    Label(master, text='Last Name').grid(row=1)
    e1 = Entry(master)
    e2 = Entry(master)
    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)
    master.mainloop()
   #def process(image, size, window, threshold, spam):

        ## set filter window and image dimensions
        W = 2 * window_size + 1
        xlength, ylength = image.shape[:2]
        vlength = W * W
        ## create 2-D image array and initialize window
        image_array = np.reshape(np.array(image, dtype=np.uint8), (ylength, xlength))
        filter_window = np.array(np.zeros((W, W)))
        target_vector = np.array(np.zeros(vlength))
        pixel_count = 0
        ## loop over image with specified window W
        for y in range(window_size, ylength - (window_size + 1)):
            for x in range(window_size, xlength - (window_size + 1)):

                ## populate window, sort, find median
                filter_window = image_array[y - window_size:y + window_size + 1, x - window_size:x + window_size + 1]
                target_vector = np.reshape(filter_window, ((vlength),))
                ## internal sort
                ##median = medians_1D.quick_select(target_vector, vlength)
                ## check for threshold
                if not window_size > 0:

                    image_array[y, x] = np.median
                    pixel_count += 1
                else:
                    scale = np.zeros(vlength)
                    for n in range(vlength):

                        scale[n] = abs(int(target_vector[n]) - int(np.median))
                    scale = np.sort(scale)
                    Sk = 1.4826 * (scale[vlength / 2])
                    if abs(int(image_array[y, x]) - int(np.median)) > (window_size * Sk):

                        image_array[y, x] = np.median
                        pixel_count += 1
        return image
        row, col = image.shape[:2]
        # % Pad the  matrix with zeros on all sides
        C = np.pad(image.shape, [math.floor(window_size / 2), math.floor(window_size / 2)], 'edge')
        lowvar = np.zeros(image.shape)
        lmean = np.zeros(image.shape)
        nvar = np.zeros(image.shape)
        temp = np.zeros(image.shape)
        NewImg = np.zeros(image.shape)

        for i in range(int(window_size / 2), row - int(window_size / 2)):
            for j in range(int(window_size / 2), col - int(window_size / 2)):
                temp[i,j] = image[i,j]
                    #C(i + (window_size - 1), j + (window_size - 1))
                tmp = temp[i, j]
                # % Find the local mean and local variance for the local region
                lmean[i, j] = tmp
                lowvar[i, j] = (math.pow(tmp, 2))
        # % Noise variance and average of the local variance
        for a in range(row):
            for b in range(col):
                nvar[a, b] = lowvar[a, b]
        nvar = nvar / row

        # % If noise_variance > local_variance then local_variance = noise_variance
        if(a.all(lowvar) < a.all(nvar)):
            lowvar = nvar

        # % Final_Image = B - (noise variance / local variance) * (B - local_mean);
        NewImg = nvar / lowvar
        NewImg = NewImg * (image - lmean)
        NewImg = image - NewImg

        return NewImg'
    def Adaptive_Filter(self, image, buf):
        x = image.shape[0]
        y = image.shape[1]
        filtered_image = np.copy(image)
@ -129,4 +200,4 @@ class Order_Statistic_Filters:

        NewImg = NewImg.astype(np.uint8)

        return NewImg"""
        return NewImg'''

