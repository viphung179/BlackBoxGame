# Author: Vi Phung
# Date: 8/3/2020
# Description: Code for BlackBoxGame

class BlackBoxGame:
    """
    Represents the game, initializes the board and the score. This class will communicate with the Board class and the Ray class. Composition is used since the Board class is used as a data member. The Ray class is used in the shoot_ray method. This class has a method to initialize the board and the player's score. This class has methods that the player would use to play the game, including shoot_ray, guess_atom, get_score, and atom_left. This class also has the update_score method that would be called by shoot_ray to update the score.
    """
    def __init__(self, pos_list):
        """
        takes in a list of atoms position as parameter and initializes the data members including board, score, atoms_left, atom positions, guesses, and entries_exit
        :param pos_list: a list of tuples that represents the locations of atoms
        """
        self._board = Board(pos_list)
        self._score = 100
        self._atoms = pos_list
        self._atoms_left = len(pos_list)
        self._guesses = None  # to keep track of guesses that has been made
        self._entries_exits = None  # to keep track of entries and exits that have been used
        self._hit_list = None
        self._reflect_list = None
        self._game_status = "started"

    def shoot_ray(self, row, col):
        """
        takes as parameter row and col of ray origin, get the exit position, update entry/exit that has been visited, and update the score
        :param row: type is integer
        :param col: type is integer
        :return: If the ray origin a corner square or a non-border square, then return False. Otherwise, shoot_ray should return a tuple of the row and column (in that order) of the exit border square. If there is no exit border square (because there was a hit), then return None,
        """
        ray = Ray(row, col)
        entry_score = None
        exit_score = None

        if ray.get_entry()[0] not in range(0,10) or ray.get_entry()[1] not in range(0,10):
            return False

        if ray.entry_is_corner() or ray.entry_is_nonborder():
            return False

        if self._entries_exits is None:
            self._entries_exits = []

        self._board.find_exit(ray)

        if ray.get_entry() not in self._entries_exits:
            self._entries_exits.append(ray.get_entry())
            entry_score = True

        if ray.get_exit() is not None and ray.get_exit() not in self._entries_exits:
            self._entries_exits.append(ray.get_exit())
            exit_score = True

        self.update_score(entry_score, exit_score)
        self.update_tracking(ray.get_entry(),ray.get_exit())
        self.update_game_status()

        return (ray.get_entry(), ray.get_exit())

    def update_tracking(self,entry, exit):
        if self._hit_list is None:
            self._hit_list = []

        if self._reflect_list is None:
            self._reflect_list = []

        if exit is None:
            self._hit_list.append(entry)
        else:
            if exit == entry:
                self._reflect_list.append(exit)

    def update_score(self, entry = None, exit = None, guess = None):
        """
        updates the player's score and does not return anything
        :param entry: default parameter, if not None, then should be True and score will be deducted
        :param exit: default parameter, if not None, then should be True and score will be deducted
        :param guess: default parameter, if not None, then should be False and score will be deducted
        """
        if self._score < 0:
            return

        if entry:
            if self._score - 1 <= 0:
                self._score = 0
            else:
                self._score -= 1

        if exit:
            if self._score - 1 <= 0:
                self._score = 0
            else:
                self._score -= 1

        # only deduct score when the guess is wrong
        if guess is False:
            if self._score - 5 <= 0:
                self._score = 0
            else:
                self._score -= 5

    def update_game_status(self):
        if self._guesses is not None and len(self._guesses) == 4:
            self._guesses.sort()
            self._atoms.sort()
            if self._guesses == self._atoms:
                self._game_status = "You won! Play again!"
            else:
                self._game_status = "You lost! Try again!"

    def guess_atom(self, row, col):
        """
        takes as parameter row and col player's guess position and determine if guess is correct, then update the score
        :return: True if guess is right, otherwise it should return False
        """
        pos = (row, col)

        if self._guesses is None:
            self._guesses = []

        if pos not in self._guesses:
            self._guesses.append(pos)
            if pos not in self._board.get_atoms_pos():
                self.update_score(None, None, False)
            else:
                self._atoms_left -= 1

        self.update_game_status()

        return pos in self._board.get_atoms_pos()

    def get_score(self):
        """
        :return: player's score
        """
        return self._score

    def get_status(self):
        return self._game_status

    def atoms_left(self):
        """
        :return: the number of atoms that haven't been guessed yet
        """
        return self._atoms_left

    def get_atoms(self):
        return self._atoms

    def get_board(self):
        return self._board

    def get_guesses(self):
        return self._guesses

    def get_hits(self):
        return self._hit_list

    def get_reflects(self):
        return self._reflect_list

    def get_entries_exits(self):
        return self._entries_exits

    def print_board(self):
        """
        prints the board and does not return anything
        """
        for row in self._board.get_board():
            print(row)



