#Nicholas Reno Casteen
#102-28-520
#Datestamp: 13/2/2018
#Assignment #4 SUPPLEMENT 2
#------------------------- DESCRIPTION -------------------------
#	This code contains light classes that hold the date for the light in our engine.

import math

class AmbientLight:
	def __init__(self):
		self.light_color = [220.0/255.0, 255.0/255.0, 255.0/255.0] #every number needs to be from 0 to 1...hmmm, but how? if 0 = 0 and 255 = 1

	def calcAmbLight(self, ShapeColor):
		Red = ShapeColor[0] * self.light_color[0] #now it's an RGB value changed by some ammount from 0 to 1.
		Green = ShapeColor[1] * self.light_color[1]
		Blue = ShapeColor[2] * self.light_color[2]

		return [Red, Green, Blue]

class PointLight:
	def __init__(self):
		self.light_color = [255.0/255.0, 255.0/255.0, 255.0/255.0]  #Color for point light
                self.spec_color = [255.0/255.0, 255.0/255.0, 255.0/255.0] #Color for specular light

		v_in = math.pow(1,2) + math.pow(1,2) + math.pow(-1,2) 
		v_mag = math.sqrt(v_in)

		x = 1.0/v_mag
		y = 1.0/v_mag
		z = (-1.0)/v_mag #This is the light vector normalized.

		self.light_vector = [x, y, z]


	def calcPointLight(self, ShapeColor, Normal):
		Red = self.light_color[0] * ShapeColor[0] * (Normal[0]*self.light_vector[0] + Normal[1]*self.light_vector[1] + Normal[2]*self.light_vector[2])
		Green = self.light_color[1] * ShapeColor[1] * (Normal[0]*self.light_vector[0] + Normal[1]*self.light_vector[1] + Normal[2]*self.light_vector[2])
		Blue = self.light_color[2] * ShapeColor[2] * (Normal[0]*self.light_vector[0] + Normal[1]*self.light_vector[1] + Normal[2]*self.light_vector[2])

		return [Red, Green, Blue]

	def calcSpecularLight(self, ShapeColor, Normal, Shine, d):
		V = [0.0, 0.0, -d] #View Vector
		v_in = math.pow(V[0],2) + math.pow(V[1],2) + math.pow(V[2],2)
		v_mag = math.sqrt(v_in)

		V[0] /= v_mag
		V[1] /= v_mag
		V[2] /= v_mag
                

		cossin = Normal[0]*self.light_vector[0] + Normal[1]*self.light_vector[1] + Normal[2]*self.light_vector[2]

		#This is basically L/2*(N*L) Because I didn't want to type it over and over

		#The 3 cases for the reflection vector
		if cossin > 0:
			light_reducta = [self.light_vector[0]/(2.0*cossin), self.light_vector[1]/(2.0*cossin), self.light_vector[2]/(2.0*cossin)]
			reflectVector = [Normal[0]-light_reducta[0], Normal[1]-light_reducta[1], Normal[2]-light_reducta[2]]
		elif cossin < 0:
			light_reducta = [self.light_vector[0]/(2.0*cossin), self.light_vector[1]/(2.0*cossin), self.light_vector[2]/(2.0*cossin)]
			reflectVector = [-Normal[0]+light_reducta[0], -Normal[1]+light_reducta[1], -Normal[2]+light_reducta[2]]
		else:
			reflectVector = [-self.light_vector[0], -self.light_vector[1], -self.light_vector[2]]

		#normalized
		v_in = math.pow(reflectVector[0],2) + math.pow(reflectVector[1],2) + math.pow(reflectVector[2],2)
		v_mag = math.sqrt(v_in)

		reflectVector[0] /= v_mag
		reflectVector[1] /= v_mag
		reflectVector[2] /= v_mag

		#More stuff pre-calculated for sake of this not being any more of a mess than it already is.
		dotPro = reflectVector[0] * V[0] + reflectVector[1] * V[1] + reflectVector[2] * V[2]
		tailendVector = math.pow(dotPro,Shine)

		Red = self.spec_color[0] * ShapeColor[0] * tailendVector
		Green = self.spec_color[1] * ShapeColor[1] * tailendVector
		Blue = self.spec_color[2] * ShapeColor[2] * tailendVector

		return [Red, Green, Blue]
		

