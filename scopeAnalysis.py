	def scopeAnalysis(self):
		"""searches for the scope or scopes,
		returns list of nodes at which the scops) live.
		also removes the scope from bb component list
		because we dont want to do analysis"""
		
		scopeNodeDict = {}
		for i in range(len(bb.componentList)):
			component = bb.componentList[i]
			if isinstance(component,Scope):
				scopeNodeDict[component.referencePin.Node.number] = i
		for node in scopeNodeDict.values():
			del bb.componentList[i]
		return scopeNodeDict.keys()
