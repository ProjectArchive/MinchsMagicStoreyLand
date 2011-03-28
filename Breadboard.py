from Matrix import *
from Location import *
from BreadboardComponent import *

class Breadboard(object):
	"""represents a breadboard.
	At root, is powered like a DAQ powers a breadboard,
	going (bottom to top) ground,2.5V,2.5V,5V"""
		
	def __init__(self):
		self.numRows = 12
		self.numColumns = 63
		self.locMatrix = Matrix(self.numColumns,self.numRows)
		self.componentList = [] #contains all BreadBoardComponents
		self.voltageOne = 2.5
		self.voltageTwo = 5
		
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
	
	def setAllFilled(self,pinList):
		"""sets all pins filled. at that point, 
		the reference pin is already defined"""
		for pin in pinList:
			self.setFilled(pin.xLoc,pin.yLoc)
			
	
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
			transLocs.append(self.translateLocation(refLoc,relLoc))
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
	
	def putReferencePin(self,aComponent,x,y):
		"""Second go.  This function puts the first pin down. 
		If component is fixed size, this does the job for you, putting down
		every pin. If it is a variable size one, you need to 
		choose the location of the next pin using putNextPin.
		"""		
		
		if self.canPutComponent(aComponent,x,y):
			
			self.componentList.append(aComponent)
			spot = self.locMatrix.getItem(x,y)
			aComponent.referencePin = spot
			if aComponent.type=='Fixed':
				absolutePinList = self.translateAllLocations(aComponent.referencePin,aComponent.pinList)
				self.setAllFilled(aComponent.pinList)
				return True
			else:
				self.setFilled(x,y)
				return True
		return False
		

	def putNextPin(self,aComponent,x,y,n=2):
		"""Puts down the nth pin of a variable 
		size component"""
		
		n-=1
		if self.canPutComponent(aComponent,x,y):
			import math
			self.setFilled(x,y)
			deltaX = aComponent.referencePin.xLoc-x
			deltaY = aComponent.referencePin.xLoc-x
			distance = (deltaX**2 + deltaY**2)**.5
			aComponent.pinList[n] = self.locMatrix.getItem(x,y)
			if distance > aComponent.radiusRange[1]:
				return False
			return True
		else:
			return False
			

	def sendToGnu(self):
		"""Takes circuit information and sends it to
		GnuCap.  This is the kitchen sink here."""
		
		nodes = []
		for component in self.componentList:
			if component.Referencepin.xLoc==a:
				return 1
			
			
			
hello = Breadboard()
minch = Resistor(100)
brad = Capacitor(10)
hello.putReferencePin(minch,4,6)
print hello.putNextPin(minch,4,7)
print hello.putReferencePin(minch,4,6)

