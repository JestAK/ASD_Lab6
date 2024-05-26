# n1 = 3
# n2 = 2
# n3 = 1
# n4 = 3

import math
import random
import turtle
from copy import deepcopy
from turtle import *
import keyboard

turtle.speed(0)

VERTEX_AMOUNT = 11
VERTEX_RADIUS = 15
FONT_SIZE = 12
FONT = ("Arial", FONT_SIZE, "normal")
SQUARE_SIZE = 500
BREAK_GAP = 10
EXTRA_GAP = 50
K = 1.0 - 1 * 0.01 - 3 * 0.005 - 0.05
TEXT_EDGE_GAP = 1


def drawVertex(x, y, text, obj=turtle):
    obj.up()
    obj.goto(x, y - VERTEX_RADIUS)
    obj.down()
    obj.circle(VERTEX_RADIUS)

    obj.up()
    obj.goto(x, y - VERTEX_RADIUS + FONT_SIZE / 2)
    obj.write(text, align="center", font=FONT)
    obj.down()

def getVertexCoords(vertexAmount, squareSize):
    vertexCoords = []

    squareStartX = -squareSize / 2
    squareStartY = squareSize / 2

    xPos = squareStartX
    yPos = squareStartY

    isXMove = 1
    isYMove = 0

    xDirection = 1
    yDirection = -1

    vertexModulus = vertexAmount % 4
    vertexStep = vertexAmount // 4

    for i in range(4):

        vertexPerSide = vertexStep

        if (vertexModulus > 0):
            vertexPerSide += 1
            vertexModulus -= 1

        if (vertexPerSide > 0): vertexGap = squareSize / vertexPerSide
        else: vertexGap = 0

        for j in range(vertexPerSide):
            vertexCoords.append({"x": round(xPos), "y": round(yPos)})
            xPos += isXMove * xDirection * vertexGap
            yPos += isYMove * yDirection * vertexGap

        xPos = round(xPos)
        yPos = round(yPos)

        if (isXMove):
            isXMove = 0
            isYMove = 1
            xDirection *= -1
        elif (isYMove):
            isYMove = 0
            isXMove = 1
            yDirection *= -1

    return vertexCoords

def generateDirMatrix(vertexAmount, k, floor = True):
    random.seed(3213)

    dirMatrix = []

    for i in range(vertexAmount):
        row = []

        for j in range(vertexAmount):
            randomNumber = random.uniform(0, 2.0)
            if (floor):
                row.append(math.floor(randomNumber * k))
            else:
                row.append(randomNumber * k)

        dirMatrix.append(row)

    return dirMatrix

def dirIntoUndirMatrix(dirMatrix):
    undirMatrix = deepcopy(dirMatrix)

    for i in range(len(undirMatrix)):
        for j in range(len(undirMatrix)):
            if (undirMatrix[i][j] != 0):
                undirMatrix[j][i] = undirMatrix[i][j]

    return undirMatrix

def getFi(vector):
    cosFi = vector[0] / math.sqrt(vector[0] ** 2 + vector[1] ** 2)
    fi = math.degrees(math.acos(cosFi))
    if (vector[1] < 0): fi = 360 - fi
    return fi

def arrow(startX, startY, endX, endY, fi=None, obj=turtle):
    vector = [endX - startX, endY - startY]
    if (fi == None):
        fi = 180 + getFi(vector)
    fi = math.pi * fi / 180
    lx = endX + 15 * math.cos(fi + 0.3)
    rx = endX + 15 * math.cos(fi - 0.3)
    ly = endY + 15 * math.sin(fi + 0.3)
    ry = endY + 15 * math.sin(fi - 0.3)

    drawLine(endX, endY, lx, ly, False, obj)
    drawLine(endX, endY, rx, ry, False, obj)

def drawLine(startX, startY, endX, endY, withArrow=False, obj=turtle):
    obj.up()
    obj.goto(startX, startY)
    obj.down()
    obj.goto(endX, endY)

    if (withArrow == True):
        arrow(startX, startY, endX, endY, obj=obj)

