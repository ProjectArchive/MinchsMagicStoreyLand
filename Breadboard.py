from Matrix import *
from Location import *

class Breadboard(object):
	"""represents a breadboard"""
	global numRows
	global numColumns
	numRows = 12
	numColumns = 63
	
	def __init__(self):
		self.locMatrix = Matrix(numRows,numColumns)
		for col in range(numColumns):
			for row in range(numRows):
				#print row,col
				#self.locMatrix.setitem(row,col,Location(col,row))
				a=1
				
				
		
	