class Ray:
    """
    Represents a ray with origin, direction, and exit. Ray object would provide ray information for the BlackBoxGame and Board class to use.
    """
    def __init__(self, row, col):
        """
        takes in row and col as parameters and initializes the origin and direction of the ray
        """
        self._row = row
        self._col = col
        self._pos = (row, col)
        self._entry = (row, col)
        self._exit = (row, col)
        self._dir = self.get_init_dir()

    def get_init_dir(self):
        """
        determines the direction of the ray, no parameter
        :return: direction of ray if the origin is legal, otherwise return None
        """
        if self._row == 0:
            direction = "move down"
        elif self._row == 9:
            direction = "move up"
        elif self._col == 0:
            direction = "move right"
        elif self._col == 9:
            direction = "move left"
        else:
            direction = None

        return direction


    def entry_is_nonborder(self):
        """
        determines if ray origin is non-border, no parameter
        :return: True if ray origin is not on the border, otherwise return False
        """
        if self._row not in [0, 9] and self._col not in [0, 9]:
            return True

        return False

    def entry_is_corner(self):
        """
        takes no parameter and determines if ray origin is corner of board
        :return: True if ray origin is on corner, otherwise return False
        """
        if self._pos in [(0, 0), (0, 9), (9, 0), (9, 9)]:
            return True

        return False

    def get_pos(self):
        """
        takes no parameter and returns a tuple that represents current position of the ray
        """
        return self._pos

    def set_pos(self, row, col):
        """
        takes row and col as parameter and set them to current position of the ray
        """
        self._row = row
        self._col = col
        self._pos = (row, col)

    def get_dir(self):
        """
        takes no parameter and returns current direction of the ray
        """
        return self._dir

    def set_dir(self, dir):
        """
        takes direction as parameter and set it to ray's direction
        """
        self._dir = dir

    def get_exit(self):
        """
        takes no parameter and returns the exit position of the ray
        """
        return self._exit

    def set_exit(self, exit):
        """
        takes as parameter a tuple that represents the exit position of the ray and set it to ray's exit
        """
        self._exit = exit

    def get_entry(self):
        """
        takes no parameter and returns the entry position of the ray
        """
        return self._entry