def getOrtVector(startX, startY, endX, endY):
    vector = [endX - startX, endY - startY]
    vectorLenght = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
    ortVector = [vector[0] / vectorLenght, vector[1] / vectorLenght]
    return ortVector

def normVector(ortVector):
    nVector = [-ortVector[1], ortVector[0]]
    return nVector

def isOnSameSide(Ax, Ay, Bx, By):
    if((Ax == Bx) and (abs(Ax) == SQUARE_SIZE/2)): return True
    elif((Ay == By) and (abs(Ay) == SQUARE_SIZE/2)): return True
    else: return False

def vertexBetween(vertexA, vertexB):
    distance = min(abs(vertexB - vertexA), VERTEX_AMOUNT - abs(vertexB - vertexA))
    return distance

dirMatrix = generateDirMatrix(VERTEX_AMOUNT, K)

def generateMatrixC(matrixA, matrixB):
    result = []
    for i in range(len(matrixA)):
        resultRow = []
        for j in range(len(matrixA[0])):
            resultRow.append(math.ceil(matrixA[i][j] * matrixB[i][j] * 100))
        result.append(resultRow)
    return result

def generateMatrixD(matrixC):
    result = []
    for i in range(len(matrixC)):
        resultRow = []
        for j in range(len(matrixC[0])):
            if (matrixC[i][j] > 0):
                resultRow.append(1)
            else:
                resultRow.append(0)
        result.append(resultRow)
    return result

def generateMatrixH(matrixD):
    result = []
    for i in range(len(matrixD)):
        resultRow = []
        for j in range(len(matrixD[0])):
            if (matrixD[i][j] != matrixD[j][i]):
                resultRow.append(1)
            else:
                resultRow.append(0)
        result.append(resultRow)
    return result

def generateMatrixTr(vertexAmount):
    result = []
    for i in range(vertexAmount):
        resultRow = []
        for j in range(vertexAmount):
            if (i < j):
                resultRow.append(1)
            else:
                resultRow.append(0)
        result.append(resultRow)
    return result

def generateMatrixW(matrixD, matrixH, matrixTr, matrixC):
    result = []
    for i in range(len(matrixD)):
        resultRow = []
        for j in range(len(matrixD[0])):
            resultRow.append((matrixD[i][j] + matrixH[i][j] * matrixTr[i][j]) * matrixC[i][j])
        result.append(resultRow)
    return dirIntoUndirMatrix(result)

matrixB = generateDirMatrix(VERTEX_AMOUNT, K, False)
matrixC = generateMatrixC(dirIntoUndirMatrix(dirMatrix), matrixB)
matrixD = generateMatrixD(matrixC)
matrixH = generateMatrixH(matrixD)
matrixTr = generateMatrixTr(VERTEX_AMOUNT)
matrixW = generateMatrixW(matrixD, matrixH, matrixTr, matrixC)

print("WEIGHT MATRIX")
for row in matrixW:
    print(row)
print("\n")

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def addNode(self, data):
        if (self.head == None):
            self.head = Node(data)
        else:
            newNode = Node(data)
            newNode.next = self.head
            self.head = newNode

    def removeNode(self, data):
        if self.head == None:
            return

        currentNode = self.head

        while (currentNode.next.data != data):
            currentNode = currentNode.next

        currentNode.next = currentNode.next.next

    def printLinkedList(self):
        currentNode = self.head
        while (currentNode != None):
            print(currentNode.data)
            currentNode = currentNode.next

    def findByIndex(self, index):
        if self.head == None:
            return None

        currentNode = self.head
        currentIndex = 0

        while (currentNode != None):
            if (currentIndex == index):
                return currentNode.data
            currentNode = currentNode.next
            currentIndex += 1

        return None

    def findByData(self, data):
        if self.head == None:
            return None

        currentNode = self.head
        currentIndex = 0

        while (currentNode != None):
            if (currentNode.data == data):
                return currentIndex
            currentNode = currentNode.next
            currentIndex += 1

        return None

    def getLength(self):
        if self.head == None:
            return None

        currentNode = self.head
        length = 0

        while (currentNode != None):
            length += 1
            currentNode = currentNode.next

        return length

