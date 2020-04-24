# File name: GUI.py
# Written by: Nikhita
# Date: April 19, 2020

from graphics import *
from NikhitaButton import *
from Board import *

class GUI:
    def __init__(self):

        # make window
        self.win = GraphWin("Othello",1200,750)
        self.win.setBackground("forestgreen")

        # draw grid
        corner = Point(500,75)
        tileSideLength = 75
        
        for row in range(9):
            p1 = Point(corner.getX(),corner.getY()+(tileSideLength*row))
            p2 = Point(p1.getX()+(tileSideLength*8),p1.getY())
            Line(p1,p2).draw(self.win)
            
            for column in range(9):
                p1 = Point(corner.getX()+(tileSideLength*column),corner.getY())
                p2 = Point(p1.getX(),p1.getY()+(tileSideLength*8))
                Line(p1,p2).draw(self.win)

        # quit  button
        self.quitButton = Button(Point(50,20),70,22,"Quit",self.win)
        self.quitButton.activate("red")

        # pick color
        text = Text(Point(230,325),"Please pick a color.")
        text.setSize(25)
        text.setTextColor("white")
        text.draw(self.win)

        whiteOutline = Rectangle(Point(100,375), Point(200,425))
        whiteOutline.setFill("white")
        whiteOutline.draw(self.win)
        self.whiteButton = Button(Point(150,400),70,25,"White",self.win)
        self.whiteButton.activate("white")

        blackOutline = Rectangle(Point(250,375),Point(350,425))
        blackOutline.setFill("black")
        blackOutline.draw(self.win)
        self.blackButton = Button(Point(300,400),70,25,"Black",self.win)
        self.blackButton.activate("white")

        # make initial pieces
        self.newPiece(1,[3,3],False)
        self.newPiece(1,[4,4],False)
        self.newPiece(-1,[3,4],False)
        self.newPiece(-1,[4,3],False)
        

    def click(self):
        while True:
            
            coord = self.win.getMouse()

            if self.quitButton.clicked(coord):
                self.win.close()
                return "Quit"
            
            elif self.blackButton.clicked(coord):
                return -1
            
            elif self.whiteButton.clicked(coord):
                return 1

            elif 500<coord[0]<1175 and 75<coord[1]<750:
                tile = self.coordToPos(coord)
                return tile
                
            
        
    def startGame(self):

        color = self.click()
        if not color=="Quit":
            # undraw stuff asking which color the player wants to be
            self.blackButton.deactivate()
            self.whiteButton.deactivate()
            cover = Rectangle(Point(100,100),Point(400,600))
            cover.setFill("forestgreen")
            cover.setOutline("forestgreen")
            cover.draw(self.win)
            
            # score
            whiteLabel = Text(Point(100,150),"White:")
            whiteScore = Text(Point(150,150),"0")
            blackLabel = Text(Point(100,200),"Black:")
            blackScore = Text(Point(150,200),"0")
            textLst = [whiteLabel,whiteScore,blackLabel,blackScore]

            for text in textLst:
                text.setSize(25)
                text.setTextColor("white")
                text.draw(self.win)

            self.whiteScore,self.blackScore = textLst[1],textLst[3]

        return color
        
    def updateScore(self,color,score):
        if color==1:
            self.whiteScore.setText(str(score))
        else:
            self.blackScore.setText(str(score))

    #def updateMessage(color,moveInd,validMoveInd):

    def newPiece(self,color,pos,flipInd):
        flipPieceLst = setPiece(pos,color)
        
        coord = self.posToCoord(pos)
        
        piece = Circle(coord,25)
        if color==1:
            piece.setFill("white")
        else:
            piece.setFill("black")
        piece.draw(self.win)

        if flipInd==True:
            for piece in flipPieceLst:
                color = getPiece(piece)
                setPiece(piece,color*-1)
                

    def posToCoord(self,pos):
        y = 75+37.5+75*pos[1]
        x = 500+37.5+75*pos[0]
        coord = Point(x,y)
        return coord

    def coordToPos(self,coord):
        x,y=coord[0],coord[1]
        pos = [0,0]
        pos[0] = (x-500)//75
        pos[1] = (y-75)//75
        return pos
    
        
