# 15-112, Summer 2, Term Project
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Full name: Oktay Comu
# Andrew ID: ocomu
# Section: C
# Created: 26.7.2017  19:39
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# WORKS CITED
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Animation MVC barebones from course notes:
#    https://pd43.github.io/notes/code/events-example0.py
#
# Vector rotation algorithms from stackoverflow:
#    https://stackoverflow.com/questions/14607640/rotating-a-vector-in-3d-space
#
# Tkinter open file dialog from Youtube video and comments:
#    https://www.youtube.com/watch?v=iUmqLGUktek
#
# Tkinter save file dialog from Stack Overflow:
#    https://stackoverflow.com/questions/19476232/save-file-dialog-in-tkinter
#
# Tkinter additional UI elements form tutorialspoint:
#    https://www.tutorialspoint.com/python/python_gui_programming.htm
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


import math
from tkinter import *
from tkinter import filedialog


# # # # # # # # # # # # # # # # # # # #
# Classes
# # # # # # # # # # # # # # # # # # # #

class Vector3(object):
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return '{ x: %f, y: %f, z: %f }' % (self.x, self.y, self.z)

    def __add__(self, other):
        # Add x,y,z coordinates together
        if type(other) == Vector3:
            return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        # Subtract x,y,z coordinates from one another
        if type(other) == Vector3:
            return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def getX(self):
        return self.x

    def setX(self, x):
        self.x = x

    def getY(self):
        return self.y

    def setY(self, y):
        self.y = y

    def getZ(self):
        return self.z

    def setZ(self, z):
        self.z = z

    # rotation algorithms from stack overflow
    # https://stackoverflow.com/questions/14607640/rotating-a-vector-in-3d-space

    def rotateX(self, a):
        # Rotate around the X axis
        self.y, self.z = self.y * math.cos(a) - self.z * math.sin(a), \
                         self.y * math.sin(a) + self.z * math.cos(a)

    def rotateY(self, a):
        # Rotate around the Y axis
        self.x, self.z = self.x * math.cos(a) + self.z * math.sin(a), \
                         -self.x * math.sin(a) + self.z * math.cos(a)

    def rotateZ(self, a):
        # Rotate around the Z axis
        self.x, self.y = self.x * math.cos(a) - self.y * math.sin(a), \
                         self.x * math.sin(a) + self.y * math.cos(a)

    # vector operations

    def dot(self, vect):
        # dot product
        return self.x * vect.x + self.y * vect.y + self.z * vect.z

    def cross(self, vect):
        # cross product
        return Vector3(self.y * vect.z - self.z * vect.y,
                       self.z * vect.x - self.x * vect.z,
                       self.x * vect.y - self.y * vect.x)

    def getSize(self):
        return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5

    def getCamVals(self, data):
        # translate 3D coordinates into 2D position by taking the dot product
        # of the difference vector from the camera to the vertex with the
        # x and y unit vectors of the camera and scaling them according to
        # their distances from the camera
        tempVect = self - data.camera.position
        camDistance = tempVect.getSize()

        if camDistance >= 0 or True:
            return (
                data.width / 2 - tempVect.dot(
                    data.camera.xVector) / camDistance * 1000,
                data.height / 2 + tempVect.dot(
                    data.camera.yVector) / camDistance * 1000
            )
        return None

    def getDistance(self, pos):
        return ((self.x - pos.x) ** 2 + (self.y - pos.y) ** 2 + (
                    self.z - pos.z) ** 2) ** 0.5

    def getTuple(self):
        return (self.x, self.y, self.z)


class Object(object):
    def __init__(self, faces=[]):
        self.face = faces


