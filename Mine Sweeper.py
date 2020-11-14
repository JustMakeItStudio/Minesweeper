# Tile renderer. Mine swepper
# If it comes across another 0 and its already displayed then it will not check further, it should
import math
import pygame as pg
import pygame_gui as gui
import numpy as np
import time
from random import randint, getrandbits
from tkinter import *

def alert_popup(title, message, path):
    """Generate a pop-up window for special messages."""
    root = Tk()
    root.title(title)
    w = 400     # popup window width
    h = 200     # popup window height
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = (sw - w)/2
    y = (sh - h)/2
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    m = message
    m += '\n'
    m += path
    w = Label(root, text=m, width=120, height=10)
    w.pack()
    b = Button(root, text="OK", command=root.destroy, width=10)
    b.pack()
    mainloop()

class Tile:
    def __init__(self, xpos, ypos, isBomb, number, state, i, j):
        self.xpos = xpos
        self.ypos = ypos
        self.state = state # 0: Unclicked, 1: Clicked 
        self.isBomb = isBomb # True: it's a bomb, False: it's not a bomb
        self.number = number # An integer of bombs that are around the tile (1 tile away including diagonal)
        self.i = i # An integer showing the node in the x axis
        self.j = j # An integer showing the node in the y axis
    
    def getX(self):
        return self.xpos
    def getY(self):
        return self.ypos
    def getIsBomb(self):
        return self.isBomb  
    def getNumber(self):
        return self.number  
    def getState(self):
        return self.state
    def getValues(self):
        return [self.xpos, self.ypos, self.isBomb, self.number, self.state, self.i, self.j]

    def setX(self, x):
        self.xpos = x
    def setY(self, y):
        self.ypos = y
    def setIsBomb(self, isBomb):
        self.isBomb = isBomb  
    def setNumber(self, number):
        self.number = number
    def setState(self, state):
        self.state = state
    def setValues(self,state):
        self.state = state
      
    def addNumber(self, number):
        self.number += number

