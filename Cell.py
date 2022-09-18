import pygame
from constants import *

class Cell:

    def __init__(self, x, y, width, height, row, col):
        self.rect = pygame.Rect(x, y, width, height)
        self.val = None
        self.potential = "123456789"
        self.fill_color = WHITE
        self.row = row
        self.col = col

    def __repr__(self):
        return str(self.val)
    def draw(self, mw):
        pygame.draw.rect(mw, self.fill_color, self.rect)
        pygame.draw.rect(mw, GREY, self.rect, 2)
        if self.val is not None:
            font = pygame.font.Font(None, 50,).render(self.val, True, BLACK)
            mw.blit(font, (self.rect.x + FONTSEP, self.rect.y + FONTSEP))
        else:
            potText1 = pygame.font.SysFont(POTFONT, POTFONTSIZE).render(self.potential[0:5],True, BLACK)
            potText2 = pygame.font.SysFont(POTFONT, POTFONTSIZE).render(self.potential[5:], True, BLACK)
            mw.blit(potText1, (self.rect.x + TEXTBORDERSEP, self.rect.y + TEXTBORDERSEP))
            mw.blit(potText2, (self.rect.x + TEXTBORDERSEP, self.rect.y + SMALLSEP + TEXTBORDERSEP))


    def setVal(self, val):
        self.val = val



