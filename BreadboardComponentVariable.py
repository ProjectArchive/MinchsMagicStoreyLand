class BreadboardComponentVariable(object):
	"""An abstraction of a breadboard component--ones 
	that have no fixed dimension, like a resistor or a wire"""
	
	def __init__(self,pinRange,pinList):
		""" Radius range is the minimum to maximum number
		of pins this thing can expand to.
		"""

		self.pinList=pinList
		self.pinRange = pinRange
		self.referencePin = None #Organize placement via this absolute
		#pin, it is the Location of REF in pinList if this component
		#has been placed on the breadboard.
		
	def __repr__(self):
		return 'component of %d pins' % (len(self.pinList))
		
	class resistor(object):
		"""A two pin resistor"""
		
		def __init__(self,location1,location2):
			"""location is location of bottom left pin"""
			self.location1 = location1
			self.location2 = location2
			
		def __repr__(self):
			return "resistor at %d and %d"  % (self.location1, self.location2)
		
HDK = BreadboardComponentVariable.resistor(5,6)
something  = BreadboardComponentVariable((1,5),[5])
print HDK
print something

