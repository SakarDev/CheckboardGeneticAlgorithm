import random
from PIL import Image
from random import randrange
from copy import deepcopy

error = 10
size = 8
samples = 4
numberOfColors = 4
# initialize random population (4 matrixes)
populations =([[[randrange(numberOfColors) for x in range(size)] for i in range(size)] for i in range(samples)])
parents=[]
halfRowWiseBestParts = []
halfColWiseBestParts = []

def printList3d(list3d):
    for list2d in list3d:
        print("")
        for list1d in list2d:
            print(list1d)
    
def saveAsImages(name):
    colors = [(255,0,0),(0,255,0),(0,0,255),(255,255,255)]
    for index in range(samples):
        img = Image.new("RGB", (size,size))
        pixels = img.load()
        for i in range(size):
            for j in range(size):
                pixels[i,j] = colors[populations[index][i][j]]
        img = img.resize((20*size,20*size), Image.Resampling.NEAREST)
        img.save('C:/geneticAlgorithmImages/'+name+str(index)+'.png')

#calculateFitness
def calculateFitness() :
    global populations,error
    fitnessErr = []
    for sample in populations:  
        error = 0
        for i in range(0,size-1):
            for j in range(0,size-1):
                if(sample[i][j] == sample[i][j+1]):
                    error+=1
                if(sample[i][j] == sample[i+1][j]):
                    error+=1
                if(j==size-2):    
                    if(sample[i][j+1] == sample[i+1][j+1]):
                        error+=1
                if(i==size-2):
                    if(sample[i+1][j] == sample[i+1][j+1]):
                        error+=1
        print('error', error)
        fitnessErr.append(error) 
    # best samples of population will be located at the first indexes (sorted)
    fitnessErr, populations = zip(*sorted(zip(fitnessErr, populations) ))
    print('fitnessErr', fitnessErr)
    print('\n populations sorted by fitnessErr from best to worst')
    printList3d(populations)
    error = fitnessErr[0]

def calculateRowWise(start, end, sample, fitnessErrRowWise):
    global halfRowWiseBestParts
    error = 0
    for i in range(start,end-1):
        for j in range(0,size-1):
            if(sample[i][j] == sample[i][j+1]):
                error+=1
            if(sample[i][j] == sample[i+1][j]):
                error+=1
            if(j==end-2):
                if(sample[i][j+1] == sample[i+1][j+1]):
                    error+=1
            if(i==end-2):
                if(sample[i+1][j] == sample[i+1][j+1]):
                    error+=1
    fitnessErrRowWise +=(error,)
    halfRowWiseBestParts = halfRowWiseBestParts + tuple([[sample[i][0:] for i in range(start,end)]])
    return fitnessErrRowWise
    
def calculateColWise(start, end, sample, fitnessErrColWise):
    global halfColWiseBestParts
    error = 0
    for i in range(start,end-1):
        for j in range(0,size-1):
            if(sample[j][i] == sample[j][i+1]):
                error+=1
            if(sample[j][i] == sample[j+1][i]):
                error+=1
            if(i==end-2):
                if(sample[j][i+1] == sample[j+1][i+1]):
                    error+=1
            if(j==size-2):
                if(sample[j+1][i] == sample[j+1][i+1]):
                    error+=1
    fitnessErrColWise +=(error, )  
    halfColWiseBestParts=halfColWiseBestParts + tuple([[sublist[start:end] for sublist in sample]])
    return fitnessErrColWise
    
def calculateHalfPartFitnessPerEachParent():
    global halfRowWiseBestParts, halfColWiseBestParts, parents, size
    halfSize = int(size/2)
    halfRowWiseBestParts = halfColWiseBestParts = fitnessErrRowWise = fitnessErrColWise = tuple([])
    for sample in parents:
        fitnessErrRowWise = calculateRowWise(0, halfSize, sample, fitnessErrRowWise)     # top half
        fitnessErrRowWise = calculateRowWise(halfSize, size, sample, fitnessErrRowWise)  # bottom half
        fitnessErrColWise = calculateColWise(0, halfSize, sample, fitnessErrColWise)     # left half
        fitnessErrColWise = calculateColWise(halfSize, size, sample, fitnessErrColWise)  # right half
    fitnessErrRowWise, halfRowWiseBestParts = zip(*sorted(zip(fitnessErrRowWise, halfRowWiseBestParts) ))
    fitnessErrColWise, halfColWiseBestParts = zip(*sorted(zip(fitnessErrColWise, halfColWiseBestParts) ))
    print('fitnessErrColWise', fitnessErrColWise)
    print('fitnessErrRowWise', fitnessErrRowWise)
    print('halfRowWiseBestParts')
    printList3d(halfRowWiseBestParts)
    print('halfColWiseBestParts')
    printList3d(halfColWiseBestParts)

    
def selectParent():
    global populations , parents
    parents=populations[0:2]
    printList3d(parents)

def crossover() :
    global parents, populations, halfRowWiseBestParts, halfColWiseBestParts
    parents = parents + tuple([(halfRowWiseBestParts[0] + halfRowWiseBestParts[1])])
    parents = parents + tuple([(halfRowWiseBestParts[1] + halfRowWiseBestParts[0])])
    parents = parents + tuple([(halfRowWiseBestParts[0] + halfRowWiseBestParts[2])])
    parents = parents + tuple([(halfRowWiseBestParts[2] + halfRowWiseBestParts[0])])
    newArr = tuple([[0 for x in range(size)] for j in range(size)] for i in range(1))   
    parents = parents + deepcopy(columnWiseCombination(0, 1, halfColWiseBestParts, newArr))
    parents = parents + deepcopy(columnWiseCombination(1, 0, halfColWiseBestParts, newArr))
    parents = parents + deepcopy(columnWiseCombination(0, 2, halfColWiseBestParts, newArr))
    parents = parents + deepcopy(columnWiseCombination(2, 0, halfColWiseBestParts, newArr))
    populations = parents
    printList3d(populations)
    
def columnWiseCombination(index1, index2, halfColWiseBestParts, newArr):
    for i in range(len(halfColWiseBestParts[0])):
        for j in range(len(halfColWiseBestParts[0][i])):
            newArr[0][i][j] = halfColWiseBestParts[index1][i][j] 
            newArr[0][i][j+4] = halfColWiseBestParts[index2][i][j]
    return newArr
    
def mutation() :
    global populations, parents
    mutate = random.randint(1,10)
    # mutation probability is 0.1
    if mutate == 1 : 
        newValue = random.randint(0,numberOfColors-1)
        x = random.randint(0,len(populations)-1)
        y = random.randint(0,size-1)
        z = random.randint(0,size-1)
        print( f'Mutation happened at x: {x}, y: {y}, z: {z}, old value: {parents[x][y][z]}, new value: {newValue}.')
        parents[x][y][z] = newValue
        populations = parents
        printList3d(populations)
    else:
        print("Mutation didn't happen.")


saveAsImages('original-')   # save the 4 initial dynamic populations
while(error > 0):
    print("\n\n printList3d(populations)")
    printList3d(populations)
    print("\n\n calculateFitness()")
    calculateFitness()
    print("\n\n selectParent()")
    selectParent() 
    print("\n\n calculateHalfPartFitnessPerEachParent()")
    calculateHalfPartFitnessPerEachParent()
    print("\n\n crossover()")
    crossover()
    print("\n\n mutation()")
    mutation()

# save 4 best output images (0.png is the one having no repeated colors in the neighbors )
saveAsImages('output-')
print("\n\n saveAsImages()")
print('Error: ', error, 'in the following matrix: ')
for arr in populations[0]:
    print(arr)

