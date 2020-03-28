# conda install -c pytorch -c fastai fastai
# make sure to have 'trained_othello_CNN.pkl' in the working dir

import torch
import fastai
import PIL
import numpy as np
from Othello import othello
from Othello_CNN import OthelloCNN
from othello_ai import decisionRule_ai


class NN_ai(othello.ai):
    def __init__(self, marker):
        self.name = "NN"
        self.marker = marker
        self.learn = fastai.vision.load_learner("", "trained_othello_CNN.pkl")
        self.learn.model.float()
        self.greedy = decisionRule_ai(marker)
        self.search_mode = 'NN'
        self.depth = 0

    def getMove(self, board):
        player1_mat = np.where(board == self.marker, 1, 0)
        player2_mat = np.where(board == ((-1) * self.marker), 1, 0)
        empty_mat = np.zeros((8, 8))
        mat_3 = np.dstack((player1_mat, player2_mat, empty_mat))
        mat_img = PIL.Image.fromarray((mat_3).astype(np.uint8))
        mat_tensor = fastai.vision.pil2tensor(mat_img, np.float32)
        mat_Image = fastai.vision.Image(mat_tensor)

        move = self.learn.predict(mat_Image)
        move_string = str(move[0])
        x = int(move_string[0])
        y = int(move_string[2])
        move_output = [x, y]

        if not self.isValidMove(board, self.marker, x, y):
            # If not a valid move, then use greedy algo
            print("ERROR!")
            move = self.greedy.getMove(board)

        #print("NN move: ", str(move_output[0]), ",", str(move_output[1]))
        return move_output
