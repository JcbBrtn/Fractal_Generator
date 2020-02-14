import random
import numpy as np
import tkinter as tk

class Fractal:
    def __init__(self, pixWid, pixHeight, xRan):
        self.pixelWidth = pixWid
        self.pixelHeight = pixHeight
        self.ratio = 1.0 * self.pixelHeight/ self.pixelWidth
        self.xRange = xRan
        self.yRange = self.xRange * self.ratio
        self.centerX = 0
        self.centerY = 0
        self.maxCount = 50
        self.Pixels_Per_Xunit = 0
        self.Pixels_Per_Yunit = 0
        self.calcPixPerUnit()
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=self.pixelWidth, height=self.pixelHeight, bg="#ffffff")
        self.canvas.pack()
        self.fract = tk.PhotoImage(width=self.pixelWidth, height=self.pixelHeight)
        self.canvas.create_image((self.pixelWidth//2, self.pixelHeight//2), image=self.fract, state="normal")
        self.root.bind('<Button 1>', self.zoomIn)
        self.root.bind('<Button 3>', self.zoomIn)
        self.maxDistance = self.findMagnitude(self.xRange, self.yRange)

        self.draw()

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
        self.centerX = event.x
        self.centerY = event.y
        self.xRange = self.xRange/2
        self.yRange = self.xRange * self.ratio
        self.calcPixPerUnit()
        self.maxDistance = self.findMagnitude(self.xRange, self.yRange)
        print('Zooming in on ' + str(event.x) + ',' + str(event.y)) 
        self.draw()

    def function(self, a, b, a0, b0):
        x,y = self.fakeSin(a,b)
        return x, y

    def iterate(self, a, b):
        count = 0
        a0 = a
        b0 = b
        distance = -1

        while(count < self.maxCount and distance < self.maxDistance):
            distance = self.findMagnitude(a,b)
            a, b = self.function(a, b, a0, b0)
            count+=1

        if count >= self.maxCount:
            return '#000000'
        elif distance>= self.maxDistance:
            return '#aa3377'
        else:
            return '#333333'

    def draw(self):
        for x in range(self.pixelWidth):
            for y in range(self.pixelHeight):
                #map to a pixel in the graph space
                a = 1.0 * x/(self.Pixels_Per_Xunit) - self.xRange + self.centerX
                b = -1.0*y/(self.Pixels_Per_Yunit) + self.yRange + self.centerY

                self.fract.put(self.iterate(a,b), (x,y))


myFrac = Fractal(1000,2000, 6)
tk.mainloop()

