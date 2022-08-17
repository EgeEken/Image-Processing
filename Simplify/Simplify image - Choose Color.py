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
    width = img.size[0]
    height = img.size[1]
    res = np.zeros(height,width)
    for x in range(width):
        for y in range(height):
            res[y, x] = img_colors[x,y]
    return res

def scan_direction(dirlist, x, y, matrix):
    res = []
    for i in dirlist:
        if i == 1:
            res.append(matrix[y-1, x-1])
        elif i == 2:
            res.append(matrix[y-1, x])
        elif i == 3:
            res.append(matrix[y-1, x+1])
        elif i == 4:
            res.append(matrix[y, x-1])
        elif i == 6:
            res.append(matrix[y, x+1])
        elif i == 7:
            res.append(matrix[y+1, x-1])
        elif i == 8:
            res.append(matrix[y+1, x])
        elif i == 9:
            res.append(matrix[y+1, x+1])
    return res

def around(matrix,x,y):
    neighbors = []
    if x != 0 and x != (len(matrix[0]) - 1):
        if y != 0 and y != (len(matrix) - 1):
            neighbors = scan_direction([1,2,3,4,6,7,8,9], x,y, matrix)
        elif y == 0:
            neighbors = scan_direction([4,6,7,8,9], x,y, matrix)
        elif y == (len(matrix) - 1):
            neighbors = scan_direction([1,2,3,4,6], x,y, matrix)
    elif x == 0:
        if y != 0 and y != (len(matrix) - 1):
            neighbors = scan_direction([2,3,6,8,9], x,y, matrix)
        elif y == 0:
            neighbors = scan_direction([6,8,9], x,y, matrix)
        elif y == (len(matrix) - 1):
            neighbors = scan_direction([2,3,6], x,y, matrix)
    elif x == (len(matrix[0]) - 1):
        if y != 0 and y != (len(matrix) - 1):
            neighbors = scan_direction([1,2,4,7,8], x,y, matrix)
        elif y == 0:
            neighbors = scan_direction([4,7,8], x,y, matrix)
        elif y == (len(matrix) - 1):
            neighbors = scan_direction([1,2,4], x,y, matrix)
    return neighbors

def check_contrast(matrix, x, y):
    res = 0.0
    c1 = matrix[y, x]
    neighbors = around(matrix, x, y)
    for c2 in neighbors:
        res += distance(c1, c2)
    return res

def create_contrast_matrix(img):
    img_colors = img.convert('RGB')
    img_colorpixels = load(img_colors)
    width = img.size[0]
    height = img.size[1]
    colormatrix = np.zeros((height,width))
    colormatrix = np.array(colormatrix, dtype=tuple)
    contrastmatrix = np.zeros((height,width))
    for x in range(width):
        for y in range(height):
            colormatrix[y, x] = img_colorpixels[x,y]
    for x in range(width):
        for y in range(height):
            contrastmatrix[y, x] = check_contrast(colormatrix, x, y)
    return contrastmatrix

def simplify(img, threshold):
    width = img.size[0]
    height = img.size[1]
    contrastmatrix = create_contrast_matrix(img)
    res = PIL.Image.new(mode = "RGB", size = (width, height), color = (255, 255, 255))
    res_pixels = load(res)
    for x in range(width):
        for y in range(height):
            if contrastmatrix[y, x] >= threshold:
                res_pixels[x, y] = (0,0,0)
    save(res, 'Simplified_' + str(threshold))

def simplifymain():
    namecheck = True
    while namecheck:
        imgname = input('Image file name: ')
        try:
            img = open(imgname)
            namecheck = False
        except:
            print("That file doesn\'t exist.")
    width = img.size[0]
    height = img.size[1]
    start = time.time()
    contrastmatrix = create_contrast_matrix(img)
    end = time.time()
    print('Matrix created in ' + str(round(end-start, 2)) + ' seconds.')
    cont = True
    while cont:
        threshold = input('Threshold (enter \'done\' if that\'s all): ')
        if threshold != '' and threshold in 'done|stop|no':
            cont = False
        else:
            backr = int(input('Background color R: '))
            backg = int(input('Background color G: '))
            backb = int(input('Background color B: '))
            backgroundcolor = (backr, backg, backb)
            paintr = int(input('Paint color R: '))
            paintg = int(input('Paint color G: '))
            paintb = int(input('Paint color B: '))
            paintcolor = (paintr, paintg, paintb)
            res = PIL.Image.new(mode = "RGB", size = (width, height), color = backgroundcolor)
            start = time.time()
            res_pixels = load(res)
            threshold = float(threshold)
            for x in range(width):
                for y in range(height):
                    if contrastmatrix[y, x] >= threshold:
                        res_pixels[x, y] = paintcolor
            save(res, imgname + '_simplified_' + str(threshold))
            end = time.time()
            print('Created ' + imgname + '_simplified_' + str(threshold) + '.png in ' + str(round(end-start, 2)) + ' seconds.')

simplifymain()
