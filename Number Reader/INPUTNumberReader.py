import numpy as np
import pygame as pg
import os
import sys


class BinaryImage:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pixels = np.zeros((width, height))
    
    def draw(self, x, y):
        self.pixels[x, y] = 1

    def clear(self):
        self.pixels = np.zeros((self.width, self.height))

    def data(self):
        res = []
        for i in self.pixels:
            for j in i:
                res.append(int(j))
        return np.array(res)

class Inputs:
    def __init__(self, imagewidth, imageheight, coef = 10, font = "arial.ttf", fontsize = 50):
        self.width = imagewidth * coef
        self.height = imageheight * coef
        self.coef = coef
        self.font = pg.font.SysFont(font, fontsize)
        self.screen = pg.display.set_mode((self.width, self.height))

    def pos2index(self, pos):
        return (pos[1]//self.coef, pos[0]//self.coef)

    def draw(self, image):
        self.screen.fill((255, 255, 255))
        for i in range(self.width//self.coef):
            for j in range(self.height//self.coef):
                if image.pixels[j, i]:
                    pg.draw.rect(self.screen, (0, 0, 0), (i*self.coef, j*self.coef, self.coef, self.coef))
        pg.display.update()

    def validpos(self, event):
        try:
            return event.pos[0] < self.width and event.pos[1] < self.height
        except:
            return False

    def input(self):
        self.screen.fill((255, 255, 255))
        image = BinaryImage(self.width//self.coef, self.height//self.coef)
        cont = True
        while cont:
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    pg.quit()
                    sys.exit()
                elif event.type == pg.MOUSEBUTTONDOWN or (pg.mouse.get_pressed()[0] and self.validpos(event)):
                    image.draw(self.pos2index(event.pos)[0], self.pos2index(event.pos)[1])
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN or event.key == pg.K_SPACE:
                        return image.data()
                    elif event.key == pg.K_BACKSPACE or event.key == pg.K_DELETE or event.key == pg.K_z or event.key == pg.K_LCTRL:
                        image.clear()
                self.draw(image)
    
    def output(self, prediction):
        self.screen.fill((255, 255, 255))
        text = self.font.render(str(prediction), True, (0, 0, 0))
        self.screen.blit(text, (self.width//2 - text.get_width()//2, self.height//2 - text.get_height()//2))
        pg.display.update()
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    pg.quit()
                    sys.exit()
                if (event.type == pg.KEYDOWN and (event.key == pg.K_RETURN or event.key == pg.K_SPACE)) or event.type == pg.MOUSEBUTTONDOWN:
                    return None

def forward_prop(W1, b1, W2, b2, pixels):
    Z1 = np.dot(W1, pixels.T) + b1
    A1 = np.maximum(0, Z1)
    Z2 = np.dot(W2, A1) + b2
    A2 = np.exp(Z2) / sum(np.exp(Z2))
    return Z1, A1, Z2, A2

def predict(img, W1, b1, W2, b2):
    _, _, _, A2 = forward_prop(W1, b1, W2, b2, img.T)
    return np.argmax(A2, 0)

def wb_file_input(inputtxt:str, default, shape:tuple, shapefix:bool = False):
    while True:
        a = input(inputtxt)
        if a == "":
            a = default
        if ".txt" not in a:
            a += ".txt"
        try:
            a = np.loadtxt(a, dtype = float)
            if shapefix:
                a = a.reshape(shape)
            if (a.shape == shape):
                return a
            print("Shape of file does not match, try again")
        except FileNotFoundError:
            print("File not found, try again")
    
def main():

    w1 = wb_file_input("Weights 1 file name? (default: W1.txt):", "W1.txt", (10, 256))
    w2 = wb_file_input("Weights 2 file name? (default: W2.txt):", "W2.txt", (10, 10))
    B1 = wb_file_input("Biases 1 file name? (default: b1.txt):", "b1.txt", (10, 1), True)
    B2 = wb_file_input("Biases 2 file name? (default: b2.txt):", "b2.txt", (10, 1), True)
    
    pg.init()
    pg.display.set_caption("Number Reader")
    inputs = Inputs(16, 16, 40)

    while True:
        pixels = inputs.input()
        inputs.output(predict(pixels.T.reshape(pixels.T.shape[0], 1), w1, B1, w2, B2)[0])

if __name__ == "__main__":
    main()



