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
    res = np.zeros(width,height)
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

def is_grain(matrix, x, y):
    if matrix[y, x] == (255,255,255):
        return False
    neighbors = around(matrix, x, y)
    for c in neighbors:
        if c == (0,0,0):
            return False
    return True

def create_contrast_matrix(img):
    img_colors = img.convert('RGB')
    img_colorpixels = load(img_colors)
    width = img.size[0]
    height = img.size[1]
    colormatrix = np.zeros((width,height))
    colormatrix = np.array(colormatrix, dtype=tuple)
    contrastmatrix = np.zeros((width,height))
    for x in range(width):
        for y in range(height):
            colormatrix[y, x] = img_colorpixels[x,y]
    for x in range(width):
        for y in range(height):
            contrastmatrix[y, x] = check_contrast(colormatrix, x, y)
    return contrastmatrix

def create_simplified_matrix(img, threshold):
    width = img.size[0]
    height = img.size[1]
    contrastmatrix = create_contrast_matrix(img)
    res = np.zeros((width,height))
    res = np.array(res, dtype=tuple)
    for x in range(width):
        for y in range(height):
            if contrastmatrix[y, x] >= threshold:
                res[y, x] = (0,0,0)
            else:
                res[y, x] = (255,255,255)
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

def grain_cleaner(matrix):
    width = len(matrix[0])
    height = len(matrix)
    res = np.zeros((width,height))
    res = np.array(res, dtype=tuple)
    for x in range(width):
        for y in range(height):
            if is_grain(matrix, x, y):
                res[y, x] = (255,255,255)
            else:
                res[y, x] = matrix[y, x]
    return res
                
    
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
            threshold = float(threshold)
            dcount = int(input("Enter direction count for edge detection checks (integer multiples of 8 only) : "))
            matrix = grain_cleaner(create_simplified_matrix(img, threshold))
            backr = int(input('Background color R: '))
            backg = int(input('Background color G: '))
            backb = int(input('Background color B: '))
            backgroundcolor = (backr, backg, backb)
            res = PIL.Image.new(mode = "RGB", size = (width, height), color = backgroundcolor)
            original = load(open(imgname))
            start = time.time()
            res_pixels = load(res)
            for x in range(width):
                for y in range(height):
                    if is_inside(x, y, matrix, dcount):
                        res_pixels[x, y] = original[x, y]
            save(res, imgname + '_cropped_' + str(threshold) + '_' + str(dcount))
            end = time.time()
            print('Created ' + imgname + '_cropped_' + str(threshold) + '_' + str(dcount) + '.png in ' + str(round(end-start, 2)) + ' seconds.')

simplifymain()
