from PIL import Image
import numpy
import math
import time
import os

def neighbours(img, pointC, yy, xx, neigh=8):
	if(neigh==4):
		pointsToCheck = numpy.array([[yy, xx-1], [yy-1, xx], [yy, xx+1], [yy+1,xx]])
		pointsArray = numpy.array([2,1,0,3])
		eightPoints = numpy.array([[yy, xx-1], [yy-1, xx-1], [yy-1, xx], [yy-1, xx+1], [yy, xx+1], [yy+1, xx+1], [yy+1, xx], [yy+1, xx-1]])
		for i in range(8):
			if(numpy.array_equal(pointC, eightPoints[i]) and i % 2 != 0):
				newC = i+1
				if(i+1 >= 8):
					newC = 0
				pointC = eightPoints[newC]
	else:
		pointsToCheck = numpy.array([[yy, xx-1], [yy-1, xx-1], [yy-1, xx], [yy-1, xx+1], [yy, xx+1], [yy+1, xx+1], [yy+1, xx], [yy+1, xx-1]])
		pointsArray = numpy.array([4,3,2,1,0,7,6,5])
	#pointsToCheckZero = numpy.array([[yy, xx-1, 0], [yy-1, xx-1,0], [yy-1, xx,0], [yy-1, xx+1,0], [yy, xx+1,0], [yy+1, xx+1,0], [yy+1, xx,0], [yy+1, xx-1,0]])
	print("Point C = " + str(pointC))
	print("Point B: x = " + str(xx) + ", y = " + str(yy))
	for i in range(neigh):
		if numpy.array_equal(pointC, pointsToCheck[i]):
			firstPoint = i+1
			if(firstPoint >= neigh):
				firstPoint = 0
			break
	for i in range(neigh-1):
		#print(pointsToCheck[firstPoint])
		if(img[pointsToCheck[firstPoint, 0], pointsToCheck[firstPoint, 1]] == 255):
			bPoint = [pointsToCheck[firstPoint, 0], pointsToCheck[firstPoint, 1]]
			direction = pointsArray[firstPoint]
			if(i > 0):
				cPoint = numpy.array([pointsToCheck[firstPoint-1, 0], pointsToCheck[firstPoint-1, 1]])
			else:
				cPoint = numpy.array([pointsToCheck[neigh-1, 0], pointsToCheck[neigh-1, 1]])
			break
		if(firstPoint < neigh-1):
			firstPoint+=1
		else:
			firstPoint = 0
	return bPoint, cPoint, direction

def getDirectionValue(direction, neigh=8):
	if(neigh == 4):
		directions = numpy.array([[0, 1], [-1, 0], [0, -1], [1,0]]) # 0 1 2 3
	else:
		directions = numpy.array([[0, 1], [-1,1], [-1, 0], [-1,-1], [0, -1], [1, -1], [1, 0], [1,1]]) #0 1 2 3 4 5 6 7
	return directions[direction]

def normalizeChain(chain, neigh=8):
	chainNormalized = []
	for i in range(chain.size-1):
		if(i == 0):
			valueNormalized = (chain[i] - chain[chain.size-1]) % neigh
		else:
			valueNormalized = (chain[i+1] - chain[i]) % neigh
		chainNormalized.append(valueNormalized)
	return numpy.array(chainNormalized)

def chaincode(img, neigh=8):
	path = "Images"
	save_path = os.path.join(path, "result_chaincode_neigh="+str(neigh)+"_", img)
	im = Image.open(os.path.join(path, img), "r")
	imageArray = numpy.array(im, dtype=numpy.uint8)
	#print(len(imageArray.shape))
	if(len(imageArray.shape) == 3):
		imageArray = imageArray[:, :, 0]
	#print(imageArray[0])
	width, height = im.size
	newImageArray = numpy.zeros((height, width), dtype=numpy.uint8)
	#encontrar ponto mais acima e a esquerda
	found = False
	chainArray = []
	for yy in range(height):
		for xx in range(width):
			if(imageArray[yy, xx] == 255):
				bZero = numpy.array([yy, xx])
				cZero = numpy.array([yy, xx-1])
				found = True
				break
		if(found):
			break
	#find bOne
	bOne, cOne, direction = neighbours(imageArray, cZero, bZero[0], bZero[1], neigh)
	chainArray.append(direction)
	b = bOne
	c = cOne
	while(True):
		nk, nkminusone, direction = neighbours(imageArray, c, b[0], b[1], neigh)
		if(numpy.array_equal(b,bZero) and numpy.array_equal(nk, bOne)):
			break
		chainArray.append(direction)
		b = nk
		c = nkminusone
	chainArray = numpy.array(chainArray)
	chainNormalized = normalizeChain(chainArray, neigh)
	#print(chainArray)
	#numpy.savetxt("chain.txt", chainArray, fmt="%d")
	#numpy.savetxt("chainNormalized.txt", chainNormalized, fmt="%d")
	#create the new image
	point = bZero
	print("Chain Normalized Size: " + str(chainNormalized.size))
	print("First Point = " + str(point))
	for i in range(chainArray.size):
		#print("Point Before: " + str(point))
		if(point[0] < height and point[1] < width and point[0] > 0 and point[1] > 0):
			newImageArray[point[0], point[1]] = 255
		point += getDirectionValue(chainArray[i], neigh)
		#print("Point After: " + str(point))
	#return newImageArray
	os.makedirs(os.path.dirname(save_path), exist_ok=True)
	Image.fromarray(newImageArray).save(save_path)

