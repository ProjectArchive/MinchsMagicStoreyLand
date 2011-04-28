from Voltage import *

class Node(object):
	"""This class represents the in-between
	for spice and the breadboard class.  A Node lives at a Location
	and each Node has a unique number to it; several Locations share the
	same Node.  Nodes have Voltages, but unless it is a power rail or someone 
	places an input device on it, the Voltage has a value of 0 volts.
	What number Node it is depends on a calculation
	done in Breadboard, and if there is no Node at a Location, such as between rows,
	the value is -1 for debugging purposes."""

	def __init__(self,number=-1):
		self.number = number
		self.voltage = Voltage()
			
	
	def __repr__(self):
		return 'the %gth node' % self.number
