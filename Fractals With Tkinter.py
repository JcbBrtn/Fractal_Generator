import random
import numpy as np
import tkinter as tk

class Fractal:
    def __init__(self, pixWid, pixHeight, totalX, xRan):
        self.pixelWidth = pixWid
        self.pixelHeight = pixHeight
        self.ratio = 1.0 * self.pixelHeight/ self.pixelWidth
        self.blownUpX = totalX
        self.blownUpY = totalX * self.ratio
        self.xRange = xRan
        self.yRange = self.xRange * self.ratio
        self.centerX = 0
        self.centerY = 0
        self.maxCount = 50
        self.Pixels_Per_Xunit = 0
        self.Pixels_Per_Yunit = 0
        self.calcPixPerUnit()
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=self.blownUpX, height=self.blownUpY, bg="#FFFFFF")
        self.canvas.pack()
        #self.fract = tk.PhotoImage(width=self.pixelWidth, height=self.pixelHeight)
        #self.canvas.create_image((self.pixelWidth//2, self.pixelHeight//2), image=self.fract, state="normal")
        self.root.bind('<Button 1>', self.zoomIn)
        self.root.bind('<Button 3>', self.heightenRes)
        self.maxDistance = self.findMagnitude(self.xRange, self.yRange)

        self.setUp()

    def calcPixPerUnit(self):
        self.Pixels_Per_Xunit = self.pixelWidth/(2*self.xRange)
        self.Pixels_Per_Yunit = self.pixelHeight/(2*self.yRange)

    def division(self, x,y,a,b):
        """
        defined as x+yi / a + bi
        """
        real = (a*x + b*y)/(a*a + b*b)
        img = (a*y - b*x)/(a*a + b*b)
        return real, img

    def multiply(self, x, y, a, b):
        """
        Defined Multiplication for imaginary numbers:
        x+yi, a+bi are the defined parameters.
        """
        return a*x-b*y, x*b+a*y

    def addition(self, x, y, a, b):
        return x+a, y+b

    def fakeDiv(self, x, y, c):
        """
        input: x+yi and some constant c.
        Output: (x+yi)/(ci)
        """
        a = -1* y / c
        b = c/x
        return a,b

    def fakeSin(self, x, y):
        """
        Not the real sin function for complex numbers.
        However, it still produced a notable result and thus should be looked into further.
        """
        a,b = self.exp(x,y)
        c,d = self.exp(-x,-y)
        a = a-c
        b = b-d
        a, b = self.fakeDiv(a, b, 2)
        return a, b

    def exp(self, x, y):
        #e^(x+yi)
        return np.exp(x)*np.cos(y), np.exp(x)*np.sin(y)
                      
    def findMagnitude(self, x, y):
        return np.sqrt(1.0 * (x**2 + y**2))

    def zoomIn(self, event):
        x = self.pixelWidth*(event.x / self.blownUpX)
        y = self.pixelHeight*(event.y / self.blownUpY)
        self.centerX = 1.0 * self.xRange/self.pixelWidth * x + (self.centerX - self.xRange/2)
        self.centerY = 1.0 * self.yRange/self.pixelHeight * y + (self.centerY - self.yRange/2)
        self.xRange = self.xRange/2
        self.yRange = self.xRange * self.ratio
        self.calcPixPerUnit()
        print('The Range over x: ' + str(self.xRange))
        print('Zooming in on new CenterX: ' + str(self.centerX) + ', and CenterY: ' + str(self.centerY))
        self.setUp()

    def heightenRes(self, event):
        self.pixelWidth = int(self.blownUpX/((self.blownUpX / self.pixelWidth)/2))
        self.pixelHeight = int(self.blownUpY/((self.blownUpY / self.pixelHeight)/2))
        self.calcPixPerUnit()
        print('Clearing up Resolution by 50%')
        print('The Pixel sizes are still: ' + str((self.blownUpX / self.pixelWidth)) + ', ' + str((self.blownUpY / self.pixelHeight)))
        
        self.setUp()

    def function(self, a, b, a0, b0):
        x,y = self.multiply(a, b, a, b)
        #x,y = self.exp(a,b)
        return x -0.7269, y + 0.1889
        #return x+a0, y+b0
        #return x, y

    def iterate(self, a, b):
        count = 0
        a0 = a
        b0 = b
        distance = -1

        while(count < self.maxCount and distance < self.maxDistance):
            distance = self.findMagnitude(a,b)
            a, b = self.function(a, b, a0, b0)
            count+=1
            
        rd = hex(count % 4 * 64)[2:].zfill(2)
        gr = hex(count % 16 * 16)[2:].zfill(2)
        bl = hex(count % 4 * 64)[2:].zfill(2)
        return '#' + rd + gr + bl
        

    def setUp(self):
        pic = []
        for x in range(self.pixelWidth):
            picRow = []
            for y in range(self.pixelHeight):
                #map to a pixel in the graph space
                a = 1.0 * self.xRange/self.pixelWidth * x + (self.centerX - self.xRange/2)
                b = 1.0 * self.yRange/self.pixelHeight * y + (self.centerY - self.yRange/2)

                picRow.append(self.iterate(a,b))
            pic.append(picRow)
        self.draw(pic)

    def draw(self, picArr):
        pixelsPerBoxX = int(self.blownUpX / self.pixelWidth)
        pixelsPerBoxY = int(self.blownUpY / self.pixelHeight)
        for x in range(self.pixelWidth):
            for y in range(self.pixelHeight):
                self.canvas.create_rectangle(x * pixelsPerBoxX, y * pixelsPerBoxY, (x + 1) * pixelsPerBoxX,
                                             (y+1) * pixelsPerBoxY, fill=picArr[x][y] ,outline=picArr[x][y])
        print('###Your Fractal is good to go!###')


myFrac = Fractal(50,50,850, 6)
tk.mainloop()