class Board:
    """
    Represents the board, initializes the board with atoms positions. This class will get information from the Ray class and use it in methods that let the BlackBoxGame class know where the exit is. There is a method to update the direction of the ray if it cannot keep moving in the original direction and a method that updates the exit of the ray if the ray has reached a border.
    """
    def __init__(self, pos_list):
        """
        initializes the board with atoms positions
        :param pos_list: list of tuples that represents atoms positions
        """
        self._atoms_pos = pos_list

    def get_board(self):
        """
        takes no parameters and return a list of lists that represents the current board
        """
        board = [['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
                 ['1', " ", " ", " ", " ", " ", " ", " ", " ", 'b'],
                 ['2', " ", " ", " ", " ", " ", " ", " ", " ", 'b'],
                 ['3', " ", " ", " ", " ", " ", " ", " ", " ", 'b'],
                 ['4', " ", " ", " ", " ", " ", " ", " ", " ", 'b'],
                 ['5', " ", " ", " ", " ", " ", " ", " ", " ", 'b'],
                 ['6', " ", " ", " ", " ", " ", " ", " ", " ", 'b'],
                 ['7', " ", " ", " ", " ", " ", " ", " ", " ", 'b'],
                 ['8', " ", " ", " ", " ", " ", " ", " ", " ", 'b'],
                 ['9', "b", "b", "b", "b", "b", "b", "b", "b", 'b']]
        for pos in self._atoms_pos:
            board[pos[0]][pos[1]] = "x"

        return board

    def get_atoms_pos(self):
        """
        takes no parameters and return a list of tuples that represents the current atoms positions
        """
        return self._atoms_pos

    def get_neighbor_pos(self, pos):
        """
        gets neighbors of a position
        :param pos: tuple that represents row and column of position
        :return: a dictionary that holds the neighbors of pos
        """
        neighbors = {}
        neighbors["top"] = (pos[0] - 1, pos[1])
        neighbors["left"] = (pos[0], pos[1] - 1)
        neighbors["right"] = (pos[0], pos[1] + 1)
        neighbors["bottom"] = (pos[0] + 1, pos[1])
        return neighbors

    def get_next_pos(self, ray):
        """
        gets the next position that the ray wants to move to based on its current pos and direction
        :param ray: Ray object
        :return: a tuple (row,col) that represents position on Board
        """
        cur_pos = ray.get_pos()
        if ray.get_dir() == "move down":
            next_pos = (cur_pos[0] + 1, cur_pos[1])
        elif ray.get_dir() == "move up":
            next_pos = (cur_pos[0] - 1, cur_pos[1])
        elif ray.get_dir() == "move right":
            next_pos = (cur_pos[0], cur_pos[1] + 1)
        elif ray.get_dir() == "move left":
            next_pos = (cur_pos[0], cur_pos[1] - 1)
        else:
            next_pos = None
        return next_pos

    def can_move(self, ray):
        """
        checks if the ray can move to the next square on the board
        :param ray: Ray object
        :return: True if ray can move, otherwise, return False
        """
        next_pos = self.get_next_pos(ray)
        neighbors = self.get_neighbor_pos(next_pos)
        direction = ray.get_dir()

        # check to see if the position that the ray wants to move to has horizontal or vertical neighbors, if yes, then the move is not possible
        if self.is_in_bound(next_pos):
            if direction == "move down" or direction == "move up":
                if neighbors["left"] in self._atoms_pos or neighbors["right"] in self._atoms_pos:
                    return False

            if direction == "move right" or direction == "move left":
                if neighbors["top"] in self._atoms_pos or neighbors["bottom"] in self._atoms_pos:
                    return False
            return True
        return False

    def is_in_bound(self, pos):
        """
        checks if position is on board but non-border
        :param pos: tuple that represents position on board
        :return: True if position is on board and non-border, False if not
        """
        if pos[0] in range(1, 9) and pos[1] in range(1, 9):
            return True

        return False

    def update_direction(self, ray):
        """
        updates direction of ray and does not return anything
        :param ray: Ray object
        """
        next_pos = self.get_next_pos(ray)
        cur_dir = ray.get_dir()
        neighbors = self.get_neighbor_pos(next_pos)  # neighbors of the next position the ray wants to move to
        if cur_dir == "move down" or cur_dir == "move up":
            if neighbors["left"] in self._atoms_pos and neighbors["right"] in self._atoms_pos:
                ray.set_dir(None)  # this represents a double deflection since there are neighbors on both sides
            elif neighbors["left"] in self._atoms_pos:
                ray.set_dir("move right")
            elif neighbors["right"] in self._atoms_pos:
                ray.set_dir("move left")

        if cur_dir == "move right" or cur_dir == "move left":
            if neighbors["top"] in self._atoms_pos and neighbors["bottom"] in self._atoms_pos:
                ray.set_dir(None)  # this represents a double deflection since there are neighbors on both sides
            elif neighbors["top"] in self._atoms_pos:
                ray.set_dir("move down")
            elif neighbors["bottom"] in self._atoms_pos:
                ray.set_dir("move up")

    def find_exit(self, ray):
        """
        finds exit of ray and update the ray's exit, does not return anything
        :param ray: Ray object
        """
        next_pos = self.get_next_pos(ray)
        counter = 0

        # while loop keeps running unless the next pos is on the border or ray hits atom or there's double deflection
        while self.is_in_bound(next_pos):
            counter += 1
            if self.can_move(ray):
                ray.set_pos(next_pos[0], next_pos[1])  # updates cur pos of ray to next pos
                if ray.get_pos() in self._atoms_pos:  # if ray hits atom, function returns, exit updated to None
                    ray.set_exit(None)
                    return
            else:
                self.update_direction(ray)
                if ray.get_dir() is None:  # is ray's direction is None, there's double deflection
                    ray.set_exit(ray.get_entry())  # double deflection means exit is the same as entry
                    return
            next_pos = self.get_next_pos(ray)

        # if while loop was ran only once, then the ray was reflected
        if counter == 1:
            ray.set_exit(ray.get_entry())
            return

        ray.set_exit(next_pos)

# game = BlackBoxGame([(5, 5), (1, 6), (4, 5), (6, 2), (1, 1)])
# game.print_board()
# print("first move")
# print(game.shoot_ray(1,0))
# print(game.get_hits())
# print(game.get_score())
# print("second move")
# print(game.shoot_ray(0,4))
# print(game.get_score())
# print("third move")
# print("guess", game.guess_atom(2,3))
# print(game.get_score())
# print("atoms left",game.atoms_left())
# print("4th move")
# print(game.shoot_ray(5,2))
# print(game.get_score())
# print("5th move")
# print("guess", game.guess_atom(1,6))
# print(game.get_score())
# print("6th move")
# print("guess", game.guess_atom(1,6))
# print(game.get_score())
# print("atoms left",game.atoms_left())
# print("7th move")
# print(game.shoot_ray(8,0))
# print(game.get_score())
# print("8th move")
# print(game.shoot_ray(6,0))
# print(game.get_score())

