from PIL import Image
from PIL import ImageColor
import numpy as np
import math

def createFractal():
    xRange = 15
    yRange = 100
    XPixels = 1000
    YPixels = 666
    fract = Image.new('RGBA', (XPixels, YPixels))
    Picture_Width, Picture_Height = fract.size
    Pixels_Per_Xunit = Picture_Width/(2*xRange)
    Pixels_Per_Yunit = Picture_Height/(2*yRange)
    aStart = a = bStart = b = 0
    memory = []
    zMemory = []
    color = (0,0,0)
    distance = -1
    
    for x in range(Picture_Width):
        for y in range(Picture_Height):
            aStart = a = 1.0 * x/(Pixels_Per_Xunit) - xRange
            bStart = b = -1.0*y/(Pixels_Per_Yunit) + yRange
            count = 0
            memory = []
            zMemory = []
            color = (0, 0, 0)
            distance = -1
            
            while(count < 25 and (distance < 500) and not((a,b) in memory)):
                #print(aStart, bStart, a , b , distance)
                memory.append((a,b))
                distance = findMagnitude(a,b)
                zMemory.append(distance)
                a, b = FractalFunction(a, b, aStart, bStart)
                count+=1

            if (a,b) in memory:
                color = (255, 0, 255)
            elif distance >= 200:
                rate = (zMemory[-1]/zMemory[-2])/200
                if(rate > 1):
                    rate = 1
                color = (int(255), int(255 * rate), int(255))
            else:
                color = (0,0,0)
            fract.putpixel((x, y), color)
    fract.save("Fractal.png")
    fract.show()

def FractalFunction(x, y, zx_0, zy_0):
    """
    Inputs are of the form x+yi
    outputs tuple in form a+bi
    """
    a, b = cos(x,y)
    return a + zx_0, b + zy_0

def findMagnitude(x, y):
    return np.sqrt(1.0 * (x**2 + y**2))

def exp(x, y):
    #e^(x+yi)
    return np.exp(x)*np.cos(y), np.exp(x)*np.sin(y)

def cos(x, y):
    a,b = exp(x,y)
    c,d = exp(-x,-y)
    a = a+c
    b = b+d
    return a/2, b/2

def multiply(x, y, a, b):
    """
    Defined Multiplication for imaginary numbers:
    x+yi, a+bi are the defined parameters.
    """
    return a*x-b*y, x*b+a*y

def addition(x, y, a, b):
    return x+a, y+b
    
createFractal()
    
