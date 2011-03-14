from Breadboard import *
from BreadboardComponent import *
from Location import *

theBreadboard = Breadboard()
abc = BreadboardComponent(2,1,[RelativeLocation(),RelativeLocation(1,0)])

print theBreadboard.putComponent(abc,0,0)
print theBreadboard.isFilled(0,0)
