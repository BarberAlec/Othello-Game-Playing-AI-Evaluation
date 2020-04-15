
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import pickle


# In[112]:


# file = pd.read_csv(r'C:\Users\Dhruv\Desktop\TCD\Year 5\Sem2\Untitled Folder\PastCompetitions\Othello2006.csv')
# heading = file['moves/__text']

#  DONT NEED THIS NOW _ CODE FOR CONVETING INTO PICKLEs
# for j in range(len(heading)):
#     a = heading[j]

#     con = []
#     for i in range(0,len(a),2):
#         temp = a[i:i+2]
#         num = int(temp[1:2])
#         num = num-1
#         temp = temp[0:1] + str(num)
#         if(temp[0] == 'a'):
#             temp = '0' + temp[1:2]
#         elif(temp[0] == 'b'):
#             temp = '1' + temp[1:2]
#         elif(temp[0] == 'c'):
#             temp = '2' + temp[1:2]
#         elif(temp[0] == 'd'):
#             temp = '3' + temp[1:2]
#         elif(temp[0] == 'e'):
#             temp = '4' + temp[1:2]
#         elif(temp[0] == 'f'):
#             temp = '5' + temp[1:2]
#         elif(temp[0] == 'g'):
#             temp = '6' + temp[1:2]
#         elif(temp[0] == 'h'):
#             temp = '7' + temp[1:2]
        
#         con.append(temp)
# #     print(con)
   

#         with open('2006_game_'+str(j)+'.txt', 'wb') as fp:
#             pickle.dump(con, fp)


# In[108]:


for j in range(5):
    with open('2003_game_'+str(j)+'.txt', 'rb') as fp:
        b = pickle.load(fp)
    print(b)


# In[6]:


def getmove():
#     Opens the pickle file
# TO DO: run the code till the list is empty
    with open('2003_game_0.txt', 'rb') as fp:
        moves = pickle.load(fp)
    move = moves[0]
#     Generates the moves on the board
    x = int(move[0]) 
    y = int(move[1]) 
    moves.pop(0)
    return [x,y]

        


# In[7]:


getmove()

