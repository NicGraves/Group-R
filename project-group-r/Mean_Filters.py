import numpy as np
class Mean_Filters:
    #5x5 mask
    def Arithmetic_Mean_Filter(self, image, buf):
        height = image.shape[0]-2
        width = image.shape[1]-2
        sum = 0
        buffer=2
        arithmeticImage = image.copy()
        for y in range(buffer,height):
            for x in range(buffer,width):

                filterValues = image[y-buffer:y+buffer+1, x-buffer:x+buffer+1]
                for i in range(filterValues.shape[0]):
                    for j in range(filterValues.shape[1]):
                        sum = sum + filterValues[i,j]

                nVal=filterValues.shape[0]
                mVal=filterValues.shape[1]
                #print(nVal,mVal)
                arithmeticImage[y,x]=float(sum/(nVal*mVal))
                sum=0
        #print(image)
        return arithmeticImage
    #3x3 mask
    def Geometric_Mean_Filter(self, image, buf):
        height = image.shape[0]-2
        width = image.shape[1]-2
        buffer=2
        geometricImage = image.copy()
        product=1
        for y in range(buffer,height):
            for x in range(buffer,width):
               filterValues = image[y - buffer:y + buffer - 1, x - buffer:x + buffer - 1]
               for i in range(filterValues.shape[0]):
                   for j in range(filterValues.shape[1]):
                       if(filterValues[i,j]==0):
                           filterValues[i,j]=1

                       product = product * (filterValues[i, j]**(1.0/9))

               geometricImage[y,x]=product
               product=1

        return geometricImage
    #2x2 mask
    def Harmonic_Mean_Filter(self, image, buf):
        height = image.shape[0] - 2
        width = image.shape[1] - 2
        buffer=2
        inverseAddition = 0
        harmonicImage = image.copy()
        for y in range(2, height):
            for x in range(2, width):
                filterValues = image[y - buffer:y + buffer-2, x - buffer:x + buffer-2]
                #  print(type(filterValues))
                for i in range(filterValues.shape[0]):
                    for j in range(filterValues.shape[1]):
                        if(filterValues[i,j]==0):
                            filterValues[i,j]=1
                        inverseAddition = inverseAddition + 1.0/(float(filterValues[i,j]))

                #print(filterValues)
                #print(4.0/(inverseAddition))
                harmonicImage[y, x] = 4.0/(float(inverseAddition))
                inverseAddition = 0
        return harmonicImage
