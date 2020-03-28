from Othello import othello
import numpy as np
import matplotlib.pyplot as plt
from progress.bar import Bar
import pandas as pd
import threading as thr
import time


#TODO: Fix Threading

class othello_eval:
    def __init__(self, bot1, bot2, runs=8, adverse=False):
        self.MC_runs = runs
        self.gameStartEvalResult = 0
        self.gameStartEvalVar = 0
        self.gameStartEvalTestedVals = 0
        self.bot1 = bot1
        self.bot2 = bot2
        self.adverse = adverse

    def gameStartEval(self, values2test=np.arange(0, 10)):
        results = np.zeros((len(values2test), self.MC_runs))
        nodesVisitedArray = np.zeros((len(values2test), self.MC_runs))
        self.gameStartEvalTestedVals = values2test

        # thread_list = list()
        # function_results = [None] * len(values2test)
        MC_bar = Bar('Processing', max=len(values2test))
        # Start threads for each Simulation
        for j, start in enumerate(values2test):
            # time.sleep(0.2)
            # x = thr.Thread(target=self._one_data_MC_run_, args=(j,function_results,self.bot1, self.bot2, start,self.MC_runs))
            # thread_list.append(x)
            # x.start()
            results[j, :], nodesVisitedArray[j, :] = self._one_data_MC_run_no_thread_(self.bot1, self.bot2, start,self.MC_runs)
            MC_bar.next()
        # # End threads
        # for index, thread in enumerate(thread_list):
        #     thread.join()
        #     # process results
        #     results[index,:] = function_results[0][0]
        #     nodesVisitedArray[index,:] = function_results[0][1]
        
        MC_bar.finish()

        # Save nodes visited and Results
        if self.adverse:
            pd.DataFrame(nodesVisitedArray).to_csv(
                "./Search_Mode_Results/"
                + self.bot1.search_mode
                + "_depth"
                + str(self.bot1.depth)
                + "_nodesV.csv",
                header=None,
                index=None,
            )
            pd.DataFrame(results).to_csv(
                "./Search_Mode_Results/"
                + self.bot1.search_mode
                + "_depth"
                + str(self.bot1.depth)
                + "_wins.csv",
                header=None,
                index=None,
            )
        self.gameStartEvalResult = np.mean(results, axis=1)
        self.gameStartEvalVar = np.var(results, axis=1)

    def _one_data_MC_run_(self,name,results, bot1, bot2, start, runs):
        result = np.zeros((1, runs))
        nodesVisitedArray = np.zeros((1, runs))
        for i in range(self.MC_runs):
            game = othello(bot1=self.bot1, bot2=self.bot2, verbose=False)
            score = game.startgame(start_move=start)
            result[0,i] = int(score["1"] > score["-1"])

            # Store Nodes visited for search Alg and reset nodes
            if self.bot1.name == "minimax":
                nodesVisitedArray[0,i] = self.bot1.nodesVistited
            if self.bot1.name == "minimax":
                self.bot1.nodesVistited = 0

        results[name] = (result, nodesVisitedArray)

    def _one_data_MC_run_no_thread_(self, bot1, bot2, start, runs):
        result = np.zeros((1, runs))
        nodesVisitedArray = np.zeros((1, runs))
        for i in range(self.MC_runs):
            game = othello(bot1=self.bot1, bot2=self.bot2, verbose=False)
            score = game.startgame(start_move=start)
            result[0,i] = int(score["1"] > score["-1"])

            # Store Nodes visited for search Alg and reset nodes
            if self.bot1.name == "minimax":
                nodesVisitedArray[0,i] = self.bot1.nodesVistited
            if self.bot1.name == "minimax":
                self.bot1.nodesVistited = 0

        return  (result, nodesVisitedArray)

    def plotGameStartResults(self):
        plt.errorbar(
            self.gameStartEvalTestedVals,
            self.gameStartEvalResult,
            self.gameStartEvalVar,
            ls="none",
            fmt="-o",
            label=self.bot1.search_mode + "_" + str(self.bot1.depth),
        )
        plt.ylim((0, 1))
        plt.title(
            self.bot1.search_mode
            + " vs "
            + self.bot2.name
            + " : Effect of game start time to performance"
        )
        plt.xlabel("Number of Random turns before game begins")
        plt.ylabel("Proportion of " + self.bot1.search_mode + " wins")
        plt.legend()

        plt.savefig(
            "./Search_Mode_Results/depth_"
            + str(self.bot1.depth)
            + "_"
            + self.bot1.search_mode
            + ".png"
        )
        plt.show()
