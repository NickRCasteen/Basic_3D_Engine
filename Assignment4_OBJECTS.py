#Nicholas Reno Casteen
#102-28-520
#Datestamp: 13/2/2018
#Assignment #4 SUPPLEMENT 1
#------------------------- DESCRIPTION -------------------------
#	This code is a collection of classes to be used by the assignment 2 program. It defines 3 3-D objects to draw.

class Pyramid:
    def __init__(self):
	#POINTS#
        self.apex = [0.0,50.0,100.0]
        self.base1 = [-50.0,-50.0,50.0] #front left
        self.base2 = [50.0,-50.0,50.0] #front right
        self.base3 = [50.0,-50.0,150.0] #back right
        self.base4 = [-50.0,-50.0,150.0] #back left

	#POLYGONS#
        self.frontpoly = [self.apex, self.base1, self.base2]
        self.rightpoly = [self.apex, self.base2, self.base3]
        self.backpoly = [self.apex, self.base3, self.base4]
        self.leftpoly = [self.apex, self.base4, self.base1]
        self.bottompoly1 = [self.base4, self.base3, self.base1]
        self.bottompoly2 = [self.base1, self.base3, self.base2]

	#MODEL#
        self.Model = [self.bottompoly1, self.bottompoly2, self.frontpoly, self.rightpoly, self.backpoly, self.leftpoly]

	#POINT CLOUD#
        self.PointCloud = [self.apex, self.base1, self.base2, self.base3, self.base4]

        #SURFACES
        self.surface01 = [self.frontpoly]
        self.surface02 = [self.rightpoly]
        self.surface03 = [self.backpoly]
        self.surface04 = [self.leftpoly]
        self.surface05 = [self.bottompoly1, self.bottompoly2]

        self.ShadingSurface = [self.surface01, self.surface02, self.surface03, self.surface04, self.surface05]

        #SHADING PROPERTIES
        self.color = [78.0/255.0, 73.0/255.0, 90.0/255.0] #RGB
        self.shininess = 5.0 #curly N

    def reset(self):
    #Doin' it the stupid way for now. Mostly because it's not passed in. A point cloud would need an associated "default position" object for generality.
    #I decided this method might as well go into the object since the default values are so specific TO that object.
        self.PointCloud[0][0] = 0.0
        self.PointCloud[0][1] = 50.0
        self.PointCloud[0][2] = 100.0
        self.PointCloud[1][0] = -50.0
        self.PointCloud[1][1] = -50.0
        self.PointCloud[1][2] = 50.0
        self.PointCloud[2][0] = 50.0
        self.PointCloud[2][1] = -50.0
        self.PointCloud[2][2] = 50.0
        self.PointCloud[3][0] = 50.0
        self.PointCloud[3][1] = -50.0
        self.PointCloud[3][2] = 150.0
        self.PointCloud[4][0] = -50.0
        self.PointCloud[4][1] = -50.0
        self.PointCloud[4][2] = 150.0


