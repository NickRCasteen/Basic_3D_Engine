#Nicholas Reno Casteen
#102-28-520
#Datestamp: Feb 26 2018 2:40 AM
#Assignment #5 SUPPLEMENT 1
#------------------------- DESCRIPTION -------------------------
#	This file holds the classes for the objects to be rendered in the scene, including their methods for detecting intersection and calculating pixel color.

import math


#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> #SPHERE# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
class sphere:
	def __init__(self, center, colorrgb, radius):
		#Be sure to pass in illumination model function
		self.centerpoint = center
		self.color = colorrgb
		self.r = radius

	def get_color(self, x, z):
		return self.color

	def intersect(self, viewvector, rayvector, t):
		#info will be:
		#info[0] = 1 for intersected 0 for not intersected
		#info[1] = t, left unchanged if we didn't intersect or there's something closer.
		#info[2] = the intersection point. So there's info[2][0], info[2][1] and info[2][2]
		#info[3] = the normal of the surface, info[3][0], info[3][1], info[3][2]. Even checkerboard outputs this. It has to.

		#TODO: If this doesn't work, you probably fucked something here. Try splitting it.
		#ASPHERE
		asphere = rayvector[0]*rayvector[0] + rayvector[1]*rayvector[1] + rayvector[2]*rayvector[2]

		#BSPHERE
		bsphere1 = 2.0 * rayvector[0] * (viewvector[0]-self.centerpoint[0])
		bsphere2 = 2.0 * rayvector[1] * (viewvector[1]-self.centerpoint[1])
		bsphere3 = 2.0 * rayvector[2] * (viewvector[2]-self.centerpoint[2]) #Basically

		bsphere = bsphere1 + bsphere2 + bsphere3

		#CSPHERE
		csphere1 = self.centerpoint[0]*self.centerpoint[0]+self.centerpoint[1]*self.centerpoint[1]+self.centerpoint[2]*self.centerpoint[2]

		csphere2 = viewvector[0]*viewvector[0]+viewvector[1]*viewvector[1]+viewvector[2]*viewvector[2]

		csphere3 = 2.0*(-self.centerpoint[0]*viewvector[0]-self.centerpoint[1]*viewvector[1]-self.centerpoint[2]*viewvector[2])

		csphere4 = self.r*self.r


		csphere = csphere1 + csphere2 + csphere3 - csphere4

		#DISCRIMINATE.
		disc = bsphere*bsphere-4.0*asphere*csphere

		if disc < 0:
			info = [0,t,0,0] #Ray lands behind our head.
		else:
			ts1 = (-bsphere + math.sqrt(disc)) / (2.0 * asphere)
			ts2 = (-bsphere - math.sqrt(disc)) / (2.0 * asphere)
			if ts1 >= ts2:
				tsphere = ts2
			else:
				tsphere = ts1

			if t < tsphere:
				#TODO: If problems exist, just make that first 1 a 0 and say no intersection. In fact, fuck it. Do it now.
				info = [0,t,0,0]
			else:
				#The intersection with the object
				interx = viewvector[0] + rayvector[0] * tsphere
				intery = viewvector[1] + rayvector[1] * tsphere
				interz = viewvector[2] + rayvector[2] * tsphere
				intersect = [interx, intery, interz]

				#The normal...of the sphere.
				obj_normx = intersect[0] - self.centerpoint[0]
				obj_normy = intersect[1] - self.centerpoint[1]
				obj_normz = intersect[2] - self.centerpoint[2]
				object_normal = [obj_normx, obj_normy, obj_normz]

				info = [1, tsphere, intersect, object_normal]

		return info


	def point_intensity(self, depth, rayvector, intersection, normalvector, lightintensity, raytracefunction, obList):

		cosine_phi = (-rayvector[0]) * normalvector[0] + (-rayvector[1]) * normalvector[1] + (-rayvector[2]) * normalvector[2]

		if cosine_phi > 0:
			rx = normalvector[0] - (-rayvector[0]) / (2.0 * cosine_phi)
			ry = normalvector[1] - (-rayvector[1]) / (2.0 * cosine_phi)
			rz = normalvector[2] - (-rayvector[2]) / (2.0 * cosine_phi)
		if cosine_phi == 0:
			rx = rayvector[0]
			ry = rayvector[1]
			rz = rayvector[2]
		else:
			#essentially if cosine_phi < 0
			rx = -normalvector[0] + (-rayvector[0]) / (2.0 * cosine_phi)
			ry = -normalvector[1] + (-rayvector[1]) / (2.0 * cosine_phi)
			rz = -normalvector[2] + (-rayvector[2]) / (2.0 * cosine_phi)

		output_ray = [rx, ry, rz]

		#this'll get the reflected stuff. Mm-mm.
		global_rgb = raytracefunction(depth-1, intersection, output_ray, obList)

		#So now we'll have hard-coded percentages. We have the global returned from trace_ray and the intensity from the light model.
		#intensity incorporates the color of the object.
		ir = 0.5 * global_rgb[0]+ 0.5 * lightintensity[0]
		ig = 0.5 * global_rgb[1]+ 0.5 * lightintensity[1]
		ib = 0.5 * global_rgb[2]+ 0.5 * lightintensity[2]

		return [ir,ig,ib]


