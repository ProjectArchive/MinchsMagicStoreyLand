#! /usr/bin/env python
from Tkinter import *
import tkMessageBox

class BreadboardCanvas(Canvas):
	"""This is the GUI"""
	def __init__(self,master):
		"""Initialize yourself"""
		"""Initialise the base class"""
		Canvas.__init__(self,master,width=200,height=500)
		self.pack()

class BreadboardFrame(Frame):
	"""This is the GUI"""
	def __init__(self,master=None):
		"""Initialize yourself"""
		"""Initialise the base class"""
		Frame.__init__(self,master)
		"""Set the Window Title"""
		self.master.title("Minch's Magic Storey Land!")
		"""Display the main window"
		with a little bit of padding"""
		self.grid(padx=10,pady=10)
		self.createWidgets()
		self.pack()
	   
	def createWidgets(self):
		"""Create all the widgets that we need"""
		"""Create the Text"""
		self.lbText = Label(self, text="Enter Text:")
		self.lbText.grid(row=0, column=0)
		"""Create the Entry, set it to be a bit wider"""
		self.enText = Entry(self)
		self.enText.grid(row=0, column=1, columnspan=3)
		self.bbcanvas=BreadboardCanvas(self)
		"""Create the Button, set the text and the 
		command that will be called when the button is clicked"""
		self.btnDisplay = Button(self, text="Display!", command=self.Display)
		self.btnDisplay.grid(row=0, column=4)
		
	def Display(self):
		"""Called when btnDisplay is clicked, displays the contents of self.enText"""
		tkMessageBox.showinfo("Text", "You typed: %s" % self.enText.get())
		

if __name__ == "__main__":
	guiFrame = BreadboardFrame(Tk())
	guiFrame.master.mainloop()
