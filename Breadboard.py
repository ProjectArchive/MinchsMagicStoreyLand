from Matrix import *
from Location import *
from BreadboardComponent import *

class Breadboard(object):
	"""represents a breadboard.
	At root, is powered like a DAQ powers a breadboard,
	going (bottom to top) ground,2.5V,2.5V,5V"""

	def __init__(self): #maybe this should take on voltage rail
		self.numRows = 18
		self.numColumns = 63
		self.locMatrix = Matrix(self.numColumns,self.numRows)
		self.componentList = []
		self.voltageOne = 2.5 #fillers for now
		self.voltageTwo = 5 
		self.voltageThree = 5
		self.voltageFour = 0
		
		for x in range(self.numColumns):
			for y in range(self.numRows):
				self.locMatrix.setItem(x,y,Location(x,y)) #some node logic needs to occur here

	def __repr__(self):
		return self.locMatrix.__repr__() #pretty okay for debugging

	def getLocation(self,x,y):
		return self.locMatrix.getItem(x,y)

	def isFilled(self,x,y):
		return self.getLocation(x,y).isFilled

	def setFilled(self,x,y):
		"""fills a pin"""
		self.getLocation(x,y).isFilled = True

	def setUnfilled(self,x,y):
		"""unfills a pin"""
		self.getLocation(x,y).isFilled = False

	def setAllFilled(self,pinList):
		"""sets all pins filled. at that point, 
		the reference pin is already defined"""
		for pin in pinList:
			self.setFilled(pin.xLoc,pin.yLoc)

	def setAllUnfilled(self,pinList):
		"""sets all pins filled. at that point, 
		the reference pin is already defined"""
		for pin in pinList:
			self.setUnfilled(pin.xLoc,pin.yLoc)

	def translateLocation(self,referenceLocation,relativeLocation):
		"""A method to return the absolute location produced by
		translating the referenceLocation by the displacements specified
		by the relativeLocation. This method returns a reference to an AbsoluteLocation.
		"""
		xCoord = referenceLocation.xLoc + relativeLocation.xLoc
		yCoord = referenceLocation.yLoc + relativeLocation.yLoc
		return self.getLocation(xCoord,yCoord)

	def translateAllLocations(self,refLoc,relLocs):
		transLocs = []
		for relLoc in relLocs:
			transLocs.append(self.translateLocation(refLoc,relLoc))
		return transLocs

	def canPutComponent(self,aComponent,pinPositions): 
		"""Tests whether or not a component can be placed at the
		reference (absolute) x,y coordinate by checking each pin
		specified by the pinList of aComponent"""
		flag=True		
		for i in range(0,len(pinPositions),2):
			x = pinPositions[i]
			y = pinPositions[i+1]
			refLocTest = self.getLocation(x,y) #the loc to test at
			#first test if the reference location is available
			if refLocTest == None or refLocTest.isFilled:
				flag=False
			else:
				#then check if every pin the component specifies is also
				#available, if not, then we cannot place the component here
				for relLoc in aComponent.pinList[1:]:#all but the zero'th pin in the pinlist
					if self.translateLocation(refLocTest,relLoc).isFilled:
						flag=False
		return flag

	def putComponent(self,aComponent,*args):
		"""This function puts the a component down.Give it a reference pin for a regular component.
		Give it x1,y1,x2,y2 for a variable size component. """	
		
		if self.canPutComponent(aComponent,args):
			self.componentList.append(aComponent)
			aComponent.referencePin = self.getLocation(args[0],args[1])
			if isinstance(aComponent,FixedBreadboardComponent):
				aComponent.pinList = self.translateAllLocations(aComponent.referencePin,aComponent.pinList)
				self.setAllFilled(aComponent.pinList)
				return True
			else:
				count=0
				for i in range(0,len(args),2):
					aComponent.pinList[count] = self.locMatrix.getItem(args[i],args[i+1])
					self.setFilled(args[i],args[i+1])
					count+=1
				return True
		return False

	def removeComponent(self,aComponent):
		"""removes a component from the breadboard. unfills all the holes and pops it from the breadboard component list.
		then deletes the component from memory"""		
		self.setAllUnfilled(aComponent.pinList)
		self.componentList.remove(aComponent)
		for val in globals():  #actually kills the global variable aComponent refers to
			if globals()[val]==aComponent:
				del globals()[val]
				return True
		return False
		

	def unplugComponent(self,aComponent): #pass
		self.setAllUnfilled(aComponent.pinList)
		aComponent.pinList = aComponent.standardPinList
		return True

	def checkDistance(self,x,y,aComponent):
		"""Makes sure we aren't stretching a component
		beyond its maximum length"""
		if isinstance(aComponent,FixedBreadboardComponent):
			return (x**2 + y**2)**.5 > aComponent.maxLength
		return True


bb = Breadboard()		
r = Resistor(100)
bb.putComponent(r,1,1,2,2)
m = Capacitor(50)
bb.putComponent(m,1,2,2,3)
bb.removeComponent(m)
z = OpAmp('g','aafd')
bb.putComponent(z,2,5)

print r.pinList
bb.unplugComponent(r)
print r.pinList



