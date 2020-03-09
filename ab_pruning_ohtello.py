import matplotlib.pyplot as plt
import numpy as np
from Othello import othello
from othello_ai import human_ai, decisionRule_ai, NN_ai
import copy

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
    def __init__(self, marker, set_depth=2):
        self.name = "minimax"
        self.marker = marker
        self.next_state_mn = []
        self.next_mn_move = 0
        self.depth = set_depth
        self.printing = False

        self.WEIGHTS = [[4, -3, 2, 2, 2, 2, -3, 4, ],
                        [-3, -4, -1, -1, -1, -1, -4, -3, ],
                        [2, -1, 1, 0, 0, 1, -1, 2, ],
                        [2, -1, 0, 1, 1, 0, -1, 2, ],
                        [2, -1, 0, 1, 1, 0, -1, 2, ],
                        [2, -1, 1, 0, 0, 1, -1, 2, ],
                        [-3, -4, -1, -1, -1, -1, -4, -3, ],
                        [4, -3, 2, 2, 2, 2, -3, 4]]

    def getMove(self, board):
        if self.printing:
            print("Im player: ", self.marker+2)

        next_move = self.getLegalMoves(board, self.marker)

        # Run MiniMax
        new_eval_ab = self.minimax(board, self.depth, True)

        # Run Alpha Beta MiniMax
        # new_eval_ab = self.alpha_beta_minmax(board,self.depth,True,float('-inf'),float('inf'))

        if self.printing:
            print("----")
            print("Eval: ", new_eval_ab)
            print("Valid Moves Options: ",self.getLegalMoves(board, self.marker))
            print("Move: (adj.) ",
                  self.next_mn_move[0]+1, ",", self.next_mn_move[1]+1)
            print("Min_max Predicted Next State")
            print(self.draw_child_board(self.next_state_mn, self.next_mn_move[0]))
            print("----")

        return self.next_mn_move


    def draw_child_board(self, board, move):
        print("----------------CHILD-------------------")
        print("Move: ", move)
        othello.drawBoard(self, board)
        print("----------------END CHILD-------------------")

    def get_children_states(self, current_board_state, maximizingPlayer):
        child_marker = self.marker if maximizingPlayer else -self.marker
        valid_moves = self.getLegalMoves(current_board_state, child_marker)
        children = []
        for move in valid_moves:
            new_board = self.createChildBoardState(
                current_board_state, move[0], move[1], child_marker)
            children.append((new_board, move))
        return children

    def game_finished(self, board):
        if 0 in board:
            return False
        else:
            return True

    def alpha_beta_minmax(self, current_board_state, depth, maximizingPlayer, alpha, beta):
        if depth == 0 or self.game_finished(current_board_state):
            return self.cornerweight(current_board_state,maximizingPlayer)
        if maximizingPlayer:
            maxEval = float('-inf')
            for child in self.get_children_states(current_board_state, True):
                if self.printing:
                    self.draw_child_board(child[0], child[1])
                eval = self.alpha_beta_minmax(
                    child[0], depth-1, False, alpha, beta)
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
                if maxEval == eval:
                    self.next_state_mn = copy.deepcopy(child[0])
                    self.next_mn_move = child[1]
            return maxEval
        else:
            minEval = float('inf')
            for child in self.get_children_states(current_board_state, False):
                if self.printing:
                    self.draw_child_board(child[0], child[1])
                eval = self.alpha_beta_minmax(
                    child[0], depth-1, True, alpha, beta)
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return minEval

    def minimax(self, current_board_state, depth, maximizingPlayer):
        if depth == 0 or self.game_finished(current_board_state):
            return self.cornerweight(current_board_state,maximizingPlayer)
        if maximizingPlayer:
            maxEval = float('-inf')
            for child in self.get_children_states(current_board_state, True):
                if self.printing:
                    self.draw_child_board(child[0], child[1])
                eval = self.minimax(child[0], depth-1, False)
                maxEval = max(maxEval, eval)
                if maxEval == eval:
                    self.next_state_mn = copy.deepcopy(child[0])
                    self.next_mn_move = child[1]
            return maxEval
        else:
            minEval = float('inf')
            for child in self.get_children_states(current_board_state, False):
                if self.printing:
                    self.draw_child_board(child[0], child[1])
                eval = self.minimax(child[0], depth-1, True)
                minEval = min(minEval, eval)
            return minEval

    #Different Heuristics defined by heur_*

    def cornerweight(self, board, maximizingPlayer):
        total = 0
        for x in range(8):
            for y in range(8):
                if board[x][y] == self.marker:
                    total += self.WEIGHTS[x][y]
                elif board[x][y] == -self.marker:
                    total -= self.WEIGHTS[x][y]
        if self.printing: print("CornerWeight: ", total)
        return total

    # Difference between max player and min player
    def heur_coinparty(self,board,marker):
        p1_pieces = len(np.where(board == marker)[0])
        p2_pieces = len(np.where(board == -marker)[0])

        return (p1_pieces - p2_pieces)

    # Capture relative difference between number of possible moves for max and min players, restrict opponents mobility and increasing own
    def heur_mobility(self, board):
        p1_pieces = len(np.where(board == self.marker)[0])
        p2_pieces = len(np.where(board == self.marker)[0])
        self.getLegalMoves
        if self.printing:
            print("Empty pieces: ", 64 - p1_pieces - p2_pieces)
            print("My pieces: ", p1_pieces)
            print("Opponent pieces: ", p2_pieces)
            print("Cost: ", p1_pieces - p2_pieces)

        return p1_pieces - p2_pieces



if __name__ == '__main__':
    # plt.imshow(WEIGHTS, cmap='hot', interpolation='nearest')
    # plt.show()

    # X is 1, O is -1
    # Create new instance of othello game with spefied ai players
    game = othello(minimax_ai(1), decisionRule_ai(-1))

    # Begin game
    score = game.startgame()
