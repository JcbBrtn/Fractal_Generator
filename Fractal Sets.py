from PIL import Image
from PIL import ImageColor
import numpy as np

def createFractal():
    xRange = 4
    yRange = 8
    XPixels = 500
    YPixels = 1000
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
            
            while(count < 100 and (distance < 200) and not((a,b) in memory)):
                #print(aStart, bStart, a , b , distance)
                memory.append((a,b))
                distance = findMagnitude(a,b)
                zMemory.append(distance)
                a, b = FractalFunction(a, b, aStart, bStart)
                count+=1

            if (a,b) in memory:
                color = (0, 127, 255)
            elif distance >= 200:
                rate = (zMemory[-1]/zMemory[-2])/400
                if(rate > 1):
                    rate = 1
                if 285 - (255*rate) > 255:
                    blue = 255
                else:
                    blue = 285 - (255*rate)
                color = (int(blue), int((255 - 255 * rate)), int(0))
            else:
                color = (255,255,255)
            fract.putpixel((x, y), color)
    fract.save("sin c=-0.09+0i.png")
    fract.show()

def FractalFunction(x, y, zx, zy):
    """
    Inputs are of the form x+yi
    zx, zy are first(base) values
    i is the iteration number
    outputs tuple in form a+bi
    """
    a, b = sin(x,y)
    #return a + c, b + d
    v, w = multiply(a, b, -.09, 0)
    return v, w

def exp(x, y):
    #e^(x+yi)
    return np.exp(x)*np.cos(y), np.exp(x)*np.sin(y)

def cos(x, y):
    a,b = exp(x,y)
    c,d = exp(-x,-y)
    a = a+c
    b = b+d
    return a/2, b/2

def division(x, y, c):
    """
    input: x+yi and some constant c.
    Output: (x+yi)/(ci)
    """
    a = -1* y / c
    b = c/x
    return a,b

def sin(x, y):
    a,b = exp(x,y)
    c,d = exp(-x,-y)
    a = a-c
    b = b-d
    a, b = division(a, b, 2)
    return a, b

def findMagnitude(x, y):
    return np.sqrt(1.0 * (x**2 + y**2))

def multiply(x, y, a, b):
    """
    Defined Multiplication for imaginary numbers:
    x+yi, a+bi are the defined parameters.
    """
    return a*x-b*y, x*b+a*y

def addition(x, y, a, b):
    return x+a, y+b
    
createFractal()
    
