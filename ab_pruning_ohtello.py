import matplotlib.pyplot as plt
import numpy as np
from Othello import othello
from othello_ai import human_ai, decisionRule_ai, minimax_ai, NN_ai


"""
Heuristic based off of paper - "An Analysis of Heuristic in Othello” - https://courses.cs.washington.edu/courses/cse573/04au/Project/mini1/RUSSIA/Final_Paper.pdf
Dont consider time as a requirement, winning proportional to depth of tree.
Greedy Algorithm and Corner Strategy
Score - addition of weights of player position on board with weights
"""

"""
Accessible Functions for Othello Board
    getCurrentScore(self, board): returns dict of 'X' and 'O' with scores.
    peekScore(self,board,x,y): returns score of board after taking given move.
    isValidMove(self, board, tile, xstart, ystart): returns bool for move legality.
    getLegalMoves(self, board, tile): reutrns list of legal moves.
    isOnCorner(self, x, y): returns True if is corner position.
"""

class minimax_ai(othello.ai):
    def __init__(self, marker):
        self.name = "minimax"
        self.marker = marker

    def getMove(self, board):
        x = 0
        y = 0
        self.cornerweight(board)
        return self.getLegalMoves(board, self.marker)[0]

    def cornerweight(self,board):
        positions = np.where(board == self.marker)
        total = 0
        for p in range(len(positions[0])):
            x = positions[0][p]
            y = positions[1][p]
            total += WEIGHTS[x+1][y+1]
            print(x,y)
        return total
            

            


# Weight Heatmap - corner strategy weights
WEIGHTS = [[4, -3, 2, 2, 2, 2, -3, 4,],
          [ -3, -4, -1, -1, -1, -1, -4, -3,],
          [ 2, -1, 1, 0, 0, 1, -1, 2,],
          [ 2, -1, 0, 1, 1, 0, -1, 2,],
         [  2, -1, 0, 1, 1, 0, -1, 2,],
         [  2, -1, 1, 0, 0, 1, -1, 2,],
          [ -3, -4, -1, -1, -1, -1, -4, -3,],
          [ 4, -3, 2, 2, 2, 2, -3, 4]]



# plt.imshow(WEIGHTS, cmap='hot', interpolation='nearest')
# plt.show()

# Create new instance of othello game with spefied ai players
game = othello(minimax_ai("X"), human_ai("O"))

# Begin game
score = game.startgame()


