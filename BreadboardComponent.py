from Location import *

class BreadboardComponent(object):
	"""An abstraction of a breadboard component, any and all components
	that live on our breadboard. """
	
	def __init__(self,attributes,displayName,technicalName,referencePin):
		""" General breadboard component. Pin #1 (index 0) is the reference pin for positioning.
		attributes are qualities, like resistance"""
		
		self.attributes = attributes
		self.displayName = displayName
		self.technicalName = technicalName
		self.referencePin = referencePin
		
	def __repr__(self):
		return str(self.referencePin)

class FixedBreadboardComponent(BreadboardComponent):
	"""An abstraction of a breadboard component--but only
	components that have a fixed size, like an op-amp.  Has attributes
	that are user defined."""
	
	def __init__(self,width,height,pinList,attributes,referencePin,displayName,technicalName):
		""" width is number columns, height is the
		number of rows, pinlist is locations where the pins are, 
		attributes are qualities (like resistance), location based
		off the location of a reference pin"""
		
		BreadboardComponent.__init__(self,attributes,displayName,technicalName,referencePin)
		self.attributes = attributes
		self.width = width
		self.height = height
		self.pinList = pinList
		
	def __repr__(self):
		return 'component of width %d height %d and %d pins' % (self.width, self.height, len(self.pinList))
class VariableBreadboardComponent(BreadboardComponent):
	"""An abstraction of a breadboard component--ones 
	that have no fixed dimension, like a resistor or a wire"""
	
	def __init__(self,radiusRange,attributes,displayName,technicalName,referencePin):
		""" Radius is the minimum to maximum number
		of pins this thing can expand to."""
		
		BreadboardComponent.__init__(self,attributes,displayName,technicalName,referencePin)
		self.radiusRange = radiusRange
		
	def __repr__(self):
		return 'component of %d pins' % (len(self.pinList))
		
class Resistor(VariableBreadboardComponent):
	"""A two pin resistor.  give it a reference point and a name"""
	
	def __init__(self,resistance):
		"""resistor having size range 1 pin to 20"""
		
		referencePin = RelativeLocation()
		displayName = 'Resistor'
		secondPin = None
		technicalName = 'R'+str(resistance)
		radiusRange = (1,20)
		attributes = resistance
		VariableBreadboardComponent.__init__(self,radiusRange,attributes,displayName,technicalName,referencePin)
		self.resistance = resistance
		
	def __repr__(self):
		return "%d ohm %s at %d,%d"  % (self.resistance,self.displayName,self.referencePin.xLoc,self.referencePin.yLoc)		
class OpAmp(FixedBreadboardComponent):
	"""An eight-pin op amp. give me a reference pin and a name"""
	
	def __init__(self):
		"""reference is location of bottom left pin"""
		
		pin1 = RelativeLocation(0,0)
		pin2 = RelativeLocation(1,0)
		pin3 = RelativeLocation(2,0)
		pin4 = RelativeLocation(3,0)
		pin5 = RelativeLocation(0,3)
		pin6 = RelativeLocation(1,3)
		pin7 = RelativeLocation(2,3)
		pin8 = RelativeLocation(3,3)
		pinList=[pin1,pin2,pin3,pin4,pin5,pin6,pin7,pin8]
		attributes=None
		displayName= 'OpAmp' 		#default
		technicalName = 'OPA551'
		
		FixedBreadboardComponent.__init__(self,4,4,pinList,attributes,pin1,displayName,technicalName)
		
	def __repr__(self):
		return "%s at %d,%d"  % (self.displayName,self.referencePin.xLoc,self.referencePin.yLoc)		


minch = OpAmp()
storey = Resistor(100)

print minch
print storey

