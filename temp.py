from Tkinter import *

class AFrame(Frame):

	def __init__(self,**kwd):
		Frame.__init__(self,**kwd)
		w = Label(self, text="Additive:")
		w.grid(sticky=E)
		w = Label(self, text="Subtractive:")
		w.grid(sticky=E)

		w = Label(self, text="Cyan", bg="cyan", height=2)
		w.grid(row=1, column=1)
		w = Label(self, text="Magenta", bg="magenta", fg="white")
		w.grid(row=1, column=2)
		w = Label(self, text="Yellow", bg="yellow", height=2)
		w.grid(row=1, column=3)

		w = Label(self, text="Red", bg="red", fg="white", height=2)
		w.grid(row=0, column=1)
		w = Label(self, text="Green", bg="green", height=3)
		w.grid(row=0, column=2)
		w = Label(self, text="Blue", bg="blue", fg="white")
		w.grid(row=0, column=3)
		
	def dummy(self):
		print 'hmm'


frame = AFrame(master=Tk(), width=1000, height=100)
frame.grid()

frame.mainloop()