def blackAndWhite(imgArray):
	height, width = imgArray.shape
	for yy in range(height):
		for xx in range(width):
			if(imgArray[yy, xx] < 128):
				imgArray[yy, xx] = 0
			else:
				imgArray[yy, xx] = 255
	return imgArray

def invertColor(imgArray):
	height, width = imgArray.shape
	for yy in range(height):
		for xx in range(width):
			if(imgArray[yy, xx] < 128):
				imgArray[yy, xx] = 255
			else:
				imgArray[yy, xx] = 0
	return imgArray

def skeleton(img):
	path = "Images"
	save_path = os.path.join(path, "result_skeleton", img)
	save_path2 = os.path.join(path, "result_skeleton", "skeleton_" + img)
	save_path3 = os.path.join(path, "result_skeleton", "skeletonInverted_" + img)
	im = Image.open(os.path.join(path, img), "r")
	imageArray = numpy.array(im, dtype=numpy.uint8)
	imageArray[imageArray > 0] = 1
	print(imageArray[200, 200])
	#imageArray = imageArray[:1, :1]
	#print(imageArray)
	imageArrayWithSkeleton = numpy.copy(imageArray)
	print(imageArrayWithSkeleton[200, 200])
	#print(imageArray[0])
	width, height = im.size
	skeletonArray = numpy.full((height, width), 1, dtype=numpy.uint8)
	skeletonArrayInverted = numpy.full((height, width), 0, dtype=numpy.uint8)
	numIterations = 1
	while(True):
		# first step
		for yy in range(height):
			for xx in range(width):
				if(imageArray[yy, xx] > 0):
					# p9 p2 p3
					# p8 p1 p4
					# p7 p6 p5
					# imageArray[yy,xx] is p1
					# those are p2, p3, p4, p5, p6, p7, p8, p9, in this order
					pointsToCheck = numpy.array([[yy-1, xx], [yy-1, xx+1], [yy, xx+1], [yy+1, xx+1], [yy+1, xx], [yy+1, xx-1], [yy, xx-1], [yy-1, xx-1]])
					nPone = 0 # N(p1)
					tPone = 0 # T(p1)
					for i in range(8):
						# T(p1) = somatorio[(1 - Ti)*(Ti+1 mod 8)]
						ti = 0
						tiPlus = 0
						if(imageArray[pointsToCheck[i, 0], pointsToCheck[i, 1]] > 0):
							nPone +=1
							ti = 1
						nextI = (i+1) % 8
						if(imageArray[pointsToCheck[nextI, 0], pointsToCheck[nextI, 1]] > 0):
							tiPlus = 1
						tPone += (1 - ti) * (tiPlus % 8)
					fourSix =  imageArray[pointsToCheck[2, 0], pointsToCheck[2, 1]] * imageArray[pointsToCheck[4, 0], pointsToCheck[4, 1]]
					pTwoFourSix = imageArray[pointsToCheck[0, 0], pointsToCheck[0, 1]] * fourSix
					pFourSixEight = fourSix * imageArray[pointsToCheck[6, 0], pointsToCheck[6, 1]]
					#if(nPone >= 2 and nPone <= 6):
					#	print("tPone = " + str(tPone))
					#	print("pTwoFourSix = " + str(pTwoFourSix))
					#	print("pFourSixEight = " + str(pFourSixEight))
					#	print("nPone = " + str(nPone))
					if(nPone >= 2 and nPone <=6 and tPone == 1 and pTwoFourSix == 0 and pFourSixEight == 0):
					#	print("Entrou primeiro if!")
						skeletonArray[yy, xx] = 0
						skeletonArrayInverted[yy, xx] = 255
						imageArrayWithSkeleton[yy, xx] = 0
		# second step
		
		imageArray = numpy.copy(imageArrayWithSkeleton)
		for yy in range(height):
			for xx in range(width):
				if(imageArray[yy, xx] > 0):
					pointsToCheck = numpy.array([[yy-1, xx], [yy-1, xx+1], [yy, xx+1], [yy+1, xx+1], [yy+1, xx], [yy+1, xx-1], [yy, xx-1], [yy-1, xx-1]])
					nPone = 0 # N(p1)
					tPone = 0 # T(p1)
					for i in range(8):
						# T(p1) = somatorio[(1 - Ti)*(Ti+1 mod 8)]
						ti = 0
						tiPlus = 0
						if(imageArray[pointsToCheck[i, 0], pointsToCheck[i, 1]] > 0):
							nPone +=1
							ti = 1
						nextI = (i+1) % 8
						if(imageArray[pointsToCheck[nextI, 0], pointsToCheck[nextI, 1]] > 0):
							tiPlus = 1
						tPone += (1 - ti) * (tiPlus % 8)
					twoEight =  imageArray[pointsToCheck[0, 0], pointsToCheck[0, 1]] * imageArray[pointsToCheck[6, 0], pointsToCheck[6, 1]]
					pTwoFourEight = twoEight * imageArray[pointsToCheck[2, 0], pointsToCheck[2, 1]]
					pTwoSixEight = twoEight * imageArray[pointsToCheck[4, 0], pointsToCheck[4, 1]]
					if(nPone >= 2 and nPone <=6 and tPone == 1 and pTwoFourEight == 0 and pTwoSixEight == 0):
						#print("Entrou segundo if!")
						skeletonArray[yy, xx] = 0
						skeletonArrayInverted[yy, xx] = 255
						#print("Image array [yy, xx] = " + str(imageArray[yy, xx]))
						imageArrayWithSkeleton[yy, xx] = 0
						#print("Image array with skeleton [yy, xx] = " + str(imageArrayWithSkeleton[yy,xx]))
						#print("Image array again [yy, xx] = " +str(imageArray[yy, xx]))
		#print("Sao iguais = " + str(numpy.array_equal(imageArray, imageArrayWithSkeleton)))
		if(numpy.array_equal(imageArray, imageArrayWithSkeleton)):
			print("Sao iguais")
			break
		imageArray = numpy.copy(imageArrayWithSkeleton)
		numIterations += 1
		#print("U??, chegou aqui")
	print("numIterations = " + str(numIterations))
	imageArray[imageArray > 0] = 255
	os.makedirs(os.path.dirname(save_path), exist_ok=True)
	Image.fromarray(imageArray).save(save_path)
	skeletonArray[skeletonArray > 0] = 255
	#print(skeletonArray)
	os.makedirs(os.path.dirname(save_path2), exist_ok=True)
	Image.fromarray(skeletonArray).save(save_path2)
	os.makedirs(os.path.dirname(save_path3), exist_ok=True)
	Image.fromarray(skeletonArrayInverted).save(save_path3)

