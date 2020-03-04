import random
import numpy as np


class othello:
    """
    Encapsulation of the board game othello
    """

    class ai:
        """
        Class to encapsulate all ai behaviour, more to come.
        To create a new ai, make a child class :)
        """

        def __init__(self,marker):
            self.name = "base_ai"
            self.marker = marker

        def peekScore(self, board, x, y):
            dupeBoard = self._duplicateBoard_(board)
            self._makeMove_(dupeBoard, self.marker, x, y)
            score = self.getCurrentScore(dupeBoard)[self.marker]
            return score

        def _makeMove_(self, board, tile, xstart, ystart):
            
            tilesToFlip = self.isValidMove(board, tile, xstart, ystart)
            if tilesToFlip == False:
                return False

            board[xstart][ystart] = tile
            for x, y in tilesToFlip:
                board[x][y] = tile
            return True

        def _duplicateBoard_(self, board):
            b = [x[:] for x in board]
            return b

        def isOnCorner(self, x, y):
            # Returns True if the position is in one of the four corners.
            return (
                (x == 0 and y == 0)
                or (x == 7 and y == 0)
                or (x == 0 and y == 7)
                or (x == 7 and y == 7)
            )

        def getCurrentScore(self, board):
            # Determine the score by counting the tiles. Returns a dictionary with keys 'X' and 'O'.
            xscore = 0
            oscore = 0
            for x in range(8):
                for y in range(8):
                    if board[x][y] == "X":
                        xscore += 1

                    if board[x][y] == "O":
                        oscore += 1

            return {"X": xscore, "O": oscore}

        def isOnBoard(self, x, y):
            return x >= 0 and x <= 7 and y >= 0 and y <= 7

        def isValidMove(self, board, tile, xstart, ystart):
            # Returns False if the player's move on space xstart, ystart is invalid.
            # If it is a valid move, returns a list of spaces that would become the player's if they made a move here.
            if board[xstart][ystart] != " " or not self.isOnBoard(xstart, ystart):
                return False

            board[xstart][ystart] = tile  # temporarily set the tile on the board.
            if tile == "X":
                otherTile = "O"
            else:
                otherTile = "X"
            tilesToFlip = []
            for xdirection, ydirection in [
                [0, 1],
                [1, 1],
                [1, 0],
                [1, -1],
                [0, -1],
                [-1, -1],
                [-1, 0],
                [-1, 1],
            ]:
                x, y = xstart, ystart
                x += xdirection  # first step in the direction
                y += ydirection  # first step in the direction
                if self.isOnBoard(x, y) and board[x][y] == otherTile:
                    # There is a piece belonging to the other player next to our piece.
                    x += xdirection
                    y += ydirection
                    if not self.isOnBoard(x, y):
                        continue

                    while board[x][y] == otherTile:
                        x += xdirection
                        y += ydirection

                        if not self.isOnBoard(
                            x, y
                        ):  # break out of while loop, then continue in for loop
                            break

                    if not self.isOnBoard(x, y):
                        continue

                    if board[x][y] == tile:
                        # There are pieces to flip over. Go in the reverse direction until we reach the original space, noting all the tiles along the way.
                        while True:
                            x -= xdirection
                            y -= ydirection
                            if x == xstart and y == ystart:
                                break
                            tilesToFlip.append([x, y])

            board[xstart][ystart] = " "  # restore the empty space
            if (
                len(tilesToFlip) == 0
            ):  # If no tiles were flipped, this is not a valid move.
                return False
            return tilesToFlip

        def getLegalMoves(self, board, tile):
            # Returns a list of [x,y] lists of valid moves for the given player on the given board.
            validMoves = []
            for x in range(8):
                for y in range(8):
                    if self.isValidMove(board, tile, x, y) != False:
                        validMoves.append([x, y])
            return validMoves

        def getMove(self, board, playerTile):
            print("WARNING: this is the base ai class, use a custom class please.")
            return

    def __init__(self):
        self.mainBoard = self.getNewBoard()
        self.resetBoard(self.mainBoard)
        self.turn = 0
        self.computerTile = ''

    def startgame(self, bot1=ai('X')):
        # Welcome message for bot1, comment out line if you want to surpress terminal outputs
        self.welcomeMessage(bot1)

        # We will always be X, random player starts
        if bot1.marker == 'X':
            self.computerTile = 'O'
        else:
            self.computerTile = 'X'

        while True:
            if self.turn == "ai":
                # bot1 turn
                # Comment these out to surpress output
                self.drawBoard(self.mainBoard)
                self.showPoints(bot1.marker, self.computerTile, self.mainBoard)

                # This is the only call to the bot1 :)
                move = bot1.getMove(self.mainBoard, bot1.marker)

                if move == "quit":
                    return
                else:
                    self.makeMove(self.mainBoard, bot1.marker, move[0], move[1])

                if self.getValidMoves(self.mainBoard, self.computerTile) == []:
                    break
                else:
                    self.turn = "rule_ai"

            else:
                # Computer's turn.
                self.drawBoard(self.mainBoard)
                self.showPoints(bot1.marker, self.computerTile, self.mainBoard)

                x, y = self.getComputerMove(self.mainBoard, self.computerTile)
                self.makeMove(self.mainBoard, self.computerTile, x, y)
                if self.getValidMoves(self.mainBoard, bot1.marker) == []:
                    break
                else:
                    self.turn = "ai"

        # Game finished, show results
        self.displayResults(bot1)

    def welcomeMessage(self, bot):
        if bot.name == "base_ai":
            print("Welcome base ai I am treating you like a human.")
        elif bot.name == "human":
            print("Welcome human.")
        else:
            print("I only know how to deal with humans at the moment, sorry.")
            return

    def displayResults(self,bot):
        self.drawBoard(self.mainBoard)
        scores = self.getScoreOfBoard(self.mainBoard)
        print("X scored %s points. O scored %s points." % (scores["X"], scores["O"]))
        if scores[bot.marker] > scores[self.computerTile]:
            print(
                "You beat the computer by %s points! Congratulations!"
                % (scores[bot.marker] - scores[self.computerTile])
            )
        elif scores[bot.marker] < scores[self.computerTile]:
            print(
                "You lost. The computer beat you by %s points."
                % (scores[self.computerTile] - scores[bot.marker])
            )
        else:
            print("The game was a tie!")

    def drawBoard(self, board):
        # This function prints out the board that it was passed. Returns None.
        HLINE = "  +---+---+---+---+---+---+---+---+"
        VLINE = "  |   |   |   |   |   |   |   |   |"
        print("    1   2   3   4   5   6   7   8")
        print(HLINE)

        for y in range(8):
            print(VLINE)
            print(y + 1, end=" ")
            for x in range(8):
                print("| %s" % (board[x][y]), end=" ")
            print("|")
            print(VLINE)
            print(HLINE)

    def resetBoard(self, board):
        # Blanks out the board it is passed, except for the original starting position.
        for x in range(8):
            for y in range(8):
                board[x][y] = " "
                # Starting pieces:
                board[3][3] = "X"
                board[3][4] = "O"
                board[4][3] = "O"
                board[4][4] = "X"

    def getNewBoard(self):
        # Creates a brand new, blank board data structure.
        board = []
        for i in range(8):
            board.append([" "] * 8)
        return board

    def isValidMove(self, board, tile, xstart, ystart):
        # Returns False if the player's move on space xstart, ystart is invalid.
        # If it is a valid move, returns a list of spaces that would become the player's if they made a move here.
        if board[xstart][ystart] != " " or not self.isOnBoard(xstart, ystart):
            return False

        board[xstart][ystart] = tile  # temporarily set the tile on the board.
        if tile == "X":
            otherTile = "O"
        else:
            otherTile = "X"
        tilesToFlip = []
        for xdirection, ydirection in [
            [0, 1],
            [1, 1],
            [1, 0],
            [1, -1],
            [0, -1],
            [-1, -1],
            [-1, 0],
            [-1, 1],
        ]:
            x, y = xstart, ystart
            x += xdirection  # first step in the direction
            y += ydirection  # first step in the direction
            if self.isOnBoard(x, y) and board[x][y] == otherTile:
                # There is a piece belonging to the other player next to our piece.
                x += xdirection
                y += ydirection
                if not self.isOnBoard(x, y):
                    continue

                while board[x][y] == otherTile:
                    x += xdirection
                    y += ydirection

                    if not self.isOnBoard(
                        x, y
                    ):  # break out of while loop, then continue in for loop
                        break

                if not self.isOnBoard(x, y):
                    continue

                if board[x][y] == tile:
                    # There are pieces to flip over. Go in the reverse direction until we reach the original space, noting all the tiles along the way.
                    while True:
                        x -= xdirection
                        y -= ydirection
                        if x == xstart and y == ystart:
                            break
                        tilesToFlip.append([x, y])

        board[xstart][ystart] = " "  # restore the empty space
        if len(tilesToFlip) == 0:  # If no tiles were flipped, this is not a valid move.
            return False
        return tilesToFlip

    def isOnBoard(self, x, y):
        # Returns True if the coordinates are located on the board.
        return x >= 0 and x <= 7 and y >= 0 and y <= 7

    def getValidMoves(self, board, tile):
        # Returns a list of [x,y] lists of valid moves for the given player on the given board.
        validMoves = []
        for x in range(8):
            for y in range(8):
                if self.isValidMove(board, tile, x, y) != False:
                    validMoves.append([x, y])
        return validMoves

    def getScoreOfBoard(self, board):
        # Determine the score by counting the tiles. Returns a dictionary with keys 'X' and 'O'.
        xscore = 0
        oscore = 0
        for x in range(8):
            for y in range(8):
                if board[x][y] == "X":
                    xscore += 1

                if board[x][y] == "O":
                    oscore += 1

        return {"X": xscore, "O": oscore}

    def firstTurn(self):
        # Who plays first
        if random.randint(0, 1) == 0:
            return "rule_ai"
        return "ai"

    def makeMove(self, board, tile, xstart, ystart):
        # Place the tile on the board at xstart, ystart, and flip any of the opponent's pieces.
        # Returns False if this is an invalid move, True if it is valid.
        tilesToFlip = self.isValidMove(board, tile, xstart, ystart)
        if tilesToFlip == False:
            return False

        board[xstart][ystart] = tile
        for x, y in tilesToFlip:
            board[x][y] = tile
        return True

    def duplicateBoard(self, board):
        b = [x[:] for x in board]
        return b

    def isOnCorner(self, x, y):
        # Returns True if the position is in one of the four corners.
        return (
            (x == 0 and y == 0)
            or (x == 7 and y == 0)
            or (x == 0 and y == 7)
            or (x == 7 and y == 7)
        )

    def getComputerMove(self, board, computerTile):
        # Given a board and the computer's tile, determine where to
        # move and return that move as a [x, y] list.
        possibleMoves = self.getValidMoves(board, computerTile)
        # randomize the order of the possible moves
        random.shuffle(possibleMoves)
        # always go for a corner if available.
        for x, y in possibleMoves:
            if self.isOnCorner(x, y):
                return [x, y]

        # Go through all the possible moves and remember the best scoring move
        bestScore = -1
        for x, y in possibleMoves:
            dupeBoard = self.duplicateBoard(board)
            self.makeMove(dupeBoard, computerTile, x, y)
            score = self.getScoreOfBoard(dupeBoard)[computerTile]
            if score > bestScore:
                bestMove = [x, y]
            bestScore = score
        return bestMove

    def showPoints(self, playerTile, computerTile, mainBoard):
        # Prints out the current score.
        scores = self.getScoreOfBoard(mainBoard)
        print(
            "You have %s points. The computer has %s points."
            % (scores[playerTile], scores[computerTile])
        )

