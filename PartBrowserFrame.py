#! /usr/bin/env python
from Tkinter import *
from Breadboard import *
from PIL import Image,ImageTk
import tkMessageBox

class PartBrowserFrame(Frame):
	PIN_PIXEL_COUNT=8
	PADDING_PIXEL_COUNT = 1
	"""This is the GUI"""
	def __init__(self,master=None):
		"""Initialize yourself"""
		"""Initialise the base class"""
		Frame.__init__(self,master)
		self.master = master
		"""Display the main window"
		with a little bit of padding"""
		self.grid(padx=10,pady=10)
		self.createWidgets()
		self.pack(fill=BOTH, expand=YES)
	   
	def createWidgets(self):
		"""Create all the widgets that we need"""
		"""Create the Text"""
		photo = ImageTk.PhotoImage(Image.open("lenna.jpg"))
		
if __name__ == "__main__":
	guiFrame = PartBrowserFrame(master=Tk())
	
	guiFrame.mainloop()


