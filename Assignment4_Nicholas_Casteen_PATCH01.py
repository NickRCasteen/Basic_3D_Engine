#Nicholas Reno Casteen
#102-28-520
#Datestamp: 13/2/2018
#Assignment #4
#------------------------- DESCRIPTION -------------------------
# This is an increment on the graphics engine code, adding implementation for shading models: Faceted, Gouraud, Phong. This also implements lighting models for
# ambient light, point light and specular light. All of these models are applied to 3 shapes in addition to a new cylinder shape.

#STARTUP
import math
from Tkinter import *
from Assignment4_OBJECTS import *
from Assignment4_LIGHTS import *

CanvasWidth = 600
CanvasHeight = 500
d = 500.0

bfc = True #Backface culling
pf = 1 #Polygon Fill
zb = True #Z-buffer

sheps = 1 #0 is for the old gang, 1 is for the new shit

lightmodel = 2 #0 for ambient only, 1 for + point diffus, 2 for + specular
shadingmodel = 1 #0 for faceted, 1 for Gouraud, 2 for Phong

ZBuffer = [] #MIGHT BE SKETCHY. LOOK INTO.
#STARTUP
#DEBUG
debug = 0 #Edges and FTABLE sorting
debug2 = 0 #Multicolor Edges
debug3 = 0 #Pre-pass shower
debug4 = 0 #Current updates
debug5 = 0
debug6 = 0
capturex = 0
capturey = 0
currpoly = 0

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------

#OBJECTS
pyramid = Pyramid()
cube = Cube()
triprism = Tri_Prism()
cyl = pseudo_cylinder()

if sheps == 1:
    ObjList = [cyl]
else:
    ObjList = [pyramid, cube, triprism]
Current = ObjList[0]
Drawing = ObjList[0]
currind = 0
currentsurface = ObjList[0].ShadingSurface[0]
#OBJECTS

#LIGHTS
Ambient_L = AmbientLight()
Point_L = PointLight()

lights = [Ambient_L, Point_L]
#LIGHTS

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------

#UNIVERSAL COMMANDS
def translate(object, displacement):
    #Whatever object we put in, no matter how many points it has we move em'.
    for points in object:
        for index in range(len(displacement)):
            points[index] += displacement[index]


def scale(object,scalefactor):
    #TODO: DUE FOR IN-PLACE UPDATE
    cp = getCenterpoint(object)
    for points in object:
        for index in range(len(points)):
            points[index] = points[index] - cp[index]
            points[index] *= scalefactor
            points[index] = points[index] + cp[index]


def rotateZ(object,degrees):
    cp = getCenterpoint(object)
    #TODO: DUE FOR IN-PLACE UPDATE
    degree = degrees*(math.pi/180)
    for points in object:
        points[0] = points[0] - cp[0]
        points[1] = points[1] - cp[1]
        tempx = points[0] * math.cos(degree) - points[1] * math.sin(degree)
        tempy = points[0] * math.sin(degree) + points[1] * math.cos(degree)
        points[0] = tempx
        points[1] = tempy
        points[0] = points[0] + cp[0]
        points[1] = points[1] + cp[1]


def rotateY(object,degrees):
    cp = getCenterpoint(object)
    #TODO: DUE FOR IN-PLACE UPDATE
    degree = degrees*(math.pi/180)
    for points in object:
        points[0] = points[0] - cp[0]
        points[2] = points[2] - cp[2]
        tempx = points[0] * math.cos(degree) + points[2] * math.sin(degree)
        tempz = -points[0] * math.sin(degree) + points[2] * math.cos(degree)
        points[0] = tempx
        points[2] = tempz
        points[0] = points[0] + cp[0]
        points[2] = points[2] + cp[2]


def rotateX(object,degrees):
    cp = getCenterpoint(object)
    #TODO: DUE FOR IN-PLACE UPDATE
    degree = degrees*(math.pi/180)
    for points in object:
        points[1] = points[1] - cp[1]
        points[2] = points[2] - cp[2]
        tempy = points[1] * math.cos(degree) - points[2] * math.sin(degree)
        tempz = points[1] * math.sin(degree) + points[2] * math.cos(degree)
        points[1] = tempy
        points[2] = tempz
        points[1] = points[1] + cp[1]
        points[2] = points[2] + cp[2]
#UNIVERSAL COMMANDS

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------

#DRAWING
#%%%%%%%%%%%%%%############# MAIN FUNCTIONS #############%%%%%%%%%%%%%%
def drawObject(object,width):
    global currpoly
    #WIREFRAME ONLY
    for poly in object:
        if checkVis(poly) == True:
            drawPoly(poly,width)
        currpoly += 1


def drawPoly(poly,width):
    global pf
    polyScanLine(poly)
    if pf == 1 or pf == 3:
        drawWireframe(poly,width)


def drawWireframe(poly,width):
    for i in range(len(poly)):
        starto = poly[i]
        if i == len(poly) - 1:
            finito = poly[0]
        else:
            finito = poly[i+1]

        drawLine(starto, finito, width)

#%%%%%%%%%%%%%%############# TOOL FUNCTIONS #############%%%%%%%%%%%%%%
def normalizeVector(vector):
    v_in = math.pow(vector[0],2) + math.pow(vector[1],2) + math.pow(vector[2],2)
    v_mag = math.sqrt(v_in)

    new_vect = vector
    new_vect[0] /= v_mag
    new_vect[1] /= v_mag
    new_vect[2] /= v_mag

    return new_vect

