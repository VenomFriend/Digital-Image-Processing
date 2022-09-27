from PIL import Image
import numpy
import math
import time
import os

numpy.set_printoptions(threshold=numpy.nan)
def valueQ(x):
	if (x<=0):
		return 0
	else:
		return x


def calc_p(x):
	#valueA = (valueQ(x+2))**3
	#valueB = (-4*(valueQ(x+1)))**3
	#valueC = (6*valueQ(x))**3
	#valueD =(-4*(valueQ(x-1)))**3

	#valueA = valueQ((x+2)**3)
	#valueB = (-4) * valueQ((x+1)**3)
	#valueC = (-6) * valueQ(x**3)
	#valueD = (-4) * valueQ((x-1)**3)

	valueA = (valueQ(x+2))**3
	valueB = (-4) * (valueQ(x+1))**3
	valueC = (-6) * (valueQ(x))**3
	valueD = (-4) * (valueQ(x-1))**3
	value = (1/6)*(valueA + valueB + valueC + valueD)
	return value


def zoom_bicubico(img, newWidth, newHeight):
        path = "zoom"
        save_path = os.path.join(path, "result_bicubico", img)
        im = Image.open(os.path.join(path, img), "r")
        imageArray = numpy.array(im, dtype=numpy.uint8)
        width, height = im.size
        if(width > newWidth):
                sr = width/newWidth
        else:
                sr = (width - 1)/newWidth
        if(height > newHeight):
                sc = height/newHeight
        else:
                sc = (height-1)/newHeight
        newImageArray = numpy.zeros((newHeight, newWidth, 3), dtype=numpy.uint8)
        for y in range(newHeight):
                for x in range(newWidth):
                        rf = x * sr
                        cf = y * sc
                        r0 = math.floor(rf)
                        c0 = math.floor(cf)
                        deltaR = rf - r0
                        deltaC = cf - c0
                        valuePixel = 0
                        for n in range(-1, 3): # somatorio de -1 a 2
                        	for m in range(-1, 3):
                        		originalPixel = 0
                        		if( ((c0 + n) < height) and ((r0 + m) < width) ):
                        			originalPixel = imageArray[c0 + n, r0 + m]
                        		newPixel = originalPixel * calc_p(deltaR - m) * calc_p(n - deltaC)
                        		valuePixel += newPixel
                        newImageArray[y, x] = valuePixel



        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        Image.fromarray(newImageArray).save(save_path)

begin = time.time()
zoom_bicubico("Zoom_in_(1).jpg", 360, 480)
#zoom_bicubico("Zoom_in_(2).jpg", 2592, 1456)
#zoom_bicubico("Zoom_in_(3).jpg", 720, 990)

#zoom_bicubico("Zoom_out_(1).jpg", 271, 120)
#zoom_bicubico("Zoom_out_(2).jpg", 317, 500)
#zoom_bicubico("Zoom_out_(3).jpg", 174, 500)
end = time.time()

print("Finalizado: " + str(round(end-begin, 2)) + "s\n")
