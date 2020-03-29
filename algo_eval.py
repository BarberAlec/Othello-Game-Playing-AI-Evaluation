from Othello import othello
from othello_ai import human_ai, decisionRule_ai
from NN_ai import NN_ai
from Othello_Evaluation import othello_eval
from ab_pruning_ohtello import minimax_ai
import numpy as np


def single_game():
    # Example single with human player against greedy algo
    game = othello(human_ai(1), decisionRule_ai(-1))
    score = game.startgame(start_move=0)

    # Example single with Nearal Network against greedy algo
    # game = othello(NN_ai(1), decisionRule_ai(-1))
    # score = game.startgame(start_move=0)

    # Example game: two humans, board starts from a random
    # legal Board State after 5 moves
    # game = othello(human_ai(1), human_ai(-1))
    # score = game.startgame(start_move=5)


def adverserial_MC():
    # Make sure search algs are always bot 1,
    # because we need to reset the nodesVisited to 0 after every game.

    # For Every Run game it will save the png and a 2d array of the nodesvisited

    # Simulation Params
    search_modes = ["MiniMax", "A-B Pruning", "Scout"]
    debth_range = range(3, 4)
    op_cond_range = np.arange(0, 20, 3)
    mc_runs = 1000

    evaluation = othello_eval(
        minimax_ai(1, depth=2, search_mode="Scout"),
        decisionRule_ai(-1),
        runs=mc_runs,
        adverse=True,
    )
    evaluation.gameStartEval(values2test=(op_cond_range))
    evaluation.plotGameStartResults(draw=False)

    for mode in search_modes:
        for d in debth_range:
            print("Running ", mode, " with a depth of ", d)
            evaluation = othello_eval(
                minimax_ai(1, depth=d, search_mode=mode),
                decisionRule_ai(-1),
                runs=mc_runs,
                adverse=True,
            )
            evaluation.gameStartEval(values2test=(op_cond_range))
            evaluation.plotGameStartResults(draw=False)

    # evaluation = othello_eval(
    #     minimax_ai(1, depth=2, search_mode="ab"),
    #     decisionRule_ai(-1),
    #     runs=20,
    #     adverse=True,
    # )
    # evaluation.gameStartEval(values2test=(np.arange(0, 20,4)))
    # evaluation.plotGameStartResults()


def NearalNetwork_MC():
    evaluation = othello_eval(NN_ai(1), decisionRule_ai(-1), runs=10)
    evaluation.gameStartEval(values2test=(np.arange(0, 20, 2)))
    evaluation.plotGameStartResults()


def main():
    # single_game()

    adverserial_MC()

    # NearalNetwork_MC()


if __name__ == "__main__":
    main()
