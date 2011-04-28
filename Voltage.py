class Voltage(object):
	"""Represents the electrical voltage at a Node object.
	Can be AC or DC, if it is AC, can be given a frequency"""
	
	def __init__(self,volts=0,voltageType='DC',frequency=0):
		"""Either AC or DC, has voltage magnitude, and frequency.
		Standard is 0VDC"""
		self.volts = volts
		self.voltageType = voltageType
		self.frequency = frequency
		
	def __add__(self,other):
		"""in case you need to add DC sources, returns 
		a new Voltage object with that sum"""
		return Voltage((self.volts + other.volts))
	
	def __repr__(self):
		return "%gV%s" %(self.volts,self.voltageType)

