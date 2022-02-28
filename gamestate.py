import numpy as np
import copy
from move import Move

class GameState:
    playerX = 1
    playerO = -1

    def __init__(self, initial_board=np.zeros(shape=(3, 3)), initial_player=1):
        assert len(initial_board.shape) == 2 and \
               initial_board.shape[0] == 3 and \
               initial_board.shape[1] == 3, print("Only 3x3 boards are allowed")

        self.board = initial_board
        self.next_player = initial_player

    def print_board(self):

        def convert(number):
            if number == self.playerX:
                return "X"
            if number == self.playerO:
                return "O"
            return " "

        for row in range(3):
            print(f"| {convert(self.board[row, 0])} | {convert(self.board[row, 1])} | {convert(self.board[row, 2])} |")


    def is_move_legal(self, move):
        if self.next_player != move.player:
            return False
        return True if self.board[move.x, move.y] == 0 else False

    def make_move(self, move: Move):
        assert self.is_move_legal(move), print("Move is illegal!")
        new_board = copy.deepcopy(self.board)
        new_board[move.x, move.y] = move.player
        return GameState(initial_board=new_board, initial_player=-1 * self.next_player)

    def legal_moves(self):
        moves = []
        n_rows = self.board.shape[0]
        n_cols = self.board.shape[1]
        for x in range(n_rows):
            for y in range(n_cols):
                move = Move(x=x, y=y, player=self.next_player)
                if self.is_move_legal(move):
                    moves.append(move)
        return moves

    def is_game_over(self):
        # Is over if we have a winner
        if self.get_game_result() == self.playerX or self.get_game_result() == self.playerO:
            return True
        # Is over if there are no legal moves
        return True if len(self.legal_moves()) == 0 else False

    def get_game_result(self):
        # if playerX is winner return 1
        # if playerX is loser return -1
        # otherwise return 0

        playerX_win_sum = self.playerX * 3
        playerO_win_sum = self.playerO * 3

        # Check for win in rows or columns
        row_sums = np.sum(self.board, axis=0)
        col_sums = np.sum(self.board, axis=1)
        for row_sum in row_sums:
            if row_sum == playerX_win_sum:
                return self.playerX
            if row_sum == playerO_win_sum:
                return self.playerO
        for col_sum in col_sums:
            if col_sum == playerX_win_sum:
                return self.playerX
            if col_sum == playerO_win_sum:
                return self.playerO
        # Check for win in diagonals
        if self.board[0, 0] == self.playerX and self.board[1, 1] == self.playerX and self.board[2, 2] == self.playerX:
            return self.playerX
        if self.board[0, 2] == self.playerX and self.board[1, 1] == self.playerX and self.board[2, 0] == self.playerX:
            return self.playerX
        if self.board[0, 0] == self.playerO and self.board[1, 1] == self.playerO and self.board[2, 2] == self.playerO:
            return self.playerO
        if self.board[0, 2] == self.playerO and self.board[1, 1] == self.playerO and self.board[2, 0] == self.playerO:
            return self.playerO

        return 0