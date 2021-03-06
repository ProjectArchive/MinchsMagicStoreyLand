import os
import subprocess
from Breadboard import *
from BreadboardComponent import *
from Location import *
from Node import *
from Voltage import *

class B2Spice(object):
	
	def __init__(self,board):
		"""initializes a B2Spice analysis object. Create some variable names
			that other methods need access to, along with some file persistence
			names. Also calls some methods used for debugging (currently suppressed)"""
		self.board = board
		self.cirName = 'CIRCUIT%d' % id(self)
		self.fileName = '%s.cir' % self.cirName
		self.resName = '%s_res' % self.cirName
		self.getNodesForPlot()
		self.inputDeviceList = self.getInputDevices()
		self.getInputDevices()
		self.rails = self.getRails()
		self.nodeList = self.getNodeList()

	def getNodesForPlot(self):
		"""maps the nth entry in a circuit to the corresponding node"""
		self.nodePlotDict = {}
		self.nodePlotDict[1] = 1
		self.nodePlotDict[2] = 2
		self.nodePlotDict[3] = 3
		
	def getRails(self):
		"""returns the voltage at every rail on the breadboard"""
		##The 0th value of the list is the bottom of the board
		topRail = self.board.rails[0]
		midTopRail = self.board.rails[1]
		midBotRail = self.board.rails[2]
		botRail = self.board.rails[3]
		return (topRail,midTopRail,midBotRail,botRail)
		
	def makeRailCards(self):
		""""makes the SPICE cards for each rail (a DC source)"""
		railCount = 1;
		railCards = ''
		for item in self.rails:
			if item != 0:
				railCards += 'V%d %g 0 dc %g \n' % (railCount,railCount,item)
				railCount += 1
		return railCards
		
	def getInputDevices(self):
		"""Creates a list of Input Device objects so B2Spice knows exactly
		what's providing voltage/current to the circuit. Does not include
		incoming voltage from voltage rails."""
		inputDeviceList = []
		for comp in self.board.componentList:
			if comp.displayName=='Input Device':
				inputDeviceList.append(comp)
		return inputDeviceList
	
	def makeInputDeviceCards(self):
		"""grabs the list of input devices from getInputDevices and makes a SPICE card for each device,
		based on the characteristics of that device. Only supports voltage sources"""
		if len(self.inputDeviceList) <1:
			return ''
		inputDeviceCards = ''
		for item in self.inputDeviceList:
			if item.attributes['Voltage Type'] == 'AC':
				inputDeviceCards += 'V%d %g 0 ac %g sin \n' % (id(item),item.pinList[0].Node.number,item.pinList[0].Node.voltage.volts)
			else:
				inputDeviceCards += 'V%d %g 0 dc %g \n' % (id(item),item.pinList[0].Node.number,item.voltage.volts)
		return inputDeviceCards

	def makeAnalysisCards(self,analysisType='tran',scopedNode=0,vMin=0,vMax=5,tstep=.01,ttotal=1,stepType='lin',numSteps=20,startFreq=.001,endFreq=100000):
		"""takes arguments for the type of analysis SPICE needs to go, with multiple default arguments, and makes the SPICE analysis cards for the chosen type
		of analysis. SPICE automatically takes care of which source to vary, depending on the type of analysis."""
		if len(self.inputDeviceList) <1:
			return '.dc V1 %g %g 1 V2 %g %g 1 V3 %g %g 1\n.print dc v(%d) \n' % (self.board.rails[1],self.board.rails[1],self.board.rails[2],self.board.rails[2],self.board.rails[3],self.board.rails[3], scopedNode)
		if analysisType == 'ac':
			return self.makeACCards(scopedNode,stepType,numSteps,startFreq,endFreq)
		elif analysisType == 'dc':
			return self.makeDCCards(scopedNode,vMin,vMax,numSteps
			)
		else:
			return self.makeTranCards(scopedNode,tstep,ttotal)
		
	def makeACCards(self,scopedNode,stepType,numSteps,startFreq,endFreq):
		"""given an argument of AC analysis, this method creates the SPICE card that tells SPICE
		to do AC analysis on a given node and print the result."""
		if len(self.inputDeviceList) <1:
			raise NameError('There are no input devices...')
		acLine = '.ac %s %g %g %g \n' % (stepType,numSteps,startFreq,endFreq)
		printLine = '.print ac v(%d) \n' % scopedNode
		return acLine + printLine
	
	def makeDCCards(self,scopedNode,vMin,vMax,numSteps):
		"""given an argument of DC analysis, this method creates the SPICE card that tells SPICE
		to do DC analysis on a given node and print the result."""
		dcInputDeviceList = []
		for item in self.inputDeviceList:
			if item.voltageType == 'DC':
				dcInputDeviceList.append(item)
		self.dcInputDeviceList = dcInputDeviceList
		inp = dcInputDeviceList[0]
		dcLine = '.dc V(%d) %g %g %g \n' % (id(inp),vMin,vMax,numSteps)
		printLine = '.print dc v(%d) \n' % scopedNode 
		return dcLine+printLine
	
	def makeTranCards(self,scopedNode,tstep,ttotal):
		"""given an argument of transient analysis, this method creates the SPICE card that tells SPICE
		to do transient analysis on a given node and print the result."""
		tranLine = '.tran %g %g \n' % (tstep, ttotal)
		printLine = '.print tran v(%d) \n' % scopedNode
		return tranLine+printLine
	
	def clearEmptyNodes(self):
		"""notes how many times a node appears in a circuit.
		if it's only one, and not power, then we take action and remove it"""
		d={}
		for component in self.board.componentList:
			for pin in component.pinList:
				d[pin.Node.number]=d.get(pin.Node.number,0)+1
		for val in d:
			if d[val]==1 and val!=1 and val!=2 and val!=3 and val!=0:
				count=-1
				for component in self.board.componentList:
					count+=1
					for pin in component.pinList:
						if pin.Node.number == val:
							del self.board.componentList[count]
		return d
		
	def getNodeList(self):
		"""Creates a list of all 
		occupied nodes on a breadboard"""
		nodeList = []
		for comp in self.board.componentList:
			for pin in comp.pinList:
				nodeList.append(pin.Node.number)
		return nodeList
		
	def getNodes(self,component):
		"""returns a string that contains
		the nodes of a component, separated by spaces"""
		nodeStr = ' '
		for pins in component.pinList:
			nodeStr += '%d ' % pins.Node.number
		return nodeStr
		
		
	
	def getAttr(self,component):
		"""returns a tuple containing the attribute
		of the component and its value,
		both as strings"""
		attributeDict = component.attributes
		attrKey = attributeDict.keys()[0]
		attrVal = attributeDict[attrKey]
		attrKey = attrKey[0] + str(id(component))
		return str(attrKey),str(attrVal)
					
	def buildVariableComponentText(self,component):
		"""creates the SPICE cards for Resistors, Capacitors and Inductors. If
		the component is a capactior, appends the card with an initial condition."""
		if isinstance(component,Capacitor):
			suffix = ' ic=0'
		else:
			suffix = ''
		nodes = self.getNodes(component)
		attr = self.getAttr(component)
		ans = attr[0] + nodes + attr[1] + suffix + '\n'
		return ans
		
		
	def buildOpAmpText(self,opamp):
		"""returns a tuple describing the nodal location of the opamp with the spice file,
		and a big line of text containing the definition of the opamp, pulled from a persistent file OPA551.txt"""
		pinDict = {}
		pinDict['notUsed1'] = opamp.pinList[0]
		pinDict['negIn'] = opamp.pinList[1]
		pinDict['plusIn'] = opamp.pinList[2]
		pinDict['negSupply'] = opamp.pinList[3]
		pinDict['flag'] = opamp.pinList[4]
		pinDict['plusSupply'] = opamp.pinList[5]
		pinDict['out'] = opamp.pinList[6]
		pinDict['notUsed2'] = opamp.pinList[7]
		opAmpNodeString = '%d %d %d %d %d' % (pinDict['plusIn'].Node.number,pinDict['negIn'].Node.number,pinDict['out'].Node.number,pinDict['plusSupply'].Node.number,pinDict['negSupply'].Node.number)		
		opAmpID = 'X%d' % id(opamp)
		subCktID = 'opamp2'
		subCktFileName = '%s.txt' % opamp.technicalName
		fin = open(subCktFileName)
		opAmpSubCkt = fin.read()
		opAmpCard = '%s %s %s\n' % (opAmpID,opAmpNodeString,subCktID)
		fin.close()
		return (opAmpCard,opAmpSubCkt)
	
	def buildNetList(self,analysisType='tran',scopedNode=0,vMin=0,vMax=5,tstep=.01,ttotal=1,stepType='lin',numSteps=20,startFreq=.001,endFreq=100000):
		"""Creates the necessary files for analysis, and then conducts the anaylsis based on input arguments from the GUI (all are defaulted). Builds the full net list
		for SPICE, using above methods. Writes the full net list to a text file, then uses Subprocess to communicate with ngspice and simulate the circuit. Writes the 
		simulation results to a file, which the GUI grapher then opens. Returns the resulting file name.
		"""
		makeFileCommand = 'touch %s' % self.fileName
		makeFileCommand2 = 'touch %s' % self.resName
		os.system(makeFileCommand)
		os.system(makeFileCommand2)
		netList = self.cirName + '\n'
		netList += self.makeRailCards()
		netList += self.makeInputDeviceCards()
		icCount = 0
		nodePlotCount = 4
		for comp in self.board.componentList:
			if isinstance(comp,VariableBreadboardComponent):
				netList += self.buildVariableComponentText(comp)
				self.nodePlotDict[nodePlotCount] = comp.pinList[0].Node.number
				nodePlotCount += 1
			elif isinstance(comp,OpAmp):
				compCard,subCktCard = self.buildOpAmpText(comp)
				netList += compCard
				self.nodePlotDict[nodePlotCount] = comp.pinList[0].Node.number
				nodePlotCount += 1
				icCount += 1
			else:
				netList += ''
		if icCount > 0:
			netList += subCktCard
		if analysisType == 'dc':
			netList += self.makeAnalysisCards('dc',scopedNode=scopedNode,vMin=vMin,vMax = vMax,numSteps=numSteps)
		if analysisType == 'ac':
			netList += self.makeAnalysisCards('ac',scopedNode=scopedNode,stepType=stepType,numSteps=numSteps,startFreq=startFreq,endFreq=endFreq)
		if analysisType == 'tran':
			netList += self.makeAnalysisCards('tran',scopedNode=scopedNode,tstep=tstep,ttotal=ttotal)
		netList += '.end'
		self.netList = netList
		#File interface stuff
		fout = open(self.fileName,'w')
		fout.write(self.netList)
		fout.close()
		res = subprocess.Popen(['ngspice','-b',self.fileName,'-r',self.resName],stdout=subprocess.PIPE).communicate()[0]
		delFileCommand = 'rm %s' % self.fileName
		os.system(delFileCommand)
		subprocess.Popen(['gwave',self.resName],stdout=subprocess.PIPE).communicate()[0]
		return self.resName
	
	def scopeAnalysis(self):
		"""searches for the scope or scopes,
		returns list of nodes at which the scops) live.
		also removes the scope from breadboard component list
		because we dont want to do analysis with them in the list"""
		
		scopeNodes =[]
		for i in range(len(bb.componentList)):
			if bb.componentList[i].displayName=='Scope':
				scopeNodes.append(bb.componentList[i])
				del bb.componentList[i]
		return scopeNodes
				
				
				
		
		
if __name__ == '__main__':
	#Yay for debugging!!
	bb = Breadboard()
	source = InputDevice(.01,'DC')
	p = OpAmp()
	W1 = Wire()
	W2 = Wire()
	W3 = Wire()
	W4 = Wire()
	C = Capacitor(.01)
	print bb.putComponent(p,3,10)
	print bb.putComponent(source,5,12)
	print bb.putComponent(W1,4,14,4,17)
	print bb.putComponent(W2,6,14,6,17)
	print bb.putComponent(W3,4,6,4,0)
	print bb.putComponent(W4,5,6,7,17)
	print bb.putComponent(C,5,14,3,16)
	b = B2Spice(bb)
	print b.nodeList
	print b.buildNetList('tran',scopedNode=25,tstep = .001,ttotal=1)
	print b.netList
	print b.nodePlotDict
	

	

