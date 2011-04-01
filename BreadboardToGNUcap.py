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
		self.width = 63
		self.height = 18
		self.l2n = self.l2nInit()
	
	def netListName(self,BreadboardComponent):
		"""uses a component's attributes and name to
		determine the first part of the component's
		netlist definition. 
		For Example:
		If the component is a resistor named Bob, then
		netListName would return RBob as the netlist name
		of the resistor.
		"""
		return BreadboardComponent.technicalName + BreadboardComponent.displayName
	
	def l2nInit(self):
		"""initializes the dictionary that relates position tuples
		to their relative nodes. nodes are 0,1,2,3 for GND, power 1,
		power 2, and power 3, and take the form 4*x at column x for the top 5 rows,
		and 4*x+1 at column x for the bottom 5 rows."""
		l2n = {}
		for i in range(self.width):
			l2n[(0,i)] = 1 #5 Volts
			l2n[(1,i)] = 2 # 2.5V
			l2n[(16,i)] = 3 # 2.5V
			l2n[(17,i)] = 0 # 0 is ground
		for i in range(3,8):
			for j in range(self.width):
				l2n[(i,j)] = 4*j
		for i in range(10,15):
			for j in range(self.width):
				l2n[(i,j)] = 4*j+1
		return l2n
			
	def nodes(self,BreadboardComponent):
		pinList = BreadboardComponent.pinList
		nodeList = []
		for item in pinList:
			nodeList.append(self.l2n[item])
		return nodeList
		
		
	def __repr__(self):
		return 'at least something worked'

B = BreadboardToGNUcap()
a = B.l2n
Resistor = Resistor(100)
Resistor.pinList = [(1,4),(5,5)]

print B.nodes(Resistor)


