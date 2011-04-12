from Node import *

class Location(object):
	"""an abstraction of a pin/hole on a BreadBoard. These are 
	typically absolute, with respect to the cartesian coordinate system
	starting at (0,0) for the top left pin. However, subclasses such as
	RelativeLocation use coordinates relative to a reference, for the
	purpose of placing components on the BreadBoard"""
	OPENSLOT =  1
	RED_LINE =  2
	BLUE_LINE = 3
	CENTER_TOP = 4
	CENTER_BOTTOM = 5
	BLANK = 6
	def __init__(self,xIn,yIn,displayFlag=Location.OPENSLOT):
		self.xLoc = xIn
		self.yLoc = yIn
		self.isFilled = False
		self.Node = Node((xIn,yIn))  #Node takes a tuple of x and y
		self.displayFlag = displayFlag
	def __repr__(self):
		suffix = '-Filled' if self.isFilled else '-Empty'
		return str((self.xLoc, self.yLoc)) + suffix
	def setDisplayFlag(self,displayFlag):
		self.displayFlag = displayFlag
		
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
