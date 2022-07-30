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
    
def distance3d(c1,c2):
    r1, g1, b1 = c1
    r2, g2, b2 = c2
    return math.sqrt((r2-r1)**2 + (g2-g1)**2 + (b2-b1)**2)

def closest(colorlist, n):
    dist = -1
    for i in colorlist:
        if i != n:
            if dist < 0 or distance3d(n,i) <= dist:
                dist = distance3d(n,i)
                closesti = i
    return closesti

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
    chains = []
    subchain = set()
    for i in colorlist:
        if not any(i in sublist for sublist in chains):
            chaincheck = i
            while closest(colorlist, chaincheck) not in subchain and not any(closest(colorlist, chaincheck) in sublist2 for sublist2 in chains):
                chaincheck = closest(colorlist, chaincheck)
                subchain.add(chaincheck)
            subchain.add(i)
            chains.append(subchain)
            subchain = set()
    print('Simplified down to', len(chains), 'colors.')
    chain_centers = [chain_center(chain) for chain in chains]
    return chain_centers

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
        print('Matrix and color set created in ' + str(round(end-start, 2)) + ' seconds.')
        print('There are', len(colorset), 'different colors of pixels in this image.')
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
            width = img.size[0]
            height = img.size[1]
            start = time.time()
            colorlist = cluster_centers(colorset)
            end = time.time()
            print('Cluster centers found in', round(end-start,2), ' seconds.')
            res = PIL.Image.new(mode = "RGB", size = (width, height), color = (255, 255, 255))
            res_pixels = load(res)
            for x in range(width):
                for y in range(height):
                    res_pixels[x,y] = closestcolor(matrix[y,x], colorlist)
            save(res, imgname[:-4] + '_Simplified_' + str(count))
            start = time.time()
            print('Created', imgname[:-4] + '_Simplified_' + str(count) + '.png in', round(start-end, 2), 'seconds.')
            count += 1
            cont = input('Simplify again?: ')
            img = open(imgname[:-4] + '_Simplified_' + str(count-1) + '.png')

colorsimplifymain()
a = input()
