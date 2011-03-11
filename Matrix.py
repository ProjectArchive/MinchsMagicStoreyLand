class Matrix(object):
	def __init__(self, cols, rows):
		self.cols = cols
		self.rows = rows
		 # initialize matrix and fill with zeroes
		self.matrix = []
		for i in range(rows):
			ea_row = []
			for j in range(cols):
				ea_row.append(0)
			self.matrix.append(ea_row)
  
	def setitem(self, col, row, v):
		self.matrix[col][row] = v
  
	def getitem(self, col, row):
		return self.matrix[col][row]
  
	def __repr__(self):
		outStr = ""
		for i in range(self.rows):
			outStr += 'Row %s = %s\n' % (i+1, self.matrix[i])
		return outStr
  
 
