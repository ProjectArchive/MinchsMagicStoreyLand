from Node import *

class Location(object):
	"""an abstraction of a pin/hole on a BreadBoard. These are 
	typically absolute, with respect to the cartesian coordinate system
	starting at (0,0) for the top left pin. However, subclasses such as
	RelativeLocation use coordinates relative to a reference, for the
	purpose of placing components on the BreadBoard"""
	
	def __init__(self,xIn,yIn):
		self.xLoc = xIn
		self.yLoc = yIn
		self.isFilled = False
		self.node = Node(xIn,yIn)
		
	def __repr__(self):
		return str((self.xLoc, self.yLoc))
		
class RelativeLocation(Location):
	"""An abstraction of a relative location, used for fitting items on
	the bread board, using a reference pin.
	"""
	
	def __init__(self,xIn=0,yIn=0,referenceLocation=None):
		""" Defaults create a REF RelativeLocation"""
		self.referenceLocation = referenceLocation
		Location.__init__(self,xIn,yIn)
		
	def __repr__(self):
		if self.xLoc == 0 and self.yLoc == 0 and self.referenceLocation==None:
			return "REF"
		return Location.__repr__(self) + " From REF"
