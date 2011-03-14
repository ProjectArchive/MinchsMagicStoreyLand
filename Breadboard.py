from Matrix import *
from Location import *
from Breadboard import *

class Breadboard(object):
	"""represents a breadboard"""
		
	def __init__(self):
		self.numRows = 12
		self.numColumns = 63
		self.locMatrix = Matrix(self.numColumns,self.numRows)
		self.componentList = [] #contains all BreadBoardComponents
		for x in range(self.numColumns):
			for y in range(self.numRows):
				self.locMatrix.setItem(x,y,Location(x,y))	
	def __repr__(self):
		return self.locMatrix.__repr__()
		
	def getLocation(self,x,y):
		return self.locMatrix.getItem(x,y)		

	def isFilled(self,x,y):
		return self.getLocation(x,y).isFilled
	
	def setFilled(self,x,y):
		self.getLocation(x,y).isFilled = True
	
	def translateLocation(self,referenceLocation,relativeLocation):
		"""A method to return the absolute location produced by
		translating the referenceLocation by the displacements specified
		by the relativeLocation. This method returns a REFERENCE to the
		location, and /DOES NOT/ create a new Location.
		"""
		xCoord = referenceLocation.xLoc + relativeLocation.xLoc
		yCoord = referenceLocation.yLoc + relativeLocation.yLoc
		return self.getLocation(xCoord,yCoord)
	
	def translateAllLocations(self,refLoc,relLocs):
		transLocs = []
		for relLoc in relLocs:
			transLocs.append(self.translateLocation(refLoc,relLoc)
		return transLocs
		
	def canPutComponent(self,aComponent,x,y,hard=False):
		"""Tests whether or not a component can be placed at the
		reference (absolute) x,y coordinate by checking each pin
		specified by the pinList of aComponent
		"""
		refLocTest = self.getLocation(x,y) #the loc to test at
		#first test if the reference location is available
		if refLocTest == None or refLocTest.isFilled:
			return False
		else:
			#then check if every pin the component specifies is also
			#available, if not, then we cannot place the component here
			for relLoc in aComponent.pinList:
				if self.translateLocation(refLocTest,relLoc).isFilled:
					return False
		return True
	
	def putComponent(self,aComponent,x,y):
		"""In this first implementation, given a reference pin Location,
		there is only one possible way for the component to be placed.
		This will need to be reworked, as some items will need to be
		able to rotate, also some items have dimensions that can be
		changed very easily (I.E. a resistor or a capacitor)
		"""		
		if self.canPutComponent(aComponent,x,y):
			aComponent.referencePin = self.locMatrix.getItem(x,y)
			absolutePinList = self.translateAllLocations(
			self.setAllFilled(x,y,aComponent.pinList)
			return True
			
		return False
