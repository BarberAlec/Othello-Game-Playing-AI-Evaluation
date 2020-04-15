
import os
from pathlib import Path
from Othello import othello
from othello_ai import human_ai, decisionRule_ai, minimax_ai, NN_ai, stringPlayer
from progress.bar import Bar

path = Path('/users/ugrad/pretoriw/Documents/5th_Year/AI/string_games')
game_names = os.listdir('/users/ugrad/pretoriw/Documents/5th_Year/AI/string_games')

bar = Bar('Playing Games..', max=len(game_names))

for game_name in game_names:

    game = othello(game_name, stringPlayer(-1), stringPlayer(1))
    score = game.startgame(start_move=0)

    bar.next()

bar.finish()
print('Finished')
