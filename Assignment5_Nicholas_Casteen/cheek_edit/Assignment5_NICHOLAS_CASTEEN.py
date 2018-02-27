#Nicholas Reno Casteen
#102-28-520
#Datestamp: Feb 26 2018 2:40 AM
#Assignment #5
#------------------------- DESCRIPTION -------------------------
#	This program is a standalone program, with copy-pasted methods from the previous assignment programs. This program simulates light trajectory using
#	ray-tracing to create a mirror-effect on all objects while also incorporating phong lighting.

import math
from Tkinter import *
from Assignment4_LIGHTS import *
from Assignment5_Objects import *

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> SET UP
CanvasWidth = 700
CanvasHeight = 700
d = 800.0
ZBuffer = []
#LIGHTS
Ambient_L = AmbientLight()
Point_L = PointLight()

lights = [Ambient_L, Point_L]
#OBJECTS
floor = checkerboard()
sphere1 = sphere([300.0, -200.0, 600.0], [120.0/255.0, 180.0/255.0, 0.0/255.0], 250.0)
sphere2 = sphere([0.0, 200.0, 4000.0], [255.0/255.0, 0.0/255.0, 250.0/255.0], 500.0)

Objs = [floor, sphere1, sphere2]

ypos = 0.0
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> SET UP

#STUFF
def draw():
	global d
	global CanvasWidth
	global CanvasHeight
	global Objs
	global ypos
	#SO HERE WE GO, Doing it n doing it n doin it well
	#This will be the full draw function that encapsulates the ray trace for every solitary pixel.

	#>>>> STARTING VARS <<<<
	#screen values
	pixel_x = 0 #For the pixel we're on, in terms of tkinter
	pixel_y = 0
	screen_x = 0 #For the center-justified coords
	screen_y = 0
	#vectors
	camera_vector = [0.0,0.0,-d] #Our eyeball
	ray_vector = [0.0,0.0,0.0] #The vector for the beam shooting out of our eye
	light_intensity = [0.0/255.0,0.0/255.0,0.0/255.0] #The RGB
	#depth
	depth = 5 #the starting depth for every raytrace.

	flushZBuffer()

	#TODO: Is starting on 0 hurting us?
	for pixel_y in range(int(CanvasHeight)):
		for pixel_x in range(int(CanvasWidth)):
			#Now we have a pixel to work on. Of course we want to be center-justified thank you very much.
			screen_x = pixel_x - (CanvasWidth/2.0) #Aha! Center justified is just the pixel minus half the max canvaswidth!
			screen_y = (CanvasHeight/2.0) - pixel_y

			#Now for our specific eyeball ray:
			ray_vector[0] = screen_x - camera_vector[0]
			ray_vector[1] = screen_y - camera_vector[1]
			ray_vector[2] = 0 - camera_vector[2] #That's what ol' uncle mike taught me.

			#Next, for this pixel, we'll get our RGB from the traced ray.
			light_intensity = trace_ray(depth, camera_vector, ray_vector, Objs)

			#Then, draw the pixel!
			drawPixel(pixel_y, pixel_x, getpixelcolor(light_intensity))
		if pixel_y%3 == 0:
			ypos += 1


