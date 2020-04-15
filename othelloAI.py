import random
import torch
import fastai
import PIL
import copy
import numpy as np
from fastai.vision import *
import matplotlib.pyplot as plt
from othelloGame import othello



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
        self.name = "Human"
        self.marker = marker
        self.search_mode = 'Human'
        self.depth = 0

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
        self.name = "Greedy"
        self.marker = marker
        self.search_mode = 'Greedy'
        self.depth = 0

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

class NN_ai(othello.ai):
    def __init__(self, marker):
        self.name = "NN"
        if marker != -1 and marker != +1:
            print('ERROR: please pass a marker as either +1 or -1.')
            return -1
        self.marker = marker
        self.learn = load_learner("", "CNN_research/trained_othello_CNN.pkl")
        self.learn.model.float()
        self.greedy = decisionRule_ai(marker)
        self.search_mode = 'NN'
        self.depth = 0

    def getMove(self, board):
        player1_mat = np.where(board == self.marker, 1, 0)
        player2_mat = np.where(board == ((-1) * self.marker), 1, 0)
        empty_mat = np.zeros((8, 8))
        mat_3 = np.dstack((player1_mat, player2_mat, empty_mat))
        mat_img = PIL.Image.fromarray((mat_3).astype(np.uint8))
        mat_tensor = pil2tensor(mat_img, np.float32)
        mat_Image = Image(mat_tensor)

        move = self.learn.predict(mat_Image)
        move_string = str(move[0])
        x = int(move_string[0])
        y = int(move_string[2])
        move_output = [x, y]

        if not self.isValidMove(board, self.marker, x, y):
            # If not a valid move, then use greedy algo
            
            # This error print happens too often....
            #print("ERROR!")
            move_output = self.greedy.getMove(board)

        #print("NN move: ", str(move_output[0]), ",", str(move_output[1]))
        return move_output


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


    # Args # 
    marker:  1 or -1
    depth: depth of search tree
    search_mode: minimax/ab/scout
