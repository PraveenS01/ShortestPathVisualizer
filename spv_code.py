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
screen_width = 800 # Must Be Multiple Of line_dy 
screen_height = 800 # Must be Multiple Of line_dx

# Setting Up The Screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Shortest Path Visualiser (BFS)')

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

# Some Needed Initialized Variables And Data Structures
algorithm = "BFS"
dRow = [-1, 0, 0, 1]
dCol = [0, -1, 1, 0]

def resetWindow():
    global k, source, target, blocks, pathFound, path, line_dx, line_dy, gameOn, num_rows, num_cols

    k = 0
    source = None
    target = None
    blocks = []
    pathFound = 1
    path = []
    line_dx = 20
    line_dy = 20
    gameOn = True
    num_rows, num_cols = screen_height // line_dx, screen_width // line_dy

    screen.fill(white)

    while line_dx < screen_height or line_dy < screen_width:
        if line_dx < screen_height:
            # Add Horizontal Line
            pygame.draw.line(screen, black, (0, line_dx), (screen_width, line_dx))
            line_dx += 20

        if line_dy < screen_width:
            # Add Vertical Line
            pygame.draw.line(screen, black, (line_dy, 0), (line_dy, screen_height))
            line_dy += 20

    pygame.display.update()

# Update Algorithm
def toggleAlgorithm():
    global algorithm

    if algorithm == "BFS":
        algorithm = "Bidirectional BFS"
    else:
        algorithm = "BFS"

    pygame.display.set_caption('Shortest Path Visualiser ({})'.format(algorithm))

# Checking Validity Of A Neighbour
def isValid(row, col):
    return (row >= 0) and (col >= 0) and (row < num_rows) and (col < num_cols)

# Visualizes BFS and Finds A Shortest Path If Exist
def pathMoverBFS(src, dest):
    d = [[-1 for i in range(num_cols)] for i in range(num_rows)]
    d[src.x][src.y] = 0
    visited = [[False for i in range(num_cols)] for i in range(num_rows)]
    visited[src.x][src.y] = True
    q = deque()
    s = Node(src, 0)
    q.append(s)
    ok = False
    while (len(q) > 0):
        curr = q.popleft()
        pt = curr.pt

        if not (pt.x == src.x and pt.y == src.y) and not (pt.x == dest.x and pt.y == dest.y):
            rect = pygame.Rect(20 * pt.y, 20 * pt.x, 19, 19)
            pygame.draw.rect(screen, turquoise, rect)
            pygame.display.update()

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
                if (xx < num_rows - 1 and d[xx + 1][yy] == dist - 1):
                    pathmoves.append([xx + 1, yy])
                    xx += 1
                if (yy > 0 and d[xx][yy - 1] == dist - 1):
                    pathmoves.append([xx, yy - 1])
                    yy -= 1
                if (yy < num_cols - 1 and d[xx][yy + 1] == dist - 1):
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
                    pygame.draw.rect(screen, purple, rect)
                    pygame.display.update()
    if not ok:
        return -1

