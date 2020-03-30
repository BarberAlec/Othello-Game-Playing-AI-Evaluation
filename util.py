import numpy as np
import matplotlib.pyplot as plt



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
        # scout_data = np.genfromtxt(
        #     "./Search_Mode_Results/Scout_depth3_wins.csv", delimiter=","
        # )
    NN_data = np.genfromtxt(
        "./Search_Mode_Results/NN_wins.csv", delimiter=","
    )

    minimax_plot_y = np.mean(minimax_data, axis=1)
    minimax_plot_var = np.var(minimax_data, axis=1)
    ab_prun_plot_y = np.mean(ab_prun_data, axis=1)
    ab_prun_plot_var = np.var(ab_prun_data, axis=1)
    # scout_plot_y = np.mean(scout_data, axis=1)
    # scout_plot_var = np.var(scout_data, axis=1)
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
        
        # ax.plot(
        #     x, 
        #     scout_plot_y, 
        #     "bx", 
        #     label="Scout: Depth=2", 
        #     markersize=marker_size
        # )

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


if __name__ == "__main__":
    plotAfterSimulation(depth=3)
