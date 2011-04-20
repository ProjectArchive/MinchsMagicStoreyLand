from Matrix import *
from Location import *
from BreadboardComponent import *
import os
import pickle


class Breadboard(object):
	"""represents a breadboard.
	By default, is powered like a DAQ powers a breadboard,
	going (bottom to top) ground,2.5V,2.5V,5V"""
	
	def __init__(self): 
		self.numRows = 18
		self.numColumns = 63
		self.locMatrix = Matrix(self.numColumns,self.numRows)
		self.componentList = []
		self.rails= [0 , 5 , 5 , 2.5] #voltage rails
		self.initializeLocations()
		self.nodeCreation()
		self.detailLocations()
		
	def initializeLocations(self):
		"""creates locations at every spot.
		doesnt deal with nodes, voltages, or flags"""
				
		for x in range(self.numColumns):
			for y in range(self.numRows):
				self.locMatrix.setItem(x,y,Location(x,y))
	
	def getLocation(self,x,y):
		return self.locMatrix.getItem(x,y)
		
	def assignNodeHoriz(self,x,y,number):
		"""assigns nodes based on the previous nodes
		for a horizontal node, like rails"""
		if self.getLocation(x-1,y).Node.number !=-1:
			self.locMatrix.getItem(x,y).Node = self.locMatrix.getItem(x-1,y).Node
		else:
			self.locMatrix.getItem(x,y).Node = Node(number)
	
	def assignNodeVert(self,x,y,number):
		"""assigns nodes based on the previous nodes
		for a vertical node, like the columns"""
		if self.getLocation(x,y-1).Node.number !=-1:
			self.locMatrix.getItem(x,y).Node = self.locMatrix.getItem(x,y-1).Node
		else:
			self.locMatrix.getItem(x,y).Node=Node(number)
			
	def nodeCreation(self):
		"""goes through each position on the bb and assigns
		nodes to the locations. nodes are 0,1,2,3 for GND, power 1,
		power 2, and power 3"""
		
		width = 63
		for i in range(width):
			self.assignNodeHoriz(i,0,1) #5 Volts
			self.assignNodeHoriz(i,1,2) # 2.5V
			self.assignNodeHoriz(i,16,3) # 2.5V
			self.assignNodeHoriz(i,17,0) # 0 is ground
		for y in range(3,8):
			for x in range(width):
				self.assignNodeVert(x,y,4*x)
		for y in range(10,15):
			for x in range(width):
				self.assignNodeVert(x,y,4*x+1)
	
	def detailLocations(self):
		"""assigns display flags.
		Fills the gaps.
		adds voltage at the rails"""
				
		for x in range(self.numColumns):
			for y in range(self.numRows):
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
				if y==0:	
					self.setNodeVoltage(x,y,self.rails[3])	#sets power at top rail
				if y==1:
					self.setNodeVoltage(x,y,self.rails[2])	#sets power at second from top rail
				if y==16:
					self.setNodeVoltage(x,y,self.rails[1])	#sets power at third from top rail
				if y==17:
					self.setNodeVoltage(x,y,self.rails[0])	#sets power at bottom rail
					
	def __repr__(self):
		return self.locMatrix.__repr__() 
		
	def setNodeVoltage(self,x,y,voltage,voltageType='DC',frequency=0):
		"""makes a node have a nonzero voltage,
		or whatever voltage you want."""
		self.getLocation(x,y).Node.voltage = Voltage(voltage,voltageType,frequency)
		return True
			
	
	def clearNodeVoltage(self,x,y):
		"""sets a voltage to zero."""
		self.setNodeVoltage(x,y,0)
		return True
	
	def getNodeVoltage(self,x,y):
		"""returns voltage at a location"""
		return self.getLocation(x,y).Node.voltage

	def isFilled(self,x,y):
		return self.getLocation(x,y).isFilled

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
			if x>self.numColumns or y>self.numRows:
				return False
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
		"""This function puts the a component down. Give it a reference pin for a regular component.
		Give it x1,y1,x2,y2 for a variable size component, or x,y for an input device. """	
		
		if self.canPutComponent(aComponent,args):
			self.componentList.append(aComponent)
			aComponent.referencePin = self.getLocation(args[0],args[1])
			
			if isinstance(aComponent,FixedBreadboardComponent): #opamps
				aComponent.pinList = self.translateAllLocations(aComponent.referencePin,aComponent.pinList)
				self.setAllFilled(aComponent.pinList)
				aComponent.deadPins = self.translateAllLocations(aComponent.referencePin,aComponent.pinList)
				self.setAllFilled(aComponent.deadPins)
				return True
				
			elif isinstance(aComponent,VariableBreadboardComponent):	#resistors
				count=0
				for i in range(0,len(args),2):
					aComponent.pinList[count] = self.locMatrix.getItem(args[i],args[i+1])
					self.setFilled(args[i],args[i+1])
					count+=1
				return True
				
			elif isinstance(aComponent,InputDevice):	#input devices
				self.setAllFilled(aComponent.pinList)
				aComponent.pinList[0].xLoc,aComponent.pinList[0].yLoc=args[0],args[1]
				self.setNodeVoltage(args[0],args[1],aComponent.voltage.volts,aComponent.voltageType,aComponent.frequency)
				return True
		return False
	


	def removeComponent(self,aComponent):
		"""removes a component from the breadboard. unfills all the holes and pops it from the breadboard component list.
		then deletes the component from memory"""		
		self.setAllUnfilled(aComponent.pinList)
		self.setAllUnfilled(aComponent.deadPins)
		self.componentList.remove(aComponent)
		if isinstance(aComponent,InputDevice):
			self.clearNodeVoltage(aComponent.pinList[0].xLoc,aComponent.pinList[0].yLoc)
		for val in globals():  #actually kills the global variable aComponent refers to
			if globals()[val]==aComponent:
				del globals()[val]
				return True
		return False
		
	def clearBreadboard(self):
		""" Removes all components from component list
		unfills all pins deletes all components from memory """
		for component in self.componentList:
			self.removeComponent(component)

	def unplugComponent(self,aComponent): 
		"""removes a breadboard component from the bb by unfilling its pins
		and then switching all locations to rel locs"""
		self.setAllUnfilled(aComponent.pinList)
		self.setAllUnfilled(aComponent.deadPins)
		if isinstance(aComponent,InputDevice):
			self.clearNodeVoltage(aComponent.pinList[0].xLoc,aComponent.pinList[0].yLoc)
		aComponent.pinList = aComponent.standardPinList
		return True


	def checkDistance(self,x,y,aComponent):
		"""Makes sure we aren't stretching a component
		beyond its maximum length"""
		if isinstance(aComponent,VariableBreadboardComponent):
			return (x**2 + y**2)**.5 > aComponent.maxLength
		return True
		
	def saveBreadboard(self,saveFileName):
		"""checks if the filetype is a .txt first.
		pickles the object to a string and saves it to the
		working directory"""
		if saveFileName[-4:] != '.txt':
			saveFileName = saveFileName + '.txt'
		os.system('touch ' + saveFileName)
		s = pickle.dumps(self)	
		try:
			fin = open(saveFileName,'w')
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
	
	def flipComponent(self,aComponent):
		"""Flips a fixed bbc horizontally."""
		firstHalf = aComponent.pinList[:len(aComponent.pinList)/2]
		secondHalf = aComponent.pinList[len(aComponent.pinList)/2:]
		#~ print firstHalf,secondHalf
		firstHalf.reverse()
		secondHalf.reverse()
		#~ print firstHalf,secondHalf
		firstHalf.append(secondHalf)
		aComponent.pinList = firstHalf
		return True

if __name__ == "__main__":
	bb = Breadboard()
	a = OpAmp('hello')
	bb.putComponent(a,3,7)
	c = Resistor(10)
	d = Capacitor(5)
	r = InputDevice(10)
	
	bb.putComponent(c,4,4,4,5)
	bb.putComponent(d,5,4,5,5)
	bb.putComponent(r,3,3)
	print a.pinList
	bb.flipComponent(a)
	print a.pinList
	


