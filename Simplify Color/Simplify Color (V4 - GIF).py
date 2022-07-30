from PIL import Image
import PIL
import time
import math
import numpy as np
import random
import imageio

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

def colorset_create(matrix_img):
    res = set()
    for i in matrix_img:
        for j in i:
            if j not in res:
                res.add(j)
    return res
    
def colorlist_pop(colorset, precision):
    return random.sample(list(colorset), int(precision))

def closestcolor(c, colorset):
    if c in colorset:
        return c
    mindist = 500
    for color in colorset:
        dist = distance(c, color)
        if dist < mindist:
            mindist = dist
            mincolor = color
    return mincolor

def colorsimplify(img, matrix, colorset, precision, count):
    width = img.size[0]
    height = img.size[1]
    start = time.time()
    if precision < 1.0 and precision > 0:
        colorlist = colorlist_pop(colorset, len(colorset)*precision)
    else:
        colorlist = colorlist_pop(colorset, precision)
    res = PIL.Image.new(mode = "RGB", size = (width, height), color = (255, 255, 255))
    res_pixels = load(res)
    for x in range(width):
        for y in range(height):
            res_pixels[x,y] = closestcolor(matrix[y,x], colorlist)
    save(res, imgname[:-4] + '_Simplified_' + str(precision) + '_' + str(count))
    end = time.time()
    print('Created ' + imgname[:-4] + '_Simplified_' + str(precision) + '_' + str(count) + '.png in ' + str(round(end-start, 2)) + ' seconds.')

a = False
while not a:
    imgname = input('Image file name: ')
    try:
        img = open(imgname)
        a = True
    except:
        print('File not found (either doesn\'t exist, is not in this folder, or has a different format, try again)')
matrix = matrix_create(img)
colorset = colorset_create(matrix)
print('There are', len(colorset), 'different colors of pixels in this image.')
precision = float(input('Precision (Enter either a fraction between 0 and 1, or a number of total colors left to use): '))
amount = int(input('Image count: '))
FPS = int(input('FPS count: '))
for count in range(amount):
    colorsimplify(img, matrix, colorset, precision, count)


filename = imgname[:-4] + '_Simplified_' + str(precision) + '_'
                 
filenames = [filename + str(i) + '.png' for i in range(count)]

with imageio.get_writer(filename + 'GIF.gif', mode='I', duration=round(1/FPS, 2)) as writer:
    for filename in filenames:
        image = imageio.imread(filename)
        writer.append_data(image)
