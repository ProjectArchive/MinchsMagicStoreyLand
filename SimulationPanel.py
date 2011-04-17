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
 		wx.Panel.__init__(self, parent,*args,**kwargs)
 		self.parent = parent
 		
 		
		self.bVerticalSizer = wx.BoxSizer(wx.VERTICAL)
		
		image = wx.Image('res/simulate_image.png')
		image.Rescale(50,50,wx.IMAGE_QUALITY_HIGH)
		self.startSimulationButton = wx.BitmapButton(self, -1, wx.BitmapFromImage(image))
		self.sstartSimulationButton = wx.BitmapButton(self, -1, wx.BitmapFromImage(image))

		self.bVerticalSizer.Add(self.startSimulationButton,0, wx.ALL|wx.ALIGN_CENTER, 5)
		self.bVerticalSizer.Add(self.sstartSimulationButton,0, wx.ALL|wx.ALIGN_CENTER, 5)
		self.SetSizerAndFit(self.bVerticalSizer)
		
class Example(wx.Frame):
	"""Dummy frame"""
	def __init__(self, parent, title):
		wx.Frame.__init__(self,parent, title=title)
		sPanel = SimulationPanel(parent=self)
		self.Fit()
		self.Show()

if __name__ == '__main__':
	"""hey, this is how you incorporate testing into a module! @Dan @Noam"""
	app = wx.App()
	Example(None, title='Size')
	app.MainLoop()