def getpixelcolor(x):
    #x is a rgb array. TRUNCATE THE NUMBERS.

    a = int(x[0]*255) #x is a collection of intensities, from 0 to 1, for r, g, and b. *255 and we know the rgb value.
    b = int(x[1]*255)
    c = int(x[2]*255)

    #This is a cheap, hackney shite.
    if a > 255:
        a = 255
    if b > 255:
        b = 255
    if c > 255:
        c = 255
    #More of the same
    if a < 0:
        a = 0
    if b < 0:
        b = 0
    if c < 0:
        c = 0

    final1 = '{:02x}'.format(a)
    final2 = '{:02x}'.format(b)
    final3 = '{:02x}'.format(c)

    truefinal = "#" + final1 + final2 + final3

    return truefinal


def polyScanLine(poly):
    global debug
    global currind
    global currpoly
    global lights #The list of lights...all 2 of them,
    global Drawing #The current model, to get information.
    global lightmodel #The selected lightmodel.
    global shadingmodel #The selected shading model.
    global currentsurface #The surface we're looking at for calculation

    A = project(poly[0])
    B = project(poly[1])
    C = project(poly[2])

    #TODO: THIS SECTION ESTABLISHES VARIABLES
    #Next, our edges are A-B, B-C, C-A. Take 3 ymaxes. Be sure to "distort" the ys.
    if A[1] >= B[1]:
        E1ymax = A[1]#See, if they're both the same, max and min will be the same. I'll make the logic skip over a straight edge.
        E1ymin = B[1]
    else:
        E1ymax = B[1] #If A[1] is NOT greater than B[1] then the A-B edge's ymax is B.
        E1ymin = A[1]

    if B[1] >= C[1]:
        E2ymax = B[1] #See, if they're both the same, max and min will be the same. I'll make the logic skip over a straight edge.
        E2ymin = C[1]
    else:
        E2ymax = C[1] #If B[1] is NOT greater than C[1] then the B-C edge's ymax is C.
        E2ymin = B[1]

    if C[1] >= A[1]:
        E3ymax = C[1] #See, if they're both the same, max and min will be the same. I'll make the logic skip over a straight edge.
        E3ymin = A[1]
    else:
        E3ymax = A[1] #If C[1] is NOT greater than A[1] then the C-A edge's ymax is A.
        E3ymin = C[1]

    #TODO: THIS SECTION IS FOR DX AND X. TODO: THIS MIGHT BE WONK
    #Next, get the dex and the x.
    #edge1
    if B[1] == A[1]:
        E1dx = 0.0 #So if both points rest on the same y dx will be 0
    else:
        E1dx = -((B[0]-A[0])/(B[1]-A[1]))
    if A[1] >= B[1]:
        tempx = A[0]
    else:
        tempx = B[0] #because x1 changes depending on which point has a higher up y. Makes sense, that's the first one you'll touch.
    E1x = tempx + (E1dx/2.0) #Our initial X, which will help sorting our edges. Consider the case B[1] = A[1]. We'll skip it.
    #X MIGHT BE WRONG. NEED TO TALK TO MIKE.


    #edge2
    if C[1] == B[1]:
        E2dx = 0.0
    else:
        E2dx = -((C[0]-B[0])/(C[1]-B[1]))
    #Which one is x?
    if B[1] >= C[1]:
        tempx = B[0]
    else:
        tempx = C[0] #because x1 changes depending on which point has a higher up y
    E2x = tempx + (E2dx/2.0) #Our initial X, which will help sorting our edges.


    #edge3
    if A[1] == C[1]:
        E3dx = 0.0
    else:
        E3dx = -((A[0]-C[0])/(A[1]-C[1]))
    if C[1] >= A[1]:
        tempx = C[0]
    else:
        tempx = A[0] #because x1 changes depending on which point has a higher up y
    E3x = tempx + (E3dx/2.0) #Our initial X, which will help sorting our edges.


    #Z BUFFER
    #edge 1, A to B
    if A[1] > B[1]:
        E1ztop = A[2]
        E1dz = ((B[2]-A[2])/(B[1]-A[1])) #zs over ys
    elif A[1] < B[1]:
        E1ztop = B[2] #We need to record the topmost z so we have a place to actually start.
        E1dz = ((A[2]-B[2])/(A[1]-B[1])) #zs over ys
    else:
        E1ztop = A[2]
        E1dz = 0 #doesn't matter I hope...skipping scanlines skips zs, too. Good-o.


    #edge 2, B to C
    if B[1] > C[1]:
        E2ztop = B[2]
        E2dz = ((C[2]-B[2])/(C[1]-B[1])) #zs over ys
    elif B[1] < C[1]:
        E2ztop = C[2] #We need to record the topmost z so we have a place to actually start.
        E2dz = ((B[2]-C[2])/(B[1]-C[1])) #zs over ys
    else:
        E2ztop = B[2]
        E2dz = 0 #doesn't matter I hope...


    #edge 3, C to A
    if C[1] > A[1]:
        E3ztop = C[2]
        E3dz = ((A[2]-C[2])/(A[1]-C[1])) #zs over ys
    elif C[1] < A[1]:
        E3ztop = A[2] #We need to record the topmost z so we have a place to actually start.
        E3dz = ((C[2]-A[2])/(C[1]-A[1])) #zs over ys
    else:
        E3ztop = C[2]
        E3dz = 0 #doesn't matter I hope...


    #SHADING AND INTENSITY STUFF. ADDING:
        #I = [rgb] | dI = [rgb] | MaxNormal = [xyz] | MinNormal = [xyz]
        #TODO: ADD THE GOURAUD TOOLS NEEDED.


        #Now we've built our supplementary values, I and dI. Let's go and use them in Gouraud!


    if shadingmodel == 2 or shadingmodel == 1:
        #This'll be for Phong
        #Supplement 01 will be that edge's max vertex normal
        #Supplement 02 will be that edge's min vertex normal
        if A[1] > B[1]:
            E1ShadeSupp_01 = getVertexNormal(poly[0], currentsurface)
            E1ShadeSupp_02 = getVertexNormal(poly[1], currentsurface)

        elif A[1] < B[1]:
            E1ShadeSupp_01 = getVertexNormal(poly[1], currentsurface)
            E1ShadeSupp_02 = getVertexNormal(poly[0], currentsurface)

        else:
            E1ShadeSupp_01 = [0,0,0]
            E1ShadeSupp_02 = [0,0,0]

        #EDGE 2
        if B[1] > C[1]:
            E2ShadeSupp_01 = getVertexNormal(poly[1], currentsurface)
            E2ShadeSupp_02 = getVertexNormal(poly[2], currentsurface)

        elif B[1] < C[1]:
            E2ShadeSupp_01 = getVertexNormal(poly[2], currentsurface)
            E2ShadeSupp_02 = getVertexNormal(poly[1], currentsurface)

        else:
            E2ShadeSupp_01 = [0,0,0]
            E2ShadeSupp_02 = [0,0,0]

        #EDGE 3
        if C[1] > A[1]:
            E3ShadeSupp_01 = getVertexNormal(poly[2], currentsurface)
            E3ShadeSupp_02 = getVertexNormal(poly[0], currentsurface)

        elif C[1] < A[1]:
            E3ShadeSupp_01 = getVertexNormal(poly[0], currentsurface)
            E3ShadeSupp_02 = getVertexNormal(poly[2], currentsurface)

        else:
            E3ShadeSupp_01 = [0,0,0]
            E3ShadeSupp_02 = [0,0,0]

        if shadingmodel == 1:
            E1ShadeSupp_01 = getLightIntensity(E1ShadeSupp_01) #Here, we pre-get the intensity for each point.
            E1ShadeSupp_02 = getLightIntensity(E1ShadeSupp_02)

            E2ShadeSupp_01 = getLightIntensity(E2ShadeSupp_01)
            E2ShadeSupp_02 = getLightIntensity(E2ShadeSupp_02)

            E3ShadeSupp_01 = getLightIntensity(E3ShadeSupp_01)
            E3ShadeSupp_02 = getLightIntensity(E3ShadeSupp_02)

    else:
        E1ShadeSupp_01 = [0,0,0]
        E1ShadeSupp_02 = [0,0,0]

        E2ShadeSupp_01 = [0,0,0]
        E2ShadeSupp_02 = [0,0,0]

        E3ShadeSupp_01 = [0,0,0]
        E3ShadeSupp_02 = [0,0,0] #We only need EITHER I[rgb]/dI[rgb] OR MXN[xyz]/MIN[xyz]. And they're both vectors so we can be a little cheeky.

    

    edge1 = [E1ymax, E1ymin, E1dx, E1x, E1ztop, E1dz, E1ShadeSupp_01, E1ShadeSupp_02]
    edge2 = [E2ymax, E2ymin, E2dx, E2x, E2ztop, E2dz, E2ShadeSupp_01, E2ShadeSupp_02]
    edge3 = [E3ymax, E3ymin, E3dx, E3x, E3ztop, E3dz, E3ShadeSupp_01, E3ShadeSupp_02]

    FTABLE = [edge1, edge2, edge3]


    #TODO: THIS IS THE SORTING OF THE TABLE
    for i in range(3):
        #We'll do 2 passes.
        for x in range(2):
            #First, see if the ymax for the current is less than the next one.
            if FTABLE[x][0] < FTABLE[x+1][0]:
                temp = FTABLE[x] #if so, swap those ftable entries.
                FTABLE[x] = FTABLE[x+1]
                FTABLE[x+1] = temp
            elif FTABLE[x][0] == FTABLE[x+1][0]:
                #We'll check if the x value of current is greater than x value of next. If so, gotta swap.
                if FTABLE[x][3] > FTABLE[x+1][3]:
                    temp = FTABLE[x] #if so, swap those ftable entries.
                    FTABLE[x] = FTABLE[x+1]
                    FTABLE[x+1] = temp


    if FTABLE[0][0] == FTABLE[1][0] and FTABLE[1][0] == FTABLE[2][0] and FTABLE[2][0] == FTABLE[0][0]:

        for i in range(len(FTABLE)):
            #Check every entry in FTBALE
            if FTABLE[i][0] == FTABLE[i][1]:
                #This only happens if FTABLE[i] is a straight edge!
                helper = FTABLE[1]
                FTABLE[1] = FTABLE[i]
                FTABLE[i] = helper

        if FTABLE[0][3] > FTABLE[2][3]:
            helper = FTABLE[0]
            FTABLE[0] = FTABLE[2]
            FTABLE[2] = helper

    if FTABLE[0][0]-FTABLE[0][1] <= 3.0:
        FTABLE[0][1] = FTABLE[0][0] #ymax and ymin the same now. Neato.

    if FTABLE[1][0]-FTABLE[1][1] <= 3.0:
        FTABLE[1][1] = FTABLE[1][0] #ymax and ymin the same now. Neato.

    if FTABLE[2][0]-FTABLE[2][1] <= 3.0:
        FTABLE[2][1] = FTABLE[2][0]
    #SORTING FINITO

    if shadingmodel == 0:
        Shade_Faceted(FTABLE, poly)
    elif shadingmodel == 1:
        Shade_Gouraud(FTABLE, poly)
    else:
        Shade_Phong(FTABLE, poly)