class Camera(object):
    def __init__(self, x, y, z, alpha, beta, radius, fX=0, fY=0, fZ=0):
        self.position = Vector3(x, y, z)
        self.focus = Vector3(fX, fY, fZ)
        self.a = alpha
        self.b = beta
        self.radius = radius
        self.renderList = []
        self.renderVertex = []
        self.renderGrid = []
        self.updateVectors()

    def getPos(self):
        return self.position

    def setPos(self, vector):
        if type(vector) == Vector3:
            self.position = vector

    def getAlpha(self):
        return self.a

    def setAlpha(self, a):
        self.a = 0 if a < 0 else (math.pi / 2 if a > math.pi / 2 else a)
        self.updateVectors()

    def getBeta(self):
        return self.b

    def setBeta(self, a):
        self.b = a
        self.updateVectors()

    def getRadius(self):
        return self.radius

    def setRadius(self, r):
        self.radius = r
        self.updateVectors()
        self.updateArcPos()

    def updateVectors(self):
        # initialize rotation vectors according to the x and y axis and then
        # rotate them according to the alpha and beta angles of the camera
        self.xVector = Vector3(1, 0, 0)
        self.xVector.rotateY(self.b)
        self.yVector = Vector3(0, -1, 0)
        self.yVector.rotateX(self.a)
        self.yVector.rotateY(self.b)
        self.zVector = self.yVector.cross(self.xVector)

    def updateArcPos(self):
        self.position = Vector3(
            self.focus.x - math.sin(self.b) * math.cos(self.a) * self.radius,
            self.focus.y + math.sin(self.a) * self.radius,
            self.focus.z - math.cos(self.b) * math.cos(self.a) * self.radius
        )

    def updateRenderVertex(self, data):
        res = []
        # put the translated 2D vertex positions into the renderVertex list
        # preserving the order that they appear in
        for v in data.vertex:
            res.append(v.getCamVals(data))
        self.renderVertex = res

    def updateRenderList(self, data):
        self.updateRenderVertex(data)

        if self.renderList == []:
            res = []
            for obj in data.object:
                res.extend(data.object[obj].face)
            # sort the faces according to the average distance of all their
            # vertices so that the face closest to the camera is drawn last
            # (painter's algorithm)
            self.renderList = sorted(res, reverse=True, key=lambda item:
            getAverageDistanceToCamera(data, item))
        else:
            self.renderList = sorted(self.renderList, reverse=True,
                                     key=lambda
                                         item: getAverageDistanceToCamera(data,
                                                                          item))

        # Update grid points
        self.renderGrid = []
        for face in data.gridDots:
            self.renderGrid.append([v.getCamVals(data) for v in face])

        data.drawUpdate = True


def getAverageDistanceToCamera(data, l):
    total = 0
    for i in l:
        total += (data.vertex[i - 1] - data.camera.getPos()).getSize()
    return total / len(l)


def distance(x1, y1, x2, y2):
    # distance between two points
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


# Animation barebones from course notes

# events-example0.py
# Barebones timer, mouse, and keyboard events


# MODEL VIEW CONTROLLER (MVC)
####################################
# MODEL:       the data
# VIEW:        redrawAll and its helper functions
# CONTROLLER:  event-handling functions and their helper functions
####################################


####################################
# customize these functions
####################################


# Initialize the data which will be used to draw on the screen.

def getVerticesInList(l):
    result = []
    for e in l:
        e = e.split('/')[0]
        if type(e) == str and len(e) > 0 and e.isdigit():
            result.append(int(e))
    return result


def getFloatsInList(l):
    result = []
    for e in l:
        test = e.replace('.', '', 1)
        if type(test) == str and len(test) > 0:
            if test.isdigit() or (test[0] == '-' and test[1:].isdigit()):
                result.append(float(e))
            elif 'e' in test:
                result.append(0)

    return result


def printObj(obj):
    print('OBJECT:\n\tFaces:')
    for i in range(len(obj.face)):
        print('\t f' + str(i + 1), '\t%s' % obj.face[i])


