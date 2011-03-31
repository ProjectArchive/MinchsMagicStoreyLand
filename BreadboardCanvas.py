from Tkinter import *
from Breadboard import *
PIN_PIXEL_COUNT = 7
PADDING_PIXEL_COUNT = 1


def drawBreadboard(breadBoard,canvas):
	for yNum in range(breadBoard.numRows):
		for xNum in range(breadBoard.numColumns):
			print(yNum,xNum)
			startX = 1 + ((PIN_PIXEL_COUNT+PADDING_PIXEL_COUNT)*xNum)
			startY = 1 + ((PIN_PIXEL_COUNT+PADDING_PIXEL_COUNT)*yNum)
			color = 'green'
			if breadBoard.getLocation(xNum,yNum).isFilled:
				color = 'red'
			canvas.create_rectangle(startX,startY,startX+PIN_PIXEL_COUNT,startY+PIN_PIXEL_COUNT,fill=color)
	canvas.pack()
		



top = Tk()
myBoard = Breadboard()
C = Canvas(top, bg="white", height=600, width=900)
bitm = BitmapImage("@pinhole.xbm")

#C.create_bitmap(2,2,bitmap=bitm)
drawBreadboard(myBoard,C)
C.pack()
#for i in range(15):
#	C.create_rectangle(1+((3+1)*i), 1,4+((3+1)*i) , 4, fill="blue",outline='white')
top.mainloop()