def flushZBuffer():
    global ZBuffer
    ZBuffer = [[float('inf') for i in range(CanvasWidth)] for j in range(CanvasHeight)] #0,0 is top left, just like display.
    #Also, everything is now infinity, and we can check if a pixel is smaller. MIGHT BE SQUICK BUT I THINK IT WORKED?
    #i is x and j is y. Need to keep that in mind.



#%%%%%%%%%%%%%%############# CANVAS PRIMITIVE FUNCTIONS #############%%%%%%%%%%%%%%
def drawPixel(y, x, rgb, z):
    global pf
    global ZBuffer
    global debug5

    display = convertToDisplayCoordinates([x, y])
    if pf == 3:
        pass
    else:
        #does this pixel's z < the same position in the ZBuffer
        if debug5 == 1:
            print int(display[1])
            print int(display[0])
            pause()
        if z < ZBuffer[int(display[1])][int(display[0])] or zb == False: #TODO MIGHT BE SQUICKY
            w.create_oval(display[0], display[1], display[0], display[1], outline=rgb)
            ZBuffer[int(display[1])][int(display[0])] = z #update ZBuffer
        else:
            pass


def drawLine(start,end, widt):
    #TODO: DEFINE CUSTOM LINE DRAW WITH PIXELS TO RESPECT Z-BUFFER.
    tempStart = project(start) 
    tempEnd = project(end)
    displayStart = convertToDisplayCoordinates(tempStart)
    displayEnd = convertToDisplayCoordinates(tempEnd)
    w.create_line(displayStart[0], displayStart[1], displayEnd[0], displayEnd[1], width=widt)


