import matplotlib.pyplot as plt
import numpy as np
import Utils as utl

class Image():
    def __init__(self, img=None, type="png", name="image", noise=0, median=False, gauss=False):
        self.path = utl.Path()
        self.name = name
        self.type = type
        self.noise = noise
        self.arr = None
        self.shapes = None
        self.median = median
        self.gauss = gauss

        if (isinstance(img, str)):
            self.name = img
            self.arr = np.array(plt.imread(self.path.getFileDir(self.name + "." + self.type)), dtype=int)
            self.imageToGray()
        else:
            self.arr = np.asarray(img, dtype=int)
        self.shapes = self.arr.shape
        
    def imageToGray(self):
        if (len(self.arr.shape) == 3):
            self.arr = np.array(np.dot(self.arr[...,:3], [0.299, 0.587, 0.114]), dtype=int)

    def setImg(self, image, convert=False):
        self.arr = np.asarray(image, dtype=int)
        self.shapes = self.arr.shape
        if convert:
            self.imageToGray()

    def show(self, mode="Greys_r"):
        plt.imshow(self.arr, cmap=mode)
        plt.show()

    def save(self, extension=None, mode="Greys_r"):
        name = self.path.getNameResult(self.name+"."+self.type, extension)
        plt.imsave(self.path.getPathSave(name), self.arr, cmap=mode)

    def clear(self, kernel=None, times=2, side=3):
        gaussian_filter = np.array([
            [1/16, 1/8, 1/16],
            [1/8,  1/4, 1/8],
            [1/16, 1/8, 1/16],
        ])

        if (kernel is None):
            kernel = np.ones((side, side))

        if (self.median):
            for _ in range(times):
                self.arr = self.windowConvolve(kernel, np.median)
        if (self.gauss):
            for _ in range(times):
                self.arr = self.windowConvolve(gaussian_filter, np.sum)

    def convolve(self, kernel):
        return self.windowConvolve(kernel, np.sum)

    def windowConvolve(self, kernel, function):
        m, n = kernel.shape
        pad_h, pad_w = (m//2), (n//2)
        H, W = self.arr.shape

        img = np.ones((H + pad_h * 2, W + pad_w * 2)) * 128
        new_img = np.ones((H + pad_h * 2, W + pad_w * 2))
        img[pad_h:-pad_h, pad_w:-pad_w] = self.arr

        for i in range(pad_h, H+pad_h):
            for j in range(pad_w, W+pad_w):
                new_img[i,j] = function(np.multiply(img[i-pad_h:i+m-pad_h, j-pad_w:j+n-pad_w], kernel))

        return new_img[pad_h:-pad_h,pad_w:-pad_w]

    def features(self):
        n00 = self.momentCentral(self.arr, 0, 0)
        n11 = self.momentCentral(self.arr, 1, 1) / (n00 ** 2)
        n12 = self.momentCentral(self.arr, 1, 2) / (n00 ** 2.5)
        n21 = self.momentCentral(self.arr, 2, 1) / (n00 ** 2.5)
        n02 = self.momentCentral(self.arr, 0, 2) / (n00 ** 2)
        n03 = self.momentCentral(self.arr, 0, 3) / (n00 ** 2.5)
        n20 = self.momentCentral(self.arr, 2, 0) / (n00 ** 2)
        n30 = self.momentCentral(self.arr, 3, 0) / (n00 ** 2.5)
        
        mi1 = n20 + n02
        mi2 = (n20 - n02)**2 + 4*((n11)**2)
        mi3 = (n30 - (3*n12))**2 + ((3*n21) - n03)**2
        mi4 = (n30 + n12)**2 + (n21 - n03)**2
        mi5 = (n30 - (3*n12))*(n30 + n12)*((n30+n12)**2 - 3*((n21+n03)**2)) + ((3*n21) - n03)*(n21 + n03)*(3*((n30 + n12)**2) - (n21 + n03)**2)
        mi6 = (n20 - n02)*( ((n30+n12)**2) - (n21 + n03)**2 ) + 4*n11*(n30 + n12)*(n21 + n03)
        mi7 = ((3*n21) - n03)*(n30 + n12)*(((n30 + n12)**2) - 3*((n21 + n03)**2)) + ((3*n12) - n30)*(n21 + n03)*(3*((n30 + n12)**2) - (n21 + n03)**2)

        return [mi1, mi2, mi3, mi4, mi5, mi6, mi7]

    def momentCentral(self, arr, p, q):
        momCen, momPQ = 0, [0, 0, 0]

        for y in range(arr.shape[0]):
            for x in range(arr.shape[1]):
                momPQ[0] += (x**0) * (y**0) * arr[y, x]
                momPQ[1] += (x**1) * (y**0) * arr[y, x]
                momPQ[2] += (x**0) * (y**1) * arr[y, x]
        
        moment = [momPQ[1]/momPQ[0], momPQ[2]/momPQ[0]]

        for y in range(arr.shape[0]):
            for x in range(arr.shape[1]):
                momCen += ((x - moment[0])**p) * ((y - moment[1])**q) * arr[y, x]
        return momCen

class Histogram():
    def __init__(self):
        self.path = utl.Path()

    def getValues(self, arr, show=False):
        y_arr = np.zeros(256, dtype=int)
        for y in range(len(arr)):
            for x in range(len(arr[0])):
                y_arr[int(arr[y,x])] += 1
        if (show):
            plt.show()
        return y_arr

    def diff(self, original, result):
        y_arr = np.subtract(original, result)
        y_arr[y_arr < 0] = 0
        return y_arr

    def save(self, y_arr, name, extension="histogram", color="black"):
        name = self.path.getNameResult(name, extension)
        x_arr = [x for x in range(256)]

        plt.bar(x_arr, y_arr, width=1, color=color)
        plt.plot(x_arr, y_arr, color=color)
        plt.title("Histograma")
        plt.xlabel("Pixel")
        plt.ylabel("Frequência")
        plt.savefig(self.path.getPathSave(name))
        plt.close()