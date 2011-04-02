from Tkinter import *
from Breadboard import *

PIN_PIXEL_COUNT = 7
PADDING_PIXEL_COUNT = 1

def drawBreadboard(breadBoard,canvas):
	for yNum in range(breadBoard.numRows):
		for xNum in range(breadBoard.numColumns):
			#print(yNum,xNum, breadBoard.getLocation(xNum,yNum).isFilled)
			startX = 1 + ((PIN_PIXEL_COUNT+PADDING_PIXEL_COUNT)*xNum)
			startY = 1 + ((PIN_PIXEL_COUNT+PADDING_PIXEL_COUNT)*yNum)
			color = 'green'
			if breadBoard.getLocation(xNum,yNum).isFilled:
				color = 'red'
			canvas.create_rectangle(startX,startY,startX+PIN_PIXEL_COUNT,startY+PIN_PIXEL_COUNT,fill=color)
	canvas.pack(fill=BOTH, expand=YES)

def funFunFunction():
	print 'ohh hai'

breadBoard = Breadboard()

top = Tk()
f = Frame(top,width=100,height=300)
f.pack(fill=BOTH, expand=YES)
cv = Canvas(f, width=800, height=200, bg='white')
#cv.pack(fill=BOTH, expand=YES)
drawBreadboard(breadBoard,cv)
b1 = Button( f, text='Hello', height=1, width=10, padx=0, pady=1,command=funFunFunction)
b1.pack(side=BOTTOM, anchor=E, padx=4, pady=4)

top.mainloop()


