#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       Part of Minch's Magic Storey Land 2011
#
#       Copyright 2011 Cory Dolphin <wcdolphin@gmail.com>       
import wx
from Breadboard import *
from PIL import Image

class PartBrowserPanel(wx.Panel):
	def __init__(self, parent, *args, **kwargs):
		wx.Panel.__init__(self, parent,*args,**kwargs)
		self.SetBackgroundColour((11, 11, 11))
#		imageFile = "res/resistor_image.png"
#		image1 = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).Rescale(70,70,wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
		self.bSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.nameToBitmap = {}
		self.gatherCommonComponents()
		self.createButtons()
		#button1 = wx.BitmapButton(self, id=-1, bitmap=self.nameToBitmap['resistor'])
		#self.bSizer.Add(button1)
		#button2 = wx.BitmapButton(self, id=-1, bitmap=self.nameToBitmap['capacitor'])
		#self.bSizer.Add(button2)
		self.SetSizerAndFit(self.bSizer)
		
	def gatherCommonComponents(self):
		#generate this common componentnamelistsomewhere...
		self.commonComponentNameList = ['resistor','capacitor','wire']
		for componentName in self.commonComponentNameList:
			print str(componentName)
			self.nameToBitmap[componentName] = wx.Image('res/' + str(componentName) + '_image.png').Rescale(70,70,wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()

	def createButtons(self):
		self.buttonGroup = ButtonGroup(self)
		for name in self.nameToBitmap.keys():
			print name
			button1 = wx.BitmapButton(self, id=-1, bitmap=self.nameToBitmap[name])
			button1.typeName = name
			self.buttonGroup.addButton(button1,name)
			self.bSizer.Add(button1,0,wx.ALL,5)
			
	def onMotion(self,event):
		"""A generic onMotion event, TODO:look at hierachy, which event is invoked first?		"""
		x,y= self.bitmapToXY.get(event.GetEventObject())
		print event.GetEventObject().GetSize()
		print self.breadBoard.getLocation(x,y)
		#print "motion event:", event.m_x, event.m_y



class ButtonGroup(object):
	
	def __init__(self,parent):
		self.parent = parent
		self.currentName = None
		self.currentButton = None
	
	def addButton(self,button,label):
		button.Bind(wx.EVT_BUTTON,self.buttonPressed)
	
	def buttonPressed(self,event):
		if self.currentButton == event.GetEventObject():
			self.currentButton.set

class Example(wx.Frame):
	"""Dummy frame"""
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent,title=title)
		PartBrowserPanel(self)
		self.Fit()
		self.Show()


if __name__ == '__main__':
	"""hey, this is how you incorporate testing into a module! @Dan @Noam"""
	app = wx.App()
	Example(None, title='Size')
	app.MainLoop()


