#! /usr/bin/env python
from Tkinter import *
from Breadboard import *
from BreadboardComponent import *
from BreadboardFrame import *
from PartBrowserFrame import *
import tkMessageBox

class MainFrame(Frame):
	"""This is the GUI"""
	def __init__(self,breadBoard,master=None):
		"""Initialize yourself"""
		"""Initialise the base class"""
		Frame.__init__(self,master)
		self.master = master
		self.master.title("Minch's Magic Storey Land!")

		self.breadBoard = breadBoard
		self.grid(padx=10,pady=10)
		self.createWidgets()
		self.pack(fill=BOTH, expand=YES)
	def placeAnOpAmp(self):
		self.breadBoard.putComponent(Resistor(100),1,1,2,2)
		print 'placed an op amp'
		self.breadBoardFrame.redraw()
		
	def createWidgets(self):
		"""Create all the widgets that we need"""
		"""Create the Text"""
		self.breadBoardFrame = BreadboardFrame(self.breadBoard,master=self)
		self.breadBoardFrame.pack(side = LEFT)
		self.partBrowserFrame = PartBrowserFrame(master=self)
		self.partBrowserFrame.pack(side = BOTTOM)
		self.createMenu()
	
	def createMenu(self):
		self.menu = Menu(self)
		self.master.config(menu=self.menu)

		self.filemenu = Menu(self.menu)
		self.menu.add_cascade(label="File", menu=self.filemenu)
		self.filemenu.add_command(label="New", command=self.callback)
		self.filemenu.add_command(label="Open...", command=self.callback)
		self.filemenu.add_separator()
		self.filemenu.add_command(label="Exit", command=self.callback)
		self.helpmenu = Menu(self.menu)
		self.menu.add_cascade(label="Help", menu=self.helpmenu)
		self.helpmenu.add_command(label="About...", command=self.callback)
		
	def callback():
		print 'callback'


if __name__ == "__main__":
	guiFrame = MainFrame(Breadboard(),Tk())	
	guiFrame.mainloop()
