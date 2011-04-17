from Matrix import *
from Location import *
from BreadboardComponent import *
import os
import pickle


class Breadboard(object):
	"""represents a breadboard.
	By default, is powered like a DAQ powers a breadboard,
	going (bottom to top) ground,2.5V,2.5V,5V"""
	
	def __init__(self): #maybe this should take on voltage rail
		self.numRows = 18
		self.numColumns = 63
		self.locMatrix = Matrix(self.numColumns,self.numRows)
		self.componentList = []
		self.railZero = Voltage(2.5) 
		self.railOne = Voltage(5) 
		self.railTwo = Voltage(5)
		self.railThree = Voltage(0)
		
		for x in range(self.numColumns):
			for y in range(self.numRows):
				self.locMatrix.setItem(x,y,Location(x,y)) #some node logic needs to occur here
				if y==2: #fills pins between rows
					self.setFilled(x,y)
					self.setDisplayFlag(x,y,Location.BLUE_LINE)
				if y==15:
					self.setFilled(x,y)
					self.setDisplayFlag(x,y,Location.RED_LINE)
				if y==8:
					self.setFilled(x,y)
					self.setDisplayFlag(x,y,Location.CENTER_BOTTOM)
				if y==9:
					self.setFilled(x,y)
					self.setDisplayFlag(x,y,Location.CENTER_TOP)
				if x%7==0 and (y==0 or y==1 or y==16 or y==17): #fills pins between power fivesomes
					self.setFilled(x,y)
					self.setDisplayFlag(x,y,Location.BLANK)
				if x==0:	
					self.setNodeVoltage(x,y,self.railZero)	#sets power at top rail
				if x==1:
					self.setNodeVoltage(x,y,self.railOne)	#sets power at second from top rail
				if x==16:
					self.setNodeVoltage(x,y,self.railTwo)	#sets power at third from top rail
				if x==17:
					self.setNodeVoltage(x,y,self.railThree)	#sets power at fourth from top rail
					
	def __repr__(self):
		return self.locMatrix.__repr__() 

	def setNodeVoltage(self,x,y,voltage):
		"""makes a node have a nonzero voltage."""
		self.locMatrix.matrix[x][y].Node.voltage = voltage
		return True
	
	def subtractNodeVoltage(self,x,y,voltage):
		"""Reduces a node's voltage reduced by a certain amount.
		This exists in order to allow for multiple power sources on same node.
		Maybe not that useful, but totally doable by a user."""
		
		newVoltage = self.locMatrix.matrix[x][y].Node.voltage.volts - voltage.volts
		print newVoltage
		self.setNodeVoltage(x,y,newVoltage)
		return True

	def getLocation(self,x,y):
		return self.locMatrix.getItem(x,y)

	def isFilled(self,x,y):
		return self.getLocation(x,y).isFilled
	
	def getNodeVoltage(self,x,y):
		return self.getLocation(x,y).Node.voltage

	def setFilled(self,x,y):
		"""fills a pin"""
		self.getLocation(x,y).isFilled = True
	
	def setDisplayFlag(self,x,y,displayFlag):
		self.getLocation(x,y).setDisplayFlag(displayFlag)

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
		Give it x1,y1,x2,y2 for a variable size component, or x,y for an input device. """	
		
		if self.canPutComponent(aComponent,args):
			self.componentList.append(aComponent)
			aComponent.referencePin = self.getLocation(args[0],args[1])
			if isinstance(aComponent,FixedBreadboardComponent):
				aComponent.pinList = self.translateAllLocations(aComponent.referencePin,aComponent.pinList)
				self.setAllFilled(aComponent.pinList)
				return True
			elif isinstance(aComponent,VariableBreadboardComponent):
				count=0
				for i in range(0,len(args),2):
					aComponent.pinList[count] = self.locMatrix.getItem(args[i],args[i+1])
					self.setFilled(args[i],args[i+1])
					count+=1
				return True
			elif isinstance(aComponent,InputDevice):
				self.setAllFilled(aComponent.pinList)
				self.setNodeVoltage(args[0],args[1],aComponent.voltage)
		return False
	


	def removeComponent(self,aComponent):
		"""removes a component from the breadboard. unfills all the holes and pops it from the breadboard component list.
		then deletes the component from memory"""		
		self.setAllUnfilled(aComponent.pinList)
		self.componentList.remove(aComponent)
		if isinstance(aComponent,InputDevice):
			self.subtractNodeVoltage(aComponent.pinList[0].xLoc,aComponent.pinList[0].yLoc,aComponent.voltage)
		for val in globals():  #actually kills the global variable aComponent refers to
			if globals()[val]==aComponent:
				del globals()[val]
				return True
		return False
		
	def clearBreadboard(self):
		""" Removes all components from component list
		unfills all pins
		deletes all components from memory """
		for component in self.componentList:
			self.removeComponent(component)

	def unplugComponent(self,aComponent): 
		"""removes a breadboard component from the bb by unfilling its pins
		and then switching all locations to rel locs"""
		self.setAllUnfilled(aComponent.pinList)
		aComponent.pinList = aComponent.standardPinList
		return True


	def checkDistance(self,x,y,aComponent):
		"""Makes sure we aren't stretching a component
		beyond its maximum length"""
		if isinstance(aComponent,FixedBreadboardComponent):
			return (x**2 + y**2)**.5 > aComponent.maxLength
		return True
		
	def saveBreadboard(self,savedFileName):
		"""checks if the filetype is a .txt first.
		pickles the object to a string and saves it to the
		working directory"""
		if savedFileName[-4:] != '.txt':
			savedFileName = savedFileName + '.txt'
		os.system('touch ' + savedFileName)
		s = pickle.dumps(self)	
		try:
			fin = open(savedFileName,'w')
			fin.write(s)
			fin.close()
			return True
		except:
			return False
	
	@staticmethod
	def openBreadboard(openFileName):
		"""Opens a pickled breadboard text file"""
		f1 = open(openFileName)
		s = ''
		for line in f1:
			s = s + line
		try:
			bb = pickle.loads(s)
			return bb
		except:
			return None

if __name__=='__main__':
	bb = Breadboard()
	r = InputDevice(10,'DC')
	b = Resistor(10)
	bb.putComponent(r,3,3)
	print bb.getNodeVoltage(3,3)
	#~ bb.putComponent(b,3,4)
	#~ print bb.componentList
	bb.removeComponent(r)
	print bb.getNodeVoltage(3,3)
	bb.saveBreadboard('cool_beans4')
	cc = Breadboard.openBreadboard('cool_beans4.txt')
	print cc.componentList