class Grid:
    SCREEN_WIDTH = 500 # width (in px)
    SCREEN_HEIGHT = 500 # height (in px)
    TileWidth = 1 # initializing the width of tile (in px)
    TileHeight = 1 # initializing the height of tile (in px)
    tilesMatrix = [] # initializing the matrix of Tile instances
    WHITE=(255,255,255)
    BLUE=(0,0,255)
    BLACK=(0,0,0)
    RED = (255,0,0)

    def __init__(self, ni, nj):
        self.grid = [[0]*ni,[0]*nj] # Number of nodes in x and y direction
        self.ni = ni
        self.nj = nj
        pg.init()
        self.WIN = pg.display.set_mode((Grid.SCREEN_WIDTH, Grid.SCREEN_HEIGHT), pg.RESIZABLE) # creates a screen of 600px X 800px
        pg.display.set_caption('Tile Renderer V02 - Mine Swepper V01')
        self.font = pg.font.Font(None, 25)
        for i in range(self.ni):
            tempLst = []
            for j in range(self.nj):
                tempLst.append(Tile(xpos=i * Grid.TileWidth, ypos=j * Grid.TileHeight, isBomb=np.random.choice([1,0,0,0,0,0,0,0,0,0,0]*10), number=0, state=0, i=i, j=j)) #  getrandbits(1)
            Grid.tilesMatrix.append(tempLst)
        for i in range(round((ni-1)*(nj-1)/10)):
            Grid.tilesMatrix[randint(0,ni-1)][randint(0,nj-1)].setState(1)
        # loop through the tiles to mark the number (of bombs surrounding) of each one
        for i in range(self.ni):
            for j in range(self.nj):
                # Center box
                if 0 < i < self.ni-1 and 0 < j < self.nj-1:
                    if Grid.tilesMatrix[i+1][j].getIsBomb():
                        Grid.tilesMatrix[i][j].addNumber(1)
                    if Grid.tilesMatrix[i-1][j].getIsBomb():
                        Grid.tilesMatrix[i][j].addNumber(1)
                    if Grid.tilesMatrix[i][j+1].getIsBomb():
                        Grid.tilesMatrix[i][j].addNumber(1)
                    if Grid.tilesMatrix[i][j-1].getIsBomb():
                        Grid.tilesMatrix[i][j].addNumber(1)
                    if Grid.tilesMatrix[i+1][j+1].getIsBomb():
                        Grid.tilesMatrix[i][j].addNumber(1)
                    if Grid.tilesMatrix[i-1][j-1].getIsBomb():
                        Grid.tilesMatrix[i][j].addNumber(1)
                    if Grid.tilesMatrix[i-1][j+1].getIsBomb():
                        Grid.tilesMatrix[i][j].addNumber(1)
                    if Grid.tilesMatrix[i+1][j-1].getIsBomb():
                        Grid.tilesMatrix[i][j].addNumber(1)
                # Left vertical line
                if i == 0 and 0 < j < self.nj-1:
                    if Grid.tilesMatrix[i+1][j].getIsBomb():
                        Grid.tilesMatrix[i][j].addNumber(1)
                    if Grid.tilesMatrix[i][j+1].getIsBomb():
                        Grid.tilesMatrix[i][j].addNumber(1)
                    if Grid.tilesMatrix[i][j-1].getIsBomb():
                        Grid.tilesMatrix[i][j].addNumber(1)
                    if Grid.tilesMatrix[i+1][j+1].getIsBomb():
                        Grid.tilesMatrix[i][j].addNumber(1)
                    if Grid.tilesMatrix[i+1][j-1].getIsBomb():
                        Grid.tilesMatrix[i][j].addNumber(1)
                # Top line
                if 0 < i < self.ni-1 and j == 0:
                    if Grid.tilesMatrix[i+1][j].getIsBomb():
                        Grid.tilesMatrix[i][j].addNumber(1)
                    if Grid.tilesMatrix[i-1][j].getIsBomb():
                        Grid.tilesMatrix[i][j].addNumber(1)
                    if Grid.tilesMatrix[i][j+1].getIsBomb():
                        Grid.tilesMatrix[i][j].addNumber(1)
                    if Grid.tilesMatrix[i-1][j+1].getIsBomb():
                        Grid.tilesMatrix[i][j].addNumber(1)
                    if Grid.tilesMatrix[i+1][j+1].getIsBomb():
                        Grid.tilesMatrix[i][j].addNumber(1)
                # Right vertical line
                if i == self.ni-1 and 0 < j < self.nj-1:
                    if Grid.tilesMatrix[i-1][j].getIsBomb():
                        Grid.tilesMatrix[i][j].addNumber(1)
                    if Grid.tilesMatrix[i][j+1].getIsBomb():
                        Grid.tilesMatrix[i][j].addNumber(1)
                    if Grid.tilesMatrix[i][j-1].getIsBomb():
                        Grid.tilesMatrix[i][j].addNumber(1)
                    if Grid.tilesMatrix[i-1][j-1].getIsBomb():
                        Grid.tilesMatrix[i][j].addNumber(1)
                    if Grid.tilesMatrix[i-1][j+1].getIsBomb():
                        Grid.tilesMatrix[i][j].addNumber(1)
                # Bottom line
                if 0 < i < self.ni-1 and j == self.nj-1:
                    if Grid.tilesMatrix[i+1][j].getIsBomb():
                        Grid.tilesMatrix[i][j].addNumber(1)
                    if Grid.tilesMatrix[i-1][j].getIsBomb():
                        Grid.tilesMatrix[i][j].addNumber(1)
                    if Grid.tilesMatrix[i][j-1].getIsBomb():
                        Grid.tilesMatrix[i][j].addNumber(1)
                    if Grid.tilesMatrix[i+1][j-1].getIsBomb():
                        Grid.tilesMatrix[i][j].addNumber(1)
                    if Grid.tilesMatrix[i-1][j-1].getIsBomb():
                        Grid.tilesMatrix[i][j].addNumber(1)
                # Top left corner
                if i == 0 and j == 0:
                    if Grid.tilesMatrix[i+1][j].getIsBomb():
                        Grid.tilesMatrix[i][j].addNumber(1)
                    if Grid.tilesMatrix[i][j+1].getIsBomb():
                        Grid.tilesMatrix[i][j].addNumber(1)
                    if Grid.tilesMatrix[i+1][j+1].getIsBomb():
                        Grid.tilesMatrix[i][j].addNumber(1)
                # Top right corner
                if i == self.ni-1 and j == 0:
                    if Grid.tilesMatrix[i-1][j].getIsBomb():
                        Grid.tilesMatrix[i][j].addNumber(1)
                    if Grid.tilesMatrix[i][j+1].getIsBomb():
                        Grid.tilesMatrix[i][j].addNumber(1)
                    if Grid.tilesMatrix[i-1][j+1].getIsBomb():
                        Grid.tilesMatrix[i][j].addNumber(1)
                # Bottom right corner
                if i == self.ni-1 and j == self.nj-1:
                    if Grid.tilesMatrix[i-1][j].getIsBomb():
                        Grid.tilesMatrix[i][j].addNumber(1)
                    if Grid.tilesMatrix[i][j-1].getIsBomb():
                        Grid.tilesMatrix[i][j].addNumber(1)
                    if Grid.tilesMatrix[i-1][j-1].getIsBomb():
                        Grid.tilesMatrix[i][j].addNumber(1)
                # Bottom left corner
                if i == 0 and j == self.nj-1:
                    if Grid.tilesMatrix[i+1][j].getIsBomb():
                        Grid.tilesMatrix[i][j].addNumber(1)
                    if Grid.tilesMatrix[i][j-1].getIsBomb():
                        Grid.tilesMatrix[i][j].addNumber(1)
                    if Grid.tilesMatrix[i+1][j-1].getIsBomb():
                        Grid.tilesMatrix[i][j].addNumber(1)
        self.GameLoop()

    def initialize(self):    
        self.font = pg.font.Font(None, round(Grid.SCREEN_HEIGHT/10))
        Grid.TileHeight = Grid.SCREEN_HEIGHT / self.nj
        Grid.TileWidth = Grid.SCREEN_WIDTH / self.ni
        for i in range(self.ni):
            tempLst = []
            for j in range(self.nj):
                Grid.tilesMatrix[i][j].setX(i * Grid.TileWidth)
                Grid.tilesMatrix[i][j].setY(j * Grid.TileHeight)
        
    def GameLoop(self):
        running = True
        while (running):
            pg.display.update() # updates the screen
            self.drawGrid()
            ev = pg.event.get() # get all events
            for event in ev:
                if event.type == pg.MOUSEBUTTONUP:
                    pos = pg.mouse.get_pos() # x and y
                    running = self.pressed(pos)
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.VIDEORESIZE:
                    self.WIN = pg.display.set_mode((event.w, event.h), pg.RESIZABLE)
                    Grid.SCREEN_WIDTH = event.w
                    Grid.SCREEN_HEIGHT = event.h
                    self.initialize()
            if running is None: 
                running = True

    def pressed(self, pos):
        for x in range(self.ni):
            for y in range(self.nj):
                if (pos[0] > Grid.tilesMatrix[x][y].getX() and pos[0] < Grid.tilesMatrix[x][y].getX() + Grid.TileWidth):
                    if (pos[1] > Grid.tilesMatrix[x][y].getY() and pos[1] < Grid.tilesMatrix[x][y].getY() + Grid.TileHeight):
                        print(f"Number: {Grid.tilesMatrix[x][y].getNumber()}.")
                        Grid.tilesMatrix[x][y].setState(1)
                        if Grid.tilesMatrix[x][y].getIsBomb():
                            alert_popup("Death box", "You died.", "Continue..")
                            return True
                        else:
                            if Grid.tilesMatrix[x][y].getNumber() == 0:
                                self.checkArround(x, y)
                            return True



    def checkArround(self,i,j):
        # loop through the tiles to revial the tiles that are grouped with the one clicked
        print(f"The i: {i} and the j: {j}")
        # Center box
        if 0 < i < self.ni-1 and 0 < j < self.nj-1:
            if Grid.tilesMatrix[i+1][j].getNumber() == 0 and Grid.tilesMatrix[i+1][j].getState() == 0:
                Grid.tilesMatrix[i+1][j].setState(1)
                self.checkArround(i+1,j)
            if Grid.tilesMatrix[i-1][j].getNumber() == 0 and Grid.tilesMatrix[i-1][j].getState() == 0:
                Grid.tilesMatrix[i-1][j].setState(1)
                self.checkArround(i-1,j)
            if Grid.tilesMatrix[i][j+1].getNumber() == 0 and Grid.tilesMatrix[i][j+1].getState() == 0:
                Grid.tilesMatrix[i][j+1].setState(1)
                self.checkArround(i,j+1)
            if Grid.tilesMatrix[i][j-1].getNumber() == 0 and Grid.tilesMatrix[i][j-1].getState() == 0:
                Grid.tilesMatrix[i][j-1].setState(1)
                self.checkArround(i,j-1)
        # Left vertical line
        if i == 0 and 0 < j < self.nj-1:
            if Grid.tilesMatrix[i+1][j].getNumber() == 0 and Grid.tilesMatrix[i+1][j].getState() == 0:
                Grid.tilesMatrix[i+1][j].setState(1)
                self.checkArround(i+1,j)
            if Grid.tilesMatrix[i][j+1].getNumber() == 0 and Grid.tilesMatrix[i][j+1].getState() == 0:
                Grid.tilesMatrix[i][j+1].setState(1)
                self.checkArround(i,j+1)
            if Grid.tilesMatrix[i][j-1].getNumber() == 0 and Grid.tilesMatrix[i][j-1].getState() == 0:
                Grid.tilesMatrix[i][j-1].setState(1)
                self.checkArround(i,j-1)
        # Top line
        if 0 < i < self.ni-1 and j == 0:
            if Grid.tilesMatrix[i+1][j].getNumber() == 0 and Grid.tilesMatrix[i+1][j].getState() == 0:
                Grid.tilesMatrix[i+1][j].setState(1)
                self.checkArround(i+1,j)
            if Grid.tilesMatrix[i-1][j].getNumber() == 0 and Grid.tilesMatrix[i-1][j].getState() == 0:
                Grid.tilesMatrix[i-1][j].setState(1)
                self.checkArround(i-1,j)
            if Grid.tilesMatrix[i][j+1].getNumber() == 0 and Grid.tilesMatrix[i][j+1].getState() == 0:
                Grid.tilesMatrix[i][j+1].setState(1)
                self.checkArround(i,j+1)
        # Right vertical line
        if i == self.ni-1 and 0 < j < self.nj-1:
            if Grid.tilesMatrix[i-1][j].getNumber() == 0 and Grid.tilesMatrix[i-1][j].getState() == 0:
                Grid.tilesMatrix[i-1][j].setState(1)
                self.checkArround(i-1,j)
            if Grid.tilesMatrix[i][j+1].getNumber() == 0 and Grid.tilesMatrix[i][j+1].getState() == 0:
                Grid.tilesMatrix[i][j+1].setState(1)
                self.checkArround(i,j+1)
            if Grid.tilesMatrix[i][j-1].getNumber() == 0 and Grid.tilesMatrix[i][j-1].getState() == 0:
                Grid.tilesMatrix[i][j-1].setState(1)
                self.checkArround(i,j-1)
        # Bottom line
        if 0 < i < self.ni-1 and j == self.nj-1:
            if Grid.tilesMatrix[i+1][j].getNumber() == 0 and Grid.tilesMatrix[i+1][j].getState() == 0:
                Grid.tilesMatrix[i+1][j].setState(1)
                self.checkArround(i+1,j)
            if Grid.tilesMatrix[i-1][j].getNumber() == 0 and Grid.tilesMatrix[i-1][j].getState() == 0:
                Grid.tilesMatrix[i-1][j].setState(1)
                self.checkArround(i-1,j)
            if Grid.tilesMatrix[i][j-1].getNumber() == 0 and Grid.tilesMatrix[i][j-1].getState() == 0:
                Grid.tilesMatrix[i][j-1].setState(1)
        # Top left corner
        if i == 0 and j == 0:
            if Grid.tilesMatrix[i+1][j].getNumber() == 0 and Grid.tilesMatrix[i+1][j].getState() == 0:
                Grid.tilesMatrix[i+1][j].setState(1)
                self.checkArround(i+1,j)
            if Grid.tilesMatrix[i][j+1].getNumber() == 0 and Grid.tilesMatrix[i][j+1].getState() == 0:
                Grid.tilesMatrix[i][j+1].setState(1)
                self.checkArround(i,j+1)
        # Top right corner
        if i == self.ni-1 and j == 0:
            if Grid.tilesMatrix[i-1][j].getNumber() == 0 and Grid.tilesMatrix[i-1][j].getState() == 0:
                Grid.tilesMatrix[i-1][j].setState(1)
                self.checkArround(i-1,j)
            if Grid.tilesMatrix[i][j+1].getNumber() == 0 and Grid.tilesMatrix[i][j+1].getState() == 0:
                Grid.tilesMatrix[i][j+1].setState(1)
                self.checkArround(i,j+1)
        # Bottom right corner
        if i == self.ni-1 and j == self.nj-1:
            if Grid.tilesMatrix[i-1][j].getNumber() == 0 and Grid.tilesMatrix[i-1][j].getState() == 0:
                Grid.tilesMatrix[i-1][j].setState(1)
                self.checkArround(i-1,j)
            if Grid.tilesMatrix[i][j-1].getNumber() == 0 and Grid.tilesMatrix[i][j-1].getState() == 0:
                Grid.tilesMatrix[i][j-1].setState(1)
                self.checkArround(i,j-1)
        # Bottom left corner
        if i == 0 and j == self.nj-1:
            if Grid.tilesMatrix[i+1][j].getNumber() == 0 and Grid.tilesMatrix[i+1][j].getState() == 0:
                Grid.tilesMatrix[i+1][j].setState(1)
                self.checkArround(i+1,j)
            if Grid.tilesMatrix[i][j-1].getNumber() == 0 and Grid.tilesMatrix[i][j-1].getState() == 0:
                Grid.tilesMatrix[i][j-1].setState(1)
                self.checkArround(i,j-1)


    def drawGrid(self):
        text = None
        for i in range(self.ni):
            for j in range(self.nj):
                pg.draw.rect(self.WIN,Grid.WHITE,(Grid.tilesMatrix[i][j].getX(),Grid.tilesMatrix[i][j].getY(),Grid.TileWidth,Grid.TileHeight))
                if (Grid.tilesMatrix[i][j].getState() == 0):
                    color = Grid.BLACK
                elif (Grid.tilesMatrix[i][j].getState() == 1):
                    if (Grid.tilesMatrix[i][j].getIsBomb() == True):
                        color = Grid.RED
                    else:
                        color = Grid.BLUE
                        text = self.font.render(str(Grid.tilesMatrix[i][j].getNumber()), True, Grid.WHITE)
                        text_rect = text.get_rect(center=(Grid.tilesMatrix[i][j].getX()+Grid.TileWidth/2, Grid.tilesMatrix[i][j].getY()+Grid.TileHeight/2))
                pg.draw.rect(self.WIN,color,(Grid.tilesMatrix[i][j].getX()+1,Grid.tilesMatrix[i][j].getY()+1,Grid.TileWidth-1,Grid.TileHeight-1))
                if text is not None: self.WIN.blit(text, text_rect)
                # draw text


newGrid = Grid(15,15) # ni, nj
