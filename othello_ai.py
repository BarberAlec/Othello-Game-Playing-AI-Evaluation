from Othello import othello
import random

"""
Functions othello.ai provide:

    getCurrentScore(self, board): returns dict of 'X' and 'O' with scores.
    peekScore(self,board,x,y): returns score of board after taking given move.

    isValidMove(self, board, tile, xstart, ystart): returns bool for move legality.
    getLegalMoves(self, board, tile): reutrns list of legal moves.

    isOnCorner(self, x, y): returns True if is corner position.

Contact Alec if other funcitionality is required.
"""


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
        print(possibleMoves)
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
