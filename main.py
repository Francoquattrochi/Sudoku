import pygame
from Cell import Cell
from constants import *
from random import choice
from time import sleep

pygame.init()
mw = pygame.display.set_mode((750, 750))
clock = pygame.time.Clock()
isRunning = True

history = []


def createBoard():
    board = []
    for i in range(9):
        row = []
        for j in range(9):
            row.append(Cell(XSEP + i * CELLSIZE, YSEP + j * CELLSIZE, CELLSIZE, CELLSIZE, i, j))
        board.append(row)
    return board


def drawBoard():
    for row in board:
        for cell in row:
            cell.draw(mw)
    for i in range(2):
        x = XSEP + CELLSIZE * 3 * (i + 1)
        pygame.draw.line(mw, BLACK, (x, YSEP), (x, YSEP + CELLSIZE * 9), 5)
    for i in range(2):
        y = YSEP + CELLSIZE * 3 * (i + 1)
        pygame.draw.line(mw, BLACK, (XSEP, y), (XSEP + CELLSIZE * 9, y), 5)


def updateCell(row, col):
    vert = getVertical(row, col)
    adjacent = getSquare(row, col)
    horz = getHorizontal(row, col)
    merged = vert + adjacent + horz
    for cell in merged:
        cell.potential = cell.potential.replace(board[row][col].val, " ")
        cell.fill_color = GREY


def getCell(x, y):
    row = int((x - XSEP) / CELLSIZE)
    col = int((y - YSEP) / CELLSIZE)
    return row, col


def getVertical(row, col):
    vert = []
    for i in range(9):
        vert.append(board[row][i])
    return vert


def getSquare(row, col):
    midRow = (col // 3) * 3 + 1
    midCol = (row // 3) * 3 + 1
    adjacent = []
    for i in range(midRow - 1, midRow + 2):
        for j in range(midCol - 1, midCol + 2):
            adjacent.append(board[j][i])
    return adjacent


def getHorizontal(row, col):
    horizontal = []
    for i in range(9):
        horizontal.append(board[i][col])
    return horizontal

def getOrderedAvailability():
    D = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: []}
    for row in board:
        for cell in row:
            if cell.val is None:
                D[len(cell.potential.replace(" ", ""))].append(cell)
    for key in D:
        if D[key] and key != 0:
            return D[key]
    return []


def autoPlace(available):
    randCell = choice(available)
    randCell.setVal(choice(randCell.potential.replace(" ", "")))
    updateCell(randCell.row, randCell.col)


def resetColor():
    for row in board:
        for cell in row:
            cell.fill_color = WHITE


def addToHistory():
    newBoard = []
    for i in range(9):
        row = []
        for j in range(9):
            currRect = board[i][j].rect
            currCell = Cell(currRect.x, currRect.y, currRect.width, currRect.height, i, j)
            currCell.potential = board[i][j].potential
            currCell.val = board[i][j].val
            row.append(currCell)
        newBoard.append(row)
    history.append(newBoard)



board = createBoard()
while isRunning:
    pygame.display.update()
    clock.tick(40)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        if event.type == pygame.KEYDOWN:
            key = event.unicode
            # Checks that key is a number from 1 to 9
            if key in "123456789":
                x, y = pygame.mouse.get_pos()
                # Checks if event occurred on screen
                if XSEP < x < XSEP + CELLSIZE * 9 and YSEP < y < YSEP + CELLSIZE * 9:
                    row, col = getCell(x, y)
                    currCell = board[row][col]
                    if currCell.val is None:
                        resetColor()
                        addToHistory()
                        currCell.setVal(key)
                        updateCell(row, col)
            elif event.key == pygame.K_r:
                board = createBoard()
                history = []
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_SPACE]:
        resetColor()
        available = getOrderedAvailability()
        if len(available) > 0:
            addToHistory()
            autoPlace(available)
    if pressed[pygame.K_z]:
        if len(history) > 0:
            board = history.pop()
    drawBoard()
