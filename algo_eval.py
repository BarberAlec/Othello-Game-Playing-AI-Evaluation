"""
This is the file that all evaluations will take place, ideally we should
not have to access Othello.py again :)
"""
from Othello import othello
from othello_ai import human_ai, decisionRule_ai
from NN_ai import NN_ai
from Othello_Evaluation import othello_eval
from ab_pruning_ohtello import minimax_ai
import numpy as np

# Create new instance of othello game with spefied ai players
# game = othello(human_ai("X"), decisionRule_ai("O"))
# game = othello(human_ai("X"), human_ai("O"))
# game = othello(human_ai(1), decisionRule_ai(-1))

# game = othello(NN_ai(1), decisionRule_ai(-1))
# #game = othello(human_ai(1), human_ai(-1))
# score = game.startgame(start_move=0)

# Begin game
# score = game.startgame(start_move=5)


# Make sure search algs are always bot 1, because we need to reset the nodesVisited to 0 after every game. 
search_modes = ["minimax","ab","scout"]


for mode in range(3):
    for d in range(1,2): # Depths
        print("Running ", search_modes[mode]," with a depth of ",d)
        evaluation = othello_eval(minimax_ai(1,depth=d,search_mode=search_modes[mode]), decisionRule_ai(-1), runs=2)
        evaluation.gameStartEval(values2test=(np.arange(0,3)))
        evaluation.plotGameStartResults()


evaluation = othello_eval(NN_ai(1), decisionRule_ai(-1), runs=500)
evaluation.gameStartEval(values2test=(np.arange(0,20)))
evaluation.plotGameStartResults()


# evaluation = othello_eval(minimax_ai(1,depth=2,search_mode='ab'), decisionRule_ai(-1), runs=20,True)
# evaluation.gameStartEval(values2test=(np.arange(0,3)))
# evaluation.plotGameStartResults()

#For Every Run game it will save the png and a 2d array of the nodesvisited


