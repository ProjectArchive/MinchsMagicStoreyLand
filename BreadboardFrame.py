#! /usr/bin/env python
from Tkinter import *
from Breadboard import *
import tkMessageBox

class BreadboardFrame(Frame):
	"""This is the GUI"""
	def __init__(self,breadBoard,master=None):
		"""Initialize yourself"""
		"""Initialise the base class"""
		Frame.__init__(self,master)
		self.master.title("Minch's Magic Storey Land!")
		self.breadBoard = breadBoard
		"""Display the main window"
		with a little bit of padding"""
		self.grid(padx=10,pady=10)
		self.createWidgets()
		self.pack()
	   
	def createWidgets(self):
		"""Create all the widgets that we need"""
		"""Create the Text"""
		self.breadBoardCanvas = BreadboardCanvas(self.breadBoard,master=self)
		
	def Display(self):
		"""Called when btnDisplay is clicked, displays the contents of self.enText"""
		tkMessageBox.showinfo("Text", "You typed: %s" % self.enText.get())

class BreadboardCanvas(object):
	def __init__(self,breadBoard,master=None,width=600,height=200):
		self.breadBoard = breadBoard
		self.canvas = Canvas(master=master,width=width,height=height)
		self.canvas.pack()
	

if __name__ == "__main__":
	guiFrame = BreadboardFrame(Tk(),Breadboard())
	
	guiFrame.mainloop()
