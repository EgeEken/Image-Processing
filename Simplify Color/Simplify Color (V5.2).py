from PIL import Image
import PIL
import time
import math
import numpy as np
import random

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
    res = np.array(np.zeros((height,width)), dtype=tuple)
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

def closest(colorlist, n):
    dist = -1
    for i in colorlist:
        if i != n:
            if dist < 0 or distance(n,i) <= dist:
                dist = distance(n,i)
                closesti = i
    return closesti

def closest2(colorlist):
    dist = -1
    closestgroup = set()
    for i in colorlist:
        close = closest(colorlist, i)
        if dist < 0 or distance(close, i) <= dist:
            dist = distance(close, i)
            closestgroup = {i, close}
    return closestgroup

def chain_center(chain):
    xtotal = 0
    ytotal = 0
    ztotal = 0
    for coord in chain:
        x,y,z = coord
        xtotal += x
        ytotal += y
        ztotal += z
    return (int(xtotal/len(chain)),int(ytotal/len(chain)),int(ztotal/len(chain)))

def cluster_centers(colorlist):
    chains = [closest2(colorlist)]
    for i in colorlist:
        if i not in chains[0]:
            chains.append({i})
    print('Simplified down to', len(chains), 'colors.')
    chain_centers = [chain_center(chain) for chain in chains]
    return chain_centers

def colorsimplifymain():
    a = False
    while not a:
        imgname = input('Image file name: ')
        try:
            img = open(imgname)
            a = True
        except FileNotFoundError:
            print('File not found (either doesn\'t exist, is not in this folder, or has a different format, try again)')
    cont = 'again'
    count = 0
    while cont in 'again|continue|yes':
        start = time.time()
        matrix = matrix_create(img)
        colorset = colorset_create(matrix)
        end = time.time()
        startcount = len(colorset)
        print('Matrix and color set created in ' + str(round(end-start, 2)) + ' seconds.')
        print('There are', startcount, 'different colors of pixels in this image.')
        if len(colorset) == 1:
            fpscheck = True
            while fpscheck:
                FPS = input('FPS count: ')
                try:
                    FPS = int(math.sqrt(int(FPS))**2)
                    fpscheck = False
                except:
                    print('Enter positive integer for fps.')
            import imageio
            start = time.time()
            filenames = [imgname]
            filename = imgname[:-4] + '_Simplified_'
            filenames.extend([filename + str(i) + '.png' for i in range(count)])
            with imageio.get_writer(filename + 'GIF.gif', mode='I', duration=round(1/FPS, 2)) as writer:
                for filename in filenames:
                    image = imageio.imread(filename)
                    writer.append_data(image)
            cont = 'stop'
            end = time.time()
            print(filename + 'GIF.gif created in', round(end-start,2), 'seconds.')
        else:
            colorcountcheck = True
            while colorcountcheck:
                colorcount = input("How many colors do you want to drop?: ")
                try:
                    colorcount = int(colorcount)
                    colorcountcheck = False
                except:
                    print("Enter an integer.")
            width = img.size[0]
            height = img.size[1]
            start = time.time()
            while len(colorset) != startcount - colorcount:
                colorlist = cluster_centers(colorset)
                colorset = colorlist
            end = time.time()
            print('Cluster centers dropped down by the desired amount, down to', startcount - colorcount ,'in', round(end-start,2), ' seconds.')
            res = PIL.Image.new(mode = "RGB", size = (width, height), color = (255, 255, 255))
            res_pixels = load(res)
            for x in range(width):
                for y in range(height):
                    if matrix[y,x] in colorlist:
                        res_pixels[x,y] = matrix[y,x]
                    else:
                        res_pixels[x,y] = closest(colorlist, matrix[y,x])
            save(res, imgname[:-4] + '_Simplified_' + str(count) + '_' + str(len(colorlist)))
            start = time.time()
            print('Created', imgname[:-4] + '_Simplified_' + str(count) + '_' + str(len(colorlist)) + '.png in', round(start-end, 2), 'seconds.')
            cont = input('Simplify again?: ')
            img = open(imgname[:-4] + '_Simplified_' + str(count) + '_' + str(len(colorlist)) + '.png')
            count += 1

colorsimplifymain()
a = input()
