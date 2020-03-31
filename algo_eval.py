from Othello import othello
from othello_ai import human_ai, decisionRule_ai
from NN_ai import NN_ai
from Othello_Evaluation import othello_eval
from ab_pruning_ohtello import minimax_ai
import numpy as np


def single_game():
    # Example single with human player against greedy algo
    search_modes = ["MiniMax", "A-B Pruning", "Scout"]
    game = othello(minimax_ai(1, depth=4, search_mode=search_modes[0]), decisionRule_ai(-1))
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
    heuristics = ['All','Coin_Party','Stability','Frontier_Discs','Weight_Matrix','Corner_Closeness','Corner','Mobility']
    debth_range = range(3, 4)
    op_cond_range = np.arange(0, 30)
    mc_runs = 100


    # evaluation = othello_eval(
    #     minimax_ai(1, depth=2, search_mode="A-B Pruning"),
    #     decisionRule_ai(-1),
    #     runs=mc_runs,
    #     adverse=True,
    # )
    # evaluation.gameStartEval(values2test=(op_cond_range))
    # evaluation.plotGameStartResults(draw=False)

    for f in range(len(heuristics)):
        for s in range(f,len(heuristics)):
            evaluation = othello_eval(
            minimax_ai(1, depth=1, search_mode="A-B Pruning",heur=heuristics[f]),
           minimax_ai(-1, depth=1, search_mode="A-B Pruning",heur=heuristics[s]),
            runs=mc_runs,
            adverse=True,
            )
            evaluation.gameStartEval(values2test=(op_cond_range))
            evaluation.plotGameStartResults(draw=False)

    # for mode in search_modes:
    #     for d in debth_range:
    #         print("Running ", mode, " with a depth of ", d)
    #         evaluation = othello_eval(
    #             minimax_ai(1, depth=d, search_mode=mode),
    #             decisionRule_ai(-1),
    #             runs=mc_runs,
    #             adverse=True,
    #         )
    #         evaluation.gameStartEval(values2test=(op_cond_range))
    #         evaluation.plotGameStartResults(draw=False)

    # evaluation = othello_eval(
    #     minimax_ai(1, depth=2, search_mode="ab"),
    #     decisionRule_ai(-1),
    #     runs=20,
    #     adverse=True,
    # )
    # evaluation.gameStartEval(values2test=(np.arange(0, 20,4)))
    # evaluation.plotGameStartResults()


def NearalNetwork_MC():
    op_cond_range = np.arange(0, 20, 3)
    mc_runs = 4000

    evaluation = othello_eval(NN_ai(1), decisionRule_ai(-1), runs=mc_runs)
    evaluation.gameStartEval(values2test=(op_cond_range))
    evaluation.plotGameStartResults()


def SingleModeEval_MC():
    # Temp Fucntion for testing one simulationat a time in a differnet process

    # Simulation Params
    search_modes = ["MiniMax", "A-B Pruning", "Scout"]
    debth_range = range(3, 4)
    op_cond_range = np.arange(0, 20, 3)
    mc_runs = 10

    evaluation = othello_eval(
        minimax_ai(1, depth=4, search_mode=search_modes[0]),
        decisionRule_ai(-1),
        runs=mc_runs,
        adverse=True,
    )
    evaluation.gameStartEval(values2test=(op_cond_range))
    evaluation.plotGameStartResults(draw=False)

def main():
    #single_game()

    adverserial_MC()

    # NearalNetwork_MC()

    # SingleModeEval_MC()

if __name__ == "__main__":
    main()