def project(point):
    ps = []
    ps.append(float(d*point[0]/(d+point[2])))
    ps.append(float(d*point[1]/(d+point[2])))
    ps.append(float(point[2]/(d+point[2])))
    return ps


def convertToDisplayCoordinates(point):
    displayXY = []
    logicOriginX = (CanvasWidth / 2) - 1
    logicOriginY = (CanvasHeight / 2) - 1
    displayXY.append(logicOriginX + point[0])
    displayXY.append(logicOriginY - point[1])
    return displayXY


def getCenterpoint(object):
    maxX = object[0][0]
    minX = object[0][0]
    maxY = object[0][1]
    minY = object[0][1]
    maxZ = object[0][2]
    minZ = object[0][2]

    for points in object:
        if points[0] > maxX : maxX = points[0]
        if points[0] < minX : minX = points[0]
        if points[1] > maxY : maxY = points[1]
        if points[1] < minY : minY = points[1]
        if points[2] > maxZ : maxZ = points[2]
        if points[2] < minZ : minZ = points[2]

    CenterX = (minX + maxX)/2
    CenterY = (minY + maxY)/2
    CenterZ = (minZ + maxZ)/2

    Centerpoint = [CenterX, CenterY, CenterZ]
    return Centerpoint

#%%%%%%%%%%%%%%############# TECHNICAL 3D FUNCTIONS #############%%%%%%%%%%%%%%
def getSurfaceNormal(poly):
    p0 = poly[0] #Save all the points into separate arrays
    p1 = poly[1]
    p2 = poly[2]

    alpha = [p2[0] - p0[0], p2[1] - p0[1], p2[2] - p0[2]] #Yeah, we're going there.
    beta = [p1[0] - p0[0], p1[1] - p0[1], p1[2] - p0[2]]

    A = alpha[1]*beta[2] - alpha[2]*beta[1] #Our surface normal values, the cross-product between the 2 vectors we've chosen from p0->p1 and p0->p2
    B = -(alpha[0]*beta[2] - alpha[2]*beta[0])
    C = alpha[0]*beta[1] - alpha[1]*beta[0]

    #Normalizing
    normvector = normalizeVector([A, B, C])


    return normvector


def getVertexNormal(point, surface):
    valid_poly = []
    for poly in surface:
        for testpoint in poly:
            if point[0] == testpoint[0] and point[1] == testpoint[1] and point[2] == testpoint[2]:
                #There's a match, meaning it's the same point!
                if getSurfaceNormal(poly) not in valid_poly:
                    x = getSurfaceNormal(poly)
                    valid_poly.append(x) #This will build a list of polygons that use the point

    #NOW WE HAVE AN ARRAY OF VALID, NON-REPEATED NORMALS. TIME TO ADD.
    X = 0.0
    Y = 0.0
    Z = 0.0
    for add_vect in valid_poly:
        X += add_vect[0]
        Y += add_vect[1]
        Z += add_vect[2]

    #And now to normalize.
    #And here's the final normal for the vertex
    ey = normalizeVector([X, Y, Z])
    return ey


