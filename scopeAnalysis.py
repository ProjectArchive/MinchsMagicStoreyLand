from Matrix import *
from Location import *
from BreadboardComponent import *
from Breadboard import *
import os
import pickle
import copy

def scopeAnalysis(bb):
	"""searches for the scope or scopes,
	returns list of nodes at which the scops) live.
	also removes the scope from bb component list
	because we dont want to do analysis on them as components"""
	
	scopeNodeDict = {}
	count=0
	for i in range(len(bb.componentList)):
		component = bb.componentList[i]
		if component.displayName=='Scope':
			scopeNodeDict[component.referencePin.Node.number] = i
	for node in scopeNodeDict.values():
		del bb.componentList[i-count]
		count+=1
	return scopeNodeDict.keys()
	
bb = Breadboard.openBreadboard('yousuckatcoding.txt')
c = Scope()
d = Scope()
print bb.putComponent(c,20,3)
print bb.putComponent(d,21,3)
print bb.componentList
print scopeAnalysis(bb)
print bb.componentList

