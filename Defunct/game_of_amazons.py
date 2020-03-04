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
        self.board[9, 3] = 2
        self.board[6, 9] = 2
        self.board[9, 6] = 2
        self.whites_turn = True

    def board_print(self):
        print(self.board)

    def take_turn(self, player, start_pos, end_pos, arrow_pos):
        """
        player: int [1-2]: white or black
        """
        # Create copy of board in case future move part is illegal
        board_copy = self.board
        legal = True

        if board_copy[start_pos] == player:
            [board_copy, legal] = self._turn_move_(board_copy, start_pos, end_pos)
            if not legal:
                return False
        else:
            return False

        [board_copy, legal] = self._turn_arrow_(board_copy, end_pos, arrow_pos)
        if not legal:
            return False

        self.board = board_copy
        return True

    def _turn_move_(self, board, start_pos, end_pos):
        """
        Checks if legal move, then takes move on copy of board
        """
        # Check if destination is free
        if board[end_pos] != 0:
            return board, False

        # Check if position is accessible via straight lines
        if abs(start_pos[0] - end_pos[0]) != abs(start_pos[1] - end_pos[1]):
            # Not a diagonal move, check straight move
            if not ((start_pos[0] == end_pos[0]) or (start_pos[1] == end_pos[1])):
                return board, False
            else:
                # We are moving in a straight line, check for obstacles
                # TODO
                print("Check for obs")
        else:
            legal

        return board, True

    def _turn_arrow_(self, board, curr_pos, arrow_pos):
        # Check if arrow destination is empty
        if board[arrow_pos] != 0:
            return board, False

        # Check if position is accessible via straight lines
        if abs(curr_pos[0] - arrow_pos[0]) != abs(curr_pos[1] - arrow_pos[1]):
            # Not a diagonal move, check straight move
            if not ((curr_pos[0] == arrow_pos[0]) or (curr_pos[1] == arrow_pos[1])):
                return board, False

        # Move is possible, dont need to consider obstacles so complete move
        board[arrow_pos] = 3
        return board, True


def main():
    game = amazons_game()
    game.board_print()
    game.take_turn(1, (0, 3), (5, 3), (5, 5))
    game.board_print()


if __name__ == "__main__":
    main()