def pathMoverBidirectionalBFS(src, dest):
    terminate = False
    vertex = None
    visited_f, visited_b = set(), set()
    df, db = [[float('inf') for i in range(num_cols)] for i in range(num_rows)], [[float('inf') for i in range(num_cols)] for i in range(num_rows)]
    qf, qb = deque([(src.x, src.y)]), deque([(dest.x, dest.y)])

    visited_f.add((src.x, src.y))
    visited_b.add((dest.x, dest.y))

    df[src.x][src.y] = 0
    db[dest.x][dest.y] = 0

    while len(qf) > 0 or len(qb) > 0:
        if len(qf) > 0:
            # Search Forward
            u = qf.popleft()

            if u != (src.x, src.y):
                rect = pygame.Rect(20 * u[1], 20 * u[0], 19, 19)
                pygame.draw.rect(screen, turquoise, rect)
                pygame.display.update()

            for i in range(4):
                row, col = u[0] + dRow[i], u[1] + dCol[i]

                if isValid(row, col) and ([row, col] not in blocks) and ((row, col) not in visited_f):
                    visited_f.add((row, col))
                    df[row][col] = df[u[0]][u[1]] + 1
                    qf.append((row,col))

                    rect = pygame.Rect(20 * col, 20 * row, 19, 19)
                    pygame.draw.rect(screen, purple, rect)
                    pygame.display.update()

                if (row,col) in visited_b:
                    vertex = (row,col)
                    terminate = True
                    break

            if terminate:
                break

        if len(qb) > 0:
            # Search Backward
            v = qb.popleft()

            if v != (dest.x, dest.y):
                rect = pygame.Rect(20 * v[1], 20 * v[0], 19, 19)
                pygame.draw.rect(screen, turquoise, rect)
                pygame.display.update()

            for i in range(4):
                row, col = v[0] + dRow[i], v[1] + dCol[i]

                if isValid(row, col) and ([row, col] not in blocks) and ((row, col) not in visited_b):
                    visited_b.add((row, col))
                    db[row][col] = db[v[0]][v[1]] + 1
                    qb.append((row, col))

                    rect = pygame.Rect(20 * col, 20 * row, 19, 19)
                    pygame.draw.rect(screen, purple, rect)
                    pygame.display.update()

                if (row,col) in visited_f:
                    vertex = (row,col)
                    terminate = True
                    break

            if terminate:
                break

    # No Path Found
    if not vertex:
        return -1

    # Build Forward Path
    x,y = vertex[0], vertex[1]
    forward_path = [(x,y)]
    flag = True

    while flag:
        for i in range(4):
            row, col = x + dRow[i], y + dCol[i]

            if not isValid(row, col):
                continue

            if x == src.x and y == src.y:
                flag = False
                break

            if df[row][col] == df[x][y] - 1:
                forward_path.append((row,col))
                x,y = row,col

    forward_path = forward_path[::-1]

    # Build Backward Path
    x,y = vertex[0], vertex[1]
    backward_path = []
    flag = True

    while flag:
        for i in range(4):
            row, col = x + dRow[i], y + dCol[i]

            if not isValid(row, col):
                continue

            if x == dest.x and y == dest.y:
                flag = False
                break

            if db[row][col] == db[x][y] - 1:
                backward_path.append((row,col))
                x,y = row,col

    return forward_path + backward_path

resetWindow()

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
                    pygame.draw.rect(screen, black, rect)

        if event.type == pygame.KEYDOWN:
            # Start Visualizing The BFS And Try To Find A Shortest Path
            if event.key == pygame.K_SPACE:
                k = 30
                if k == 30:
                    if algorithm == "BFS":
                        path = pathMoverBFS(source, target)
                    elif algorithm == "Bidirectional BFS":
                        path = pathMoverBidirectionalBFS(source, target)
                
                    if path != -1:
                        path.pop(0)
                        path.append([target.x, target.y])

            # Toggle Between The Two Algorithms
            elif event.key == pygame.K_1:
                toggleAlgorithm()

            # Back To Normal (Fresh Start)
            if event.key == pygame.K_BACKSPACE or event.key == pygame.K_x:
                resetWindow()

            # Random Walls Or Maze
            if event.key == pygame.K_m and k == 20:
                count = 0
                while count <= 100:
                    count += 1
                    b = [None, None]
                    b[0] = random.randint(0, screen_width)
                    b[1] = random.randint(0, screen_height)
                    if (target.x != ((20 * (b[1] // 20) + 1) // 20) or target.y != ((20 * (b[0] // 20) + 1) // 20)) and (
                            source.x != ((20 * (b[1] // 20) + 1) // 20) or source.y != ((20 * (b[0] // 20) + 1) // 20)):
                        blocks.append([((20 * (b[1] // 20) + 1) // 20), ((20 * (b[0] // 20) + 1) // 20), ])
                        rect = pygame.Rect(20 * (b[0] // 20) + 1, 20 * (b[1] // 20) + 1, 19, 19)
                        pygame.draw.rect(screen, black, rect)

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
