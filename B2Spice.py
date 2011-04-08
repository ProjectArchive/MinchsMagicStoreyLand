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
	
	def getNodes(self,BreadboardComponent):
		nodeStr = ' '
		for pins in BreadboardComponent.pinList:
			nodeStr += str(pins.Node.node) + ' '
		return nodeStr
		
	def getAttr(self,BreadboardComponent):
		attributeDict = BreadboardComponent.attributes
		attrKey = attributeDict.keys()[0]
		attrVal = attributeDict[attrKey]
		attrKey = attrKey[0] + str(id(BreadboardComponent))
		return str(attrKey),str(attrVal)
		
	def buildText(self,BreadboardComponent):
		nodes = self.getNodes(BreadboardComponent)
		attr = self.getAttr(BreadboardComponent)
		ans = attr[0] + nodes + attr[1]
		return ans
	
	def getRail(self,Breadboard):
		compList = Breadboard.componentList
		for comp in compList:
			for pin in comp.pinList:
				if pin.Node.node < 4 and pin.Node.node >0:
					voltagePower = pin.Node.voltage
					voltageNode = pin.Node.node
		return voltagePower,voltageNode
		
	def writeVoltageSource(self,Breadboard):
		vPower,vNode = self.getRail(Breadboard)
		sourceName = str(id(Breadboard))
		groundNode =  '0'
		powerNode = str(vNode)
		power = str(vPower)
		return sourceName + ' ' + groundNode + ' ' + powerNode + ' ' + power
		
	def buildNetList(self,Breadboard):
		netList = self.cirName + '\n'
		compList = Breadboard.componentList
		for components in compList:
			netList += self.buildText(components) + '\n'
		source = self.writeVoltageSource(Breadboard)
		netList += source + '\n'
		netList += 'end'
		return netList
		
		
	def sendBbToSpice(self,Breadboard):
		fileName = self.cirName + '.cir'
		netList = self.buildNetList(Breadboard)
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

inter = B2Spice()
bb = Breadboard()
r1 = Resistor(50)
r2 = Resistor(60)
c1 = Capacitor(.000001)
#~ w1 = Wire()
bb.putComponent(r1,1,1,1,2)
bb.putComponent(r2,3,2,3,3)
bb.putComponent(c1,3,4,4,4)
#~ bb.putComponent(w1,5,6,6,6)
#~ print r.pinList
inter.sendBbToSpice(bb)
