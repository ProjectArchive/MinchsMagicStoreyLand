from Location import *
import copy

class BreadboardComponent(object):
	"""An abstraction of a breadboard component, any and all components
	that live on our breadboard. """
	
	def __init__(self,attributes,displayName,spiceName,technicalName,referencePin,pinList):
		""" General breadboard component. Pin #1 (index 0) is the reference pin for positioning.
		attributes are qualities, like resistance"""
		self.attributes = attributes #attributes is a dict of attributes i.e. "resistance":50
		self.displayName = displayName #informal name, i.e. resistor/opAmp
		self.technicalName = technicalName #model number, i.e. OPA551
		self.spiceName = spiceName #the string used to interface with third party program/library
		self.referencePin = referencePin #the upper left pin of this component
		self.pinList = pinList #a list (initially) of RelativeLocations representing pin geometry with respect to the referencePin
		self.standardPinList = copy.copy(pinList) #saves initialized relativelocaiton list

	def __repr__(self):
		return '%s' % self.displayName


class FixedBreadboardComponent(BreadboardComponent):
	"""An abstraction of a breadboard component--but only
	components that have a fixed size, like an op-amp.  Has attributes
	that are user defined. """
	
	def __init__(self,width,height,pinList,attributes,displayName,spiceName,technicalName,referencePin,deadPins):
		""" width is number columns, height is the
		number of rows, pinlist is locations where the pins are, 
		attributes are qualities (like resistance), location based
		off the location of a reference pin"""
		
		BreadboardComponent.__init__(self,attributes,displayName,spiceName,technicalName,referencePin,pinList)
		self.width = width
		self.height = height
		self.deadPins = deadPins

	#~ def __repr__(self):
		#~ return '%s of size %dx%d attributes %s and %g pins at ref pin %g,%g' % (self.displayName,self.width, self.height,str(self.attributes), len(self.pinList),self.pinList[0].xLoc,self.pinList[0].yLoc)

class VariableBreadboardComponent(BreadboardComponent):
	"""An abstraction of a breadboard component--ones 
	that have no fixed dimension, like a resistor or a wire"""
	
	def __init__(self,maxLength,attributes,displayName,spiceName,technicalName,referencePin,pinList):
		""" maxLength is the maximum number
		of pins this thing can expand to."""
		BreadboardComponent.__init__(self,attributes,displayName,spiceName,technicalName,referencePin,pinList)
		self.maxLength = maxLength

	#~ def __repr__(self):
		#~ return '%s of %s %s at ref pin %g,%g' %(self.displayName,str(self.attributes.keys()),str(self.attributes.values()),self.pinList[0].xLoc,self.pinList[0].yLoc)

class Resistor(VariableBreadboardComponent):
	"""A two pin resistor having size range 1 pin to 30"""
	
	def __init__(self,resistance):
		"""give it a resistance. it is situated at
		relativeLocation 0,0"""
		maxLength = 30
		attributes = {'Resistance':resistance} #'string' mapping to int
		displayName = 'Resistor'
		spiceName = 'R'
		technicalName = 'Resistor'
		referencePin = RelativeLocation()
		secondPin = RelativeLocation(0,0)
		pinList = [referencePin,secondPin]
		VariableBreadboardComponent.__init__(self,maxLength,attributes,displayName,spiceName,technicalName,referencePin,pinList)

class Wire(Resistor):
	"""A two pin wire"""
	
	def __init__(self):
		"""its a wire, but actually a pico-ohm resistor"""
		Resistor.__init__(self,10**-9)
	
	def __repr__(self):
		return "Wire at ref pin %g,%g" %(self.referencePin.xLoc,self.referencePin.yLoc)

class Capacitor(VariableBreadboardComponent):
	"""A two pin capacitor of size 1 to 30 pins"""

	def __init__(self,capacitance):
		"""Give it a capacitance"""
		maxLength = 30
		attributes = {'Capacitance':capacitance}
		displayName = 'Capacitor'
		spiceName = 'C'
		technicalName = 'Capacitor'
		referencePin = RelativeLocation()
		secondPin = RelativeLocation()
		pinList = [referencePin,secondPin]
		VariableBreadboardComponent.__init__(self,maxLength,attributes,displayName,spiceName,technicalName,referencePin,pinList)

