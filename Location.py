class Location(object):
	"""Each location represents
	a pin on the breadboard"""
	
	global isFilled
	global xLoc
	global yLoc
	
	def __init__(self,xIn,yIn):
		xLoc = xIn
		yLoc = yIn
		isFilled = False
		
	
