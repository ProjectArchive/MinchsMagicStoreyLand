import os
from Breadboard import *
from BreadboardComponent import *
from Location import *

class BreadboardToGNUcap(object):
	"""encapsulatst4es a set of methods to
	turn BreadBoard Components into a netlist
	line usable by GNUcap. Also contains anaylsis
	options and the interface with GNUcap"""
	def __init__(self):
		self.width = 63
		self.height = 18
	
	def getNodes(self,BreadboardComponent):
		nodeStr = ' '
		for pins in BreadboardComponent.pinList:
			nodeStr += str(pins.node) + ' '
		return nodeStr
		
	def getAttr(self,BreadboardComponent):
		attributeDict = BreadboardComponent.attributes
		attrKey = attributeDict.keys()[0]
		attrVal = attributeDict[attrKey]
		return str(attrKey[0]),str(attrVal)
		
	def buildText(self,BreadboardComponent):
		nodes = self.getNodes(BreadboardComponent)
		attr = self.getAttr(BreadboardComponent)
		ans = attr[0] + nodes + attr[1]
		return ans
		
	def builtNetList(self,Breadboard):
		netList = ''
		compList = Breadboard.componentList
		for components in compList:
			netList += self.buildText(components) + '\n'
		return netList
		
	def talkToSPICE
		
	
	def __repr__(self):
		return 'at least something worked'
