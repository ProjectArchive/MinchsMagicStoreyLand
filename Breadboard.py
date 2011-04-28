from Matrix import *
from Location import *
from BreadboardComponent import *
import os
import pickle
import copy


class Breadboard(object):
	"""represents a Breadboard.  It consists of a matrix (list of lists)
	of Location objects.  Each Location object is then pointed at
	a particular node object. The coordinate system is (x,-y) or column, 
	row in the matrix.  By default, it is powered like a DAQ powers a breadboard,
	going (bottom to top) ground,2.5V,2.5V,5V.  """
	
	def __init__(self): 
		self.numRows = 18
		self.numColumns = 63
		self.locMatrix = Matrix(self.numColumns,self.numRows)
		self.componentList = []
		self.rails= [0 , 2.5 , 2.5 , 5] #voltage rails. bottom to top. y = 17 16 1 0
		self.initializeLocations()		#assigns Location objects to each coordinate
		self.nodeCreation()				#assigns functional Nodes to proper Locations
		self.detailLocations()			#sets power rails and display flags
		
	def initializeLocations(self):
		"""creates Location objects at every spot in the local matrix.
		doesnt deal with nodes, voltages, or flags"""
		for x in range(self.numColumns):
			for y in range(self.numRows):
				self.locMatrix.setItem(x,y,Location(x,y))
	
	def getLocation(self,x,y):
		"""returns the Location object at a given x,y coordinate"""
		if x>=self.numColumns or y>=self.numRows:
			return None
		if (x<0 and x!=-1) or (y<0):
			return None
		return self.locMatrix.getItem(x,y)
		
	def assignNodeHoriz(self,x,y,number):
		"""assigns a Node object to a Location.
		If the previous x Location already has a Node, the current
		Location simply points to that previous one.
		Represents the fact that power at the rails is all the same node electrically"""
		if self.getLocation(x-1,y).Node.number !=-1:
			self.locMatrix.getItem(x,y).Node = self.locMatrix.getItem(x-1,y).Node
		else:
			self.locMatrix.getItem(x,y).Node = Node(number)
	
	def assignNodeVert(self,x,y,number):
		"""assigns a Node object to a Location.
		If the previous y Location already has a Node, the current
		Location simply points to that previous one.
		Represents the fact that power at each 'five family'
		vertical group is at the same electrical node"""
		if self.getLocation(x,y-1).Node.number !=-1:
			self.locMatrix.getItem(x,y).Node = self.locMatrix.getItem(x,y-1).Node
		else:
			self.locMatrix.getItem(x,y).Node=Node(number)
			
	def nodeCreation(self):
		"""goes through each x,y coordinate on the bb and assigns
		Node objects to all Locations that exist (not including the ones between pins)
		nodes are 0,1,2,3 for GND, power 1,	power 2, and power 3."""
		
		for i in range(self.width):
			self.assignNodeHoriz(i,0,1) #5 Volts
			self.assignNodeHoriz(i,1,2) # 2.5V
			self.assignNodeHoriz(i,16,3) # 2.5V
			self.assignNodeHoriz(i,17,0) # 0 is ground
		for y in range(3,8):
			for x in range(self.width):
				self.assignNodeVert(x,y,4*x)
		for y in range(10,15):
			for x in range(self.width):
				self.assignNodeVert(x,y,4*x+1)
	
	def detailLocations(self):
		"""assigns display flags, which are for coloring the GUI.
		Sets the Location objects at coordinates at which there are no pins 
		to Filled.
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
				if (x+1)%6==0 and (y==0 or y==1 or y==16 or y==17): #fills pins between power fivesomes
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
		"""returns all Locations"""
		return self.locMatrix.__repr__() 
		
	def setNodeVoltage(self,x,y,voltage,voltageType='DC',frequency=0):
		"""changes the Voltage object a particular Location's Node"""
		self.getLocation(x,y).Node.voltage = Voltage(voltage,voltageType,frequency)
		return True

	
	def clearNodeVoltage(self,x,y):
		"""sets the Voltage at a Location's Node to zero."""
		self.setNodeVoltage(x,y,0)
		return True
	
	def getNodeVoltage(self,x,y):
		"""returns Voltage at a Location"""
		return self.getLocation(x,y).Node.voltage

	def isFilled(self,x,y):
		"""tells if a pin at a certain Location is filled"""
		return self.getLocation(x,y).isFilled

	def setFilled(self,x,y):
		"""fills a pin at a Location"""
		self.getLocation(x,y).isFilled = True
	
	def setDisplayFlag(self,x,y,displayFlag):
		"""a helper function for setting the color of certain pins in 
		the BB"""
		self.getLocation(x,y).setDisplayFlag(displayFlag)

	def setUnfilled(self,x,y):
		"""unfills a pin at a given Location"""
		self.getLocation(x,y).isFilled = False

	def setAllFilled(self,pinList):
		"""sets all given Locations to be filled. at that point, 
		the reference pin is already defined"""
		for pin in pinList:
			self.setFilled(pin.xLoc,pin.yLoc)

	def setAllUnfilled(self,pinList):
		"""sets all given Locations to be unfilled"""
		for pin in pinList:
			self.setUnfilled(pin.xLoc,pin.yLoc)

	def translateLocation(self,referenceLocation,relativeLocation):
		"""A method to return the absolute Location produced by
		converting the referenceLocation and relativeLocation.
		This method returns a reference to an (absolute) Location.
		"""
		xCoord = referenceLocation.xLoc + relativeLocation.xLoc
		yCoord = referenceLocation.yLoc + relativeLocation.yLoc
		return self.getLocation(xCoord,yCoord)

	def translateAllLocations(self,refLoc,relLocs):
		"""goes through a list of reference pin Locations and relative Locations
		and returns a list of corresponding converted (absolute) Locations"""
		transLocs = []
		for relLoc in relLocs:
			transLocs.append(self.translateLocation(refLoc,relLoc))
		return transLocs

	def canPutComponent(self,aComponent,pinPositions): 
		"""Tests whether or not a component can be placed at the
		reference x,y coordinate by checking if each translated Location
		specified by the pinList of aComponent if filled"""

		for i in range(0,len(pinPositions),2):
			x = pinPositions[i]
			y = pinPositions[i+1]
			refLocTest = self.getLocation(x,y) #the loc to test at
			#first test if the reference location is available
			if refLocTest == None or refLocTest.isFilled:
				return False
			else:
				#then check if every pin the component specifies is also
				#available, if not, then we cannot place the component here
				for relLoc in aComponent.pinList[1:]:#all but the zero'th pin in the pinlist
					if self.translateLocation(refLocTest,relLoc)==None or self.translateLocation(refLocTest,relLoc).isFilled:
						return False
		return True

	def putComponent(self,aComponent,*args):
		"""This function puts the a component down. First it checks if it can put the component down.
		Then it translates all the relative Locations to absolute ones and fills all the pins.
		Adjusts the component's pin list accordingly.
		Also adds the component to the bb's component list.
		It takes x and y positions as arguments, depending on what type of component, you give it more or less """	
		
		if self.canPutComponent(aComponent,args):
			self.componentList.append(aComponent)
			aComponent.referencePin = self.getLocation(args[0],args[1])
			
			if isinstance(aComponent,FixedBreadboardComponent): #opamps
				aComponent.pinList = self.translateAllLocations(aComponent.referencePin,aComponent.pinList)
				self.setAllFilled(aComponent.pinList)
				aComponent.deadPins = self.translateAllLocations(aComponent.referencePin,aComponent.deadPins)
				self.setAllFilled(aComponent.deadPins)
				if aComponent.displayName=='Input Device':	#Sets voltage from input device
					self.setNodeVoltage(args[0],args[1],aComponent.voltage.volts,aComponent.voltageType,aComponent.frequency)
				return True
				
			elif isinstance(aComponent,VariableBreadboardComponent):	#resistors
				count=0
				for i in range(0,len(args),2):
					aComponent.pinList[count] = self.locMatrix.getItem(args[i],args[i+1])
					self.setFilled(args[i],args[i+1])
					count+=1
				return True
				
		return False


	def removeComponent(self,aComponent):
		"""removes a component from the breadboard. unfills all the Locations it was anchored to
		 and pops it from the breadboard component list. then deletes the component from memory. 
		 if its an op amp this function also unfills the pins in between.
		 If an input device it sets the voltage back to zero"""
		self.setAllUnfilled(aComponent.pinList)
		self.componentList.remove(aComponent)
		if isinstance(aComponent,InputDevice):
			self.clearNodeVoltage(aComponent.pinList[0].xLoc,aComponent.pinList[0].yLoc)
		elif isinstance(aComponent,FixedBreadboardComponent):
			self.setAllUnfilled(aComponent.deadPins)
		for val in globals():  #actually kills the global variable aComponent refers to
			if globals()[val]==aComponent:
				del globals()[val]
				return True
		return False
		
	def clearBreadboard(self):
		""" Removes all components from component list
		unfills all pins deletes all components from memory.
		Sets all nodes back to zero.
		Puts rails back to standard."""
		
		while len(self.componentList) > 0:
			for pin in self.componentList[0].pinList:
				self.clearNodeVoltage(pin.xLoc,pin.yLoc)
			self.removeComponent(self.componentList[0])		
		self.setVoltageAtRail0(0) 	#standard
		self.setVoltageAtRail1(2.5)	
		self.setVoltageAtRail2(2.5)
		self.setVoltageAtRail3(5)

	def unplugComponent(self,aComponent): 
		"""removes a breadboard component, but doesn't delete.
		unfills the Locations the breadboard was previously on, and
		reverts the component's pin list to its original list of 
		Relative Locations.  this allows you to put the component back down somewhere else"""
		self.setAllUnfilled(aComponent.pinList)
		self.setAllUnfilled(aComponent.deadPins)
		if isinstance(aComponent,InputDevice): #set voltage back to normal
			self.clearNodeVoltage(aComponent.pinList[0].xLoc,aComponent.pinList[0].yLoc)
		aComponent.pinList = aComponent.standardPinList
		return True


	def checkDistance(self,x,y,aComponent):
		"""Makes sure we aren't stretching a variable component
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
		"""Opens a pickled breadboard text file.
		This is a static method because we want to be able to open
		a breadboard before we have one initialized"""
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
		"""Rotates a fixed bbc pi radians.
		Useful for op amps, which might be oriented left-right
		or right-left depending on the user"""
		if not isinstance(aComponent,FixedBreadboardComponent):
			return False
		pinListCopy = copy.copy(aComponent.pinList)
		lenth = len(aComponent.pinList)
		for i in range(lenth):
			aComponent.pinList[i] = pinListCopy[(i+lenth/2)%(lenth)]  #adds half the length
		return True
	
	def getComponentAtLocation(self,x,y): 
		"""returns the component at a Location"""
		for component in self.componentList:
			for pin in component.pinList:
				if pin.xLoc==x and pin.yLoc==y:
					return component
			if isinstance(component,FixedBreadboardComponent):
				for pin in component.deadPins:
					if pin.xLoc==x and pin.yLoc==y:
						return component
		return None

		
	def setVoltageAtRail1(self,voltage):
		"""sets Node Voltage at the second rail, second from
		bottom, y=16"""
		self.rails[1]=voltage
		self.setNodeVoltage(0,16,voltage)
		return True
		
	def setVoltageAtRail2(self,voltage):
		"""sets Node Voltage at third from bottom rail,
		second from top,y=1"""
		self.rails[2]=voltage
		self.setNodeVoltage(0,1,voltage)
		return True
		
	def setVoltageAtRail3(self,voltage):
		"""sets Node Voltage at topmost rail,y=0"""
		self.rails[3]=voltage
		self.setNodeVoltage(0,0,voltage)
		return True


if __name__ == "__main__":
	bb = Breadboard()
