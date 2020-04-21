# File: Button.py
# Written by: Nikhita
# Date: September 24, 2019
# creates a button class to make nice buttons
from graphics import *

class Button:
    # accessors
    def getCenter(self):
        return self.center
    def getWidth(self):
      return self.width
    def getHeight(self):
        return self.height
    def getLabel(self):
        return self.label
    def getActiveInd(self):
        return self.activeInd
    
    # methods
    def activate(self,color):
        self.label.setFill('black')
        self.outline.setWidth(2)
        self.outline.setFill(color)
        self.activeInd = True
    def deactivate(self):
        self.label.setFill('darkgrey')
        self.outline.setWidth(1)
        self.outline.setFill('white')
        self.activeInd = False
    def clicked(self,clickPoint):
        wasClicked = False
        if self.yMin <= clickPoint.getY() and self.yMax >= clickPoint.getY():
            if self.xMin <= clickPoint.getX() and self.xMax >= clickPoint.getX():
                if self.activeInd == True:
                    wasClicked = True
        return wasClicked
    # get rid of the button
    def undraw(self):
        self.outline.undraw()
        self.label.undraw()
        self.buttonRectangle.undraw()
        
        
        
        
    # constructor
    def __init__(self,center,width,height,label,win):
        # find x mins and maxs and y mins and maxs for points outlining rectangle
        self.xMin = center.getX() - width/2
        self.xMax = center.getX() + width/2
        self.yMin = center.getY() - height/2
        self.yMax = center.getY() + height/2

        # two corners of the rectangle
        pt1 = Point(self.xMin, self.yMin)
        pt2 = Point(self.xMax, self.yMax)

        # draw the rectangle
        self.buttonRectangle = Rectangle(pt1,pt2)
        self.buttonRectangle.draw(win)
        self.outline = Rectangle(pt1,pt2)
        self.outline.draw(win)
        

        # draw button label
        self.label = Text(center,label)
        self.label.setSize(18)
        self.label.draw(win)

        # start with button deactivated
        self.deactivate()

        
    
