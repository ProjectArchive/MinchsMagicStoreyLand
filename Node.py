from Voltage import *

class Node(object):
	"""This class represents the in-between
	for spice and the breadboard class"""

	def __init__(self,number):
		"""assigns the node a number
		based on its position use the predetermined 
		nodeDictionary. takes in a tuple containing x and y"""
		
		self.node = number
		self.voltage = Voltage()
			
	
	def __repr__(self):
		return 'the %gth node' % self.node
