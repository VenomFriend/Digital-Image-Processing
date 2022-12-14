from PIL import Image
import numpy
import math
import time
import os

#numpy.set_printoptions(threshold=numpy.nan)

def medianWeightTimes(img, r, times):
		#print("Entered median weight")
		path = "Images"
		size = (2*r) + 1
		save_path = os.path.join(path, "result_filters", "resultadoPeso_" + str(size) + "x" + str(size) + "_" + str(times) + "vezes_"  + img)
		im = Image.open(os.path.join(path, img), "r")
		imageArray = numpy.array(im, dtype=numpy.uint8)
		width, height = im.size
		newImageArray = numpy.zeros((height, width), dtype=numpy.uint8)
		size = (2*r) + 1
		for t in range(times):
			for y in range(height):
					for x in range(width):
							arrayToOrder = []
							for i in range(-r, r+1):
									for j in range(-r, r+1):
											weight = size - abs(i) - abs(j)
											if(y + i >= 0 and y+i < height and x+ j >= 0 and x+j < width):
													for k in range(weight):
															arrayToOrder.append(imageArray[y+i,x+j])
											else:
													for k in range(weight):
															arrayToOrder.append(0)
							#print("Array to order: ")
							#print(arrayToOrder)
							arrayToOrder.sort()
							elementN = math.ceil(len(arrayToOrder)/2)
							newImageArray[y, x] = arrayToOrder[elementN]
							#imageArray[y, x] = arrayToOrder[elementN]
			imageArray = numpy.array(newImageArray, dtype=numpy.uint8)



		os.makedirs(os.path.dirname(save_path), exist_ok=True)
		Image.fromarray(newImageArray).save(save_path)
		#Image.fromarray(imageArray).save(save_path)


def medianTimes(img, r, times):
		#print("Entered median times")
		path = "Images"
		size = (2*r) + 1
		save_path = os.path.join(path, "result_filters", "resultadoMediana_" + str(size) + "x" + str(size) + "_" + str(times) + "vezes_"  + img)
		im = Image.open(os.path.join(path, img), "r")
		imageArray = numpy.array(im, dtype=numpy.uint8)
		width, height = im.size
		newImageArray = numpy.zeros((height, width), dtype=numpy.uint8)
		size = (2*r) + 1
		for t in range(times):
			for y in range(height):
					for x in range(width):
							arrayToOrder = []
							for i in range(-r, r+1):
									for j in range(-r, r+1):
											if(y + i >= 0 and y+i < height and x+ j >= 0 and x+j < width):
													arrayToOrder.append(imageArray[y+i,x+j])
											else:
													arrayToOrder.append(0)
							arrayToOrder.sort()
							elementN = 2*((r**2) + r)
							newImageArray[y, x] = arrayToOrder[elementN]
			imageArray = newImageArray



		os.makedirs(os.path.dirname(save_path), exist_ok=True)
		Image.fromarray(newImageArray).save(save_path)



def alphaTrimming(img, r, alpha):
		#print("Entered alpha trimming")
		path = "Images"
		size = (2*r) + 1
		alphaStart = alpha // 2
		save_path = os.path.join(path, "result_filters", "resultadoAlpha_" + str(size) + "x" + str(size) + "_"  + str(alpha) + "Alpha_" + img)
		im = Image.open(os.path.join(path, img), "r")
		imageArray = numpy.array(im, dtype=numpy.uint8)
		width, height = im.size
		newImageArray = numpy.zeros((height, width, 3), dtype=numpy.uint8)
		size = (2*r) + 1
		for y in range(height):
				for x in range(width):
						arrayToOrder = []
						arrayTrimmed = []
						for i in range(-r, r+1):
								for j in range(-r, r+1):
										weight = size - abs(i) - abs(j)
										if(y + i >= 0 and y+i < height and x+ j >= 0 and x+j < width):
												for k in range(weight):
														arrayToOrder.append(imageArray[y+i,x+j])
										else:
												for k in range(weight):
														arrayToOrder.append(0)
						arrayToOrder.sort()
						arraySize = len(arrayToOrder)
						for z in range(arraySize - alpha):
							arrayTrimmed.append(arrayToOrder[alphaStart + z])
						averageValue = 0
						trimSize = len(arrayTrimmed)
						for w in range(trimSize):
							averageValue += arrayTrimmed[w]
						averageValue //= trimSize
						newImageArray[y, x] = averageValue
						#imageArray[y, x] = arrayToOrder[elementN]



		os.makedirs(os.path.dirname(save_path), exist_ok=True)
		Image.fromarray(newImageArray).save(save_path)
		#Image.fromarray(imageArray).save(save_path)