class Vertex:
    def __init__(self, number):
        self.number = number

class Edge:
    def __init__(self, start, end, weight):
        self.start = start
        self.end = end
        self.weight = weight

def drawEdge(vertexA, vertexB, graphType, isDoubleWay, obj = turtle):


    if (graphType == "dir"): withArrow = True
    elif (graphType == "undir"): withArrow = False
    vertexCoords = getVertexCoords(VERTEX_AMOUNT, SQUARE_SIZE)
    startX = vertexCoords[vertexA]["x"]
    startY = vertexCoords[vertexA]["y"]
    if (vertexA == vertexB):
        fi = round(getFi([startX, startY]))
        if (((0 < fi) and (fi < 45)) or ((315 < fi) and (fi < 360))):
            fi = 0
            obj.setheading(270)
        elif (((45 < fi) and (fi < 135))):
            fi = 90
            obj.setheading(0)
        elif (((135 < fi) and (fi < 225))):
            fi = 180
            obj.setheading(90)
        elif (((225 < fi) and (fi < 315))):
            fi = 270
            obj.setheading(180)
        elif (fi == 45):
            obj.setheading(315)
        elif (fi == 135):
            obj.setheading(45)
        elif (fi == 225):
            obj.setheading(135)
        else:
            obj.setheading(225)

        obj.up()
        obj.goto(startX + math.cos(math.radians(fi)) * VERTEX_RADIUS, startY + math.sin(math.radians(fi)) * VERTEX_RADIUS)
        obj.down()
        obj.circle(10)
        if (graphType == "dir"):
            arrow(turtle.pos()[0], turtle.pos()[1], turtle.pos()[0], turtle.pos()[1],
                  150 + turtle.heading(), obj)

    else:
        extraGapVector = [0, 0]
        endX = vertexCoords[vertexB]["x"]
        endY = vertexCoords[vertexB]["y"]
        midX = (startX + endX) / 2
        midY = (startY + endY) / 2
        ortVector = getOrtVector(startX, startY, endX, endY)

        if (isOnSameSide(startX, startY, endX, endY)):
            vBetween = vertexBetween(vertexA, vertexB) - 1
            extraGapOrtVector = getOrtVector(0, 0, midX, midY)
            extraGapVector = [extraGapOrtVector[0] * EXTRA_GAP * vBetween, extraGapOrtVector[1] * EXTRA_GAP * vBetween]

        if (isDoubleWay == True and graphType == "dir"):
            nVector = normVector(ortVector)
            nVector[0] = nVector[0] * BREAK_GAP
            nVector[1] = nVector[1] * BREAK_GAP
            drawLine(startX + ortVector[0] * 15, startY + ortVector[1] * 15,
                     midX + nVector[0] + extraGapVector[0],
                     midY + nVector[1] + extraGapVector[1], False, obj)
            drawLine(midX + nVector[0] + extraGapVector[0], midY + nVector[1] + extraGapVector[1],
                     endX - ortVector[0] * 15,
                     endY - ortVector[1] * 15, True, obj)

        else:
            drawLine(startX + ortVector[0] * 15, startY + ortVector[1] * 15,
                     midX + extraGapVector[0],
                     midY + extraGapVector[1], False, obj)
            drawLine(midX + extraGapVector[0], midY + extraGapVector[1],
                     endX - ortVector[0] * 15,
                     endY - ortVector[1] * 15, withArrow, obj)

        nVector = normVector(ortVector)
        nVector[0] = nVector[0] * BREAK_GAP
        nVector[1] = nVector[1] * BREAK_GAP
        textPosX = midX - nVector[0] + extraGapVector[0]
        textPosY = midY - nVector[1] + extraGapVector[1]
        obj.up()
        obj.goto(textPosX, textPosY)
        obj.down()
        obj.write(matrixW[vertexA][vertexB], align='center', font=("Arial", 6, "normal"))
        obj.up()



