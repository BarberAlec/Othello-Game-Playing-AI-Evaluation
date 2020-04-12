# File to create a table of heuristics playin against each other
import os
import pandas as pd
import matplotlib.pyplot as plt
# import scipy
import numpy as np
from numpy import genfromtxt

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
        # search_depth = temp[1].replace('depth', '')
        # print(temp[0],' ',search_depth)
        # df = genfromtxt(DIRECTORY+entry, delimiter=',')
        # print(np.mean(df))
        # if(temp[0].lower()=='scout'):
        #     scout.append(np.mean(df))
        # elif(temp[0].lower()=='minimax'):
        #     minimax.append(np.mean(df))
        # elif(temp[0].lower()=='a-b pruning'):
        #     ab.append(np.mean(df))
        # 
        # (df.mean(axis=1)).plot(kind='line',x='Depth',y='Nodes Visited',label=search_depth)

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
            