def mpp(img, radius=16):
	path = "Images"
	save_path = os.path.join(path, "result_mpp", "elephant_radius=" + str(radius) + ".bmp")
	im = Image.open(os.path.join(path, img), "r")
	imageArray = numpy.array(im, dtype=numpy.uint8)
	#print(imageArray)
	width, height = im.size
	#imageArray = invertColor(blackAndWhite(imageArray))
	os.makedirs(os.path.dirname(save_path), exist_ok=True)
	Image.fromarray(imageArray).save(save_path)
	heightR = height//radius
	widthR = width//radius
	newImageArray = numpy.zeros((height, width), dtype=numpy.uint8)
	print(imageArray[0, 16])
	for yy in range(heightR):
		distY = yy*radius
		for xx in range(widthR):
			distX = xx*radius
			minDistance = 999
			vertix = numpy.array([ [distY, distX], [distY, distX+radius], [distY+radius, distX+radius], [distY+radius, distX] ])
			#print(vertix)
			pointVertix = []
			hasPoint = False
			for yyy in range(radius):
				for xxx in range(radius):
					for v in range(4): # vertix
						if(imageArray[distY+yyy, distX+xxx] > 0): #if it's a blackpoint inside that square
							#print("Coordinates: y=" + str(distY+yyy) + " and x=" + str(distX+xxx))
							#print(imageArray[distY+yyy, distX+xxx])
							distance = abs(distY+yyy - vertix[v, 0]) + abs(distX+xxx - vertix[v, 1])
							if(distance<minDistance):
								hasPoint = True
								minDistance = distance
								pointVertix = vertix[v]
			if(hasPoint):
				#print(pointVertix)
				newImageArray[pointVertix[0], pointVertix[1]] = 255
	os.makedirs(os.path.dirname(save_path), exist_ok=True)
	Image.fromarray(newImageArray).save(save_path)

