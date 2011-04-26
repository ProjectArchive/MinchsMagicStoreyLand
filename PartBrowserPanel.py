#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       Part of Minch's Magic Storey Land 2011
#
#       Copyright 2011 Cory Dolphin <wcdolphin@gmail.com>       
import wx
from wx.lib.buttons import GenBitmapToggleButton
from Breadboard import *

class PartBrowserPanel(wx.Panel):
	"""Display common parts, and a part look up window, if and when we get to that stage"""
	def __init__(self, parent, *args, **kwargs):
		wx.Panel.__init__(self, parent,*args,**kwargs)
		self.bSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.nameToBitmap = {}
		self.commonComponentNameList = {'OpAmp':False,'resistor':True,'capacitor':True,'wire':True} #common components and whether or not they are flexible
		self.gatherCommonComponents()
		self.createButtons()
		self.createComboBox()
		self.SetSizerAndFit(self.bSizer)
		self.Layout()

	def gatherCommonComponents(self):
		for componentName in self.commonComponentNameList.keys():
			print str(componentName)
			self.nameToBitmap[componentName] = wx.Image('res/components/' + str(componentName).lower() + '_display_image.png').Rescale(60,60,wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()

	def createButtons(self):
		self.buttonGroup = ButtonGroup()
		for name in self.commonComponentNameList.keys():
			button1 = GenBitmapToggleButton(self, id=wx.ID_ANY, bitmap=self.nameToBitmap[name],style=wx.BU_EXACTFIT)
			button1.typeName = name
			button1.isVariable = self.commonComponentNameList[name]
			self.buttonGroup.addButton(button1,name)
			self.bSizer.Add(button1,0,wx.ALL,5)
			
	def createComboBox(self):
		sampleList = ['Inductor','Speaker','Difference Amplifier']
		self.combobox = wx.ComboBox(self, -1, "Special Components", (150, 30), wx.DefaultSize,sampleList, wx.CB_SIMPLE|wx.CB_READONLY)
		self.bSizer.Add(self.combobox,wx.ALIGN_RIGHT)
class ButtonGroup(object):
	"""encapsulate radio button features using a manager of a number of bitmaptogglebuttons. This should be built into wxpython, but is not B/C of native operations, I believe"""
	
	def __init__(self):
		""" """
		self.currentName = None
		self.currentButton = None
		self.isVariable = False #is current component variable?
		
	def addButton(self,button,label):
		button.Bind(wx.EVT_BUTTON,self.buttonPressed)
		
	def buttonPressed(self,event):
		if self.currentButton == None: #no button is currently selected, store it locally then return quickly
			self.currentButton = event.GetEventObject()
			self.currentName = self.currentButton.typeName
			self.isVariable = self.currentButton.isVariable
			return #return early, no other logic needed
		sameAsLast = self.currentButton == event.GetEventObject() #if evt is the same as our current button, the same one was pressed, nullify current and set unpressed
		if sameAsLast: #we need to set this deselected
			self.currentButton = None
			self.currentName = None
		else:
			self.currentButton.SetValue(False) #lower our last one...
			self.currentButton = event.GetEventObject()
			self.currentName = self.currentButton.typeName

class Example(wx.Frame):
	"""Dummy frame"""
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent,title=title)
		self.Sizer = wx.BoxSizer(wx.VERTICAL)
		self.Sizer.Add(PartBrowserPanel(self),1,wx.ALL)
		self.Sizer.Add(wx.Button(self,label='hello'),1,wx.ALL)
		self.SetSizer(self.Sizer)
		self.Fit()
		self.Show()


if __name__ == '__main__':
	"""hey, this is how you incorporate testing into a module! @Dan @Noam"""
	app = wx.App()
	Example(None, title='Size')
	app.MainLoop()


