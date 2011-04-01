from Matrix import *
from Location import *
from BreadboardComponent import *

class Breadboard(object):
	"""represents a breadboard.
	At root, is powered like a DAQ powers a breadboard,
	going (bottom to top) ground,2.5V,2.5V,5V"""
		
	def __init__(self):
		self.numRows = 18
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
		"""fills a pin"""
		self.getLocation(x,y).isFilled = True
	
	def setUnfilled(self,x,y):
		"""infills a pin"""
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
		by the relativeLocation. This method returns a new Location.
		"""
		xCoord = referenceLocation.xLoc + relativeLocation.xLoc
		yCoord = referenceLocation.yLoc + relativeLocation.yLoc
		newLoc =self.getLocation(xCoord,yCoord)
		return newLoc
	

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
			for relLoc in aComponent.pinList[1:]: 
				if self.translateLocation(refLocTest,relLoc).isFilled: #hmmm I think somethign is wrong?
					return False
		return True
		
	
	def putComponent(self,aComponent,*args):
		"""This function puts the a component down.
		Give it a reference pin for a regular component.
		Give it x1,y1,x2,y2 for a variable size component. """		

		if self.canPutComponent(aComponent,args[0],args[1]):
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
					self.setFilled(args[0],args[1])
					count+=1
				return True
		return False
	
	def removeComponent(self,aComponent):
		"""removes a component from the breadboard.
		essentially unfills all the holes and pops it from
		the breadboard component list."""
		
		self.setAllUnfilled(aComponent.pinList)
		self.componentList.remove(aComponent)
		
	
	def checkDistance(self,x,y,aComponent):
		"""Makes sure we aren't stretching a component
		beyond its maximum length"""
		return (x**2 + y**2)**.5 > aComponent.maxLength
<<<<<<< HEAD
			

bb = Breadboard()
minch = Wire()
Resist = Resistor(1)
bb.putComponent(Resist,1,3,4,5)
bb.putComponent(minch,1,1,2,2)
print bb.componentList
bb.removeComponent(minch)
print bb
=======
	
	def movePin(self,aComponent,x,y,xNew,yNew):
		"""I designed this function with the intent that the
		user would click a current pin on the breadboard, then click another,
		and the gui would either move the image or not depending on """
		
		count=0 #i realize this is implemented rly inefficiently but it works
		for pin in aComponent.pinList:
			if pin.xLoc==x and pin.yLoc==y:
				pinNo = count
			count+=1
			
		if self.canPutComponent(aComponent,xNew,yNew):
			self.setUnfilled(x,y)
			self.setFilled(xNew,yNew)
			if aComponent.type == 'Fixed': #this should? be ? isinstance(aComponenet,FixedBreadboardComponent
				if pinNo != 0:
					return False
				aComponent.pinList = self.translateAllLocations(self.getLocation(xNew,yNew),aComponent.pinList)
			else:
				aComponent.pinList[pinNo] = self.getLocation(xNew,yNew)
			return True
		return False
			
			
	def highlightFilled(self,x,y):
		"""returns True if pin is available. might be useful
		for the GUI is you want the pins highlighted.
		maybe this can be ran continuously on loop"""
		return self.canPutComponent(x,y)
	
	def sendToGNU(self):
		"""sends stuff to Noam-land"""
		return self.componentList
>>>>>>> 80f98ff4595cf46c6e63a63938ef24ae4ba394f6
