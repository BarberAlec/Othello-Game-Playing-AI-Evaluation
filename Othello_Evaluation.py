from Othello import othello
import numpy as np
import matplotlib.pyplot as plt
from progress.bar import Bar


class othello_eval:
    def __init__(self, bot1, bot2, runs=50):
        self.MC_runs = runs
        self.gameStartEvalResult = 0
        self.bot1 = bot1
        self.bot2 = bot2

    def gameStartEval(self):
        start_list = np.arange(0, 10)
        results = np.zeros(len(start_list))

        for j, start in enumerate(start_list):
            bar_MC = Bar("MC run " + str(j), max=self.MC_runs)
            for i in range(self.MC_runs):
                bar_MC.next()
                game = othello(bot1=self.bot1, bot2=self.bot2, verbose=False)
                score = game.startgame(start_move=start)
                results[j] = results[j] + int(score["1"] > score["-1"])
            results[j] = results[j] / self.MC_runs
            bar_MC.finish()
        self.gameStartEvalResult = results

    def plotGameStartResults(self):
        plt.plot(np.arange(0, 10), self.gameStartEvalResult)
        plt.ylim((0, 1))
        plt.title(
            self.bot1.name
            + " vs "
            + self.bot2.name
            + " : Effect of game start time to performance"
        )
        plt.xlabel("Number of Random turns before game begins")
        plt.ylabel("Proportion of " + self.bot1.name + " wins")
        plt.show()

