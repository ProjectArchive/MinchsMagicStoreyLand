#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       Part of Minch's Magic Storey Land 2011
#
#       Copyright 2011 Cory Dolphin <wcdolphin@gmail.com>       
from Breadboard import *
from BreadboardPanel import *

class BreadboardFrame(wx.Frame):
	"""Dummy frame"""
	def __init__(self, parent, title):
		super(Example, self).__init__(parent, title=title, 
			size=(700, 300))
		BreadboardPanel(self,Breadboard())
		self.Show()


if __name__ == '__main__':
	"""hey, this is how you incorporate testing into a module! @Dan @Noam"""
	app = wx.App()
	Example(None, title="Minch's Magic Storey Land")
	app.MainLoop()