def openFile(data):
    # open .obj file and parse all its lines. Store all vertices and faces into
    # the data instance

    # Source: File dialog tutorial:
    # https://www.youtube.com/watch?v=iUmqLGUktek
    tempDir = filedialog.askopenfilename(filetypes=[('OBJ File', '*.obj')],
                                         title='Open OBJ File To Edit...')
    if tempDir == '' or tempDir[-4:-1] + tempDir[-1] != '.obj':
        return False
    data.fileDir = tempDir

    print('\n\n\n LOADING NEW FILE... \n\n\n')
    data.object, data.vertex, data.camera.renderList, objCount = dict(), [], [], 0
    data.object[objCount] = Object([])
    data.tempSelect, data.openFileLines, lastChar = None, [], 'v'
    deselectVertex(data)

    data.fileText.set(data.fileDir)

    mini = 0
    with open(data.fileDir) as f:
        for line in f:
            data.openFileLines.append(line)
            splitLine = line.strip().split(' ')
            if splitLine[0] == 'v':
                if lastChar != 'v':
                    objCount += 1
                    lastChar = 'v'
                    data.object[objCount] = Object([])
                numsInLine = getFloatsInList(splitLine)
                x, y, z = numsInLine[0], numsInLine[1], numsInLine[2]
                mini = min(y, mini)
                data.vertex.append(Vector3(x, y, z))
            elif splitLine[0] == 'f':
                lastChar = 'f'
                data.object[objCount].face.append(getVerticesInList(splitLine))

    for v in data.vertex:
        v.setY(v.getY() - mini)

    for obj in data.object:
        print('Object %s:\n' % obj)
        printObj(data.object[obj])

    maxi = 0
    for v in data.vertex:
        maxi = max(v.getSize(), maxi)
    # set the camera radius so that it covers most of the objects
    data.camera.setRadius(maxi * 4)
    data.camera.updateRenderList(data)


def saveFile(data):
    # only open save as dialog if there is already an open file
    if len(data.openFileLines) < 1:
        return
    # Source: Stack Overflow:
    # https://stackoverflow.com/questions/19476232/save-file-dialog-in-tkinter
    fileName = filedialog.asksaveasfilename(defaultextension='.obj',
                                            initialfile='newFile.obj',
                                            title='Save OBJ File As...',
                                            filetypes=[('OBJ File', '*.obj')])
    if len(fileName) < 3:
        return
    with open(fileName, 'w+') as f:
        vCount = 0
        for line in data.openFileLines:
            splitLine = line.strip().split(' ')
            if splitLine[0] == 'v':
                (splitLine[1], splitLine[2], splitLine[3]) = \
                    (str(data.vertex[vCount].x),
                     str(data.vertex[vCount].y),
                     str(data.vertex[vCount].z))
                splitLine.append('\n')
                f.write(' '.join(splitLine))
                vCount += 1
            else:
                f.write(line)


def updateDraw(data):
    data.drawUpdate = True


def initTopFrame(data):
    data.topFrame = Frame(data.root, bg="gray",
                          bd=5, padx=128, pady=5, relief=GROOVE)

    data.openButton = Button(data.topFrame, text="Save As", command=lambda:
    saveFile(data))
    data.openButton.grid(row=0, column=0)

    data.topPadding.append(Label(data.topFrame, text="", bg="gray", padx=2))
    data.topPadding[-1].grid(row=0, column=1)

    data.openButton = Button(data.topFrame, text="Open", command=lambda:
    openFile(data))
    data.openButton.grid(row=0, column=2)

    data.topPadding.append(Label(data.topFrame, text="", bg="gray", padx=2))
    data.topPadding[-1].grid(row=0, column=3)

    data.fileText = StringVar()
    data.fileText.set('Open a .obj file...')
    data.fileTextLabel = Label(data.topFrame, textvariable=data.fileText,
                               bg="gray", fg="white")
    data.fileTextLabel.grid(row=0, column=4)

    data.topFrame.pack(side=TOP)


