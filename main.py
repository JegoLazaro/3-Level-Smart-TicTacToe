import math
import random
from sys import exit
from collections import defaultdict
import pygame
from pygame import mixer
from pygame.locals import *

pygame.init()

computer = 1
human = 2
# Sounds
mixer.music.load('bgsound.wav')
mixer.music.play()
laser = mixer.Sound('laser.wav')


easy = 0
medium = 0
hard = 8000

symbolO = 3
symbolX = 4

utility = -1000

# Color Shortcuts
Gold = (255, 215, 0)
MSB = (123, 104, 238)
black = (0, 0, 0)
white = (255, 255, 255)
red = (200, 0, 0)
blue = (0, 0, 200)


class Player:
    def __init__(self, player, symbol, init):
        self.player = player
        self.symbol = symbol
        self.init = init

    # Board Setup
    def disBoard(self, board):
        self.board = board

    def getMove(self):
        pass

    def onClick(self, location):
        pass

    def getSymbol(self, symbol):
        if symbol == symbolO:
            return symbolX
        else:
            return symbolO



class humanMove(Player):
    def __init__(self, symbol, init):
        super().__init__(human, symbol, init)
        self.lastmove = -1

    def GetMove(self):
        if (self.lastmove != -1):
            move = self.lastmove
            self.lastmove = -1
            return move

    def onClick(self, cell):
        if cell not in self.board.moves:
            self.lastmove = cell

class computerMove(Player):
    def __init__(self, symbol, init, difficulty = hard):
        super().__init__(computer, symbol, init)
        self.lastmove = -1
        self.maxnodes = difficulty

        self.cutoff = False
        self.nodes = 0
        self.max = 0
        self.min = 0
        self.turn = 0


    def GetMove(self):
        nMove = [move for move in self.board.celltuples if move not in self.board.moves]

        if len(nMove) == 16:
            self.turn += 1
            return (0, 0)

        if len(nMove) == 14 and (0, 1) in nMove:
            self.turn += 1
            return (0, 1)
        elif len(nMove) == 14:
            self.turn += 1
            return (0, 2)
        self.loop = 0

        self.cutoff = False
        self.nodes = 0
        self.max = 0
        self.min = 0


        self.turn += 1

        val, move, maxdepth = self.MaxValue(utility, 1000)
        print("\nMove: ", self.turn)
        if self.cutoff:
            print("Depth:", maxdepth)
            print("Nodes generated:", self.nodes + 1)
            print("Max prunings:", self.max)
            print("Min prunings:", self.min)
        return move

    def GetScore(self):
        if self.board.Draw():
            return 0
        elif self.board.GetWinner() == self.symbol:
            return 1
        return -1


    def MaxValue(self, alpha, beta, y=0):
        self.nodes += 1
        y += 1
        depth = y
        maxpos = None
        maxval = utility

        if level == 'easy' or level == 'Easy':
            number = random.randint(0,3)
        elif level == "hard" or level == "Hard" or level == "medium" or level == "Medium":
            number = 3

        for move in self.board.getPos():
            self.loop += 1
            self.board.Move(move, self.symbol)

            if self.nodes >= self.maxnodes:
                self.cutoff = True
                move1 = 0
                move2 = 0
                move3 = 0
                comp1 = 0
                comp2 = 0
                comp3 = 0
                for line in self.board.winningcon:
                    coor1, coor2, coor3 = line
                    val = self.board.board[coor1] + self.board.board[coor2] + self.board.board[coor3]
                    val2 = self.board.board[coor1] + self.board.board[coor2] + self.board.board[coor3]

                    for i in range(number):
                        if val == self.symbol * number:
                            move3 += 1
                            break
                        if val == self.symbol * 1:
                            move2 += 1
                            break
                        if val == self.symbol:
                            move1 += 1
                            break
                        val -= self.getSymbol(self.symbol)

                    for i in range(number):
                        if val2 == self.getSymbol(self.symbol) * number:
                            comp3 += 1
                            break
                        if val2 == self.getSymbol(self.symbol) * 1:
                            comp2 += 1
                            break
                        if val2 == self.getSymbol(self.symbol):
                            comp1 += 1
                            break
                        val2 -= self.symbol

                score = 6 * move3 + number * move2 + move1 - (6 * comp3 + number * comp2 + comp1)
            else:
                if self.board.GameOver():
                    score = self.GetScore()
                else:
                    score, movepos, depth = self.MinValue(alpha, beta, y)  # call to min 'player'

            self.board.remove()

            if score >= beta:
                return score, move, depth
            if score > alpha:
                alpha = score

            if score > maxval:
                maxval = score
                maxpos = move

            if score == 1:
                self.max += 1
                break
        return maxval, maxpos, depth


    def MinValue(self, alpha, beta, y = 0):
        y += 1
        depth = y
        minpos = None
        minval = 1000

        for move in self.board.getPos():
            self.loop += 1
            self.board.Move(move, self.getSymbol(self.symbol))  # make move

            if self.board.GameOver():
                score = self.GetScore()  # score of terminal condition
            else:
                score, movepos, depth = self.MaxValue(alpha, beta, y)

            self.board.remove()

            if score < alpha:
                return score, move, depth
            if score < beta:
                beta = score

            if score < minval:
                minval = score
                minpos = move
            if score == -1:
                self.min += 1
                break

        return minval, minpos, depth



