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
		###make resistor button
		photo = Image.open("res/resistor_image.png")
		photo=ImageTk.PhotoImage(photo.resize((50, 50), Image.ANTIALIAS))
		self.resistorButton = Button(image=photo)
		self.resistorButton.image = photo
		self.resistorButton.grid(row=0,column=0)
		###make capacitor button
		photo = Image.open("res/capacitor_image.png")
		photo=ImageTk.PhotoImage(photo.resize((50, 50), Image.ANTIALIAS))
		self.capacitorButton = Button(image=photo)
		self.capacitorButton.image = photo
		self.capacitorButton.grid(row=0,column=1)
		###make wire button
		photo = Image.open("res/wire_image.png")
		photo=ImageTk.PhotoImage(photo.resize((50, 50), Image.ANTIALIAS))		
		self.wireButton = Button(image=photo)
		self.wireButton.image = photo
		self.wireButton.grid(row=0,column=2)
				
		
if __name__ == "__main__":
	guiFrame = PartBrowserFrame(master=Tk())
	
	guiFrame.mainloop()


