class Voltage(object):
	"""Represents the voltage at a node.
	Can be AC or DC"""
	
	def __init__(self,volts=0,voltageType='DC',frequency=None):
		"""Either AC or DC, has voltage, and frequency.
		Standard is 0VDC"""
		self.volts = volts
		self.voltageType = voltageType
		self.frequency = frequency
		
	def __add__(self,other):
		return self.volts + other.volts
	
	def __repr__(self):
		return "%gV%s" %(self.volts,self.currentType)
		
		