def checkVis(poly):
    global d #gotta declare global.
    global bfc
    #This function will check the visibility of a given polygon.
    if bfc == True:
        p0 = poly[0] #Save all the points into separate arrays
        p1 = poly[1]
        p2 = poly[2]

        nvect = getSurfaceNormal(poly)

        D = (p0[0]*nvect[0]) + (p0[1]*nvect[1]) + (p0[2]*nvect[2]) 

        ch = (-d*nvect[2]) - D 

        if ch > 0:
            return True
        else:
            return False
    else:
        return True

#%%%%%%%%%%%%%%############# SHADING MODELS #############%%%%%%%%%%%%%%
def Shade_Faceted(STABLE, poly):
    normal = getSurfaceNormal(poly)
    rgb_raw = getLightIntensity(normal) #This is per-poly

    rgb = getpixelcolor(rgb_raw)


    startedge = STABLE[0]
    endedge = STABLE[1]

    curry = startedge[0] #This is the maxy of our start edge
    startx = startedge[3] #This is the starting x.
    endx = endedge[3] #And the ending x.

    startz = startedge[4] + startedge[5]
    endz = endedge[4] + endedge[5] 


    while curry > startedge[1] and curry > endedge[1]:
    #Let's think about this. So we want it to draw a line across ymin? Well, the ymin of one edge is the y max of another.
        currx = startx #Start x either beings or is edited.
        currz = startz #same thing here. TODO: SQUICKY
        while currx < endx:
            drawPixel(curry, currx, rgb, currz) #curry should scan all the way down the polygon, curr x should scan across. Currz does its thing.
            currx += 1.0 #add currx by 1. Next pixel over.
            currz += ((endz-startz)/(endx-startx)) #currz has a formula for "moving over"

        curry -= 1.0 #curry has to go down, down, down, until it surpasses the miny of either edge.
        startx += startedge[2]
        endx += endedge[2] #Here's the dx for both endx and startx. This will alter them before we start a new line.
        startz += startedge[5]
        endz += endedge[5]

    #TODO: SECOND PASS FUCKUP
    if curry <= startedge[1]:
        #the startedge has fallen off. It must be replaced.
        startedge = STABLE[2] #Curry should already be at this one's maxy. The startx and endx should be right on the vertex. So we can just do pass 2
        startx = startedge[3]
        startz = startedge[4] + startedge[5] #the new startedge gives the new startz
    else:
        endedge = STABLE[2] #It's either start edge or end edge. If it was both, it's a straight edge which will kill the loop instantly.
        endx = endedge[3]
        endz = endedge[4] + endedge[5] #perhaps?

    while curry > startedge[1] and curry > endedge[1]:
        currx = startx #wait a fucking sucking second. What if startx changed.
        currz = startz
        #and...where the hell is endx???
        #We sometimes have a line going haywire and a few dropped pixels.
        while currx < endx:

            drawPixel(curry, currx, rgb, currz)
            currx += 1.0 #add currx by 1. Next pixel over.
            currz += ((endz-startz)/(endx-startx))

        curry -= 1.0 #curry has to go down, down, down, until it surpasses the miny of either edge.
        startx += startedge[2]
        endx += endedge[2] #Here's the dx for both endx and startx
        startz += startedge[5]
        endz += endedge[5]

    #And that...should complete the polygon. Z-buffer stuff is taken care of in the pixel drawing.