class OpAmp(FixedBreadboardComponent):
	"""An eight-pin op amp. doesnt have any attributes.
	We start counting pins at 1, like in the real world"""
	
	def __init__(self,technicalName):
		"""reference is location of bottom left pin
		8 pins. bottom left is reference pin"""		
		referencePin = RelativeLocation()
		pin2 = RelativeLocation(1,0)
		pin3 = RelativeLocation(2,0)
		pin4 = RelativeLocation(3,0)
		pin5 = RelativeLocation(3,-3)
		pin6 = RelativeLocation(2,-3)
		pin7 = RelativeLocation(1,-3)
		pin8 = RelativeLocation(0,-3)
		pinList = [referencePin,pin2,pin3,pin4,pin5,pin6,pin7,pin8]
		
		deadPin0 = RelativeLocation(0,-1)
		deadPin1 = RelativeLocation(1,-1)
		deadPin2 = RelativeLocation(2,-1)
		deadPin3 = RelativeLocation(3,-1)
		deadPin4 = RelativeLocation(0,-2)
		deadPin5 = RelativeLocation(1,-2)
		deadPin6 = RelativeLocation(2,-2)
		deadPin7 = RelativeLocation(3,-2)
		deadPins = [deadPin0,deadPin1,deadPin2,deadPin3,deadPin4,deadPin5,deadPin6,deadPin7]

		attributes = {} #for our purposes, unneeded (max current? rail to rail? max power?)
		displayName = 'OpAmp' #default
		spiceName = 'X'
	
		FixedBreadboardComponent.__init__(self,4,4,pinList,attributes,displayName,spiceName,technicalName,referencePin,deadPins)

class QuadChip(FixedBreadboardComponent):
	"""A 14 pin op amp.
	We start counting pins at 1, like in the real world"""
	
	def __init__(self,technicalName):
		"""reference is location of bottom left pin
		14 pins. bottom left is reference pin"""		
		referencePin = RelativeLocation()
		pin2 = RelativeLocation(1,0)
		pin3 = RelativeLocation(2,0)
		pin4 = RelativeLocation(3,0)
		pin5 = RelativeLocation(4,0)
		pin6 = RelativeLocation(5,0)
		pin7 = RelativeLocation(6,0)
		pin8 = RelativeLocation(6,-3)
		pin9 = RelativeLocation(5,-3)
		pin10 = RelativeLocation(4,-3)
		pin11 = RelativeLocation(3,-3)
		pin12 = RelativeLocation(2,-3)
		pin13 = RelativeLocation(1,-3)
		pin14 = RelativeLocation(0,-3)
	
		deadPin0 = RelativeLocation(0,-1)
		deadPin1 = RelativeLocation(1,-1)
		deadPin2 = RelativeLocation(2,-1)
		deadPin3 = RelativeLocation(3,-1)
		deadPin4 = RelativeLocation(4,-1)
		deadPin5 = RelativeLocation(5,-1)
		deadPin6 = RelativeLocation(6,-1)
		deadPin7 = RelativeLocation(0,-2)
		deadPin8 = RelativeLocation(1,-2)
		deadPin9 = RelativeLocation(2,-2)
		deadPin10 = RelativeLocation(3,-2)
		deadPin11 = RelativeLocation(4,-2)
		deadPin12 = RelativeLocation(5,-2)
		deadPin13 = RelativeLocation(6,-2)
		deadPins = [deadPin0,deadPin1,deadPin2,deadPin3,deadPin4,deadPin5,deadPin6,deadPin7,deadPin8,deadPin9,deadPin10,deadPin11,deadPin12,deadPin13]
	
		pinList = [referencePin,pin2,pin3,pin4,pin5,pin6,pin7,pin8,pin9,pin10,pin11,pin12,pin13,pin14]
		attributes = {} #for our purposes, unneeded (max current? rail to rail? max power?)
		displayName = 'QuadChip' #default
		spiceName = 'e' #?maybe...
		
		FixedBreadboardComponent.__init__(self,7,4,pinList,attributes,displayName,spiceName,technicalName,referencePin,deadPins)

class InputDevice(BreadboardComponent):
	"""An input device.  Is capable of outputting AC or DC
	Takes in voltage as an integer.
	Only one pin, as the other one is usually grounded. MAYBE?"""
	
	def __init__(self,voltage,voltageType='DC',frequency=0,currentOrVoltage='Voltage'):
		referencePin = RelativeLocation(0,0)
		self.voltage = Voltage(voltage,voltageType,frequency)
		self.voltageType = voltageType
		self.frequency = frequency
		self.currentOrVoltage=currentOrVoltage
		pinList = [referencePin]
		attributes={}
		if self.currentOrVoltage=='Current':
			displayName = 'Current Input Device'
			technicalName = '%gAmps %s %gHz' % (self.voltage.volts,self.voltageType,self.frequency)
			spiceName = 'I'
		else:
			displayName = 'Voltage Input Device'
			technicalName = '%gVolts %s %gHz' % (self.voltage.volts,self.voltageType,self.frequency)
		
		#~ technicalName = '%g%s%gHz' % (self.voltage.volts,self.voltageType,self.frequency)
		spiceName = 'V'
		BreadboardComponent.__init__(self,attributes,displayName,spiceName,technicalName,referencePin,pinList)
		
class Scope(BreadboardComponent):
	"""Basically a flag for the gui to make a plot"""

	def __init__(self):
		attributes={}
		displayName = 'Scope'
		spiceName = ''
		technicalName = ''
		referencePin = RelativeLocation(0,0)
		pinList = [referencePin]
		BreadboardComponent.__init__(self,attributes,displayName,spiceName,technicalName,referencePin,pinList)
