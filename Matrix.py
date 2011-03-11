class Matrix(object):
	"""This class is an abstraction of a two dimensional matrix, where
	there is a list which stores columns, and a given value lives at 
	the index column, row. EX: the value at a given index is found by
	accessing the column in which it lives, at the row'th index of said
	column """
	def __init__(self , cols , rows):
		self.numColumns = cols
		self.numRows = rows
		 # initialize matrix and fill with zeroes
		self.matrix = []
		for i in range(self.numColumns): #for every column we must make a column of length numRows
			ea_col = [] #initalize an empty column
			for j in range(self.numRows): #there are numRows rows in a column
				ea_col.append(0)
			self.matrix.append(ea_col)#append this column to the row
			# which contains column, the overarching matrix
  
	def setItem(self, col, row, v):
		#to set a value, we first get the column in which it lives,
		#then the index at which that value lives, the rowNumber.
		self.matrix[col][row] = v
  
	def getItem(self, col, row):
		return self.matrix[col][row]
  
	def __repr__(self):
		outStr = ""
		for y in range(self.numRows): #grab a "row" index
			currentStr = ""
			for x in range(self.numColumns): #grab a "col" in which that value lives
				currentStr += self.matrix[x][y].__repr__()
			outStr += currentStr + "\n"
		return outStr
  
 
