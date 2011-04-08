from Voltage import *

class Node(object):
	"""This class represents the in-between
	for spice and the breadboard class"""

	def __init__(self,position):
		"""assigns the node a number
		based on its position use the predetermined 
		nodeDictionary. takes in a tuple containing x and y"""
		
		self.position = position
		nodeDict = self.nodeDictionary()
		self.node = nodeDict.get((position),-1)
		self.voltage = Voltage()

	
	def nodeDictionary(self):
		"""initializes the dictionary that relates position tuples
		to their relative nodes. nodes are 0,1,2,3 for GND, power 1,
		power 2, and power 3"""
		
		width = 63
		l2n = {}
		for i in range(width):
			l2n[(i,0)] = 1 #5 Volts
			l2n[(i,1)] = 2 # 2.5V
			l2n[(i,16)] = 3 # 2.5V
			l2n[(i,17)] = 0 # 0 is ground
		for i in range(3,8):
			for j in range(width):
				l2n[(j,i)] = 4*j
		for i in range(10,15):
			for j in range(width):
				l2n[(j,i)] = 4*j+1
		return l2n	
			
	
	def __repr__(self):
		return 'the %gth node' % self.node
