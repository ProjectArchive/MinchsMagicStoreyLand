class BreadboardComponent(object):
	"""An abstraction of a breadboard component, any and all components
	that live on our breadboard."""
	
	def __init__(self,width,height,pinList):
		""" Width is the number is columns this component occupies
		height is the number of rows this component occupies
		pinList is a list of Locations where this component must connect
		to the breadboard. Their order within the list represents the
		pin ID to be used in implementing different functionality.
		Pin #1 (index 0) is the reference pin for positioning.
		"""
		self.width = width
		self.height = height
		self.pinList=pinList
		self.referencePin = None #Organize placement via this absolute
		#pin, it is the Location of REF in pinList if this component
		#has been placed on the breadboard.
		
	def __repr__(self):
		return str((self.width, self.height))
