import random
import pygame

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
gridwidth = 50
gridheight = 50
margin = 5
FONT = 'Calibri'
TEXTSIZE = 70


def createboard(x, y, mines):
    board = []
    for i in range(0, y):
        row = []
        for j in range(0, x):
            if [j, i] in mines:
                row.append('x')
            else:
                row.append('_')
        board.append(row)
    return board


def choose(board, solution, y, x):
    #print(board)
    #print(solution)
    if board == solution:
        print('You have solved the mine-field!\nWell done!')
        main()
    field = ''
    for i in board:
        for j in i:
            if j == 'x' or j == '_':
                field += '_ '
            else:
                field += str(j) + ' '
        field += '\n'
    print(field)
    count = findadjacent(x, y, 'x', board)
    if count == 'x':
        print('You hit a mine, game over!')
        for i in solution:
            print(i)
        main()
    board[y][x] = count
    if count == 0:
        board = spread(x, y, board, solution)
    return board



def spread(x, y, board, solution):
    xs = [x - 1, x, x + 1]
    ys = [y - 1, y, y + 1]
    for i in xs:
        for j in ys:
            if i > len(board[0]) - 1 or j > len(board) - 1 or i < 0 or j < 0 or (i == x and j == y):
                continue
            count = findadjacent(i, j, 'x', board)
            if count == 0 and board[j][i] != count:
                board[j][i] = count
                board = spread(i, j, board, solution)
            board[j][i] = count
    return board


def findadjacent(x, y, char, board):
    count = 0
    xs = [x - 1, x, x + 1]
    ys = [y - 1, y, y + 1]
    if board[y][x] == 'x':
        return 'x'
    for i in xs:
        for j in ys:
            if i > len(board[0]) - 1 or j > len(board) - 1 or i < 0 or j < 0:
                continue
            elif board[j][i] == char:
                count += 1
    return count
#circle(Surface, color, pos, radius, width=0)
#pygame.draw.circle(screen, BLUE, )


def main():
    boardsize = int(input('How big would you like the board to be? '))
    mineno = int(input('How many mines would you like there to be? '))
    pygame.init()

    WINDOW_SIZE = [(gridwidth * boardsize) + (margin * boardsize + 4),
               (gridheight * boardsize) + (margin * boardsize + 4)]
    screen = pygame.display.set_mode(WINDOW_SIZE)
    # Set title of screen
    pygame.display.set_caption("Minesweeper")
    running = True
    clock = pygame.time.Clock()

    board = createboard(boardsize, boardsize, [[random.randrange(0, boardsize), random.randrange(0, boardsize)] for i in range(0, mineno)])
    solution = [[findadjacent(x, y, 'x', board) for x in range(0, len(board[y]))] for y in range(0, len(board))]
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # User clicks the mouse. Get the position
                pos = pygame.mouse.get_pos()
                # Change the x/y screen coordinates to grid coordinates
                column = abs(pos[0] - margin) // (gridwidth + margin)
                row = abs(pos[1] - margin) // (gridheight + margin)
                print("Click ", pos, "Grid coordinates: ", row, column)
                board = choose(board, solution, row, column)
        screen.fill(BLACK)
        for row in range(boardsize):
            for column in range(boardsize):
                for i in range(0, 8):
                    if board[row][column] == i:
                        font = pygame.font.SysFont(FONT, TEXTSIZE, True, False)
                        text = font.render(str(i), True, WHITE)
                        screen.blit(text, [(margin + gridwidth) * column + gridwidth / 3,
                                       (margin + gridheight) * row,
                                       gridwidth,
                                       gridheight])
                if board[row][column] == '_' or board[row][column] == 'x':
                    pygame.draw.rect(screen,
                                 WHITE,
                                 [(margin + gridwidth) * column + margin,
                                  (margin + gridheight) * row + margin,
                                  gridwidth,
                                  gridheight])
        clock.tick(60)
        pygame.display.flip()
    pygame.quit()

main()