def momento(imgArray, p, q):
	height, width = imgArray.shape
	momPQ = 0
	for xx in range(width):
		for yy in range(height):
			momPQ += (xx**p)*(yy**q)*int(imgArray[yy, xx])
	return momPQ

def momentoCentral(imgArray, p, q):
	height, width = imgArray.shape
	momCenPQ = 0
	xBarra = momento(imgArray, 1, 0)/momento(imgArray, 0, 0)
	yBarra = momento(imgArray, 0, 1)/momento(imgArray, 0, 0)
	for xx in range(width):
		for yy in range(height):
			momCenPQ += ((xx - xBarra)**p)*((yy - yBarra)**q)*int(imgArray[yy, xx])
	return momCenPQ

def gama(p, q):
	return ( ((p+q)/2) + 1 )

def momentosInvariantes(img):
	path = "Images"
	im = Image.open(os.path.join(path, img), "r")
	imageArray = numpy.array(im, dtype=numpy.uint8)
	n20 = momentoCentral(imageArray, 2, 0)/(momentoCentral(imageArray, 0, 0) ** gama(2, 0))
	n02 = momentoCentral(imageArray, 0, 2)/(momentoCentral(imageArray, 0, 0) ** gama(0, 2))
	n30 = momentoCentral(imageArray, 3, 0)/(momentoCentral(imageArray, 0, 0) ** gama(3, 0))
	n03 = momentoCentral(imageArray, 0, 3)/(momentoCentral(imageArray, 0, 0) ** gama(0, 3))
	n12 = momentoCentral(imageArray, 1, 2)/(momentoCentral(imageArray, 0, 0) ** gama(1, 2))
	n21 = momentoCentral(imageArray, 2, 1)/(momentoCentral(imageArray, 0, 0) ** gama(2, 1))
	n11 = momentoCentral(imageArray, 1, 1)/(momentoCentral(imageArray, 0, 0) ** gama(1, 1))
	
	mi1 = n20 + n02
	mi2 = (n20 - n02)**2 + 4*((n11)**2)
	mi3 = (n30 - (3*n12))**2 + ((3*n21) - n03)**2
	mi4 = (n30 + n12)**2 + (n21 - n03)**2
	mi5 = (n30 - (3*n12))*(n30 + n12)*((n30+n12)**2 - 3*((n21+n03)**2)) + ((3*n21) - n03)*(n21 + n03)*(3*((n30 + n12)**2) - (n21 + n03)**2)
	mi6 = (n20 - n02)*( ((n30+n12)**2) - (n21 + n03)**2 ) + 4*n11*(n30 + n12)*(n21 + n03)
	mi7 = ((3*n21) - n03)*(n30 + n12)*(((n30 + n12)**2) - 3*((n21 + n03)**2)) + ((3*n12) - n30)*(n21 + n03)*(3*((n30 + n12)**2) - (n21 + n03)**2)
	momInv = numpy.array([mi1, mi2, mi3, mi4, mi5, mi6, mi7])
	numpy.savetxt("momentosInvariantes_" + img[:-4] + ".txt", momInv, delimiter=",")


begin = time.time()
#chaincode("elephant.bmp")
#skeleton("elephant.bmp")
#mpp("elephant.bmp")
# momentosInvariantes("dog_(1).jpg")
# momentosInvariantes("dog_(2).jpg")
# momentosInvariantes("dog_(3).jpg")
# momentosInvariantes("teste_(1).jpg")
# momentosInvariantes("teste_(2).jpg")
# momentosInvariantes("teste_(3).jpg")
chaincode("Image_(1).bmp", neigh=8)
end = time.time()

print("Finalizado: " + str(round(end-begin, 2)) + "s\n")
