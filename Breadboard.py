from Matrix import *
from Location import *
from Breadboard import *

class Breadboard(object):
	"""represents a breadboard"""
		
	def __init__(self):
		self.numRows = 12
		self.numColumns = 63
		self.locMatrix = Matrix(self.numColumns,self.numRows)
		for x in range(self.numColumns):
			for y in range(self.numRows):
				self.locMatrix.setItem(x,y,Location(x,y))	
	def __repr__(self):
		return self.locMatrix.__repr__()

	def isFilled(self,x,y):
		return self.locMatrix.getItem(x,y).isFilled

	def putComponent(aComponent,referencePin):
		"""
		"""
		print "hello"
