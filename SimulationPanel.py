#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       Part of Minch's Magic Storey Land 2011
#
#       Copyright 2011 Cory Dolphin <wcdolphin@gmail.com>       
from wx import *
from Breadboard import *

class SimulationPanel(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
 		wx.Panel.__init__(self, parent=parent,*args,**kwargs)
		self.bHorizontalSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.bVerticalSizer = wx.BoxSizer(wx.VERTICAL)
		image = wx.Image('res/simulate_image.png')
		image.Rescale(50,50,wx.IMAGE_QUALITY_HIGH)
		self.startSimulationButton = wx.BitmapButton(self, -1, wx.BitmapFromImage(image))
		self.bHorizontalSizer.Add(self.startSimulationButton,wx.ALIGN_CENTER)
		self.bVerticalSizer.Add(self.bHorizontalSizer)
		self.SetSizer(self.bVerticalSizer)
		
class Example(wx.Frame):
	"""Dummy frame"""
	def __init__(self, parent, title):
		super(Example, self).__init__(parent, title=title,size=(500,500))
		sPanel = SimulationPanel(parent=self,size=(25,25))
		self.Show()

if __name__ == '__main__':
	"""hey, this is how you incorporate testing into a module! @Dan @Noam"""
	app = wx.App()
	Example(None, title='Size')
	app.MainLoop()