def initBotFrame(data):
    data.botFrame = Frame(data.root, bg="gray",
                          bd=5, padx=128, pady=2, relief=GROOVE)
    data.botLeftFrame = LabelFrame(data.botFrame, bg="gray", relief=GROOVE)
    data.botRightFrame = LabelFrame(data.botFrame, bg="gray", relief=GROOVE)

    data.botPadding.append(Label(data.botLeftFrame, text=" ", bg="gray"))
    data.botPadding[-1].grid(row=0, column=0)

    # X-ray button
    data.xrayCheck = Checkbutton(data.botLeftFrame, text="X-RAY",
                                 variable=data.faceColor, onvalue='',
                                 offvalue='pink', fg="white", bg="gray",
                                 font="msserif 10 bold", selectcolor="gray20",
                                 command=lambda: updateDraw(data))
    data.xrayCheck.grid(row=0, column=1)

    data.botPadding.append(Label(data.botLeftFrame, text="  ", bg="gray"))
    data.botPadding[-1].grid(row=0, column=2)

    # Grid button
    data.gridCheck = Checkbutton(data.botLeftFrame, text="GRID",
                                 variable=data.showGrid,
                                 onvalue=True, offvalue=False, fg="white",
                                 bg="gray",
                                 font="msserif 10 bold", selectcolor="gray20",
                                 command=lambda: updateDraw(data))
    data.gridCheck.grid(row=0, column=3)

    data.botPadding.append(Label(data.botLeftFrame, text="  ", bg="gray"))
    data.botPadding[-1].grid(row=0, column=4)

    # Vector Position X Entry
    data.botPadding.append(Label(data.botRightFrame, text="Vertex  {  x:",
                                 bg="gray", padx=10, fg="white", bd=2, pady=3,
                                 font="msserif 10 bold"))
    data.botPadding[-1].grid(row=0, column=3)

    data.vEntryXVar = StringVar()
    data.vEntryXVar.set(0)
    data.vEntryX = Entry(data.botRightFrame, fg="white", bg="gray20", width=7,
                         font="msserif 10 bold", textvariable=data.vEntryXVar)
    data.vEntryX.bind('<KeyRelease>', lambda event:
    vertexEntryCheck(data, 'X', event))
    data.vEntryX.bind('<MouseWheel>', lambda event:
    vertexEntryScroll(data, 'X', event))
    data.vEntryX.grid(row=0, column=4)

    # Vector Position Y Entry
    data.botPadding.append(Label(data.botRightFrame, text=" y:",
                                 bg="gray", padx=10, fg="white", bd=2,
                                 font="msserif 10 bold"))
    data.botPadding[-1].grid(row=0, column=5)

    data.vEntryYVar = StringVar()
    data.vEntryYVar.set(0)
    data.vEntryY = Entry(data.botRightFrame, fg="white", bg="gray20", width=7,
                         font="msserif 10 bold", textvariable=data.vEntryYVar)
    data.vEntryY.bind('<KeyRelease>', lambda event:
    vertexEntryCheck(data, 'Y', event))
    data.vEntryY.bind('<MouseWheel>', lambda event:
    vertexEntryScroll(data, 'Y', event))
    data.vEntryY.grid(row=0, column=6)

    # Vector Position Z Entry
    data.botPadding.append(Label(data.botRightFrame, text=" z:",
                                 bg="gray", padx=10, fg="white", bd=2,
                                 font="msserif 10 bold"))
    data.botPadding[-1].grid(row=0, column=7)

    data.vEntryZVar = StringVar()
    data.vEntryZVar.set(0)
    data.vEntryZ = Entry(data.botRightFrame, fg="white", bg="gray20", width=7,
                         font="msserif 10 bold", textvariable=data.vEntryZVar)
    data.vEntryZ.bind('<KeyRelease>', lambda event:
    vertexEntryCheck(data, 'Z', event))
    data.vEntryZ.bind('<MouseWheel>', lambda event:
    vertexEntryScroll(data, 'Z', event))
    data.vEntryZ.grid(row=0, column=8)

    data.botPadding.append(Label(data.botRightFrame, text=" }",
                                 bg="gray", padx=10, fg="white", bd=2,
                                 font="msserif 10 bold"))
    data.botPadding[-1].grid(row=0, column=9)

    data.botLeftFrame.pack(side=LEFT)
    data.botRightFrame.pack(side=RIGHT)
    data.botFrame.pack(side=BOTTOM)


