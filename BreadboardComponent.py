from Location import *

class BreadboardComponent(object):
	"""An abstraction of a breadboard component, any and all components
	that live on our breadboard. """
	
	def __init__(self,attributes,displayName,technicalName,referencePin,pinList):
		""" General breadboard component. Pin #1 (index 0) is the reference pin for positioning.
		attributes are qualities, like resistance"""
		
		self.attributes = attributes
		self.displayName = displayName
		self.technicalName = technicalName
		self.pinList = pinList
		self.referencePin = referencePin
			
	def __repr__(self):
		return 'Generalized Component'


class FixedBreadboardComponent(BreadboardComponent):
	"""An abstraction of a breadboard component--but only
	components that have a fixed size, like an op-amp.  Has attributes
	that are user defined. """
	
	def __init__(self,width,height,pinList,attributes,displayName,technicalName,referencePin):
		""" width is number columns, height is the
		number of rows, pinlist is locations where the pins are, 
		attributes are qualities (like resistance), location based
		off the location of a reference pin"""
		
		BreadboardComponent.__init__(self,attributes,displayName,technicalName,referencePin,pinList)
		self.attributes = attributes
		self.width = width
		self.height = height
		self.maxLength = None
		
	def __repr__(self):
		return 'component of width %d height %d and %d pins' % (self.width, self.height, len(self.pinList))
		
		
class VariableBreadboardComponent(BreadboardComponent):
	"""An abstraction of a breadboard component--ones 
	that have no fixed dimension, like a resistor or a wire"""
	
	def __init__(self,maxLength,attributes,displayName,technicalName,referencePin,pinList):
		""" Radius is the aximum number
		of pins this thing can expand to."""
		
		BreadboardComponent.__init__(self,attributes,displayName,technicalName,referencePin,pinList)
		self.maxLength = maxLength
		
		
	def __repr__(self):
		return 'component'


class Wire(VariableBreadboardComponent):
	"""A two pin wire"""
	
	def __init__(self):
		"""its a wire"""
		
		maxLength = None
		attributes = None
		displayName = 'Wire'
		technicalName = ''
		referencePin = RelativeLocation(0,0)
		secondPin = RelativeLocation(0,0)
		pinList = [referencePin,secondPin]
		VariableBreadboardComponent.__init__(self,maxLength,attributes,displayName,technicalName,referencePin,pinList)
		
	def __repr__(self):
		return "%s at %d,%d"  % (self.displayName,self.referencePin.xLoc,self.referencePin.yLoc)	


class Resistor(VariableBreadboardComponent):
	"""A two pin resistor having size range 1 pin to 20"""
	
	def __init__(self,resistance):
		"""give it a resistance. it is situated at
		relativeLocation 0,0"""
		
		maxLength = 20
		attributes = resistance
		displayName = 'Resistor'
		technicalName = 'R' 
		referencePin = RelativeLocation()
		secondPin = RelativeLocation(0,0)
		pinList = [referencePin,secondPin]
		VariableBreadboardComponent.__init__(self,maxLength,attributes,displayName,technicalName,referencePin,pinList)
		self.resistance = resistance
		
	def __repr__(self):
		return "%g ohm %s at %d,%d"  % (self.resistance,self.displayName,self.referencePin.xLoc,self.referencePin.yLoc)		

class Capacitor(VariableBreadboardComponent):
	"""A two pin capacitor of size 1 to 20 pins"""
	
	def __init__(self,capacitance):
		"""Give it a capacitance"""
		
		maxLength = 20
		attributes = capacitance
		displayName = 'Capacitor'
		technicalName = 'C'
		referencePin = RelativeLocation()
		secondPin = RelativeLocation()
		pinList = [referencePin,secondPin]
		VariableBreadboardComponent.__init__(self,maxLength,attributes,displayName,technicalName,referencePin,pinList)
		self.capacitance = capacitance
		
	def __repr__(self):
		return "%g farad %s at %d,%d" % (self.capacitance,self.displayName,self.referencePin.xLoc,self.referencePin.yLoc)

class OpAmp(FixedBreadboardComponent):
	"""An eight-pin op amp. doesnt have any attributes.
	We start counting pins at 1, like in the real world"""
	
	def __init__(self):
		"""reference is location of bottom left pin
		8 pins. bottom left is reference pin"""
		
		referencePin = RelativeLocation(0,0)
		pin2 = RelativeLocation(1,0)
		pin3 = RelativeLocation(2,0)
		pin4 = RelativeLocation(3,0)
		pin5 = RelativeLocation(0,3)
		pin6 = RelativeLocation(1,3)
		pin7 = RelativeLocation(2,3)
		pin8 = RelativeLocation(3,3)
		pinList=[referencePin,pin2,pin3,pin4,pin5,pin6,pin7,pin8]
		attributes=None
		displayName= 'OpAmp' 		#default
		technicalName = 'OPA551'
		
		FixedBreadboardComponent.__init__(self,4,4,pinList,attributes,displayName,technicalName,referencePin)
		
	def __repr__(self):
		return "%s at %d,%d"  % (self.displayName,self.referencePin.xLoc,self.referencePin.yLoc)		
class QuadChip(FixedBreadboardComponent):
	"""A four op-amp chip. we start counting pins
	at 1, like in the circuit diagrams"""
	
	def __init__(self):
		
		referencePin = RelativeLocation()
		pin2 = RelativeLocation(1,0)
		pin3 = RelativeLocation(2,0)
		pin4 = RelativeLocation(3,0)
		pin5 = RelativeLocation(4,0)
		pin6 = RelativeLocation(5,0)
		pin7 = RelativeLocation(6,0)
		pin8 = RelativeLocation(0,0)
		pin9 = RelativeLocation(1,3)
		pin10 = RelativeLocation(2,3)
		pin11 = RelativeLocation(3,3)
		pin12 = RelativeLocation(4,3)
		pin13 = RelativeLocation(5,3)
		pin14 = RelativeLocation(6,3)
		pinList=[referencePin,pin2,pin3,pin4,pin5,pin6,pin7,pin8,pin9,pin10,pin11,pin12,pin13,pin14]
		width = 7
		height = 4
		attributes = None
		displayName = 'Quad Chip'
		technicalName = 'HDL551'
		FixedBreadboardComponent.__init__(self,width,height,pinList,attributes,displayName,technicalName,referencePin)
	
	def __repr__(self):
		return "%s at %d,%d" % (self.displayName,self.referencePin.xLoc,self.referencePin.yLoc)
