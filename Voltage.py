class Voltage(object):
	"""Represents the voltage at a node.
	Can be AC or DC"""
	
	def __init__(self,currentType='DC',volts=0,frequency=None):
		"""Either AC or DC, has voltage, and frequency.
		Standard is 0VDC"""
		self.currentType = currentType
		self.volts = volts
		self.frequency = None
		
	def __repr__(self):
		return "%gV%s" %(self.volts,self.currentType)