def vertexEntryCheck(data, box, event):
    # check if entered vertex coordinates are valid and apply them if they are

    entryBox = data.__dict__['vEntry' + box]
    entryVar = data.__dict__['vEntry' + box + 'Var']
    test = entryVar.get().replace('.', '', 1)
    if type(test) == str and len(test) > 0:
        if test.isdigit() or (test[0] == '-' and test[1:].isdigit()):
            if data.curSelect != None:
                data.vertex[data.curSelect].__dict__[box.lower()] = \
                    float(entryVar.get())
                data.camUpdate = True
            return None

    if data.curSelect == None:
        entryVar.set(0)
    else:
        entryVar.set(data.vertex[data.curSelect].__dict__[box.lower()])


def vertexEntryScroll(data, box, event):
    if data.curSelect != None:
        res = data.vertex[data.curSelect].__dict__[box.lower()] + \
              event.delta * (data.camera.radius + 10) / 12000
        data.vertex[data.curSelect].__dict__[box.lower()] = res
        data.__dict__['vEntry' + box + 'Var'].set(res)
        data.camUpdate = True


def init(data):
    # load data as appropriate
    data.lastMousePosX = None
    data.lastMousePosY = None
    data.showInfo = True
    data.faceColor = StringVar()
    data.faceColor.set('pink')
    data.showGrid = BooleanVar()
    data.showGrid.set(True)
    data.botPadding = []
    data.topPadding = []
    data.camUpdate = True
    data.drawUpdate = True
    data.fileDir = ""
    data.object = dict()
    data.vertex = []
    data.gridDots = []
    data.mouseX = 0
    data.mouseY = 0
    data.mouseMoved = False
    data.tempSelect = None
    data.curSelect = None
    data.openFileLines = []

    data.root.title("A 3D Editor by Oktay Comu")
    data.root.resizable(width=False, height=False)

    # UI Elements
    # Source: Additional UI element information from
    # https://www.tutorialspoint.com/python/python_gui_programming.htm

    initTopFrame(data)
    initBotFrame(data)

    data.camera = Camera(0, 0, 0, math.pi / 4, 0, 15, 0, 2, 0)
    data.camera.updateArcPos()

    # Initialize grid points
    for i in range(20):
        for j in range(20):
            data.gridDots.append(
                [Vector3(i - 10, 0, j - 10), Vector3(i - 10, 0, j - 9),
                 Vector3(i - 9, 0, j - 9), Vector3(i - 9, 0, j - 10)])
            data.camera.renderGrid.append(
                [v.getCamVals(data) for v in data.gridDots[-1]])


# These are the CONTROLLERs.
# IMPORTANT: CONTROLLER does *not* draw at all!
# It only modifies data according to the events.

def selectVertex(data, i):
    data.curSelect = i
    data.vEntryXVar.set(data.vertex[i].x)
    data.vEntryYVar.set(data.vertex[i].y)
    data.vEntryZVar.set(data.vertex[i].z)


def deselectVertex(data):
    data.curSelect = None
    data.vEntryXVar.set(0)
    data.vEntryYVar.set(0)
    data.vEntryZVar.set(0)


def mousePressed(event, data):
    # use event.x and event.y
    if data.tempSelect != None:
        if data.tempSelect == data.curSelect:
            deselectVertex(data)
        else:
            selectVertex(data, data.tempSelect)
        data.drawUpdate = True


def keyPressed(event, data):
    if event.keysym == "Up":
        data.camera.setAlpha(data.camera.a + math.pi / 90)
    elif event.keysym == "Down":
        data.camera.setAlpha(data.camera.a - math.pi / 90)
    data.camera.updateRenderList(data)


def mouseMotion(event, data):
    data.mouseX, data.mouseY, data.mouseMoved = event.x, event.y, True
    data.drawUpdate = True


def b1Motion(event, data):
    # rotate the camera while clicking and dragging
    if data.lastMousePosX == None:
        data.lastMousePosX, data.lastMousePosY = event.x, event.y
    else:
        dX, dY = event.x - data.lastMousePosX, event.y - data.lastMousePosY
        data.camera.setAlpha((data.camera.a + dY / 800))
        data.camera.setBeta((data.camera.b - dX / 800))
        data.lastMousePosX, data.lastMousePosY = event.x, event.y
        data.camUpdate = True


