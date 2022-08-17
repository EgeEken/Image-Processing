from PIL import Image
import PIL
import time
import math
import numpy as np

def save(img, name):
    img.save(name + ".png", "PNG")

def open(imgname):
    return Image.open(imgname)

def load(image):
    return image.load()

def distance(c1,c2):
    r1,g1,b1 = c1
    r2,g2,b2 = c2
    return math.sqrt(((r2-r1)**2+(g2-g1)**2+(b2-b1)**2))
    
def matrix_create(img):
    img_colors = img.convert('RGB')
    img_colorpixels = load(img_colors)
    width = img.size[0]
    height = img.size[1]
    res = np.array(np.zeros((width,height)), dtype=tuple)
    for x in range(width):
        for y in range(height):
            res[y, x] = img_colorpixels[x,y]
    return res
    
def distance3d(c1,c2):
    r1, g1, b1 = c1
    r2, g2, b2 = c2
    return math.sqrt((r2-r1)**2 + (g2-g1)**2 + (b2-b1)**2)

def saturate(c, coef):
    if coef == 0:
        return c
    r, g, b = c
    cmax = max(c)
    cmin = min(c)

    if r == cmax:
        rmin = cmax
    elif r == cmin:
        rmin = 0
    else:
        rmin = 2*r - cmax
    
    if g == cmax:
        gmin = cmax
    elif g == cmin:
        gmin = 0
    else:
        gmin = 2*g - cmax

    if b == cmax:
        bmin = cmax
    elif b == cmin:
        bmin = 0
    else:
        bmin = 2*b - cmax
    
    if coef < 0:
        rchange = (r - cmax) * coef
        gchange = (g - cmax) * coef
        bchange = (b - cmax) * coef
        return (int(r + rchange), int(g + gchange), int(b + bchange))

    rchange = (r - rmin) * coef
    gchange = (g - gmin) * coef
    bchange = (b - bmin) * coef
    return (int(r - rchange), int(g - gchange), int(b - bchange))

def saturationmain():
    a = False
    while not a:
        imgname = input('Image file name: ')
        try:
            img = open(imgname)
            a = True
        except FileNotFoundError:
            print('File not found (either doesn\'t exist, is not in this folder, or has a different format, try again)')
    a = False
    while not a:
        coefdist = input('Coefficient increments: ')
        try:
            coefdist = round(float(coefdist), 4)
            a = True
        except ValueError:
            print('Invalid input, please try again.')
    cont = 'continue'
    coef = -1
    start = time.time()
    matrix = matrix_create(img)
    print('Matrix created in ' + str(round(time.time()-start, 2)) + ' seconds.')
    width = img.size[0]
    height = img.size[1]
    while coef <= 1:
        start = time.time()
        res = PIL.Image.new(mode = "RGB", size = (width, height), color = (255, 255, 255))
        res_pixels = load(res)
        for x in range(width):
            for y in range(height):
                res_pixels[x,y] = saturate(matrix[y,x], coef)
        save(res, imgname[:-4] + '_Saturated_' + str(coef))
        print('Created', imgname[:-4] + '_Saturated_' + str(coef) + '.png in', round(time.time()-start, 2), 'seconds.')
        coef += coefdist
        coef = round(coef, 4)

saturationmain()
a = input()
