from Othello import othello
import random
import numpy as np
from pathlib import Path

numpy_save_path = Path('/users/ugrad/pretoriw/Documents/5th_Year/AI/numpy_boards_moves')

"""
Functions othello.ai provide:

    getCurrentScore(self, board): returns dict of 'X' and 'O' with scores.
    peekScore(self,board,x,y): returns score of board after taking given move.

    isValidMove(self, board, tile, xstart, ystart): returns bool for move legality.
    getLegalMoves(self, board, tile): reutrns list of legal moves.

    isOnCorner(self, x, y): returns True if is corner position.

Contact Alec if other funcitionality is required.
"""


class stringPlayer(othello.ai):
    def __init__(self, marker):
        self.name = "stringPlayer"
        self.marker = marker

    def getMove(self, board, count, game_string, game_name):
        # Get the move for this board layout
        # print(self.marker)
        if count == len(game_string):
            # print('Am in quit place bois')
            move = "quit"
            return move
        # print("getmovve counter:",count)
        move = game_string[count]

        if (count%2 == 1):
            board_copy = board * -1
        else:
            board_copy = board

        # Get the player position matrices
        player1_mat = np.where(board_copy == self.marker, 1, 0)
        player2_mat = np.where(board_copy == ((-1)*self.marker), 1, 0)

        # Concatenate the matrices
        mat_3d = np.dstack((player1_mat, player2_mat))

        # Get the x and y components
        x = str(int(move[0]))
        y = str(int(move[1]))

        # Define the file name and path
        name = x + y + '_' + game_name[:-4] + '.npy'
        save_path = numpy_save_path / name

        # Save the 3D numpy matrix
        np.save(save_path, mat_3d)

        return [int(move[0]), int(move[1])]

class human_ai(othello.ai):
    def __init__(self, marker):
        self.name = "human"
        self.marker = marker

    def getMove(self, board):
        DIGITS1TO8 = "1 2 3 4 5 6 7 8".split()
        while True:
            print("Enter your move, or quit")
            move = input().lower()
            if move == "quit":
                return "quit"
            if len(move) == 2 and move[0] in DIGITS1TO8 and move[1] in DIGITS1TO8:
                x = int(move[0]) - 1
                y = int(move[1]) - 1
                if self.isValidMove(board, self.marker, x, y) == False:
                    continue
                else:
                    break
            else:
                print(
                    "That is not a valid move. Type the x digit (1-8), then the y digit (1-8)."
                )
                print("For example, 81 will be the top-right corner.")
        return [x, y]


class decisionRule_ai(othello.ai):
    def __init__(self, marker):
        self.name = "decison_rule"
        self.marker = marker

    def getMove(self, board):
        possibleMoves = self.getLegalMoves(board, self.marker)
        # randomize possible moves
        random.shuffle(possibleMoves)

        # Corners are opimial always
        for x, y in possibleMoves:
            if self.isOnCorner(x, y):
                return [x, y]

        # Go through all the possible moves and remember the best scoring move
        bestScore = -1
        for x, y in possibleMoves:
            score = self.peekScore(board, x, y)
            if score > bestScore:
                bestMove = [x, y]
                bestScore = score
        return bestMove


class minimax_ai(othello.ai):
    def __init__(self, marker):
        self.name = "minimax"

    def getMove(self, board):
        x = 0
        y = 0
        return [x, y]


class NN_ai(othello.ai):
    def __init__(self, marker):
        self.name = "NN"
        self.marker = marker

    def getMove(self, board):
        x = 0
        y = 0
        return [x, y]
