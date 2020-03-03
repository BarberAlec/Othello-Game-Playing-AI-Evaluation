#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
View Past competitions, Contains competitions from 2003-2006 each with around 500 games. Competitions between expert players.

Data Features
    event/_date	- year of competition
    event/_name	
    result/_winner	- color of winner
    result/_type - normal
    player/0/_color	
    player/0/_name	
    player/1/_color	
    player/1/_name	
    moves/_game	- e.g. 8x8. All games 8x8
    moves/_type	- flat
    moves/__text - Moves like chess - f5d6c3d3c4f4f6g5e6d7e3g6g3c5e7d8b6f7c6b5a6a4e8f8g4b3h5d2a5c2b4a7c8a3g8b7c7f2e1f3e2h3h6h4g7h8h7g2a8b8a2b2b1c1a1d1f1h1h2g1
    __text - Final score

Use for:
    Exploratory Analysis
    Deep/Neural Network Training

"""
import random
import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd
import os
from textwrap import wrap
import os
from glob import glob


PATH = os.getcwd()+"/PastCompetitions"
EXT = "*.csv"


class HelperFuncs(object):

    def parseGame(self, file_name):
        othello_games = pd.read_csv(file_name) 
        print(othello_games.shape)

        for index, row in othello_games.head(n=1).iterrows():
            print(index, row)
            print(wrap(row['moves/__text'],2))



if __name__ == '__main__':
    hp = HelperFuncs()
    hp.parseGame('./PastCompetitions/Othello2006.csv')
    
    all_csv_files = [file
                 for path, subdir, files in os.walk(PATH)
                 for file in glob(os.path.join(path, EXT))]

    for file in all_csv_files:
        hp.parseGame(file)
