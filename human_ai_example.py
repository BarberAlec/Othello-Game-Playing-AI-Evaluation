from Othello import othello


class human_ai(othello.ai):
    def __init__(self):
        self.name = "human"
        
    def getPlayerMove(self, board, playerTile):
        # Let the player type in their move.
        # Returns the move as [x, y] (or returns the string 'quit')
        DIGITS1TO8 = "1 2 3 4 5 6 7 8".split()
        while True:
            print("Enter your move, or type quit to end the game")
            move = input().lower()
            if move == "quit":
                return "quit"
            if len(move) == 2 and move[0] in DIGITS1TO8 and move[1] in DIGITS1TO8:
                x = int(move[0]) - 1
                y = int(move[1]) - 1
                if self.isValidMove(board, playerTile, x, y) == False:
                    continue

                else:
                    break
            else:
                print(
                    "That is not a valid move. Type the x digit (1-8), then the y digit (1-8)."
                )
                print("For example, 81 will be the top-right corner.")
        return [x, y]