def mouseReleased(event, data):
    data.lastMousePosX, data.lastMousePosY = None, None


def mouseWheel(event, data):
    # Scale camera zoom speed according to the radius of the camera
    # This makes it so it doesn't take years for the camera to zoom in
    # if the object is too bi and the camera is too far away
    data.camera.radius = max(
        data.camera.radius - event.delta * (data.camera.radius + 1) / 1000, 0)
    data.camUpdate = True


def timerFired(data):
    if data.camUpdate:
        data.camera.updateArcPos()
        data.camera.updateRenderList(data)
        data.camUpdate = False
    if data.mouseMoved:
        # find closest vertex to mouse and highlight it if it is within
        # 6 pixels of the mouse
        mini = 9999
        minIndex = None
        for i in range(len(data.camera.renderVertex)):
            dist = distance(data.mouseX,
                            data.mouseY,
                            data.camera.renderVertex[i][0],
                            data.camera.renderVertex[i][1])
            if dist < mini:
                mini, minIndex = dist, i
        if mini < 6:
            data.tempSelect = minIndex
        else:
            data.tempSelect = None
        data.mouseMoved = False


# This is the VIEW
# IMPORTANT: VIEW does *not* modify data at all!
# It only draws on the canvas.
def redrawAll(canvas, data):
    # draw in canvas

    # draw grid first so that everything appears on top of it
    if data.showGrid.get():
        for face in data.camera.renderGrid:
            canvas.create_polygon(face, fill='', outline='gray30')

    # draw faces according to the painter's algorithm
    for face in data.camera.renderList:
        if getAverageDistanceToCamera(data, face) > 0:
            canvas.create_polygon(
                [data.camera.renderVertex[i - 1] for i in face],
                fill=data.faceColor.get(), outline='black')

    if data.tempSelect != None:
        select = data.camera.renderVertex[data.tempSelect]
        canvas.create_rectangle(select[0] - 3, select[1] - 3,
                                select[0] + 3, select[1] + 3, fill='red')

    if data.curSelect != None:
        select = data.camera.renderVertex[data.curSelect]
        canvas.create_rectangle(select[0] - 3, select[1] - 3,
                                select[0] + 3, select[1] + 3, fill='yellow')

    if data.showInfo:
        c = data.camera
        canvas.create_text(10, 10, text="""Camera Attributes:\n x:\t%f\n y:\t%f
 z:\t%f\n alpha:\t%f\n beta:\t%f
 """ % (c.position.x, c.position.y, c.position.z, c.a, c.b), anchor='nw')


####################################
####################################
# use the run function as-is
####################################
####################################

# Animation barebones and run() function from course notes:
# https://pd43.github.io/notes/code/events-example0.py

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        if data.drawUpdate:
            canvas.delete(ALL)
            redrawAll(canvas, data)
            canvas.update()
            data.drawUpdate = False

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)

    def motionWrapper(event, canvas, data):
        mouseMotion(event, data)

    def b1MotionWrapper(event, canvas, data):
        b1Motion(event, data)

    def wheelWrapper(event, canvas, data):
        mouseWheel(event, data)

    def releaseWrapper(event, canvas, data):
        mouseReleased(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)

    # Set up data and call init
    class Struct(object):
        pass

    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 20  # milliseconds

    # create the root
    root = Tk()
    root.geometry('1152x648+100+100')
    data.root = root

    init(data)
    # create the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    # new binding events from:
    # https://stackoverflow.com/questions/32289175/list-of-all-tkinter-events
    root.bind("<Button-1>", lambda event:
    mousePressedWrapper(event, canvas, data))
    root.bind("<Motion>", lambda event:
    motionWrapper(event, canvas, data))
    root.bind("<B1-Motion>", lambda event:
    b1MotionWrapper(event, canvas, data))
    root.bind("<ButtonRelease-1>", lambda event:
    releaseWrapper(event, canvas, data))
    canvas.bind("<MouseWheel>", lambda event:
    wheelWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
    keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bOIII !")


run(1152, 648)
