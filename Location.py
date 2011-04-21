from Node import *
import math

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
	
	def __init__(self,xIn,yIn,node=Node(-1),displayFlag=OPENSLOT):
		"""init Location, this location is at xIn,yIn with a display flag
		 defaulted to an open slot, an empty location with no special
		 display characteristics. 
		 """
		self.xLoc = xIn
		self.yLoc = yIn
		self.isFilled = False
		self.Node = node  
		self.displayFlag = displayFlag
	
	def __repr__(self):
		"""returns an informal representation of this Location """
		suffix = '-Filled' if self.isFilled else '-Empty'
		return str((self.xLoc, self.yLoc)) + suffix
		
	
	def setDisplayFlag(self,displayFlag):
		"""Set display flag, determines the bitmap used to represent this
		 locatio on the breadboard """
		self.displayFlag = displayFlag
	
	def getLocationTuple(self):
		"""simple helper to give location as a tuple for use in GUI"""
		return (self.xLoc,self.yLoc)
		
	def distanceTo(self,otherLoc):
		if type(self) != type(otherLoc):
			return -1
		return math.sqrt((self.xLoc - otherLoc.xLoc)**2 + (self.yLoc - otherLoc.yLoc)**2)
	
			
class RelativeLocation(Location):
	"""An abstraction of a relative location, used for fitting items on
	the bread board, using a reference pin.
	"""
	
	def __init__(self,xIn=0,yIn=0,referenceLocation=None,label=''):
		""" Defaults create a REF RelativeLocation, no special display characteristics"""
		self.referenceLocation = referenceLocation
		self.label = label
		Location.__init__(self,xIn,yIn)
		
	def __repr__(self):
		if self.xLoc == 0 and self.yLoc == 0 and self.referenceLocation==None:
			return "REF"
		return Location.__repr__(self) + " From REF"
		

if __name__=="__main__":
	aLoc = Location(0,0)
	bLoc = Location(5,5)
	print aLoc.distanceTo(bLoc)