"""



class minimax_ai(othello.ai):
    def __init__(self, marker, depth,search_mode="Scout",heur='Weight_Matrix'):
        self.name = "minimax"
        self.marker = marker
        self.next_state_mn = []
        self.next_mn_move = 0
        self.depth = depth if depth>=1 else 1
        self.printing = False
        self.nodesVistited = 0
        self.search_mode = search_mode

        self.heur_name = heur
        self.heur_val = self.heur_switcher(heur)
        self.WEIGHTS = np.array([[4, -3, 2, 2, 2, 2, -3, 4, ],
                        [-3, -4, -1, -1, -1, -1, -4, -3, ],
                        [2, -1, 1, 0, 0, 1, -1, 2, ],
                        [2, -1, 0, 1, 1, 0, -1, 2, ],
                        [2, -1, 0, 1, 1, 0, -1, 2, ],
                        [2, -1, 1, 0, 0, 1, -1, 2, ],
                        [-3, -4, -1, -1, -1, -1, -4, -3, ],
                        [4, -3, 2, 2, 2, 2, -3, 4]])
        
        self.WEIGHTS_2 = np.array([[20, -3, 11, 8, 8, 11, -3, 20],
                        [-3, -7, -4, 1, 1, -4, -7, -3],
                        [11, -4, 2, 2, 2, 2, -4, 11],
                        [8, 1, 2, -3, -3, 2, 1, 8],
                        [8, 1, 2, -3, -3, 2, 1, 8],
                        [11, -4, 2, 2, 2, 2, -4, 11],
                        [-3, -7, -4, 1, 1, -4, -7, -3],
                        [20, -3, 11, 8, 8, 11, -3, 20]])
        
    def heur_switcher(self,arg):
        switcher = {
        'All': self.heur_all,
        'Coin_Party': self.heur_coinparty,
        'Stability': self.heur_stability,
        'Frontier_Discs': self.heur_frontier_discs,
        'Weight_Matrix': self.heur_cornerweight,
        'Corner_Closeness': self.heur_corner_closeness,
        'Corner': self.heur_corner,
        'Mobility': self.heur_mobility,
        }
        return switcher.get(arg,self.heur_all)
        

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

    def get_ordered_children_states(self, current_board_state, color):
        valid_moves = self.getLegalMoves(current_board_state, color)
        children = []
        res_children = []
        for move in valid_moves:
            new_board = self.createChildBoardState(current_board_state, move[0], move[1], color)
            children.append((new_board,self.heur_val(new_board)))
            
        sortedNodes = sorted(children, key = lambda node: node[1], reverse = True if color==self.marker else False)
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
            self.nodesVistited+=1
            return self.heur_val(current_board_state)
        if maximizingPlayer:
            maxEval = float('-inf')
            for child in self.get_children_states(current_board_state, True):
                self.nodesVistited+=1
                eval = self.alpha_beta_minmax(child[0], depth-1, False, alpha, beta)
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return maxEval
        else:
            minEval = float('inf')
            for child in self.get_children_states(current_board_state, False):
                self.nodesVistited+=1
                eval = self.alpha_beta_minmax(child[0], depth-1, True, alpha, beta)
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return minEval

    def minimax(self, current_board_state, depth, maximizingPlayer):
        if depth == 0 or self.game_finished(current_board_state):
            self.nodesVistited+=1
            return self.heur_val(current_board_state)
        if maximizingPlayer:
            maxEval = float('-inf')
            for child in self.get_children_states(current_board_state, True):
                self.nodesVistited+=1
                eval = self.minimax(child[0], depth-1, False)
                maxEval = max(maxEval, eval)
            return maxEval
        else:
            minEval = float('inf')
            for child in self.get_children_states(current_board_state, False):
                self.nodesVistited+=1
                eval = self.minimax(child[0], depth-1, True)
                minEval = min(minEval, eval)
            return minEval
        
    def nega_scout(self,current_board_state,depth,alpha,beta,color):
        if depth == 0 or self.game_finished(current_board_state):
            self.nodesVistited+=1
            return color*self.heur_val(current_board_state)
        
        firstChild = True
        for child in self.get_ordered_children_states(current_board_state,color):
            self.nodesVistited+=1
            if firstChild:
                firstChild = False
                score = -self.nega_scout(child,depth-1,-beta,-alpha,-color)
            else:
                score = -self.nega_scout(child,depth-1,-alpha-1,-alpha,-color)
                if alpha < score and score < beta:
                    score = -self.nega_scout(child,depth-1,-beta,-score,-color)
            alpha = max(alpha,score)
            if alpha >= beta:
                break
        return alpha

    def ng(self,current_board_state,depth,alpha,beta,color):
        if depth == 0 or self.game_finished(current_board_state):
            self.nodesVistited+=1
            return self.heur_val(current_board_state)
        
        score = float('-inf')
        n = beta
        for child in self.get_ordered_children_states(current_board_state,color):
            self.nodesVistited+=1
            cur = -self.ng(child,depth-1,-n,-alpha,-color)
            if(cur>score):
                if(n==beta or depth<=2):
                    score = cur
                else:
                    self.nodesVistited+=1
                    score = -self.ng(child,depth-1,-beta,-cur,-color)
            if(score>alpha):
                alpha = score
            if(alpha>=beta):
                return alpha
            n = alpha+1
        return score



 
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
        return (p1-p2)
    
    def heur_corner_closeness(self, board):
        close_corners = [(0,1),(1,0),(0,6),(1,7),(7,1),(6,0),(6,7),(7,6)]
        p1 = p2 = 0
        for x,y in close_corners:
            if board[x][y] == self.marker:
                p1+=1
            elif board[x][y] == -self.marker:
                p2+=1
        return -12.5*(p1-p2)

    # Static Heuristic strategy - Corners important, once captured can not be flanked by opponent, providing stability
    def heur_cornerweight(self, board):
        p1_total = 0
        p2_total = 0
        total = 0
        for x in range(8):
            for y in range(8):
                if board[x][y] == self.marker:
                    total += self.WEIGHTS_2[x,y]
                elif board[x][y] == -self.marker:
                    total -= self.WEIGHTS_2[x,y]
        if self.printing: print("Weight: ",total)
        return total
    
    def heur_frontier_discs(self,board):
        p1_total = p2_total = 0
        x1 = [-1, -1, 0, 1, 1, 1, 0, -1]
        y1 = [0, 1, 1, 1, 0, -1, -1, -1]
        empty = np.where(board == 0)
        for tile in empty:
            for k in range(8):
                try:
                    x = tile[0] + x1[k]
                    y = tile[1] + y1[k]
                    if 0<=x and x<8 and 0<=y and y<8:
                        if board[x][y] == self.marker: p1_total+=1
                        elif board[x][y] == -self.marker: p2_total+=1
                except:
                    break
        if p1_total > p2_total:
            return -100*p1_total/(p1_total+p2_total)
        elif p1_total < p2_total:
            return 100*p2_total/(p1_total+p2_total)
        else:
            return 0

    # Quantitaive representation of how vilnerable it is to being flanked. semi-/un-/stable/
    # Stable (1) - Can't be flanked in very next move
    # Semi (0) - Potentially be flanked in future, not immediately
    # Un (-1) - Can be flanked at very next move ---NOT COMPLETED----
    def heur_stability(self,board):
        children = self.get_children_states(board, False)
        sum1 = 0
        me = len(np.where(board == self.marker)[0])
        for child in children:
            me = len(np.where(board == self.marker)[0])
            diff = board - child[0]
            switch1 = len(np.where(diff == self.marker*2)[0])
            sum1-=switch1
            sum1+=me
        return sum1


    # Weights from paper -  "Playing Othello with Artificial Intelligence" (http://mkorman.org/othello.pdf)
    def heur_all(self,board):
        score = (801.724*self.heur_corner(board) 
        + 382.026*self.heur_corner_closeness(board) 
        + 78.922*self.heur_mobility(board) 
        + 10*self.heur_coinparty(board)
        + 10*self.heur_cornerweight(board) 
        + 74.396*self.heur_frontier_discs(board))
        + 100*self.heur_stability(board)
        return score
    
    def best_move(self,board):
        max_Eval = float('-inf')
        new_move = self.getLegalMoves(board, self.marker)[0]
        new_board = board
        # Go through valid moves' trees. Choose Max Evaluation Move.
        for child in self.get_children_states(board, True):
            self.nodesVistited+=1
            if self.search_mode == "MiniMax":
                eval = self.minimax(child[0], self.depth-1, False)
            elif self.search_mode == "Scout":
                eval = -self.nega_scout(child[0], self.depth-1,float('-inf'),float('inf'), -self.marker)
            elif self.search_mode == "A-B Pruning":
                eval = self.alpha_beta_minmax(child[0], self.depth-1,False,float('-inf'),float('inf'))
            if eval > max_Eval:
                max_Eval = eval
                new_move = child[1]
                new_board = child[0]
        
        # print ("Nodes Visited: ",self.nodesVistited)
        return new_move,new_board
