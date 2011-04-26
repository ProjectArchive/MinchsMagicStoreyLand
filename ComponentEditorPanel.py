#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       Part of Minch's Magic Storey Land 2011
#
#       Copyright 2011 Cory Dolphin <wcdolphin@gmail.com>       
import wx
from wx.lib.buttons import GenBitmapToggleButton
from Breadboard import *

class ComponentEditorPanel(wx.Panel):
	"""Display common parts, and a part look up window, if and when we get to that stage"""
	def __init__(self, parent,component, *args, **kwargs):
		wx.Panel.__init__(self, parent,*args,**kwargs)
		self.aDict = {}
		self.vSizer = wx.BoxSizer(wx.VERTICAL)
		self.component = component
		self.createControls()
		self.SetSizerAndFit(self.vSizer)
		self.Layout()
		
	def createControls(self):
		for key,val in self.component.attributes.items():
			tSizer = wx.BoxSizer(wx.wx.HORIZONTAL)
			aCtrl = wx.TextCtrl(parent=self,value=str(val),style=wx.TE_CENTRE)
			self.aDict[key] = aCtrl
			aLabel = wx.StaticText(parent=self,label=str(key),style=wx.TE_CENTRE)
			tSizer.Add(aLabel,1,wx.ALIGN_LEFT)
			tSizer.Add(aCtrl,1,wx.ALIGN_RIGHT)
			self.vSizer.Add(tSizer,wx.ALIGN_TOP)

		
class ComponentEditorFrame(wx.Frame):
	"""Dummy frame"""
	def __init__(self, parent,component):
		wx.Frame.__init__(self, parent,title="Edit Attributes:" + str(component))
		self.component = component
		self.Sizer = wx.BoxSizer(wx.VERTICAL)
		self.cmpPane = ComponentEditorPanel(self,self.component)
		self.Sizer.Add(self.cmpPane,1,wx.ALL)
		self.update =wx.Button(self,label='Update Settings')
		self.update.Bind(wx.EVT_BUTTON,self.buttonPressed)
		self.Sizer.Add(self.update,1,wx.ALL)
		self.SetSizer(self.Sizer)
		self.MakeModal(True)
		self.Fit()
		self.Show()
		self.Bind(wx.EVT_CLOSE,self.close)
	
	def close(self,evt):
		self.MakeModal(False)
		self.Destroy()
		
	def buttonPressed(self,evt):
		for key,val in self.component.attributes.items():
			if self.cmpPane.aDict[key].GetValue() != str(val):
				self.component.attributes[key] = float(self.cmpPane.aDict[key].GetValue())
		self.MakeModal(False)
		self.Destroy()

if __name__ == '__main__':
	"""hey, this is how you incorporate testing into a module! @Dan @Noam"""
	app = wx.App()
	aRes = Resistor(50)
	print aRes.attributes
	ComponentEditorFrame(None, aRes)
	app.MainLoop()
	print aRes.attributes
	

