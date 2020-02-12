import numpy as numpy


class amazons_game:
    def __init__(self):
        # Coordinate system is (y,x)
        self.board = numpy.zeros((10, 10), numpy.int8)
        self.board[0, 3] = 1
        self.board[3, 0] = 1
        self.board[0, 6] = 1
        self.board[3, 9] = 1

        self.board[6, 0] = 2
        self.board[9, 4] = 2
        self.board[6, 9] = 2
        self.board[9, 6] = 2
        self.whites_turn = True

    def board_print(self):
        print(self.board)

    def take_turn(self, player, start_pos, end_pos, arrow_pos):
        """
        player: int [1-2]: white or black
        """
        board_copy = self.board
        if board_copy(start_pos) == player:
            [legal, board_copy] = self.turn_move(board_copy, start_pos, end_pos)
            if not legal:
                return False
        else:
            return False

        [legal, board_copy] = self.turn_arrow(board_copy, end_pos, arrow_pos)
        if not legal:
            return False

        self.board = board_copy
        return True

    def turn_move(self, board, start_pos, end_pos):
        """
        Checks if legal move, then takes move on copy of board
        """
        # Check if destination is free
        if board[end_pos] != 0:
            return board,False

        # Check if position is accessible via straight lines
        if abs(start_pos[0]-end_pos[0]) != abs(start_pos[1]-end_pos[1]):
            # Not a diagonal move, check straight move
            if not((start_pos[0] == end_pos[0]) or (start_pos[2] == end_pos[2])):
                return board, False
            else:
                # We are moving in a straight line, check for obstacles
                # TODO
        else:
            # We are moving diagonally, check for obstactles
            # TODO

        return board, True

    def turn_arrow(self, board, curr_pos, arrow_pos):
        # TODO: east check if arrow dest is available and is in a direction we can shoot in
        return board, True


amazons_game().board_print()

