#! /usr/bin/env python
from Tkinter import *
from Breadboard import *
from BreadboardComponent import *
from BreadboardFrame import *
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
		self.b = Button(self, text="Place op amp", command=self.placeAnOpAmp)
		self.b.pack()
		
if __name__ == "__main__":
	guiFrame = MainFrame(Breadboard(),Tk())	
	guiFrame.mainloop()