class BackEndBoard:

    celltuples = [(a, b) for a in range(0, 4) for b in range(0, 4)]

    winningcon = [[(a, b) for a in range(0, 3)] for b in range(0, 3)] +\
               [[(b, a) for a in range(0, 3)] for b in range(0, 3)] + \
                 [[(0, 0), (1, 1), (2, 2)],  # Diagonal
                  [(0, 1), (1, 2), (2, 3)],
                  [(0, 3), (1, 2), (2, 1)],
                  [(0, 2), (1, 1), (2, 0)],
                  [(1, 0), (2, 1), (3, 2)],
                  [(1, 1), (2, 2), (3, 1)],
                  [(1, 2), (2, 1), (3, 0)],
                  [(0, 0), (0, 1), (0, 2)],  # Horizontal
                  [(0, 1), (0, 2), (0, 3)],
                  [(1, 0), (1, 1), (1, 2)],
                  [(1, 1), (1, 2), (1, 3)],
                  [(2, 0), (2, 1), (2, 2)],
                  [(2, 1), (2, 2), (2, 3)],
                  [(3, 0), (3, 1), (3, 2)],
                  [(3, 1), (3, 2), (3, 3)],
                  [(0, 0), (1, 0), (2, 0)],  # Vertical
                  [(1, 0), (2, 0), (3, 0)],
                  [(0, 1), (1, 1), (2, 1)],
                  [(1, 1), (2, 1), (3, 1)],
                  [(0, 2), (1, 2), (2, 2)],
                  [(1, 2), (2, 2), (3, 2)],
                  [(0, 3), (1, 3), (2, 3)],
                  [(1, 3), (2, 3), (3, 3)]]


    def __init__(self):
        self.moves = []
        self.gameover = False
        self.draw = False
        self.board = defaultdict(lambda: 0)


    def getPos(self):
        return [x for x in self.celltuples if x not in self.moves]


    def Move(self, position, symbol):
        if self.board[position] != 0:
            return False
        self.board[position] = symbol
        self.moves.append(position)
        self.checker()
        return True


    def remove(self):
        if len(self.moves) == 0:
            return False
        self.board[self.moves.pop()] = 0
        self.gameover = False
        return True

    def GameOver(self):
        return self.gameover

    def Draw(self):
        return self.draw

    # return winner of game
    def GetWinner(self):
        if self.GameOver() and not self.Draw():
            return self.winner


    def checker(self):
        for line in self.winningcon:
            coor1, coor2, coor3 = line
            if self.board[coor1] != 0 and \
                    self.board[coor1] == self.board[coor2] \
                    == self.board[coor3]:
                self.gameover = True
                self.winner = self.board[coor1]
                self.draw = False
                break
        else:
            if len(self.moves) == 16:
                self.draw = True
                self.gameover = True
            else:
                self.gameover = False