class Cube:
    def __init__(self):
        #POINTS#
        self.base1 = [100.0,-50.0,50.0] #front left
        self.base2 = [200.0,-50.0,50.0] #front right
        self.base3 = [200.0,-50.0,150.0] #back right
        self.base4 = [100.0,-50.0,150.0] #back left
        self.top1 = [100.0,50.0,50.0] #front left
        self.top2 = [200.0,50.0,50.0] #front right
        self.top3 = [200.0,50.0,150.0] #back right
        self.top4 = [100.0,50.0,150.0] #back left

	#POLYGONS#
        self.frontpoly1 = [self.top1, self.base1, self.top2] #
        self.frontpoly2 = [self.base1, self.base2, self.top2] #
        self.leftpoly1 = [self.top2, self.base2, self.top3] #
        self.leftpoly2 = [self.base2, self.base3, self.top3] #
        self.rightpoly1 = [self.top4, self.base4, self.top1] #
        self.rightpoly2 = [self.base4, self.base1, self.top1] #
        self.backpoly1 = [self.top4, self.base3, self.base4] # 
        self.backpoly2 = [self.top3, self.base3, self.top4] # 
        self.toppoly1 = [self.top4, self.top1, self.top3] #
        self.toppoly2 = [self.top1, self.top2, self.top3] #
        self.basepoly1 = [self.base4, self.base2, self.base1] 
        self.basepoly2 = [self.base3, self.base2, self.base4]

	#MODEL#
        self.Model = [self.frontpoly1, self.frontpoly2, self.leftpoly1, self.leftpoly2, self.rightpoly1, self.rightpoly2, self.backpoly1, self.backpoly2, self.toppoly1, self.toppoly2, self.basepoly1, self.basepoly2]

	#POINT CLOUD#
        self.PointCloud = [self.base1, self.base2, self.base3, self.base4, self.top1, self.top2, self.top3, self.top4]

        #SURFACES
        self.surface01 = [self.frontpoly1, self.frontpoly2]
        self.surface02 = [self.leftpoly1, self.leftpoly2]
        self.surface03 = [self.rightpoly1, self.rightpoly2]
        self.surface04 = [self.backpoly1, self.backpoly2]
        self.surface05 = [self.toppoly1, self.toppoly2]
        self.surface06 = [self.basepoly1, self.basepoly2]

        self.ShadingSurface = [self.surface01, self.surface02, self.surface03, self.surface04, self.surface05, self.surface06]

        #SHADING PROPERTIES
        self.color = [78.0/255.0, 106.0/255.0, 90.0/255.0] #RGB
        self.shininess = 2.0 #curly N

    def reset(self):
        self.PointCloud[0][0] = 100.0
        self.PointCloud[0][1] = -50.0
        self.PointCloud[0][2] = 50.0
        self.PointCloud[1][0] = 200.0
        self.PointCloud[1][1] = -50.0
        self.PointCloud[1][2] = 50.0
        self.PointCloud[2][0] = 200.0
        self.PointCloud[2][1] = -50.0
        self.PointCloud[2][2] = 150.0
        self.PointCloud[3][0] = 100.0
        self.PointCloud[3][1] = -50.0
        self.PointCloud[3][2] = 150.0
        self.PointCloud[4][0] = 100.0
        self.PointCloud[4][1] = 50.0
        self.PointCloud[4][2] = 50.0
        self.PointCloud[5][0] = 200.0
        self.PointCloud[5][1] = 50.0
        self.PointCloud[5][2] = 50.0
        self.PointCloud[6][0] = 200.0
        self.PointCloud[6][1] = 50.0
        self.PointCloud[6][2] = 150.0
        self.PointCloud[7][0] = 100.0
        self.PointCloud[7][1] = 50.0
        self.PointCloud[7][2] = 150.0


class Tri_Prism:
    def __init__(self):
        #POINTS#
        self.base1 = [-200.0,-50.0,50.0] #front left
        self.base2 = [-100.0,-50.0,50.0] #front right
        self.base3 = [-150.0,-50.0,150.0] #back center
        self.apex = [-150.0, 50.0, 100.0]

	#POLYGONS#
        self.frontpoly = [self.apex, self.base1, self.base2]
        self.leftpoly = [self.apex, self.base3, self.base1]
        self.rightpoly = [self.apex, self.base2, self.base3]
        self.bottompoly = [self.base1, self.base3, self.base2]

	#MODEL#
        self.Model = [self.frontpoly, self.leftpoly, self.rightpoly, self.bottompoly]

	#POINT CLOUD#
        self.PointCloud = [self.base1, self.base2, self.base3, self.apex]

        #SURFACES
        self.surface01 = [self.frontpoly]
        self.surface02 = [self.leftpoly]
        self.surface03 = [self.rightpoly]
        self.surface04 = [self.bottompoly]

        self.ShadingSurface = [self.surface01, self.surface02, self.surface03, self.surface04]

        #SHADING PROPERTIES
        self.color = [99.0/255.0, 106.0/255.0, 90.0/255.0] #RGB
        self.shininess = 3.5 #curly N

    def reset(self):
    #Doin' it the stupid way for now. Mostly because it's not passed in. A point cloud would need an associated "default position" object for generality.
        self.PointCloud[0][0] = -200.0
        self.PointCloud[0][1] = -50.0
        self.PointCloud[0][2] = 50.0
        self.PointCloud[1][0] = -100.0
        self.PointCloud[1][1] = -50.0
        self.PointCloud[1][2] = 50.0
        self.PointCloud[2][0] = -150.0
        self.PointCloud[2][1] = -50.0
        self.PointCloud[2][2] = 150.0
        self.PointCloud[3][0] = -150.0
        self.PointCloud[3][1] = 50.0
        self.PointCloud[3][2] = 100.0


