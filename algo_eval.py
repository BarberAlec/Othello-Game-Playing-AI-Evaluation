"""
This is the file that all evaluations will take place, ideally we should
not have to access Othello.py again :)
"""
from Othello import othello
from othello_ai import human_ai, decisionRule_ai, NN_ai
from Othello_Evaluation import othello_eval
from ab_pruning_ohtello import minimax_ai

# Create new instance of othello game with spefied ai players
# game = othello(human_ai("X"), decisionRule_ai("O"))
# game = othello(human_ai("X"), human_ai("O"))
# game = othello(human_ai(1), decisionRule_ai(-1))

# Begin game
# score = game.startgame(start_move=5)

evaluation = othello_eval(minimax_ai(1), decisionRule_ai(-1), runs=1000)
evaluation.gameStartEval()
evaluation.plotGameStartResults()
