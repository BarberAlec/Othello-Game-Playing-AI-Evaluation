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
    def __init__(self, marker):
        self.name = "minimax"
        self.marker = marker
        self.next_state_mn = []
        self.next_mn_move = 0
        self.depth = 2

        self.WEIGHTS = [[4, -3, 2, 2, 2, 2, -3, 4,],
          [ -3, -4, -1, -1, -1, -1, -4, -3,],
          [ 2, -1, 1, 0, 0, 1, -1, 2,],
          [ 2, -1, 0, 1, 1, 0, -1, 2,],
         [  2, -1, 0, 1, 1, 0, -1, 2,],
         [  2, -1, 1, 0, 0, 1, -1, 2,],
          [ -3, -4, -1, -1, -1, -1, -4, -3,],
          [ 4, -3, 2, 2, 2, 2, -3, 4]]

    def getMove(self, board):
        #print("Im player: ",self.marker+2)
        self.cornerweight(board)
        self.get_cost(board)
        next_move = self.getLegalMoves(board, self.marker)

        #Run MiniMax 
        # new_eval = self.minimax(board,self.depth,True)

        #Run Alpha Beta MiniMax
        new_eval_ab = self.alpha_beta_minmax(board,self.depth,True,float('-inf'),float('inf'))

        # print("----")
        # print("Eval: ",new_eval_ab)
        # print("Move: (adj.) ",self.next_mn_move[0]+1,",",self.next_mn_move[1]+1)
        # print("Min_max Predicted Next State")
        # print(self.draw_child_board(self.next_state_mn))
        # print("----")
        return self.next_mn_move

    def cornerweight(self,board):
        positions = np.where(board == self.marker)
        total = 0
        for x in range(8):
            for y in range(8):
                if board[x][y] == self.marker :
                    total+=self.WEIGHTS[x][y]
                elif board[x][y] == -self.marker :
                    total-=self.WEIGHTS[x][y]
        # print("CornerWeight:",total)
        return total

    def draw_child_board(self,board):
        #print("----------------CHILD-------------------")
        othello.drawBoard(self,board)
        self.cornerweight(board)
        #print("----------------END CHILD-------------------")

    def get_cost(self,board):
        p1_pieces = np.where(board == self.marker)
        empty = np.where(board == 0)
        p2_pieces = 64 - len(p1_pieces[0]) - len(empty[0])      
        cost = len(p1_pieces[0]) - p2_pieces

        # print("Empty pieces: ",len(empty[0]))
        # print("My pieces: ",len(p1_pieces[0]))
        # print("Opponent pieces: ",p2_pieces)
        # print("Cost: ",cost)

        return cost

    def get_children_state(self,current_board_state,maximizingPlayer):
        child_marker = self.marker if maximizingPlayer else -self.marker
        valid_moves = self.getLegalMoves(current_board_state,child_marker)
        children = []
        for move in valid_moves:
            new_board = self.createChildBoardState(current_board_state,move[0],move[1],child_marker)
            children.append((new_board,move))
        return children

    def game_finished(self,board):
        if 0 in board :
            return False
        else :
            return True

    def alpha_beta_minmax(self,current_board_state, depth,maximizingPlayer,alpha,beta):
        if depth == 0 or self.game_finished(current_board_state):
            return self.cornerweight(current_board_state)
        if maximizingPlayer:
            maxEval = float('-inf')
            for child in self.get_children_state(current_board_state,True):
                eval = self.alpha_beta_minmax(child[0],depth-1,False,alpha,beta)
                maxEval = max(maxEval,eval)
                alpha = max(alpha,eval)
                if beta <= alpha:
                    break
                if maxEval == eval:
                    self.next_state_mn = copy.deepcopy(child[0])
                    self.next_mn_move = child[1]
            return maxEval 
        else:
            minEval = float('inf')
            for child in self.get_children_state(current_board_state,False):
                eval = self.alpha_beta_minmax(child[0],depth-1,True,alpha,beta)
                minEval = min(minEval,eval)   
                beta = min(beta,eval) 
                if beta <= alpha:
                    break
            return minEval     

    def minimax(self,current_board_state, depth, maximizingPlayer):
        if depth == 0 or self.game_finished(current_board_state):
            return self.cornerweight(current_board_state)
        if maximizingPlayer:
            maxEval = float('-inf')
            for child in self.get_children_state(current_board_state,True):
                eval = self.minimax(child[0],depth-1,False)
                maxEval = max(maxEval,eval)
                if maxEval == eval:
                    self.next_state_mn = copy.deepcopy(child[0])
                    self.next_mn_move = child[1]
            return maxEval 
        else:
            minEval = float('inf')
            for child in self.get_children_state(current_board_state,False):
                eval = self.minimax(child[0],depth-1,True)
                minEval = min(minEval,eval)
            return minEval 







if __name__ == '__main__':
    # plt.imshow(WEIGHTS, cmap='hot', interpolation='nearest')
    # plt.show()

    # Create new instance of othello game with spefied ai players
    game = othello(minimax_ai(1), human_ai(-1))

    # Begin game
    score = game.startgame()


