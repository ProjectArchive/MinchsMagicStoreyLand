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
	def __init__(self, parent, *args, **kwargs):
		wx.Panel.__init__(self, parent,*args,**kwargs)
		self.bSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.nameToBitmap = {}
		self.gatherCommonComponents()
		self.createButtons()
		self.SetSizerAndFit(self.bSizer)
		self.Layout()
		
	def gatherCommonComponents(self):
		#generate this common componentnamelistsomewhere...
		self.commonComponentNameList = ['OpAmp','resistor','capacitor','wire']
		for componentName in self.commonComponentNameList:
			print str(componentName)
			self.nameToBitmap[componentName] = wx.Image('res/components/' + str(componentName) + '_image.png').Rescale(60,60,wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()

	def createButtons(self):
		self.buttonGroup = ButtonGroup()
		flag = True
		for name in self.nameToBitmap.keys():
			print name
			button1 = GenBitmapToggleButton(self, id=wx.ID_ANY, bitmap=self.nameToBitmap[name],style=wx.BU_EXACTFIT)
			button1.typeName = name
			self.buttonGroup.addButton(button1,name)
			self.bSizer.Add(button1,0,wx.ALL,5)


class ButtonGroup(object):
	"""encapsulate radio button features using a manager of a number of bitmaptogglebuttons. This should be built into wxpython, but is not B/C of native operations, I believe"""
	
	def __init__(self):
		""" """
		self.currentName = None
		self.currentButton = None
	
	def addButton(self,button,label):
		button.Bind(wx.EVT_BUTTON,self.buttonPressed)
		
	def buttonPressed(self,event):
		if self.currentButton == None:
			self.currentButton = event.GetEventObject()
			self.currentName = self.currentButton.typeName
			return
		sameAsLast = self.currentButton == event.GetEventObject()
		if sameAsLast:
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