def createGraph(VERTEX_AMOUNT, VERTEX_RADIUS, SQUARE_SIZE, BREAK_GAP, EXTRA_GAP, dirMatrix, graphType):
    vertexCoords = getVertexCoords(VERTEX_AMOUNT, SQUARE_SIZE)

    matrix = dirMatrix

    if (graphType == "undir"):
        undirMatrix = dirIntoUndirMatrix(dirMatrix)

        for row in undirMatrix:
            print(row)

        matrix = undirMatrix
    else:
        for row in dirMatrix:
            print(row)

    for i in range(len(vertexCoords)):
        x = vertexCoords[i]["x"]
        y = vertexCoords[i]["y"]
        drawVertex(x, y, str(i + 1))

    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if (matrix[i][j] == 1):
                if (matrix[j][i] == 1 and graphType == "dir"):
                    drawEdge(i, j, graphType, True)
                else:
                    drawEdge(i, j, graphType, False)
            if (graphType == "undir" and i == j):
                break



    turtle.setheading(0)

graphType = "undir"
createGraph(VERTEX_AMOUNT, VERTEX_RADIUS, SQUARE_SIZE, BREAK_GAP, EXTRA_GAP, dirMatrix, graphType)

def spanningTree(obj, matrixW):
    verteces = LinkedList()
    edges = LinkedList()
    verteces.addNode(0)
    haveFreeVerteces = True
    totalWeight = 0

    while(haveFreeVerteces):
        haveFreeVerteces = False

        vertecesIter = 0
        start = None
        end = None
        weight = math.inf
        listLength = verteces.getLength()
        while (vertecesIter != listLength):
            for column in range(len(matrixW)):
                if (matrixW[verteces.findByIndex(vertecesIter)][column] != 0 and verteces.findByIndex(vertecesIter) != column):
                    if (verteces.findByData(column) == None):
                        if (matrixW[verteces.findByIndex(vertecesIter)][column] < weight):
                            start = verteces.findByIndex(vertecesIter)
                            end = column
                            weight = matrixW[verteces.findByIndex(vertecesIter)][column]
                            haveFreeVerteces = True
            vertecesIter += 1

        if (haveFreeVerteces):
            verteces.addNode(end)
            edges.addNode(Edge(start, end, weight))
            totalWeight += weight

    obj.color("red")
    edgesIter = edges.getLength() - 1
    while (edgesIter != -1):
        edgeData = edges.findByIndex(edgesIter)
        keyboard.wait("space")
        drawEdge(edgeData.start, edgeData.end, "undir", False, obj)
        edgesIter -= 1

    print("TOTAL WEIGHT:")
    print(totalWeight)


class Button:
    def __init__(self, x, y, width, height, label, function, fontSize=12, color="white"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.label = label
        self.function = function
        self.fontSize = fontSize
        self.color = color

    def drawButton(self):
        up()
        goto(self.x - self.width / 2, self.y - self.height / 2)
        down()
        turtle.fillcolor(self.color)
        turtle.begin_fill()
        for i in range(2):
            turtle.forward(self.width)
            turtle.left(90)
            turtle.forward(self.height)
            turtle.left(90)
        turtle.end_fill()

        up()
        goto(self.x, self.y - self.fontSize/2)
        write(self.label, align="center", font=("Arial", self.fontSize, "normal"))

    def isButtonClicked(self, clickX, clickY):
        return ((self.x - self.width / 2 <= clickX <= self.x + self.width / 2) and
                (self.y - self.height / 2 <= clickY <= self.y + self.height / 2))

buttonsArray = []

def buttonClickHandler(x, y):
    for button in buttonsArray:
        if button.isButtonClicked(x, y):
            button.function()

spTree = turtle.Turtle()

STButton = Button(-400, 400, 140, 40, "Spanning Tree", lambda: spanningTree(spTree, matrixW))
buttonsArray.append(STButton)
STButton.drawButton()

turtle.onscreenclick(buttonClickHandler)

turtle.done()