# Visual board class
class FrontBoard:
    gridcolor = (0, 0, 205)
    colorO = (255, 0, 255)
    colorX = MSB

    def __init__(self, boardsize=600):
        self.players = []
        self.boardsize = boardsize
        self.gameboard = BackEndBoard()
        self.font = pygame.font.SysFont('Stencil Futura', 50)


    def reset(self):
        self.gameboard = BackEndBoard()
        for player in self.players:
            player.disBoard(self.gameboard)
        self.player1, self.player2 = self.player2, self.player1


    def printstatus(self, screen):
        if board.gameboard.GameOver():
            if board.gameboard.Draw():
                displayText = "Draw!"
            else:
                displayText = self.player1.init + " Wins!"
        else:
            displayText = self.player1.init + "'s turn"
        text = self.font.render(displayText, 1, (0, 0, 205))
        textpos = text.get_rect(x = screen.get_width() / 3.5, y = self.boardsize - 12)
        screen.blit(text, textpos)

    # add players to self
    def player(self, player):
        player.disBoard(self.gameboard)
        self.players.append(player)
        if (len(self.players) > 1):
            self.player1 = self.players[0]
            self.player2 = self.players[1]


    def draw(self, win):
        border = 15

        pygame.draw.line(win, self.gridcolor, (self.boardsize / 4, border), (self.boardsize / 4, self.boardsize - border), 10)
        pygame.draw.line(win, self.gridcolor, ((2 * self.boardsize) / 4, border), ((2 * self.boardsize) / 4, self.boardsize - border), 10)
        pygame.draw.line(win, self.gridcolor, ((3 * self.boardsize) / 4, border), ((3 * self.boardsize) / 4, self.boardsize - border), 10)
        pygame.draw.line(win, self.gridcolor, (border, (self.boardsize) / 4), (self.boardsize - border, (self.boardsize) / 4), 10)
        pygame.draw.line(win, self.gridcolor, (border, (2 * self.boardsize) / 4), (self.boardsize - border, (2 * self.boardsize) / 4), 10)
        pygame.draw.line(win, self.gridcolor, (border, (3 * self.boardsize) / 4), (self.boardsize - border, (3 * self.boardsize) / 4), 10)

        for move in self.gameboard.moves:
            x1, y2 = move
            quarter = int(self.boardsize / 4)

            if self.gameboard.board[move] == symbolO:
                pos = x1 * quarter + int(quarter / 2), y2 * quarter + int(quarter / 2)
                pygame.draw.circle(win, self.colorO, pos, int(quarter / 4) + 10, 8)

            elif self.gameboard.board[move] == symbolX:
                board1 = x1 * quarter + int(quarter / 5), y2 * quarter + int(quarter / 5)
                board2 = (x1 + 1) * quarter - int(quarter / 5), y2 * quarter + int(quarter / 5)
                board3 = x1 * quarter + int(quarter / 5), (y2 + 1) * quarter - int(quarter / 5)
                board4 = (x1 + 1) * quarter - int(quarter / 5), (y2 + 1) * quarter - int(quarter / 5)
                pygame.draw.line(win, self.colorX, board1, board4, 10)
                pygame.draw.line(win, self.colorX, board2, board3, 10)


    def onClick(self, position):
        x, y = position  # x and y coordinates
        if y < self.boardsize:  # if on board
            quarter = int(self.boardsize / 4)
            x2 = int(math.floor(x / quarter))
            y2 = int(math.floor(y / quarter))
            cell = x2, y2
            self.player1.onClick(cell)
        elif self.gameboard.GameOver():
            self.reset()




    def update(self):
        if not self.gameboard.GameOver():
            nextpos = self.player1.GetMove()
            if nextpos is not None:

                self.gameboard.Move(nextpos, self.player1.symbol)
                if not self.gameboard.GameOver():

                    self.player1, self.player2 = self.player2, self.player1


# main function
if (__name__ == "__main__"):
    global level
    print("\nWelcome to TacTacToe!\n")
    print("Select your difficulty\n")
    print("1. Easy\n2. Medium\n3. Hard\n")
    level = input("Select your Choice: ").lower()
    move = int(input("Please select your turn (1,2): "))
    pygame.init()  # initialization required by module
    boardsize = 600  # board size
    # screen display
    win = pygame.display.set_mode((boardsize, boardsize + 35))
    bg = pygame.image.load("space2.jpeg")
    pygame.display.set_caption('Tic Tac Toe')
    gameover = False
    clock = pygame.time.Clock()  # clock for FPS
    board = FrontBoard()  # creation of board

    if level == "easy" or level == "Easy":
        if move == 1:
            board.player(humanMove(symbolO, "Player"))  # player 1
            board.player(computerMove(symbolX, "Agent", easy))  # player 2
        elif move == 2:
            board.player(computerMove(symbolX, "Agent", easy))  # player 1
            board.player(humanMove(symbolO, "Player"))  # player 2
    elif level == "medium" or level == "Medium":
        if move == 1:
            board.player(humanMove(symbolO, "Player"))  # player 1
            board.player(computerMove(symbolX, "Agent", medium))  # player 2
        elif move == 2:
            board.player(computerMove(symbolX, "Agent", medium))  # player 1
            board.player(humanMove(symbolO, "Player"))  # player 2
    elif level == "hard" or level == "Hard":
        if move == 1:
            board.player(humanMove(symbolO, "Player"))  # player 1
            board.player(computerMove(symbolX, "Agent", hard))  # player 2
        elif move == 2:
            board.player(computerMove(symbolX, "Agent", hard))  # player 1
            board.player(humanMove(symbolO, "Player"))  # player 2
    else:
        print("Default")
        if move == 1:
            board.player(humanMove(symbolO, "Player"))  # player 1
            board.player(computerMove(symbolX, "Agent"))  # player 2
        elif move == 2:
            board.player(computerMove(symbolX, "Agent"))  # player 1
            board.player(humanMove(symbolO, "Player"))  # player 2

    while not gameover:
        clock.tick(20)
        win.fill(white)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONUP:
                board.onClick(event.pos)  # mouse click event
                laser.play()
        win.blit(bg, (0,0))
        board.update()  # update game
        board.draw(win)  # update display
        board.printstatus(win)  # print prompt
        pygame.display.update()  # render display update
