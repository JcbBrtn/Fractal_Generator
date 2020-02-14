from PIL import Image
from PIL import ImageColor
import numpy as np

def createFractal():
    xRange = 2
    yRange = 2
    XPixels = 1000
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
    bailout = 2
    maxcount = 100
    
    for x in range(Picture_Width):
        for y in range(Picture_Height):
            aStart = a = 1.0 * x/(Pixels_Per_Xunit) - xRange
            bStart = b = -1.0*y/(Pixels_Per_Yunit) + yRange
            count = 0
            memory = []
            zMemory = []
            color = (0, 0, 0)
            distance = -1
            
            while(count < maxcount and (distance < bailout) and not((a,b) in memory)):
                #print(aStart, bStart, a , b , distance)
                memory.append((a,b))
                distance = findMagnitude(a,b)
                zMemory.append(distance)
                a, b = FractalFunction(a, b, aStart, bStart)
                count+=1

            if (a,b) in memory:
                color = (0, 0, 0)
            elif distance >= 2:
                rateColor = int(255 - (maxcount /(count + 1)))
                color = (rateColor, rateColor, rateColor)
            elif (count >= maxcount):
                color = (0,0,0)
            else:
                print('else')
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
    a, b = multiply(x,y,x,y)
    #return a + c, b + d
    return a + zx, b+zy

def exp(x, y):
    #e^(x+yi)
    return np.exp(x)*np.cos(y), np.exp(x)*np.sin(y)

def cos(x, y):
    a,b = exp(x,y)
    c,d = exp(-x,-y)
    a = a+c
    b = b+d
    return a/2, b/2

def fakeDiv(x, y, c):
    """
    input: x+yi and some constant c.
    Output: (x+yi)/(ci)
    """
    a = -1* y / c
    b = c/x
    return a,b

def fakeSin(x, y):
    """
    Not the real sin function for complex numbers.
    However, it still produced a notable result and thus should be looked into further.
    """
    a,b = exp(x,y)
    c,d = exp(-x,-y)
    a = a-c
    b = b-d
    a, b = fakeDiv(a, b, 2)
    return a, b

def findMagnitude(x, y):
    return np.sqrt(1.0 * (x**2 + y**2))

def division(x,y,a,b):
    """
    defined as x+yi / a + bi
    """
    real = (a*x + b*y)/(a*a + b*b)
    img = (a*y - b*x)/(a*a + b*b)
    return real, img

def multiply(x, y, a, b):
    """
    Defined Multiplication for imaginary numbers:
    x+yi, a+bi are the defined parameters.
    """
    return a*x-b*y, x*b+a*y

def addition(x, y, a, b):
    return x+a, y+b
    
createFractal()
    
