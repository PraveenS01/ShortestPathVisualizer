# importing Necessary Libraries
import pygame
from collections import deque
import random

# Created A Point Class For Source And Target Cells
class Point:
    def __init__(self, xx, yy):
        self.x = xx
        self.y = yy


# Created A Node Class For The Path And Visualization Of Cells
class Node:
    def __init__(self, P, d):
        self.pt = P
        self.dist = d


# Initializing Pygame
pygame.init()

# Screen Dimensions
screen_width = 800
screen_height = 800

# Setting Up The Screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Shortest Path Visualiser')

# Setting Up The Colors
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0)
purple = (128, 0, 128)
grey = (255, 165, 0)
orange = (128, 128, 128)
turquoise = (64, 224, 208)

# Setting Up And Displaying The Grid
screen.fill(white)
gameOn = True
line_dx = 20
line_dy = 20
while line_dx < 800 and line_dy < 800:
    pygame.draw.line(screen, black, (0, line_dx), (800, line_dx))
    pygame.draw.line(screen, black, (line_dy, 0), (line_dy, 800))
    line_dx += 20
    line_dy += 20

# Some Needed Initialized Variables And Data Structures
k = 0
path = []
blocks = []
pathFound = 1
source = None
target = None
dRow = [-1, 0, 0, 1]
dCol = [0, -1, 1, 0]

# Checking Validity Of A Neighbour
def isValid(row, col):
    return (row >= 0) and (col >= 0) and (row < 40) and (col < 40)

# Visualizes BFS and Finds A Shortest Path If Exist
def pathMover(src, dest):
    d = [[-1 for i in range(40)] for i in range(40)]
    d[src.x][src.y] = 0
    visited = [[False for i in range(40)] for i in range(40)]
    visited[src.x][src.y] = True
    q = deque()
    s = Node(src, 0)
    q.append(s)
    ok = False
    while (len(q) > 0):
        curr = q.popleft()
        pt = curr.pt
        # Shortest Path Finding If Exist
        if (pt.x == dest.x and pt.y == dest.y):
            xx, yy = pt.x, pt.y 
            dist = curr.dist
            d[pt.x][pt.y] = dist
            pathmoves = []
            while (xx != src.x or yy != src.y):
                if (xx > 0 and d[xx - 1][yy] == dist - 1):
                    pathmoves.append([xx - 1, yy])
                    xx -= 1
                if (xx < 40 - 1 and d[xx + 1][yy] == dist - 1):
                    pathmoves.append([xx + 1, yy])
                    xx += 1
                if (yy > 0 and d[xx][yy - 1] == dist - 1):
                    pathmoves.append([xx, yy - 1])
                    yy -= 1
                if (yy < 40 - 1 and d[xx][yy + 1] == dist - 1):
                    pathmoves.append([xx, yy + 1])
                    yy += 1
                dist -= 1
            pathmoves = pathmoves[::-1]
            return pathmoves
        # BFS Visualization
        for i in range(4):
            row = pt.x + dRow[i]
            col = pt.y + dCol[i]
            if (isValid(row, col) and ([row, col] not in blocks) and (not visited[row][col])):
                visited[row][col] = True
                adjCell = Node(Point(row, col), curr.dist + 1)
                q.append(adjCell)
                d[row][col] = curr.dist + 1
                if (row == dest.x and col == dest.y) or (row == src.x and col == src.y):
                    continue
                else:
                    rect = pygame.Rect(20 * col, 20 * row, 19, 19)
                    pygame.draw.rect(screen, turquoise, rect)
                    pygame.display.update()
    if not ok:
        return -1


# Main Loop
while gameOn:
    for event in pygame.event.get():
        # EXIT the Visualization
        if event.type == pygame.QUIT:
            gameOn = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Source
            if k == 0:
                x = pygame.mouse.get_pos()
                source = Point(((20 * (x[1] // 20) + 1) // 20), ((20 * (x[0] // 20) + 1) // 20), )
                rect = pygame.Rect(20 * (x[0] // 20) + 1, 20 * (x[1] // 20) + 1, 19, 19)
                pygame.draw.rect(screen, blue, rect)
                k = 1

            # Target
            elif k == 1:
                x = pygame.mouse.get_pos()
                target = Point(((20 * (x[1] // 20) + 1) // 20), ((20 * (x[0] // 20) + 1) // 20), )
                rect = pygame.Rect(20 * (x[0] // 20) + 1, 20 * (x[1] // 20) + 1, 19, 19)
                pygame.draw.rect(screen, red, rect)
                k = 20

            # Blocks
            elif k == 20:
                b = pygame.mouse.get_pos()
                if (target.x != ((20 * (b[1] // 20) + 1) // 20) or target.y != ((20 * (b[0] // 20) + 1) // 20)) and (
                        source.x != ((20 * (b[1] // 20) + 1) // 20) or source.y != ((20 * (b[0] // 20) + 1) // 20)):
                    blocks.append([((20 * (b[1] // 20) + 1) // 20), ((20 * (b[0] // 20) + 1) // 20), ])
                    rect = pygame.Rect(20 * (b[0] // 20) + 1, 20 * (b[1] // 20) + 1, 19, 19)
                    pygame.draw.rect(screen, purple, rect)

        if event.type == pygame.KEYDOWN:
            # Start Visualizing The BFS And Try To Find A Shortest Path
            if event.key == pygame.K_SPACE:
                k = 30
                if k == 30:
                    path = pathMover(source, target)
                    if path != -1:
                        path.pop(0)
                        path.append([target.x, target.y])

            # Back To Normal (Fresh Start)
            if event.key == pygame.K_BACKSPACE or event.key == pygame.K_x:
                k = 0
                source = None
                target = None
                blocks = []
                pathFound = 1
                path = []
                screen.fill(white)
                line_dx = 20
                line_dy = 20

                while line_dx < 800 and line_dy < 800:
                    pygame.draw.line(screen, black, (0, line_dx), (800, line_dx))
                    pygame.draw.line(screen, black, (line_dy, 0), (line_dy, 800))
                    line_dx += 20
                    line_dy += 20

                pygame.display.update()

            # Random Walls Or Maze
            if event.key == pygame.K_m and k == 20:
                count = 0
                while count <= 100:
                    count += 1
                    b = [None, None]
                    b[0] = random.randint(0, 800)
                    b[1] = random.randint(0, 800)
                    if (target.x != ((20 * (b[1] // 20) + 1) // 20) or target.y != ((20 * (b[0] // 20) + 1) // 20)) and (
                            source.x != ((20 * (b[1] // 20) + 1) // 20) or source.y != ((20 * (b[0] // 20) + 1) // 20)):
                        blocks.append([((20 * (b[1] // 20) + 1) // 20), ((20 * (b[0] // 20) + 1) // 20), ])
                        rect = pygame.Rect(20 * (b[0] // 20) + 1, 20 * (b[1] // 20) + 1, 19, 19)
                        pygame.draw.rect(screen, purple, rect)

        # If Path Found Then Visualize
        if pathFound == 1 and path != -1:
            for i in path:
                if i[0] == target.x and i[1] == target.y:
                    pathFound = 0
                    continue
                rect = pygame.Rect(20 * i[1], 20 * i[0], 19, 19)
                pygame.draw.rect(screen, green, rect)
                pygame.display.update()

        pygame.display.update()


pygame.quit()