def trace_ray(depth, camera_vect, ray_vect, obList):
	global CanvasHeight
	global ypos
	#Now it's time to trace the ol ray!
	#TODO: Where oh where to normalize the vectors. We'll start by normalizing all incoming vectors when it's time to do point intensity. Should it be before?
	#STARTING VARS:
	t = 100000 #The distance of the closest object. Start with an ungodly number.
	intersection_point = [0,0,0]
	object_normal = [0,0,0]
	final_rgb = [0.0/255.0,0.0/255.0,0.0/255.0]

	intersect_index = -1 #if -1, then no intersect

	if depth == 0:
		final_rgb = [0.0/255.0,0.0/255.0,0.0/255.0]
	#elif depth == 4:
		#print "Pop depth 2"
	else:
		#The loops???
		for index, obj in enumerate(obList):
			#TODO: ADD PARAMETERS
			info = obj.intersect(camera_vect, normalizeVector(ray_vect), t)
			#info will be:
			#info[0] = 1 for intersected 0 for not intersected
			#info[1] = t, left unchanged if we didn't intersect or there's something closer.
			#info[2] = the intersection point. So there's info[2][0], info[2][1] and info[2][2]
			#info[3] = the normal of the surface, info[3][0], info[3][1], info[3][2]. Even checkerboard outputs this. It has to.
			if info[0] == 1:
				#We intersected with the object!
				#if info[1] < t:
				#the intersected object is closer than current t
				t = info[1]
				intersection_point = info[2]
				object_normal = info[3]
				intersect_index = index #This'll tell us which one to do.
				#So we only take in the smallest t.

		if intersect_index == -1:
			r = 6.0 + ypos
			g = 1.0
			b = 31.0 + ypos
			final_rgb = [r/255.0, g/255.0, b/255.0]
			
			
		else:
			#TODO: ADD PARAMETERS, WITH NORMALIZED VECTORS?
			#Why the x and z of the intersection where the circles don't need it? Because the checkerboard does and I was too lazy for inheritance.
			color = obList[intersect_index].get_color(intersection_point[0], intersection_point[2])

			#Given the object normal and the discovered colored (which, for the checkerboard, can be red or blue), get light intensity.
			light_inten = getLightIntensity(normalizeVector(object_normal), color)			

			#The full list of parameters:
				#The depth, starting from 5 until 0
				#The ray vector, normalized right here in the parameters.
				#The intersection point...incorrectly called a vector in multiple points because it's really just a starting point for the ray.
				#The object's normal, including the checkerboard's 0,1,0, normalized
				#The light intensity, given above
				#trace_ray is...this very function! Thanks, python!
				#oblist is a little cheeky thing I've done where I pass in the list of objects because...ehhhh? In case the passed in trace ray
					#function can't see the global ob list.
			final_rgb = obList[intersect_index].point_intensity(depth, normalizeVector(ray_vect), intersection_point, normalizeVector(object_normal), light_inten, trace_ray, obList)
			#Now object normal and ray vector come pre-normalized!

	return final_rgb #By now final_rgb is...something!


#DRAWING TOOLS
def drawPixel(y, x, rgb):
	global ZBuffer

	display = [x, y] #x and y are already center justified.

	w.create_oval(display[0], display[1], display[0], display[1], outline=rgb)


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

#TOOLS
def normalizeVector(vector):
	v_in = math.pow(vector[0],2) + math.pow(vector[1],2) + math.pow(vector[2],2)
	v_mag = math.sqrt(v_in)

	new_vect = vector
	new_vect[0] /= v_mag
	new_vect[1] /= v_mag
	new_vect[2] /= v_mag

	return new_vect

def flushZBuffer():
	global ZBuffer
	ZBuffer = [[float('inf') for i in range(CanvasWidth)] for j in range(CanvasHeight)] #0,0 is top left, just like display.
	#Also, everything is now infinity, and we can check if a pixel is smaller. MIGHT BE SQUICK BUT I THINK IT WORKED?
	#i is x and j is y. Need to keep that in mind.


#LIGHTING
def getLightIntensity(vector, color):
	global lights
	global d
	#Gotta pass in some vector. A surface normal? A point normal? Who can say.
	p1 = [0.0,0.0,0.0]
	p2 = [0.0,0.0,0.0]
	p3 = [0.0,0.0,0.0]


	p1 = lights[0].calcAmbLight(color) #This comes back as a rgb array

	p2 = lights[1].calcPointLight(color, vector) #This comes back as a rgb array

	p3 = lights[1].calcSpecularLight(color, vector, 3, d) #This comes back as a rgb array

	fin_r = p1[0] + p2[0] + p3[0]
	fin_g = p1[1] + p2[1] + p3[1]
	fin_b = p1[2] + p2[2] + p3[2]

	return [fin_r, fin_g, fin_b]


#STUFF
#debug
def pause():
	raw_input("Press Enter")


root = Tk()
outerframe = Frame(root)
outerframe.pack()

w = Canvas(outerframe, width=CanvasWidth, height=CanvasHeight)
w.pack()

draw()

root.mainloop()
