import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt
import os
import pandas as pd


def plotAfterSimulation(depth=2):
    line_size = 2
    marker_size = 12
    error_bars = False
    if depth==2:
        minimax_data = np.genfromtxt(
            "./Search_Mode_Results/MiniMax_depth2_wins.csv", delimiter=","
        )
        ab_prun_data = np.genfromtxt(
            "./Search_Mode_Results/A-B Pruning_depth2_wins.csv", delimiter=","
        )
        scout_data = np.genfromtxt(
            "./Search_Mode_Results/Scout_depth2_wins.csv", delimiter=","
        )
    else:
        minimax_data = np.genfromtxt(
            "./Search_Mode_Results/MiniMax_depth3_wins.csv", delimiter=","
        )
        ab_prun_data = np.genfromtxt(
            "./Search_Mode_Results/A-B Pruning_depth3_wins.csv", delimiter=","
        )
    NN_data = np.genfromtxt(
        "./Search_Mode_Results/NN_wins.csv", delimiter=","
    )

    minimax_plot_y = np.mean(minimax_data, axis=1)
    minimax_plot_var = np.var(minimax_data, axis=1)
    ab_prun_plot_y = np.mean(ab_prun_data, axis=1)
    ab_prun_plot_var = np.var(ab_prun_data, axis=1)
    NN_plot_y = np.mean(NN_data, axis=1)
    NN_plot_var = np.var(NN_data, axis=1)
    x = np.arange(0, 20, 3)

    fig, ax = plt.subplots(figsize=(12, 9))
    if error_bars:
        ax.errorbar(
            x,
            minimax_plot_y,
            minimax_plot_var,
            ls="none",
            fmt="-o",
            label="MiniMax: Depth="+str(depth),
        )
        ax.errorbar(
            x,
            ab_prun_plot_y,
            ab_prun_plot_var,
            ls="none",
            fmt="-o",
            label="A-B Pruning: Depth="+str(depth),
        )
        # ax.errorbar(
        #     x,
        #     scout_plot_y,
        #     scout_plot_var,
        #     ls="none",
        #     fmt="-o",
        #     label="Scout: Depth="+str(depth),
        # )
        ax.errorbar(
            x,
            NN_plot_y,
            NN_plot_var,
            ls="none",
            fmt="-o",
            label="CNN",
        )
    else:
        ax.plot(
            x, 
            minimax_plot_y, 
            "r+", label="MiniMax: Depth="+str(depth), 
            markersize=marker_size,
        )

        ax.plot(
            x,
            ab_prun_plot_y,
            "g.",
            label="A-B Pruning: Depth="+str(depth),
            markersize=marker_size,
        )
        ax.plot(
            x,
            NN_plot_y,
            "c*",
            label="CNN",
            markersize=marker_size,
        )

    # Dotted line for 50% point
    ax.plot(
        np.arange(-3, 23, 3), np.repeat(0.5, len(x) + 2), "k--", linewidth=line_size,
    )

    # Other plotting Params
    ax.set_ylim((0, 1))
    ax.set_xlim((-1, max(x) + 1))
    ax.set_xlabel("Number of random turns before game begins")
    ax.set_ylabel("Mean Win Rate")
    ax.legend()
    xticks = x
    ax.set_xticks(xticks)

    plt.show()


def plotWins():
    # Function to create a table of heuristics playin against each other
    DIRECTORY = './Search_Mode_Results/'
    count = 0
    scout = []
    minimax = []
    ab = []

    # fig.savefig(
    #     "./Search_Mode_Results/depth_"
    #     + str(self.bot1.depth)
    #     + "_"
    #     + self.bot1.search_mode
    #     + "_"
    #     + self.bot1.heur_name
    #     + "vs"
    #     + lab
    #     + ".png"
    # )

    entries = os.listdir(DIRECTORY)

    print('# of Files: ',len(entries))
    for entry in entries:
        if 'Weight_Matrixvs.csv' in entry : 
            count+=1
            temp = entry.split('_')
            print(temp)
            df = genfromtxt(DIRECTORY+entry, delimiter=',')
            print(np.mean(df))
            plt.scatter(range(0,4),df,label=temp[1]+' '+temp[2])
    #         search_depth = temp[1].replace('depth', '')
    #         print(temp[0],' ',search_depth)
    #         df = genfromtxt(DIRECTORY+entry, delimiter=',')
    #         print(np.mean(df))
    #         if(temp[0].lower()=='scout'):
    #             scout.append(np.mean(df))
    #         elif(temp[0].lower()=='minimax'):
    #             minimax.append(np.mean(df))
    #         elif(temp[0].lower()=='a-b pruning'):
    #             ab.append(np.mean(df))
            
    #         (df.mean(axis=1)).plot(kind='line',x='Depth',y='Nodes Visited',label=search_depth)

    # y = range(1,6)
    # print(scout)
    # print(minimax)
    # print(ab)
    # plt.plot(y,scout,label='Scout')
    # plt.plot(y,minimax,label='MiniMax')
    # plt.plot(y,ab,label='A-B Pruning')

    plt.title('Wins by AI at different board states against Greedy Player')
    plt.xlabel('Board State')
    plt.ylabel('Win %')
    plt.legend()
    plt.show()
                
def nodesVisited():
    # Function to create a table of heuristics playin against each other
    DIRECTORY = './Search_Mode_Results/'
    count = 0
    scout = []
    minimax = []
    ab = []

    entries = os.listdir(DIRECTORY)

    print('# of Files: ',len(entries))
    for entry in entries:
        if '_nodesV.csv' in entry : 
            count+=1
            temp = entry.split('_')
            search_depth = temp[1].replace('depth', '')
            print(temp[0],' ',search_depth)
            df = genfromtxt(DIRECTORY+entry, delimiter=',')
            print(np.mean(df))
            if(temp[0].lower()=='scout'):
                scout.append(np.mean(df))
            elif(temp[0].lower()=='minimax'):
                minimax.append(np.mean(df))
            elif(temp[0].lower()=='a-b pruning'):
                ab.append(np.mean(df))
            # 
            # (df.mean(axis=1)).plot(kind='line',x='Depth',y='Nodes Visited',label=search_depth)

    y = range(1,6)
    print(scout)
    print(minimax)
    print(ab)
    plt.plot(y,scout,label='Scout')
    plt.plot(y,minimax,label='MiniMax')
    plt.plot(y,ab,label='A-B Pruning')

    plt.title('Nodes Visited at Different Depths and Board States')
    plt.xlabel('Depth')
    plt.ylabel('Nodes Visited')
    plt.legend()
    plt.show()
    

if __name__ == "__main__":
    plotAfterSimulation(depth=3)
