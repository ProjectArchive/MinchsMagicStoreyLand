class Location(object):
	"""Each location represents
	a pin on the breadboard"""
		
	def __init__(self,xIn,yIn):
		self.xLoc = xIn
		self.yLoc = yIn
		self.isFilled = False
		
	def __repr__(self):
		# '(%s,%s)\n' 
		return str((self.xLoc, self.yLoc))