def Shade_Gouraud(STABLE, poly):
    #edge[6] is edge's maxnormal
    #edge[7] is edge's minnormal
    def getEdgeInten(maxInt, minInt, ys, maxy, miny):
        #Need eI = (((ys-miny)/(maxy-miny))*MaxI)+(((maxy-ys)/(maxy-miny))*MinI)
        if maxy == miny:
            bot = 1
        else:
            bot = maxy-miny

        r = (((ys-miny)/bot)*maxInt[0]) + (((maxy-ys)/bot)*minInt[0])
        g = (((ys-miny)/bot)*maxInt[1]) + (((maxy-ys)/bot)*minInt[1])
        b = (((ys-miny)/bot)*maxInt[2]) + (((maxy-ys)/bot)*minInt[2])

        return [r,g,b]

    def getCurrentInten(startInt, endInt, stx, enx, xs):
        #This needs Is = ((enx-xs)/(enx-stx)*startInt) + ((xs-stx)/(enx-stx)*endInt)
        if enx == stx:
            bot = 1
        else:
            bot = enx-stx

        r = (((enx-xs)/bot)*startInt[0]) + (((xs-stx)/bot)*endInt[0])
        g = (((enx-xs)/bot)*startInt[1]) + (((xs-stx)/bot)*endInt[1])
        b = (((enx-xs)/bot)*startInt[2]) + (((xs-stx)/bot)*endInt[2])
        return [r,g,b]

    startedge = STABLE[0]
    endedge = STABLE[1]

    curry = startedge[0] #This is the maxy of our start edge
    startx = startedge[3] #This is the starting x.
    endx = endedge[3] #And the ending x.

    startz = startedge[4] + startedge[5]
    endz = endedge[4] + endedge[5] 


    while curry > startedge[1] and curry > endedge[1]:
    #Let's think about this. So we want it to draw a line across ymin? Well, the ymin of one edge is the y max of another.
        currx = startx #Start x either beings or is edited.
        currz = startz #same thing here. TODO: SQUICKY
        while currx < endx:
            Na = getEdgeInten(startedge[6], startedge[7], curry, startedge[0], startedge[1])
            Nb = getEdgeInten(endedge[6], endedge[7], curry, endedge[0], endedge[1])
            Ns = getCurrentInten(Na, Nb, startx, endx, currx)
            rgb = getpixelcolor(Ns)

            drawPixel(curry, currx, rgb, currz) #curry should scan all the way down the polygon, curr x should scan across. Currz does its thing.
            currx += 1.0 #add currx by 1. Next pixel over.
            currz += ((endz-startz)/(endx-startx)) #currz has a formula for "moving over"

        curry -= 1.0 #curry has to go down, down, down, until it surpasses the miny of either edge.
        startx += startedge[2]
        endx += endedge[2] #Here's the dx for both endx and startx. This will alter them before we start a new line.
        startz += startedge[5]
        endz += endedge[5]

    #TODO: SECOND PASS FUCKUP
    if curry <= startedge[1]:
        #the startedge has fallen off. It must be replaced.
        startedge = STABLE[2] #Curry should already be at this one's maxy. The startx and endx should be right on the vertex. So we can just do pass 2
        startx = startedge[3]
        startz = startedge[4] + startedge[5] #the new startedge gives the new startz
    else:
        endedge = STABLE[2] #It's either start edge or end edge. If it was both, it's a straight edge which will kill the loop instantly.
        endx = endedge[3]
        endz = endedge[4] + endedge[5] #perhaps?

    while curry > startedge[1] and curry > endedge[1]:
        currx = startx #wait a fucking sucking second. What if startx changed.
        currz = startz
        #and...where the hell is endx???
        #We sometimes have a line going haywire and a few dropped pixels.
        while currx < endx:
            Na = getEdgeInten(startedge[6], startedge[7], curry, startedge[0], startedge[1])
            Nb = getEdgeInten(endedge[6], endedge[7], curry, endedge[0], endedge[1])
            Ns = getCurrentInten(Na, Nb, startx, endx, currx)
            rgb = getpixelcolor(Ns)

            drawPixel(curry, currx, rgb, currz)
            currx += 1.0 #add currx by 1. Next pixel over.
            currz += ((endz-startz)/(endx-startx))

        curry -= 1.0 #curry has to go down, down, down, until it surpasses the miny of either edge.
        startx += startedge[2]
        endx += endedge[2] #Here's the dx for both endx and startx
        startz += startedge[5]
        endz += endedge[5]


def Shade_Phong(STABLE, poly):
    #edge[6] is edge's maxnormal
    #edge[7] is edge's minnormal
    def getEdgeNorm(maxNorm, minNorm, ys, maxy, miny):
        x1 = (maxNorm[0]*(ys-miny))+(minNorm[0]*(maxy-ys))
        y1 = (maxNorm[1]*(ys-miny))+(minNorm[1]*(maxy-ys))
        z1 = (maxNorm[2]*(ys-miny))+(minNorm[2]*(maxy-ys))
        if maxy == miny:
            x2 = 1
            y2 = 1
            z2 = 1
        else:
            x2 = (1.0/(maxy-miny)) #Essentially (1/y1-y2) * (N1(ys-y2)+N2(y1-ys))
            y2 = (1.0/(maxy-miny))
            z2 = (1.0/(maxy-miny))
        x = x2 * x1
        y = y2 * y1
        z = z2 * z1

        return normalizeVector([x,y,z])

    def getCurrentNorm(startNorm, endNorm, stx, enx, xs):
        x = ((1.0/(enx-stx))*((startNorm[0]*(enx-xs))+(endNorm[0]*(xs-stx)))) #Essentially (1/xb-xa) * (Na(xb-xs)+Nb(xs-xa))
        y = ((1.0/(enx-stx))*((startNorm[1]*(enx-xs))+(endNorm[1]*(xs-stx))))
        z = ((1.0/(enx-stx))*((startNorm[2]*(enx-xs))+(endNorm[2]*(xs-stx))))

        return normalizeVector([x,y,z])

    startedge = STABLE[0]
    endedge = STABLE[1]

    curry = startedge[0] #This is the maxy of our start edge
    startx = startedge[3] #This is the starting x.
    endx = endedge[3] #And the ending x.

    startz = startedge[4] + startedge[5]
    endz = endedge[4] + endedge[5] 


    while curry > startedge[1] and curry > endedge[1]:
    #Let's think about this. So we want it to draw a line across ymin? Well, the ymin of one edge is the y max of another.
        currx = startx #Start x either beings or is edited.
        currz = startz #same thing here. TODO: SQUICKY
        while currx < endx:
            Na = getEdgeNorm(startedge[6], startedge[7], curry, startedge[0], startedge[1])
            Nb = getEdgeNorm(endedge[6], endedge[7], curry, endedge[0], endedge[1])
            Ns = getCurrentNorm(Na, Nb, startx, endx, currx)
            rgb = getpixelcolor(getLightIntensity(Ns))

            drawPixel(curry, currx, rgb, currz) #curry should scan all the way down the polygon, curr x should scan across. Currz does its thing.
            currx += 1.0 #add currx by 1. Next pixel over.
            currz += ((endz-startz)/(endx-startx)) #currz has a formula for "moving over"

        curry -= 1.0 #curry has to go down, down, down, until it surpasses the miny of either edge.
        startx += startedge[2]
        endx += endedge[2] #Here's the dx for both endx and startx. This will alter them before we start a new line.
        startz += startedge[5]
        endz += endedge[5]

    #TODO: SECOND PASS FUCKUP
    if curry <= startedge[1]:
        #the startedge has fallen off. It must be replaced.
        startedge = STABLE[2] #Curry should already be at this one's maxy. The startx and endx should be right on the vertex. So we can just do pass 2
        startx = startedge[3]
        startz = startedge[4] + startedge[5] #the new startedge gives the new startz
    else:
        endedge = STABLE[2] #It's either start edge or end edge. If it was both, it's a straight edge which will kill the loop instantly.
        endx = endedge[3]
        endz = endedge[4] + endedge[5] #perhaps?

    while curry > startedge[1] and curry > endedge[1]:
        currx = startx #wait a fucking sucking second. What if startx changed.
        currz = startz
        #and...where the hell is endx???
        #We sometimes have a line going haywire and a few dropped pixels.
        while currx < endx:
            Na = getEdgeNorm(startedge[6], startedge[7], curry, startedge[0], startedge[1])
            Nb = getEdgeNorm(endedge[6], endedge[7], curry, endedge[0], endedge[1])
            Ns = getCurrentNorm(Na, Nb, startx, endx, currx)
            rgb = getpixelcolor(getLightIntensity(Ns))

            drawPixel(curry, currx, rgb, currz)
            currx += 1.0 #add currx by 1. Next pixel over.
            currz += ((endz-startz)/(endx-startx))

        curry -= 1.0 #curry has to go down, down, down, until it surpasses the miny of either edge.
        startx += startedge[2]
        endx += endedge[2] #Here's the dx for both endx and startx
        startz += startedge[5]
        endz += endedge[5]


