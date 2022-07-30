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

def frange(dcount):
    return int(round(dcount/8, 0))

def is_inside(x, y, matrix, dcount):
    if matrix[y, x] == (0,0,0):
        return True
    f = frange(dcount)
    for xi in range(-f, 1 + f):
        for yi in range(-f, 1 + f):
            xcheck = x
            ycheck = y
            while True:
                if (xi == 0 and yi == 0) or (yi!= 0 and xi/yi == 1 and not (xi == 1 or xi  == -1)):
                    break
                xcheck += xi
                ycheck += yi
                try:
                    a = matrix[ycheck, xcheck] == (0,0,0)
                except IndexError:
                    #print('image edge', (xcheck, ycheck), 'reached on direction:', (xi, yi))
                    return False 
                if matrix[ycheck, xcheck] == (0,0,0):
                    #print('border', (xcheck, ycheck), 'found on direction:', (xi, yi))
                    break
                if xcheck < 0 or ycheck < 0:
                    #print('image edge', (xcheck, ycheck), 'reached on direction:', (xi, yi))
                    return False
    return True

def fillmain():
    cont = True
    while cont:
        while True:
            imgname = input('Image file name: ')
            try:
                img = open(imgname)
                break
            except FileNotFoundError:
                print('File not found (either doesn\'t exist, is not in this folder, or has a different format, try again)')
        while True:
            dcount = input('Check direction count (enter integer that is a multiple of 8): ')
            try:
                dcount = int(dcount)
                break
            except:
                print('Please enter an integer')
        img = open(imgname)
        width = img.size[0]
        height = img.size[1]
        start = time.time()
        count = 0
        res = PIL.Image.new(mode = "RGB", size = (width, height), color = (255,255,255))
        res_pixels = load(res)
        matrix = matrix_create(img)
        for x in range(width):
            for y in range(height):
                #print('Checking:', (x,y))
                if is_inside(x,y, matrix, dcount):
                    res_pixels[x, y] = (0,0,0)
                    #count += 1
                    #print('Filled', count, 'pixels. Last one:', (x,y))
        save(res, imgname + '_Filled_' + str(dcount) + 'D')
        end = time.time()
        print('Created', imgname + '_Filled_' + str(dcount) + 'D.png in ' + str(round(end-start, 2)) + ' seconds.')
        cont = input('Continue? (\'done\' to stop) : ')
        if cont != '' and cont in 'done|stop|no|finished':
            cont = False
        else:
            cont = True
    a = input()

fillmain()
