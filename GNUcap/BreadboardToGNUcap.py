import os
from Breadboard import *
from BreadboardComponent import *
from Location import *
class BreadboardToGNUcap(object):
	"""encapsulates a set of methods to
	turn BreadBoard Components into a netlist
	line usable by GNUcap. Also contains anaylsis
	options and the interface with GNUcap"""
	def netListName(self,BreadboardComponent):
		"""uses a component's attributes and name to
		determine the first part of the component's
		netlist definition. 
		For Example:
		If the component is a resistor named Bob, then
		netListName would return RBob as the netlist name
		of the resistor.
		"""
		if BreadboardComponent.attributes != None:
			componentPrefix = BreadBreadboardComponent.displayName[0] 
		else:
			return 1
		componentName = componentPrefix + BreadboardComponent.displayName
		return componentName
	
	def locationToNode(self, Breadboard Component):
		return locNodeDict[Location]