class pseudo_cylinder:
    def __init__(self):
        #POINTS
        #FACES GO CLOCKWISE
        self.frontface_top1 = [-50.0, 100.0, 50.0] #left top
        self.frontface_top2 = [50.0, 100.0, 50.0] #right top
        self.frontface_right1 = [100.0, 50.0, 50.0] #top right
        self.frontface_right2 = [100.0, -50.0, 50.0] #lower right
        self.frontface_bottom1 = [50.0, -100.0, 50.0] #right bottom
        self.frontface_bottom2 = [-50.0, -100.0, 50.0] #left bottom
        self.frontface_left1 = [-100.0, -50.0, 50.0] #lower left
        self.frontface_left2 = [-100.0, 50.0, 50.0] #top left
        self.frontface_center = [0.0, 0.0, 50.0] #centerpoint
        #COUNTERCLOCKWISE
        self.backface_top1 = [-50.0, 100.0, 250.0] #left top
        self.backface_top2 = [50.0, 100.0, 250.0] #right top
        self.backface_right1 = [100.0, 50.0, 250.0] #top right
        self.backface_right2 = [100.0, -50.0, 250.0] #lower right
        self.backface_bottom1 = [50.0, -100.0, 250.0] #right bottom
        self.backface_bottom2 = [-50.0, -100.0, 250.0] #left bottom
        self.backface_left1 = [-100.0, -50.0, 250.0] #lower left
        self.backface_left2 = [-100.0, 50.0, 250.0] #top left
        self.backface_center = [0.0, 0.0, 250.0] #centerpoint
    
    
        #POLYGONS
        #frontface
        self.frontface_poly1 = [self.frontface_top1, self.frontface_center, self.frontface_top2] #
        self.frontface_poly2 = [self.frontface_top2, self.frontface_center, self.frontface_right1]
        self.frontface_poly3 = [self.frontface_right1, self.frontface_center, self.frontface_right2]
        self.frontface_poly4 = [self.frontface_right2, self.frontface_center, self.frontface_bottom1]
        self.frontface_poly5 = [self.frontface_bottom1, self.frontface_center, self.frontface_bottom2]
        self.frontface_poly6 = [self.frontface_bottom2, self.frontface_center, self.frontface_left1]
        self.frontface_poly7 = [self.frontface_left1, self.frontface_center, self.frontface_left2]
        self.frontface_poly8 = [self.frontface_left2, self.frontface_center, self.frontface_top1]
        #backface
        self.backface_poly1 = [self.backface_top2, self.backface_center, self.backface_top1]
        self.backface_poly2 = [self.backface_right1, self.backface_center, self.backface_top2]
        self.backface_poly3 = [self.backface_right2, self.backface_center, self.backface_right1]
        self.backface_poly4 = [self.backface_bottom1, self.backface_center, self.backface_right2]
        self.backface_poly5 = [self.backface_bottom2, self.backface_center, self.backface_bottom1]
        self.backface_poly6 = [self.backface_left1, self.backface_center, self.backface_bottom2]
        self.backface_poly7 = [self.backface_left2, self.backface_center, self.backface_left1]
        self.backface_poly8 = [self.backface_top1, self.backface_center, self.backface_left2]
        #SIDES
        self.topside_poly1 = [self.backface_top1, self.frontface_top1, self.backface_top2] #
        self.topside_poly2 = [self.backface_top2, self.frontface_top1, self.frontface_top2]
        self.toprightside_poly1 = [self.backface_top2, self.frontface_top2, self.backface_right1]
        self.toprightside_poly2 = [self.backface_right1, self.frontface_top2, self.frontface_right1]
        self.rightside_poly1 = [self.backface_right1, self.frontface_right1, self.backface_right2]
        self.rightside_poly2 = [self.backface_right2, self.frontface_right1, self.frontface_right2]
        self.bottomrightside_poly1 = [self.backface_right2, self.frontface_right2, self.backface_bottom1]
        self.bottomrightside_poly2 = [self.backface_bottom1, self.frontface_right2, self.frontface_bottom1]
        self.bottomside_poly1 = [self.backface_bottom1, self.frontface_bottom1, self.backface_bottom2]
        self.bottomside_poly2 = [self.backface_bottom2, self.frontface_bottom1, self.frontface_bottom2]
        self.bottomleftside_poly1 = [self.backface_bottom2, self.frontface_bottom2, self.backface_left1]
        self.bottomleftside_poly2 = [self.backface_left1, self.frontface_bottom2, self.frontface_left1]
        self.leftside_poly1 = [self.backface_left1, self.frontface_left1, self.backface_left2]
        self.leftside_poly2 = [self.backface_left2, self.frontface_left1, self.frontface_left2]
        self.topleftside_poly1 = [self.backface_left2, self.frontface_left2, self.backface_top1]
        self.topleftside_poly2 = [self.backface_top1, self.frontface_left2, self.frontface_top1]
    
    
        #MODEL
        self.Model = [self.frontface_poly1, self.frontface_poly2, self.frontface_poly3, self.frontface_poly4, self.frontface_poly5, self.frontface_poly6, self.frontface_poly7, self.frontface_poly8, self.backface_poly1, self.backface_poly2, self.backface_poly3, self.backface_poly4, self.backface_poly5, self.backface_poly6, self.backface_poly7, self.backface_poly8, self.topside_poly1, self.topside_poly2, self.toprightside_poly1, self.toprightside_poly2, self.rightside_poly1, self.rightside_poly2, self.bottomrightside_poly1, self.bottomrightside_poly2, self.bottomside_poly1, self.bottomside_poly2, self.bottomleftside_poly1, self.bottomleftside_poly2, self.leftside_poly1, self.leftside_poly2, self.topleftside_poly1, self.topleftside_poly2]


        #POINT CLOUD
        self.PointCloud = [self.frontface_top1, self.frontface_top2, self.frontface_right1, self.frontface_right2, self.frontface_bottom1, self.frontface_bottom2, self.frontface_left1, self.frontface_left2, self.frontface_center, self.backface_top1, self.backface_top2, self.backface_right1, self.backface_right2, self.backface_bottom1, self.backface_bottom2, self.backface_left1, self.backface_left2, self.backface_center]

        #SURFACES
        self.surface01 = [self.topside_poly1, self.topside_poly2, self.toprightside_poly1, self.toprightside_poly2, self.rightside_poly1, self.rightside_poly2, self.bottomrightside_poly1, self.bottomrightside_poly2, self.bottomside_poly1, self.bottomside_poly2, self.bottomleftside_poly1, self.bottomleftside_poly2, self.leftside_poly1, self.leftside_poly2, self.topleftside_poly1, self.topleftside_poly2]

        self.surface02 = [self.frontface_poly1, self.frontface_poly2, self.frontface_poly3, self.frontface_poly4, self.frontface_poly5, self.frontface_poly6, self.frontface_poly7, self.frontface_poly8]

        self.surface03 = [self.backface_poly1, self.backface_poly2, self.backface_poly3, self.backface_poly4, self.backface_poly5, self.backface_poly6, self.backface_poly7, self.backface_poly8]

        self.ShadingSurface = [self.surface01, self.surface02, self.surface03]

        #SHADING PROPERTIES
        self.color = [137.0/255.0, 126.0/255.0, 157.0/255.0] #RGB
        self.shininess = 25.0 #curly N


    #RESET up to 17
    def reset(self):
        self.PointCloud[0][0] = -50.0
        self.PointCloud[0][1] = 100.0
        self.PointCloud[0][2] = 50.0

        self.PointCloud[1][0] = 50.0
        self.PointCloud[1][1] = 100.0
        self.PointCloud[1][2] = 50.0

        self.PointCloud[2][0] = 100.0
        self.PointCloud[2][1] = 50.0
        self.PointCloud[2][2] = 50.0

        self.PointCloud[3][0] = 100.0
        self.PointCloud[3][1] = -50.0
        self.PointCloud[3][2] = 50.0

        self.PointCloud[4][0] = 50.0
        self.PointCloud[4][1] = -100.0
        self.PointCloud[4][2] = 50.0

        self.PointCloud[5][0] = -50.0
        self.PointCloud[5][1] = -100.0
        self.PointCloud[5][2] = 50.0

        self.PointCloud[6][0] = -100.0
        self.PointCloud[6][1] = -50.0
        self.PointCloud[6][2] = 50.0

        self.PointCloud[7][0] = -100.0
        self.PointCloud[7][1] = 50.0
        self.PointCloud[7][2] = 50.0

        self.PointCloud[8][0] = 0.0
        self.PointCloud[8][1] = 0.0
        self.PointCloud[8][2] = 50.0

        #BACKSIDE
        self.PointCloud[9][0] = -50.0
        self.PointCloud[9][1] = 100.0
        self.PointCloud[9][2] = 250.0

        self.PointCloud[10][0] = 50.0
        self.PointCloud[10][1] = 100.0
        self.PointCloud[10][2] = 250.0

        self.PointCloud[11][0] = 100.0
        self.PointCloud[11][1] = 50.0
        self.PointCloud[11][2] = 250.0

        self.PointCloud[12][0] = 100.0
        self.PointCloud[12][1] = -50.0
        self.PointCloud[12][2] = 250.0

        self.PointCloud[13][0] = 50.0
        self.PointCloud[13][1] = -100.0
        self.PointCloud[13][2] = 250.0

        self.PointCloud[14][0] = -50.0
        self.PointCloud[14][1] = -100.0
        self.PointCloud[14][2] = 250.0

        self.PointCloud[15][0] = -100.0
        self.PointCloud[15][1] = -50.0
        self.PointCloud[15][2] = 250.0

        self.PointCloud[16][0] = -100.0
        self.PointCloud[16][1] = 50.0
        self.PointCloud[16][2] = 250.0

        self.PointCloud[17][0] = 0.0
        self.PointCloud[17][1] = 0.0
        self.PointCloud[17][2] = 250.0
