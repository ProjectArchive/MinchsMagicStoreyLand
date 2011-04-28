from Location import *
import copy

class BreadboardComponent(object):
	"""An abstraction of a breadboard component. any and all components
	that may live on our breadboard. """
	
	def __init__(self,attributes,displayName,spiceName,technicalName,referencePin,pinList):
		""" General breadboard component. Pin #1 (index 0) is the reference pin for positioning.
		attributes are qualities, like resistance"""
		self.attributes = attributes #attributes is a dict of attributes i.e. "resistance":50
		self.displayName = displayName 	#informal name, i.e. resistor/opAmp
		self.technicalName = technicalName #model number, i.e. OPA551
		self.spiceName = spiceName #the string used to interface with third party program/library
		self.referencePin = referencePin #the upper left pin of this component
		self.pinList = pinList #a list (initially) of RelativeLocations representing pin geometry with respect to the referencePin
		self.standardPinList = copy.copy(pinList) #saves initialized relative Location list so that we can revert a component back to it

	def __repr__(self):
		return '%s' % self.displayName


class FixedBreadboardComponent(BreadboardComponent):
	"""An abstraction of a breadboard component--but only
	components that have a fixed size, like an op-amp, or a scope."""
	
	def __init__(self,width,height,pinList,attributes,displayName,spiceName,technicalName,referencePin,deadPins):
		""" width is number columns, height is the
		number of rows, pinList is locations where the pins are, 
		attributes are qualities (like resistance). All pin List Locations are initially
		based relatively off the Location of a reference pin.
		deadPins are the Locations that sit underneath a component's body and can't be used"""
		
		BreadboardComponent.__init__(self,attributes,displayName,spiceName,technicalName,referencePin,pinList)
		self.width = width
		self.height = height
		self.deadPins = deadPins


class VariableBreadboardComponent(BreadboardComponent):
	"""An abstraction of a breadboard component--ones 
	that can be rotated or cut, like a resistor or a wire"""
	
	def __init__(self,maxLength,attributes,displayName,spiceName,technicalName,referencePin,pinList):
		""" maxLength is the maximum number
		of pins this thing can expand to."""
		BreadboardComponent.__init__(self,attributes,displayName,spiceName,technicalName,referencePin,pinList)
		self.maxLength = maxLength


class Resistor(VariableBreadboardComponent):
	"""A two pin resistor having size range 1 pin to 30 pins.
	Only attribute is resistance."""
	
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
	"""A two pin wire.  Has no attributes. It's actually a 
	pico-ohm resistor for the purposes of Spice, since Spice
	doesn't deal with pure wires."""
	
	def __init__(self):
		"""its a wire, but actually a pico-ohm resistor"""
		Resistor.__init__(self,10**-9)
		self.displayName = 'Wire'
		self.technicalName = 'Wire'
	
	def __repr__(self):
		return "Wire at ref pin %g,%g" %(self.referencePin.xLoc,self.referencePin.yLoc)

class Capacitor(VariableBreadboardComponent):
	"""A two pin capacitor of size 1 to 30 pins.
	Only attribute is capacitance"""

	def __init__(self,capacitance):
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
	"""An eight-pin op amp. doesnt have any attributes."""
	
	def __init__(self):
		"""reference is location of bottom left pin. the numbering of pins
		from 1 to 8 is the same as on a circuit diagram"""		
		referencePin = RelativeLocation()
		pin2 = RelativeLocation(1,0)
		pin3 = RelativeLocation(2,0)
		pin4 = RelativeLocation(3,0)
		pin5 = RelativeLocation(3,-3)
		pin6 = RelativeLocation(2,-3)
		pin7 = RelativeLocation(1,-3)
		pin8 = RelativeLocation(0,-3)
		pinList = [referencePin,pin2,pin3,pin4,pin5,pin6,pin7,pin8]
		
		#now, the pins that the op-amp covers up
		deadPin0 = RelativeLocation(0,-1)
		deadPin1 = RelativeLocation(1,-1)
		deadPin2 = RelativeLocation(2,-1)
		deadPin3 = RelativeLocation(3,-1)
		deadPin4 = RelativeLocation(0,-2)
		deadPin5 = RelativeLocation(1,-2)
		deadPin6 = RelativeLocation(2,-2)
		deadPin7 = RelativeLocation(3,-2)
		deadPins = [deadPin0,deadPin1,deadPin2,deadPin3,deadPin4,deadPin5,deadPin6,deadPin7]
		
		technicalName = 'OPA551'
		attributes = {} 
		displayName = 'OpAmp' #default
		spiceName = 'X'
	
		FixedBreadboardComponent.__init__(self,4,4,pinList,attributes,displayName,spiceName,technicalName,referencePin,deadPins)


class InputDevice(FixedBreadboardComponent):
	"""An input device.  Is capable of outputting AC or DC voltage or currrent.
	Takes in voltage or current magnitude, type, and frequency as floats and sets them 
	as attributes.
	Only one pin, and it eventually changes the Voltage at a Node.
	(We can also fudge it to be a current source, since the only difference for Spice is that
	the title is now an I instead of a V.  We simply pretend that self.volts is now self.amps. 
	it's a little hacky, but works.)"""
	
	def __init__(self,voltage,voltageType='DC',frequency=0,currentOrVoltage='Voltage'):
		referencePin = RelativeLocation(0,0)
		self.voltage = Voltage(voltage,voltageType,frequency)
		self.voltageType = voltageType
		self.frequency = frequency
		self.currentOrVoltage=currentOrVoltage
		pinList = [referencePin]
		attributes={'Voltage Type':voltageType,'Voltage':voltage,'Frequency':frequency}
		width=1
		height=1
		deadPins=[]
		if self.currentOrVoltage=='Current':
			technicalName = '%gAmps %s %gHz' % (self.voltage.volts,self.voltageType,self.frequency)
			spiceName = 'I'
		else:
			technicalName = '%gVolts %s %gHz' % (self.voltage.volts,self.voltageType,self.frequency)
			spiceName = 'V'
		displayName = 'Input Device'
		FixedBreadboardComponent.__init__(self,width,height,pinList,attributes,displayName,spiceName,technicalName,referencePin,deadPins)


class Scope(FixedBreadboardComponent):
	"""Basically a flag for the gui to make a plot.
	It only has one pin, and does nothing to change a circuit,
	no attriutes."""

	def __init__(self):
		attributes={}
		displayName = 'Scope'
		spiceName = ''
		technicalName = ''
		referencePin = RelativeLocation(0,0)
		pinList = [referencePin]
		width=1
		height=1
		deadPins=[]
		FixedBreadboardComponent.__init__(self,width,height,pinList,attributes,displayName,spiceName,technicalName,referencePin,deadPins)