def getLightIntensity(vector):
    global lightmodel
    global lights
    global Drawing
    global d
    #Gotta pass in some vector. A surface normal? A point normal? Who can say.
    p1 = [0.0,0.0,0.0]
    p2 = [0.0,0.0,0.0]
    p3 = [0.0,0.0,0.0]

    if lightmodel >= 0:
        p1 = lights[0].calcAmbLight(Drawing.color) #This comes back as a rgb array
    if lightmodel >= 1:
        p2 = lights[1].calcPointLight(Drawing.color, vector) #This comes back as a rgb array
    if lightmodel >= 2:
        p3 = lights[1].calcSpecularLight(Drawing.color, vector, Drawing.shininess, d) #This comes back as a rgb array

    fin_r = p1[0] + p2[0] + p3[0]
    fin_g = p1[1] + p2[1] + p3[1]
    fin_b = p1[2] + p2[2] + p3[2]

    return [fin_r, fin_g, fin_b]

#DRAWING

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------

#INTERFACE
def redraw():
    global currpoly
    global currentsurface
    global Drawing

    w.delete(ALL)
    flushZBuffer() #A new step. Flush the Z-buffer and rebuild it as we draw our stuff.
    global currind
    for obj in ObjList:
        wid = 1

        Drawing = obj

        if ObjList.index(obj) == currind:
            wid = 2
        for surface in obj.ShadingSurface:
            currentsurface = surface #This will globally store the surface we're dealing with, to be accessed from anywhere.
            drawObject(surface, wid) #Draws all surfaces in the list of surfaces in the objects in a list of objects. HOH.
        currpoly = 0


def reset():
    w.delete(ALL)
    Current.reset()
    redraw()


#--ADDED
def nextobj():
    global Current
    global currind
    if currind == len(ObjList) - 1:
        currind = 0
    else:
        currind += 1
    Current = ObjList[currind]
    redraw()

#TOGGLES:
def toggleSheps():
    global sheps
    global pyramid
    global cube
    global triprism
    global cyl
    global ObjList
    global Current
    global Drawing
    global currid
    global currentsurface

    if sheps == 1:
        sheps = 0
    else:
        sheps = 1

    if sheps == 1:
        ObjList = [cyl]
    else:
        ObjList = [pyramid, cube, triprism]
    Current = ObjList[0]
    Drawing = ObjList[0]
    currind = 0
    currentsurface = ObjList[0].ShadingSurface[0]

    redraw()

def toggleShadingMod():
    global shadingmodel
    #1 is color with edges; 2 is color without edges; 3 is wireframe
    if shadingmodel == 0:
        shadingmodel = 1
    elif shadingmodel == 1:
        shadingmodel = 2
    else:
        shadingmodel = 0
    redraw()

def toggleLightingMod():
    global lightmodel
    if lightmodel == 0:
        lightmodel = 1
    elif lightmodel == 1:
        lightmodel = 2
    else:
        lightmodel = 0
    redraw()

def toggleDebug():
    global pf
    if pf == 1:
        pf = 2
    elif pf == 2:
        pf = 3
    else:
        pf = 1
    redraw()

def toggleDebug2():
    global debug5
    if debug5 == 0:
        debug5 = 1
    else:
        debug5 = 0
#--ADDED

def larger():
    w.delete(ALL)
    scale(Current.PointCloud,1.1)
    redraw()

def smaller():
    w.delete(ALL)
    scale(Current.PointCloud,.9)
    redraw()

def forward():
    w.delete(ALL)
    translate(Current.PointCloud,[0,0,10])
    redraw()

def backward():
    w.delete(ALL)
    translate(Current.PointCloud,[0,0,-10])
    redraw()

def left():
    w.delete(ALL)
    translate(Current.PointCloud,[-10,0,0])
    redraw()

def right():
    w.delete(ALL)
    translate(Current.PointCloud,[10,0,0])
    redraw()

