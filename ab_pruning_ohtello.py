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
        
        self.WEIGHTS_2 = [[20, -3, 11, 8, 8, 11, -3, 20],
                        [-3, -7, -4, 1, 1, -4, -7, -3],
                        [11, -4, 2, 2, 2, 2, -4, 11],
                        [8, 1, 2, -3, -3, 2, 1, 8],
                        [8, 1, 2, -3, -3, 2, 1, 8],
                        [11, -4, 2, 2, 2, 2, -4, 11],
                        [-3, -7, -4, 1, 1, -4, -7, -3],
                        [20, -3, 11, 8, 8, 11, -3, 20]]

    def getMove(self, board):
        if self.printing:
            print("Im player: ", self.marker+2)


        # Run MiniMax
        # new_eval_ab = self.minimax(board, self.depth, True)
        next_move,next_board = self.best_move(board)

        # Run Alpha Beta MiniMax
        # new_eval_ab = self.alpha_beta_minmax(board,self.depth,True,float('-inf'),float('inf'))

        if self.printing:
            print("----")
            print("Move: ", next_move)
            print("Valid Moves Options: ",self.getLegalMoves(board, self.marker))
            print("Move: (adj.) ",
                  next_move[0]+1, ",", next_move[1]+1)
            print(self.draw_child_board(next_board, next_move))
            print("----")

        return next_move


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

    def get_ordered_children_states(self, current_board_state, maximizingPlayer):
        child_marker = self.marker if maximizingPlayer else -self.marker
        valid_moves = self.getLegalMoves(current_board_state, child_marker)
        children = []
        res_children = []
        for move in valid_moves:
            new_board = self.createChildBoardState(current_board_state, move[0], move[1], child_marker)
            children.append((new_board,self.heur_val(new_board)))
            
        sortedNodes = sorted(children, key = lambda node: node[1], reverse = True)
        sortedNodes = [node[0] for node in sortedNodes]
        for node in sortedNodes:
            res_children.append(node)
        return res_children

    def game_finished(self, board):
        if 0 in board:
            return False
        else:
            return True

    def alpha_beta_minmax(self, current_board_state, depth, maximizingPlayer, alpha, beta):
        if depth == 0 or self.game_finished(current_board_state):
            return self.heur_val(current_board_state)
        if maximizingPlayer:
            maxEval = float('-inf')
            for child in self.get_children_states(current_board_state, True):
                eval = self.alpha_beta_minmax(child[0], depth-1, False, alpha, beta)
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return maxEval
        else:
            minEval = float('inf')
            for child in self.get_children_states(current_board_state, False):
                eval = self.alpha_beta_minmax(child[0], depth-1, True, alpha, beta)
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return minEval

    def minimax(self, current_board_state, depth, maximizingPlayer):
        if depth == 0 or self.game_finished(current_board_state):
            return self.heur_val(current_board_state)
        if maximizingPlayer:
            maxEval = float('-inf')
            for child in self.get_children_states(current_board_state, True):
                eval = self.minimax(child[0], depth-1, False)
                maxEval = max(maxEval, eval)
            return maxEval
        else:
            minEval = float('inf')
            for child in self.get_children_states(current_board_state, False):
                eval = self.minimax(child[0], depth-1, True)
                minEval = min(minEval, eval)
            return minEval
        
    def nega_scout(self,current_board_state,depth,alpha,beta,color,maximizingPlayer):
        if depth == 0 or self.game_finished(current_board_state):
            return color*self.heur_val(current_board_state)
        
        fristChild = True
        for child in self.get_ordered_children_states(current_board_state, not maximizingPlayer):
            if not fristChild:
                score = -self.nega_scout(child,depth-1,-alpha-1,-alpha,-color,not maximizingPlayer)
                if alpha < score and score < beta:
                    score = -self.nega_scout(child,depth-1,-beta,-score,-color, not maximizingPlayer)
            else:
                fristChild = False
                score = -self.nega_scout(child,depth-1,-beta,-alpha,-color, not maximizingPlayer)
            alpha = max(alpha,score)
            if alpha >= beta:
                break
        return alpha
 
    def p1_p2_perc(self,p1,p2):
        if ((p1 !=0) and (p2 !=0 )) :
            return (100*(p1-p2))/(p1+p2)
        else: return 0


    #-----Different Heuristics defined by heur_-----

    # Coin Party - Difference between max player and min player
    def heur_coinparty(self,board):
        p1_pieces = len(np.where(board == self.marker)[0])
        p2_pieces = len(np.where(board == -self.marker)[0])
        if p1_pieces > p2_pieces:
            return 100*((p1_pieces)/(p1_pieces + p2_pieces))
        elif p1_pieces < p2_pieces:
            return -100*((p2_pieces)/(p1_pieces + p2_pieces))
        else:
            return 0

    # Acutal Mobility - Capture relative difference between number of possible moves for max and min players, restrict opponents mobility and increasing own
    def heur_mobility(self, board):
        try :
            p1_moves = len(self.getLegalMoves(board,self.marker)[0])
            p2_moves = len(self.getLegalMoves(board,-self.marker)[0])
            if p1_moves > p2_moves:
                m = 100*(p1_moves/(p1_moves+p2_moves))
            elif p2_moves > p1_moves:
                m = -100*(p2_moves/(p1_moves+p2_moves))
            else:
                m = 0
        except:
            m = 0
        return m
    
    # Corner - Strategy Corners important, once captured can not be flanked by opponent, providing stability
    def heur_corner(self, board):
        corners = [(0,0),(0,7),(7,7),(7,0)]
        p1 = p2 = 0
        for x,y in corners:
            if board[x][y] == self.marker:
                p1+=1
            elif board[x][y] == -self.marker:
                p2+=1
        return 25*(p1-p2)
    
    def heur_corner_closeness(self, board):
        close_corners = [(0,1),(1,0),(0,6),(1,7),(7,1),(6,0),(6,7),(7,6)]
        p1 = p2 = 0
        for x,y in close_corners:
            if board[x][y] == self.marker:
                p1+=1
            elif board[x][y] == -self.marker:
                p2+=1
        return -12.5*(p1-p2)

    # Corner strategy - Corners important, once captured can not be flanked by opponent, providing stability
    def heur_cornerweight(self, board):
        p1_total = 0
        p2_total = 0
        total = 0
        for x in range(8):
            for y in range(8):
                if board[x][y] == self.marker:
                    total += self.WEIGHTS_2[x][y]
                elif board[x][y] == -self.marker:
                    total -= self.WEIGHTS_2[x][y]
        if self.printing: print("Weight: ",total)
        return total
    
    def heur_frontier_discs(self,board):
        p1_total = p2_total = 0
        x1 = [-1, -1, 0, 1, 1, 1, 0, -1]
        y1 = [0, 1, 1, 1, 0, -1, -1, -1]
        empty = np.where(board == 0)
        if len(empty[0])>0:
            for tile in empty:
                for k in range(8):
                    x = tile[0] + x1[k]
                    y = tile[1] + y1[k]
                    if 0<=x and x<8 and 0<=y and y<8:
                        if board[x][y] == self.marker: p1_total+=1
                        elif board[x][y] == -self.marker: p2_total+=1
                
        if p1_total > p2_total:
            return -100*p1_total/(p1_total+p2_total)
        elif p1_total < p2_total:
            return 100*p2_total/(p1_total+p2_total)
        else:
            return 0

    # Quantitaive representation of how vilnerable it is to being flanked. semi-/un-/stable/
    # Stable (1) - Can't be flanked in very next move
    # Semi (0) - Potentially be flanked in future, not immediately
    # Un (-1) - Can be flanked at very next move
    def heur_stability(self,board):
        p1_stable_val = 0
        p2_stable_val = 0
        for x in range(8):
            for y in range(8):
                if board[x][y] == self.marker:
                    p1_stable_val += 1
                elif board[x][y] == -self.marker:
                    p2_stable_val -= self.WEIGHTS[x][y]

        return self.p1_p2_perc(p1_stable_val,p2_stable_val)

    def heur_val(self,board):
        score = (801.724*self.heur_corner(board) 
        + 382.026*self.heur_corner_closeness(board) 
        + 78.922*self.heur_mobility(board) 
        + 10*self.heur_coinparty(board)
        + 10*self.heur_cornerweight(board) 
        + 74.396*self.heur_frontier_discs(board))
        
        return score
    
    def best_move(self,board):
        max_Eval = float('-inf')
        new_move = self.getLegalMoves(board, self.marker)[0]
        new_board = board
        # Go through valid moves' trees. Choose Max Evaluation Move.
        for child in self.get_children_states(board, True):
            eval = self.minimax(child[0], self.depth, False)
            # eval = self.nega_scout(child[0], self.depth,float('-inf'),float('inf'), 1,False)
            # eval = self.alpha_beta_minmax(child[0], self.depth,False,float('-inf'),float('inf'))
            if eval > max_Eval:
                max_Eval = eval
                new_move = child[1]
                new_board = child[0]
                
        return new_move,new_board


if __name__ == '__main__':
    
    # plt.imshow(WEIGHTS, cmap='hot', interpolation='nearest')
    # plt.savefig('WeightMatrix_2.png')

    # X is 1, O is -1
    # Create new instance of othello game with spefied ai players
    game = othello(minimax_ai(1), decisionRule_ai(-1))

    # Begin game
    score = game.startgame(2)
