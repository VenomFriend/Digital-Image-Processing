from PIL import Image
import numpy
import math
import time
import os

numpy.set_printoptions(threshold=numpy.nan)


def DFT(array1D, invert):
        M = len(array1D)
        #print("Array 1D Lenght: " + str(M))
        multiplier = 1/(math.sqrt(M))
        #numReal = []
        #numImaginary = []
        numComplete = []
        for m in range(M):
                sumReal = 0
                sumImaginary = 0
                for u in range(M):
                        cosSenAtt = 2 * math.pi * ((m * u)/M)
                        cos = math.cos(cosSenAtt)
                        sin = math.sin(cosSenAtt)
                        if(invert):
                                sin = -sin
                        sumReal += array1D[u] * cos
                        sumImaginary += array1D[u] * -1j * sin
                sumReal *= multiplier
                sumImaginary *= multiplier
                #numReal.append(sumReal)
                #numImaginary.append(sumImaginary)
                #numComplete.append(int(round(numpy.abs(sumReal + sumImaginary))))
                numComplete.append(sumReal + sumImaginary)
        return numComplete

def DFT2D(array2D, invert):
        M = len(array2D)
        N = len(array2D[0])
        #print("Lines: " + str(M))
        #print("Columns: " + str(N))
        firstMatrix = []
        secondMatrix = []

        
        for row in range(M):
                tempRow = []
                for col in range(N):
                        tempRow.append(array2D[row][col])
                newRow = DFT(tempRow, invert)
                firstMatrix.append(newRow)
        for col in range(N):
                tempCol = []
                for row in range(M):
                        tempCol.append(firstMatrix[row][col])
                newCol = DFT(tempCol, invert)
                secondMatrix.append(newCol)
        secondMatrix = list(map(list, zip(*secondMatrix)))
        return secondMatrix


def filter(img):
        path = "Images"
        save_path = os.path.join(path, "result_frequencia", "resultado_" + img)
        im = Image.open(os.path.join(path, img), "r")
        imageArray = numpy.array(im, dtype=numpy.uint8)
        print("Imagem Sem Filtro: ")
        #print(imageArray)
        newImage = DFT2D(imageArray, False)
        #print("Imagem Com Filtro: ")
        #print(newImage)
        newImageInverted = DFT2D(newImage, True)
        print("Imagem Sem Filtro Invertida: ")
        #print(newImageInverted)
        #width, height = im.size
        newImageInverted = numpy.array(newImageInverted)
        newImageInverted = numpy.round(numpy.abs(newImageInverted))
        newImageInverted = newImageInverted.astype(numpy.uint8)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        Image.fromarray(newImageInverted).save(save_path)

testArray = [1, 3, 5, 7, 9, 8, 6, 4, 2, 0]
testMatrix = [[5, 3, 0, 2], [1, 7, 8, 3], [4, 2, 2, 2], [8, 5, 2, 1]]
test2Matrix = [[0,0,0,0,0,0,0,0], [0,0,70,80,90,0,0,0],[0,0,90,100,110,0,0,0],[0,0,110,120,130,0,0,0],[0,0,130,140,150,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]

numpy.set_printoptions(suppress=True)
#print("Original Matrix: ")
#print(numpy.matrix(test2Matrix))
#print("2D DFT Test: ")
#test2D = DFT2D(test2Matrix, False)
#print(numpy.matrix(test2D))
#print("2D DFT Invert Test: ")
#test2DInvert = DFT2D(test2D,True)
#test2DInvert = numpy.array(test2DInvert)
#test2DInvert = numpy.round(numpy.abs(test2DInvert))
#test2DInvert = test2DInvert.astype(int)
#print(numpy.matrix(test2DInvert))

begin = time.time()
#filter("Agucar_(1).jpg")
filter("Agucar_(2).jpg")
end = time.time()

print("Finalizado: " + str(round(end-begin, 2)) + "s\n")
