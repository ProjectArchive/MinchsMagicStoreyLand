#! /usr/bin/env python
from Tkinter import *
from Breadboard import *
from PIL import Image,ImageTk
import tkMessageBox

class PartBrowserFrame(Frame):
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
	   
	def createWidgets(self):
		"""Create all the widgets that we need"""
		"""Create the Text"""
		photo = Image.open("res/resistor_image.png")
		photo=ImageTk.PhotoImage(photo.resize((50, 15), Image.ANTIALIAS))
		self.resistorLabel = Label(image=photo)
		self.resistorLabel.image = photo
		self.resistorLabel.pack(side=LEFT)
		photo = Image.open("res/resistor_image.png")
		photo=ImageTk.PhotoImage(photo.resize((50, 15), Image.ANTIALIAS))

		self.capacitorLabel = Label(image=photo)
		self.capacitorLabel.image = photo
		self.capacitorLabel.pack(side=LEFT)
		
if __name__ == "__main__":
	guiFrame = PartBrowserFrame(master=Tk())
	
	guiFrame.mainloop()


