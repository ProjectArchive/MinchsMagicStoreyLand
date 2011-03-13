from Breadboard import *
from BreadboardComponent import *

theBreadboard = Breadboard()

print len(theBreadboard.locMatrix.matrix)
print len(theBreadboard.locMatrix.matrix[0])
print theBreadboard.isFilled(0,0)
refLoc= RelativeLocation() #default--> reference relative loc
relLoc = RelativeLocation(2,3,refLoc) #relative to refLoc
print relLoc