def up():
    w.delete(ALL)
    translate(Current.PointCloud,[0,10,0])
    redraw()

def down():
    w.delete(ALL)
    translate(Current.PointCloud,[0,-10,0])
    redraw()

def xPlus():
    w.delete(ALL)
    rotateX(Current.PointCloud,5)
    redraw()

def xMinus():
    w.delete(ALL)
    rotateX(Current.PointCloud,-5)
    redraw()

def yPlus():
    w.delete(ALL)
    rotateY(Current.PointCloud,5)
    redraw()

def yMinus():
    w.delete(ALL)
    rotateY(Current.PointCloud,-5)
    redraw()

def zPlus():
    w.delete(ALL)
    rotateZ(Current.PointCloud,5)
    redraw()

def zMinus():
    w.delete(ALL)
    rotateZ(Current.PointCloud,-5)
    redraw()
#INTERFACE
#debug
def pause():
    raw_input("Press Enter")

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------

#WINDOW
root = Tk()
outerframe = Frame(root)
outerframe.pack()

w = Canvas(outerframe, width=CanvasWidth, height=CanvasHeight)
w.pack()
redraw()

controlpanel = Frame(outerframe)
controlpanel.pack()

resetcontrols = Frame(controlpanel, height=100, borderwidth=2, relief=RIDGE)
resetcontrols.pack(side=LEFT)

resetcontrolslabel = Label(resetcontrols, text="Reset")
resetcontrolslabel.pack()

resetButton = Button(resetcontrols, text="Reset", fg="green", command=reset)
resetButton.pack(side=LEFT)

#--ADDED
nextcontrols = Frame(controlpanel, height=100, borderwidth=2, relief=RIDGE)
nextcontrols.pack(side=LEFT)

nextcontrolslabel = Label(nextcontrols, text="Selection")
nextcontrolslabel.pack()

nextButton = Button(nextcontrols, text="Next Object", fg="red", command=nextobj)
nextButton.pack(side=LEFT)

#Stuff for toggling drawing features
drawtoggles = Frame(controlpanel, height=100, borderwidth=2, relief=RIDGE)
drawtoggles.pack(side=LEFT)

drawtoggleslabel = Label(drawtoggles, text="Drawing Toggles")
drawtoggleslabel.pack()

toggleBfcButton = Button(drawtoggles, text="Toggle Shapes", fg="blue", command=toggleSheps)
toggleBfcButton.pack(side=LEFT)

togglePfButton = Button(drawtoggles, text="Toggle Shading", fg="blue", command=toggleShadingMod)
togglePfButton.pack(side=LEFT)

toggleZbButton = Button(drawtoggles, text="Toggle Lighting", fg="blue", command=toggleLightingMod)
toggleZbButton.pack(side=LEFT)

toggleDBButton = Button(drawtoggles, text="Wireframe", fg="green", command=toggleDebug)
toggleDBButton.pack(side=LEFT)

if debug6 == 1:
    toggleDBButton2 = Button(drawtoggles, text="snap", fg="green", command=toggleDebug2)
    toggleDBButton2.pack(side=LEFT)
#--ADDED

scalecontrols = Frame(controlpanel, borderwidth=2, relief=RIDGE)
scalecontrols.pack(side=LEFT)

scalecontrolslabel = Label(scalecontrols, text="Scale")
scalecontrolslabel.pack()

largerButton = Button(scalecontrols, text="Larger", command=larger)
largerButton.pack(side=LEFT)

smallerButton = Button(scalecontrols, text="Smaller", command=smaller)
smallerButton.pack(side=LEFT)

translatecontrols = Frame(controlpanel, borderwidth=2, relief=RIDGE)
translatecontrols.pack(side=LEFT)

translatecontrolslabel = Label(translatecontrols, text="Translation")
translatecontrolslabel.pack()

forwardButton = Button(translatecontrols, text="FW", command=forward)
forwardButton.pack(side=LEFT)

backwardButton = Button(translatecontrols, text="BK", command=backward)
backwardButton.pack(side=LEFT)

leftButton = Button(translatecontrols, text="LF", command=left)
leftButton.pack(side=LEFT)

rightButton = Button(translatecontrols, text="RT", command=right)
rightButton.pack(side=LEFT)

upButton = Button(translatecontrols, text="UP", command=up)
upButton.pack(side=LEFT)

upButton = Button(translatecontrols, text="DN", command=down)
upButton.pack(side=LEFT)

rotationcontrols = Frame(controlpanel, borderwidth=2, relief=RIDGE)
rotationcontrols.pack(side=LEFT)

rotationcontrolslabel = Label(rotationcontrols, text="Rotation")
rotationcontrolslabel.pack()

xPlusButton = Button(rotationcontrols, text="X+", command=xPlus)
xPlusButton.pack(side=LEFT)

xMinusButton = Button(rotationcontrols, text="X-", command=xMinus)
xMinusButton.pack(side=LEFT)

yPlusButton = Button(rotationcontrols, text="Y+", command=yPlus)
yPlusButton.pack(side=LEFT)

yMinusButton = Button(rotationcontrols, text="Y-", command=yMinus)
yMinusButton.pack(side=LEFT)

zPlusButton = Button(rotationcontrols, text="Z+", command=zPlus)
zPlusButton.pack(side=LEFT)

zMinusButton = Button(rotationcontrols, text="Z-", command=zMinus)
zMinusButton.pack(side=LEFT)

root.mainloop()
#WINDOW

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------

