"""
This is the file that all evaluations will take place, ideally we should
not have to access Othello.py again :)
"""
from Othello import othello
from othello_ai import human_ai, decisionRule_ai, minimax_ai, NN_ai

# Create new instance of othello game with spefied ai players
#game = othello(human_ai("X"), decisionRule_ai("O"))
#game = othello(human_ai("X"), human_ai("O"))
game = othello(decisionRule_ai("X"), decisionRule_ai("O"))

# Begin game
score = game.startgame()