def pontoMedio(img, r):
	path = "Images"
	size = (2*r) + 1
	save_path = os.path.join(path, "result_filters", "resultadoPontoMedio_" + str(size) + "x" + str(size) + img)
	im = Image.open(os.path.join(path, img), "r")
	imageArray = numpy.array(im, dtype=numpy.uint8)
	width, height = im.size
	newImageArray = numpy.zeros((height, width), dtype=numpy.uint8)
	size = (2*r) + 1
	for y in range(height):
					for x in range(width):
							arrayToOrder = []
							for i in range(-r, r+1):
									for j in range(-r, r+1):
											if(y + i >= 0 and y+i < height and x+ j >= 0 and x+j < width):
													arrayToOrder.append(imageArray[y+i,x+j])
											else:
													arrayToOrder.append(0)
							arrayToOrder.sort()
							lastValue = len(arrayToOrder) - 1
							newImageArray[y, x] = (1/2)*(int(arrayToOrder[0]) + int(arrayToOrder[lastValue]))
	os.makedirs(os.path.dirname(save_path), exist_ok=True)
	Image.fromarray(newImageArray).save(save_path)
	print("Done!")


begin = time.time()
pontoMedio("Image_(3).jpg", 1)
pontoMedio("Image_(3).jpg", 2)
pontoMedio("Image_(3).jpg", 3)
pontoMedio("Image_(4).jpg", 1)
pontoMedio("Image_(4).jpg", 2)
pontoMedio("Image_(4).jpg", 3)
# alphaTrimming("Image_(4).jpg", 1, 4)
# alphaTrimming("Image_(4).jpg", 1, 8)
# alphaTrimming("Image_(4).jpg", 2, 4)
# alphaTrimming("Image_(4).jpg", 2, 8)
# alphaTrimming("Image_(4).jpg", 3, 4)
# alphaTrimming("Image_(4).jpg", 3, 8)
# medianTimes("Image_(4).jpg", 1, 1)
# medianTimes("Image_(4).jpg", 1, 3)
# medianTimes("Image_(4).jpg", 1, 5)
# medianTimes("Image_(4).jpg", 2, 1)
# medianTimes("Image_(4).jpg", 2, 3)
# medianTimes("Image_(4).jpg", 2, 5)
# medianTimes("Image_(4).jpg", 3, 1)
# medianTimes("Image_(4).jpg", 3, 3)
# medianTimes("Image_(4).jpg", 3, 5)
# medianWeightTimes("Image_(4).jpg", 1, 1)
# medianWeightTimes("Image_(4).jpg", 1, 3)
# medianWeightTimes("Image_(4).jpg", 1, 5)
# medianWeightTimes("Image_(4).jpg", 2, 1)
# medianWeightTimes("Image_(4).jpg", 2, 3)
# medianWeightTimes("Image_(4).jpg", 2, 5)
# medianWeightTimes("Image_(4).jpg", 3, 1)
# medianWeightTimes("Image_(4).jpg", 3, 3)
# medianWeightTimes("Image_(4).jpg", 3, 5)
end = time.time()

print("Finalizado: " + str(round(end-begin, 2)) + "s\n")
