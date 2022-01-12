# Author: Hannah Boehm
# Description: A program for a two-player version of Quoridor. The game is played on a board of 9x9 cells.
#              Each player has 1 pawn and 10 fences. The objective is to move one's pawn to the opposite end
#              of the board; players can impede their opponent's progress by blocking their path with fences.


class QuoridorGame:

    def __init__(self):
        """Sets player_won to None, initializes the board and the pawns, sets turn to 1,
           and sets winner to None"""
        self._player_won = None
        self._f1 = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: []}
        self._f2 = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: []}
        self._f = {1: self._f1, 2: self._f2}
        self._players = {1: [4, 0], 2: [4, 8]}
        self._turn = 1
        self._winner = None

    def is_winner(self, player):
        """Returns whether a player won the game or not"""
        if player == self._winner:
            return True
        else:
            return False

    def get_player_coordinates(self, player):
        """Returns player coordinates"""
        return self._players[player]

    def print_board(self):
        """Returns visual representation of the current state of the board"""
        print(' 0 1 2 3 4 5 6 7 8')
        for i in range(1, 18):
            self.print_row(i)
            print()
        print()

    def print_row(self, row_num):
        """Helper function to print a row"""
        if row_num % 2 != 0:
            print(str(int(row_num / 2)), end="")
            for j in range(1, 19):
                self.print_element(row_num, j)
        else:
            for j in range(1, 19):
                self.print_h_barrier(row_num, j)

    def print_element(self, row_num, col_num):
        """Helper function to print individual fields on the board"""
        if col_num % 2 != 0:
            if self._players[1][0] == int(col_num / 2) and self._players[1][1] == int(row_num / 2):
                print('1', end="")
            elif self._players[2][0] == int(col_num / 2) and self._players[2][1] == int(row_num / 2):
                print('2', end="")
            else:
                print('.', end="")
        else:
            self.print_v_barrier(row_num, col_num)

    def print_v_barrier(self, row_num, col_num):
        """Helper function to print vertical barriers"""
        for i in self._f:
            for j in self._f[i]:
                try:
                    if self._f[i][j][0] == 'v':
                        if self._f[i][j][1] == int(col_num / 2) and self._f[i][j][2] == int(row_num / 2):
                            print('|', end="")
                            return ()
                except:
                    pass
        print(' ', end="")

    def print_h_barrier(self, row_num, col_num):
        """Helper function to print horizontal barriers"""
        for i in self._f:
            for j in self._f[i]:
                try:
                    if self._f[i][j][0] == 'h':
                        if self._f[i][j][1] == col_num / 2 - 1 and self._f[i][j][2] == row_num / 2:
                            print('_', end="")
                            return ()
                except:
                    pass
        print(' ', end="")

    def move_pawn(self, player, target_coordinates):
        """Verifies whether the move is valid, and places the pawn on the new coordinates"""
        if self._winner is not None:
            return False

        if self.check_valid_move(player, list(target_coordinates)) is True:
            self._players[player][0] = target_coordinates[0]
            self._players[player][1] = target_coordinates[1]
            if self._players[1][1] == 8:
                self._winner = 1
                self._turn = None
            elif self._players[2][1] == 0:
                self._winner = 2
                self._turn = None
            else:
                if player == 1:
                    self._turn = 2
                else:
                    self._turn = 1
            return True

        else:
            return False

    def check_valid_move(self, player, target_coordinates):
        """Checks if pawn move is valid according to the rules"""
        # ensure correct player's turn
        if self._turn != player:
            return False

        # ensure coordinates are within boundaries
        if target_coordinates[0] > 8 or target_coordinates[0] < 0:
            return False

        if target_coordinates[1] > 8 or target_coordinates[1] < 0:
            return False

        # ensure that field isn't occupied
        if target_coordinates[0] == self._players[self.other_player()][0] and target_coordinates[1] == \
                self._players[self.other_player()][1]:
            return False

        # ensure that barriers are respected
        delta_y = self._players[player][1] - target_coordinates[1]
        delta_x = self._players[player][0] - target_coordinates[0]
        delta = [delta_x, delta_y]

        if delta_y < 0 and self.find_fence('h', target_coordinates) is True:
            return False
        if delta_y > 0 and self.find_fence('h', self._players[player]) is True:
            return False
        if delta_x < 0 and self.find_fence('v', target_coordinates) is True:
            return False
        if delta_x > 0 and self.find_fence('v', self._players[player]) is True:
            return False

        if self.check_special_rule(delta, target_coordinates) is False:
            return False
        if self.check_diagonal(delta_x, delta_y, target_coordinates, player) is False:
            return False

        return True

    def check_diagonal(self, delta_x, delta_y, target_coordinates, player):
        """Checks and allows diagonal moves only under special circumstances"""
        if abs(delta_x) == 1 and abs(delta_y) == 1:
            if self.check_pos_next(target_coordinates, self._players[self.other_player()]) is False:
                return False
            d_x = self._players[player][0] - self._players[self.other_player()][0]
            d_y = self._players[player][1] - self._players[self.other_player()][1]
            if d_x == 0 and d_y > 0:
                if self.find_fence('h', self._players[self.other_player()]) is False:
                    return False
            if d_x == 0 and d_y < 0:
                if self.find_fence('h', [self._players[player][0], self._players[player][1] + 2]) is False:
                    return False
            if d_y == 0 and d_x > 0:
                if self.find_fence('v', self._players[self.other_player()]) is False:
                    return False
            if d_y == 0 and d_x < 0:
                if self.find_fence('v', [self._players[player][0] + 2, self._players[player][1]]) is False:
                    return False

        # do not allow more than one step diagonal moves
        if abs(delta_x) > 1 and abs(delta_y) > 1:
            return False

        return True

    def check_special_rule(self, delta, target_coordinates):
        """Checks if the special hopping rule applies"""
        # check if there is more than one step taken; if so, see if special exception applies
        for i in delta:
            if i > 1 or i < -1:
                if self.check_pawns_next() is False:
                    return False
                if delta[0] == 0:
                    if delta[1] < 0:
                        if self._players[self.other_player()][1] + 1 != target_coordinates[1]:
                            return False
                        if self.find_fence('h', target_coordinates) is True:
                            return False
                    if delta[1] > 0:
                        if self._players[self.other_player()][1] - 1 != target_coordinates[1]:
                            return False
                        if self.find_fence('h', [target_coordinates[0], target_coordinates[1] + 1]) is True:
                            return False
                if delta[1] == 0:
                    if delta[0] < 0:
                        if self._players[self.other_player()][0] + 1 != target_coordinates[0]:
                            return False
                        elif self.find_fence('v', target_coordinates) is True:
                            return False
                    if delta[0] > 0:
                        if self._players[self.other_player()][0] - 1 != target_coordinates[0]:
                            return False
                        elif self.find_fence('v', [target_coordinates[0] + 1, target_coordinates[1]]) is True:
                            return False

    def find_fence(self, direction, target_coordinates):
        """Checks if vertical or horizontal fence can be found at target coordinate"""
        for i in self._f:
            for j in self._f[i]:
                if self._f[i][j][1:3] == target_coordinates and direction == self._f[i][j][0]:
                    return True
        return False

    def check_pawns_next(self):
        """Checks if both pawns are next to each other"""
        delta_x = self._players[1][0] - self._players[2][0]
        delta_y = self._players[1][1] - self._players[2][1]

        if delta_x == 0:
            if self._players[1][1] == self._players[2][1] + 1 or self._players[1][1] == self._players[2][1] - 1:
                return True
        if delta_y == 0:
            if self._players[1][0] == self._players[2][0] + 1 or self._players[1][0] == self._players[2][0] - 1:
                return True
        else:
            return False

    def check_pos_next(self, pos1, pos2):
        """Checks if two positions are next to each other"""
        delta_x = pos1[0] - pos2[0]
        delta_y = pos1[1] - pos2[1]

        if delta_x == 0:
            return True
        elif delta_y == 0:
            return True
        else:
            return False

    def other_player(self):
        """Returns the opposite of current turn player"""
        if self._turn == 1:
            return 2
        if self._turn == 2:
            return 1

    def place_fence(self, player, direction, target):
        """Places fence for player at a specific orientation at target coordinates"""
        # checks for correct player placing
        if player != self._turn:
            return False

        # check if occupied
        if self.find_fence(direction, list(target)) is True:
            return False

        # ensure that there are fences left
        if self.check_fence_left(player) is False:
            return False

        # ensure that fence is placed within boundaries
        if target[0] > 8 or target[1] > 8:
            return False
        if direction == 'v' and target[0] < 1:
            return False
        if direction == 'v' and target[1] < 0:
            return False
        if direction == 'h' and target[0] < 0:
            return False
        if direction == 'h' and target[1] < 1:
            return False

        # place fence
        for i in range(1, 11):
            if self._f[player][i] == []:
                self._f[player][i] = [direction, target[0], target[1]]
                self._turn = self.other_player()
                break
        return True

    def check_fence_left(self, player):
        """Checks if player has fences left"""
        for i in range(1, 11):
            if self._f[player][i] == []:
                return True
        return False
