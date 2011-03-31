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
		self.getLocation(x,y).isFilled = True
	
	def setUnfilled(self,x,y):
		self.getLocation(x,y).isFilled = False
	
	def setAllFilled(self,pinList):
		"""sets all pins filled. at that point, 
		the reference pin is already defined"""
		for pin in pinList:
			self.setFilled(pin.xLoc,pin.yLoc)
			
	
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
	
	def putReferencePin(self,aComponent,x,y):
		"""This function puts the first pin down. 
		If the component has a fixed size, this puts down
		every pin. If it is a variable component, you need to 
		choose the location of the next pin using putNextPin.
		"""		
		
		if self.canPutComponent(aComponent,x,y):
			self.componentList.append(aComponent)
			aComponent.referencePin = Location(x,y)
			if aComponent.type=='Fixed':
				aComponent.pinList = self.translateAllLocations(aComponent.referencePin,aComponent.pinList)
				self.setAllFilled(aComponent.pinList)
				return True
			else:
				aComponent.pinList[0] = self.locMatrix.getItem(x,y)
				self.setFilled(x,y)
				return True
		return False
		

	def putNextPin(self,aComponent,x,y,n=2):
		"""Puts down the nth pin of a variable 
		size component; if you dont give a number,
		it assumes it is a two pin component.  Returns False
		if the component is too short to bridge the gap or the pin is 
		taken."""
		
		n-=1
		if self.canPutComponent(aComponent,x,y):
			self.setFilled(x,y)
			if self.checkDistance(x,y,aComponent):
				return False
				
			aComponent.pinList[n] = self.getLocation(x,y)
			return True
		else:
			return False

	def checkDistance(self,x,y,aComponent):
		return (x**2 + y**2)**.5 > aComponent.maxLength
	
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
			if aComponent.type == 'Fixed':
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
			

			
bb = Breadboard()
minch = OpAmp()
bb.putReferencePin(minch,1,1)
bb.putNextPin(minch,1,1)
bb.movePin(minch,1,1,25,5)
print minch.pinList