#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> #CHECKERBOARD# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
class checkerboard:
	def __init__(self):
		self.normal = [0.0, 1.0, 0.0]
		self.anchor_point = [0.0, -500.0, 0.0]
		self.checker_color_red = [255.0/255.0, 0.0/255.0, 0.0/255.0]
		self.checker_color_white = [255.0/255.0, 255.0/255.0, 255.0/255.0]


	def get_color(self, x, z):
		if x >= 0.0:
			cf = 1
		else:
			cf = 0

		if math.fabs(math.fmod(x, 400.0)) > 200.0:
			if cf == 1:
				cf = 0
			else:
				cf = 1

		if math.fabs(math.fmod(z, 400.0)) > 200.0:
			if cf == 1:
				cf = 0
			else:
				cf = 1

		if cf == 1:
			return self.checker_color_red
		else:
			return self.checker_color_white


	def intersect(self, viewvector, rayvector, t):
		#we've pre-defined the normal and the anchor point.
		#info will be:
		#info[0] = 1 for intersected 0 for not intersected
		#info[1] = t, left unchanged if we didn't intersect or there's something closer.
		#info[2] = the intersection point. So there's info[2][0], info[2][1] and info[2][2]
		#info[3] = the normal of the surface, info[3][0], info[3][1], info[3][2]. Even checkerboard outputs this. It has to.
		
		denom = self.normal[0] * rayvector[0] + self.normal[1] * rayvector[1] + self.normal[2] * rayvector[2]

		if math.fabs(denom) <= 0.001:
			info = [0,t,0,0] #ray parallel to plane. Avoids /0
		else:
			d = self.normal[0] * self.anchor_point[0] + self.normal[1] * self.anchor_point[1] + self.normal[2] * self.anchor_point[2]

			t_object = -(self.normal[0]*viewvector[0] + self.normal[1]*viewvector[1] + self.normal[2]*viewvector[2] - d) / denom

			x = viewvector[0] + rayvector[0] * t_object
			y = viewvector[1] + rayvector[1] * t_object
			z = viewvector[2] + rayvector[2] * t_object

			#Weird stuff happened here, having to do with how the...program did the ifs.
			if t_object < 0.0:
				info = [0,t,0,0] #no visible intersection. TODO: Here's where we define the distance of the checkerboard.
			if t < t_object or z<0.0 or z>8000.0:
				info = [0,t,0,0]
			else:
				intersect = [x,y,z]
				info = [1, t_object, intersect, self.normal]

		return info

	def point_intensity(self, depth, rayvector, intersection, normalvector, lightintensity, raytracefunction, obList):
		#Well, it's just going straight up. The actual color is taken care of by the light intensity, so no need to recompute it.

		#So, here. This gets the reflection vector from the incoming rayvector and the normal vector.
		cosine_phi = (-rayvector[0]) * normalvector[0] + (-rayvector[1]) * normalvector[1] + (-rayvector[2]) * normalvector[2]

		if cosine_phi > 0:
			rx = normalvector[0] - (-rayvector[0]) / (2.0 * cosine_phi)
			ry = normalvector[1] - (-rayvector[1]) / (2.0 * cosine_phi)
			rz = normalvector[2] - (-rayvector[2]) / (2.0 * cosine_phi)
		if cosine_phi == 0:
			rx = rayvector[0]
			ry = rayvector[1]
			rz = rayvector[2]
		else:
			#essentially if cosine_phi < 0
			rx = -normalvector[0] + (-rayvector[0]) / (2.0 * cosine_phi)
			ry = -normalvector[1] + (-rayvector[1]) / (2.0 * cosine_phi)
			rz = -normalvector[2] + (-rayvector[2]) / (2.0 * cosine_phi)

		output_ray = [rx, ry, rz]

		#Boom, reflection!
		global_rgb = raytracefunction(depth-1, intersection, output_ray, obList)

		#Light intensity has the color, red or white. Let's make this one less reflective. 40 global, 60 local
		ir = 0.5 * global_rgb[0]+ 0.5 * lightintensity[0]
		ig = 0.5 * global_rgb[1]+ 0.5 * lightintensity[1]
		ib = 0.5 * global_rgb[2]+ 0.5 * lightintensity[2]

		return [ir,ig,ib]

















