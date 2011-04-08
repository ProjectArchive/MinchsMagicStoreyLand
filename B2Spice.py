import os
from Breadboard import *
from BreadboardComponent import *
from Location import *
from Node import *

class B2Spice(object):
	"""encapsulatstes a set of methods to
	turn BreadBoard Components into a netlist
	line usable by SPICE. Also contains anaylsis
	options and the interface with SPICE"""
	def __init__(self):
		self.width = 63
		self.height = 18
		self.cirName = 'CIRCUIT'+str(id(self))
		os.system('mkdir .temp')
		os.system('cd .temp')
	
	def getNodes(self,component):
		nodeStr = ' '
		for pins in component.pinList:
			nodeStr += str(pins.Node.node) + ' '
		return nodeStr
		
	def getAttr(self,component):
		attributeDict = component.attributes
		attrKey = attributeDict.keys()[0]
		attrVal = attributeDict[attrKey]
		attrKey = attrKey[0] + str(id(component))
		return str(attrKey),str(attrVal)
		
	def buildText(self,component):
		if isinstance(component,Capacitor):
			suffix = ' ic=0'
		else:
			suffix = ''
		nodes = self.getNodes(component)
		attr = self.getAttr(component)
		ans = attr[0] + nodes + attr[1] + suffix
		return ans
	
	def getRail(self,board):
		compList = board.componentList
		for comp in compList:
			for pin in comp.pinList:
				if pin.Node.node < 4 and pin.Node.node >0:
					voltagePower = pin.Node.voltage
					voltageNode = pin.Node.node
				else:
					voltagePower = 0
					voltageNode = 0
		return voltagePower,voltageNode
		
	def getRailandAnal(self,board):
		vPower,vNode = self.getRail(board)
		sourceName = 'v' + str(id(board))
		groundNode =  '0'
		powerNode = str(vNode)
		power = str(vPower)
		sourceLine = sourceName + ' ' + groundNode + ' ' + powerNode + ' dc ' + power
		analysisLine = '.dc ' + sourceName + ' ' + power + ' ' + power + ' 1'
		return sourceLine,analysisLine
		
	def buildNetList(self,board):
		netList = self.cirName + '\n'
		sourceLine,analysisLine = self.getRailandAnal(board)
		netList += sourceLine + '\n'
		compList = board.componentList
		for components in compList:
			netList += self.buildText(components) + '\n'
		netList += analysisLine + '\n'
		netList += '.print dc v(4) \n'
		netList += '.end'
		return netList
		
		
	def sendBbToSpice(self,board):
		fileName = self.cirName + '.cir'
		netList = self.buildNetList(board)
		os.system('touch %s' % fileName) 
		fout = open(fileName,'w')
		fout.write(netList)
		fout.close()
		res = os.system('ngspice -b ' + fileName) 
		os.system('rm ' + fileName)
		os.system('cd ..')
		os.system('rm -rf .temp/')

#~ 
	#~ def getV(self,Node):
		#~ try:
			#~ os.system('v(%d)' % Node.node)
		#~ ##expect module
	
	def __repr__(self):
		return 'at least something worked'

b = B2Spice()
bb = Breadboard()
r1 = Resistor(50)
r2 = Resistor(60)
c1 = Capacitor(.000001)
#~ w1 = Wire()
print bb.putComponent(r1,3,7,31,5)
print bb.putComponent(r2,1,5,3,5)
print bb.putComponent(c1,31,3,25,13)

#~ print isinstance(c1, Capacitor)
#~ bb.putComponent(w1,5,6,6,6)
#~ print r1.pinList
print b.buildNetList(bb)
#~ inter.sendBbToSpice(bb)
