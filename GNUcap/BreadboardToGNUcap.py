import os
from Breadboard import *
from BreadboardComponent import *
from Location import *
class BreadboardToGNUcap(object):
	"""encapsulates a set of methods to
	turn BreadBoard Components into a netlist
	line usable by GNUcap. Also contains anaylsis
	options and the interface with GNUcap"""
	def __init__(self):
		self.width = Breadboard.width
		self.height = Breadboard.height
	
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
			componentPrefix = BreadboardComponent.displayName[0] 
		else:
			return 1
		componentName = componentPrefix + BreadboardComponent.displayName
		return componentName
	
	def l2nInit(self):
		l2n = {}
		for i in range(63):
			l2n[(0,i)] = 1
			l2n[(1,i)] = 2
			l2n[(16,i)] = 3
			l2n[(17,i)] = 0
		return l2n

b = BreadboardToGNUcap


