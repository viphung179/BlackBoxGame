import pygame
import BlackBox
import random

# colors:
white = (255, 255, 255)
black = (0, 0, 0)
grid_color = black
board = white
button_background = (191, 138, 84)
button_outline = black
border = (132, 82, 62)
win_color = (228, 76, 76)
screen_color = (242, 175, 94)

# constants
WIDTH = 400
HEIGHT = 400
tile_size = WIDTH // 10
button_align_w = 500
button_align_h = 150

# images and surfaces
w_page = pygame.image.load("welcomebg.jpg")
about_image = pygame.image.load("aboutpage.jpg")
flower_outline = pygame.image.load("outlineflower.png")
atom = pygame.image.load("smallflower.png")  # "Icon made by Freepik from www.flaticon.com"
atom = pygame.transform.scale(atom, (WIDTH // 10 - 4, HEIGHT // 10 - 4))
wrong = pygame.image.load("wrong.png")  # "Icon made by Pixelmeetup from www.flaticon.com"
wrong = pygame.transform.scale(wrong, (WIDTH // 10 - 4, HEIGHT // 10 - 4))
correct = pygame.image.load("correct.png")  # "Icon made by Pixelmeetup from www.flaticon.com"
correct = pygame.transform.scale(correct, (WIDTH // 10 - 4, HEIGHT // 10 - 4))
gray_out_atom = pygame.Surface((WIDTH // 10, HEIGHT // 10))
gray_out_atom.set_alpha(128)
gray_out_atom.fill(white)
main_bg_fill = pygame.Surface((WIDTH + 345, HEIGHT + 130))
main_bg_fill.set_alpha(220)
main_bg_fill.fill(screen_color)
icon = pygame.image.load("smallflower.png")
board_fill = pygame.Surface((WIDTH - tile_size, HEIGHT - tile_size))
board_fill.set_alpha(200)
board_fill.fill(white)


class Button:
    """
    represents buttons on screen
    """

    def __init__(self, color, x, y, width, height, font, text=''):
        self.color = color
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._text = text
        self._font = font

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self._x - 2, self._y - 2, self._width + 4, self._height + 4), 0)

        pygame.draw.rect(win, self.color, (self._x, self._y, self._width, self._height), 0)

        if self._text != '':
            text = self._font.render(self._text, True, black)
            win.blit(text, (
                self._x + (self._width // 2 - text.get_width() // 2),
                self._y + (self._height // 2 - text.get_height() // 2)))

    def is_over(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self._x and pos[0] < self._x + self._width:
            if pos[1] > self._y and pos[1] < self._y + self._height:
                return True

        return False


class BoardDisplay:
    """
    represents game board
    """

    def __init__(self, x, y, width, height):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._tile_w = width // 10
        self._tile_h = height // 10
        self._hover_active = True
        self._deflect_color = None
        self._end_game = False

    def draw_board(self):
        screen.fill(white)
        screen.blit(flower_outline, (500, 5))
        screen.blit(flower_outline, (-100, -150))
        screen.blit(flower_outline, (100, 400))
        screen.blit(main_bg_fill, (0, 0))
        screen.blit(board_fill, (self._x + tile_size, self._y + tile_size))

        # color border
        top = pygame.Rect(self._x, self._y, self._width, self._height // 10)
        left = pygame.Rect(self._x, self._y, self._width // 10, self._height)
        bottom = pygame.Rect(self._x, self._y + self._height // 10 * 9, self._width, self._height // 10)
        right = pygame.Rect(self._x + self._width // 10 * 9, self._y, self._width // 10, self._height)
        screen.fill(border, top)
        screen.fill(border, left)
        screen.fill(border, bottom)
        screen.fill(border, right)

    def draw_grid(self):
        for i in range(11):
            pygame.draw.line(screen, grid_color, [self._x + (i * self._width // 10), self._y],
                             [self._x + (i * self._width // 10), self._y + self._height], 1)
            pygame.draw.line(screen, grid_color, [self._x, (i * self._height // 10) + self._y],
                             [self._x + self._width, (i * self._width // 10) + self._y], 1)

    def show_guessed_atoms(self):
        """
        shows guess selection on board
        """
        if guess_box.get_pre_guesses() is not None:  # shows guesses before confirming
            for pre_guess in guess_box.get_pre_guesses():
                coord_h = get_screen_coord("y", pre_guess[0])
                coord_w = get_screen_coord("x", pre_guess[1])
                screen.blit(atom, (coord_w + 3, coord_h + 3))

        if game.get_guesses() is not None:  # shows guesses after confirming
            for pos in game.get_atoms():  # shows all flowers
                coord_h = get_screen_coord("y", pos[0])
                coord_w = get_screen_coord("x", pos[1])
                if pos in guess_box.get_pre_guesses():  # shows correct guess
                    screen.blit(gray_out_atom, (coord_w + 3, coord_h + 3))
                    screen.blit(correct, (coord_w + 3, coord_h + 3))

                else:
                    screen.blit(atom, (coord_w + 3, coord_h + 3))  # shows flower that wasn't guessed

            for guess in game.get_guesses():  # shows wrong guesses
                coord_h = get_screen_coord("y", guess[0])
                coord_w = get_screen_coord("x", guess[1])
                if guess not in game.get_atoms():
                    screen.blit(gray_out_atom, (coord_w + 3, coord_h + 3))
                    screen.blit(wrong, (coord_w + 3, coord_h + 3))

    def show_ray_hits(self):
        """
        shows entry of ray as black if ray hits flower
        """
        if game.get_hits() is not None:
            if len(game.get_hits()) > 0:
                for hit in game.get_hits():
                    self.draw_ray(hit[1], hit[0], black)

    def show_ray_reflects(self):
        """
        shows entry of ray as white if ray was reflected
        """
        if game.get_reflects() is not None:
            if len(game.get_reflects()) > 0:
                for reflect in game.get_reflects():
                    self.draw_ray(reflect[1], reflect[0], white)

    def show_deflect(self):
        """
        shows entry and exit of ray as random color if ray was deflected
        """
        if self._deflect_color is not None:
            for pos in self._deflect_color:
                self.draw_ray(pos[1], pos[0], self._deflect_color[pos])

    def show_hover(self, pos):
        """
        shows hover effect if mouse is over button or board
        """
        w_start = 2000
        h_start = 2000
        tl = (self._x, self._y)
        tr = (self._x + (9 * self._width // 10), self._y)
        bl = (self._x, self._y + (9 * self._height // 10))
        br = (self._x + (9 * self._width // 10), self._y + (9 * self._height // 10))
        corner_coords = [tl, tr, bl, br]

        if new_game_b.is_over(pos):
            my_rect = pygame.Surface((new_game_b.get_width(), new_game_b.get_height()))
            my_rect.set_alpha(50)
            screen.blit(my_rect, (new_game_b.get_x(), new_game_b.get_y()))

        if about_b.is_over(pos):
            my_rect = pygame.Surface((about_b.get_width(), about_b.get_height()))
            my_rect.set_alpha(50)
            screen.blit(my_rect, (about_b.get_x(), about_b.get_y()))

        if self._hover_active is True:  # shows hover effect on board
            for i in range(10):
                if self._x + i * self._width // 10 <= pos[0] < self._x + (i + 1) * self._width // 10:
                    w_start = self._x + i * self._width // 10
                if self._y + i * self._height // 10 <= pos[1] < self._y + (i + 1) * self._height // 10:
                    h_start = self._y + i * self._height // 10

            if (w_start, h_start) not in corner_coords:
                screen_w = pygame.display.get_surface().get_width()
                screen_h = pygame.display.get_surface().get_height()
                if w_start < screen_w and h_start < screen_h:
                    my_rect = pygame.Surface((self._tile_w, self._tile_h))
                    my_rect.set_alpha(50)
                    screen.blit(my_rect, (w_start, h_start))

            if make_guess_b.is_over(pos):
                my_rect = pygame.Surface((make_guess_b.get_width(), make_guess_b.get_height()))
                my_rect.set_alpha(50)
                screen.blit(my_rect, (make_guess_b.get_x(), make_guess_b.get_y()))

    def inactive_hover(self):
        """
        deactivates hover effect
        """
        self._hover_active = False

    def draw_ray(self, x, y, color):
        """
        draws circle on ray entries and exits, used in show_ray_hits, show_deflects, and show_ray_reflect methods
        """
        coord_h = get_screen_coord("y", y)
        coord_w = get_screen_coord("x", x)
        my_rect = pygame.Rect(coord_w, coord_h, self._tile_w, self._tile_h)
        pygame.draw.rect(screen, border, my_rect)
        pygame.draw.circle(screen, color,
                           (coord_w + tile_size // 2, coord_h + tile_size // 2),
                           tile_size // 2 - 5)
        pygame.draw.circle(screen, black,
                           (coord_w + tile_size // 2, coord_h + tile_size // 2),
                           tile_size // 2 - 4, 1)

    def update_board(self):
        self.show_guessed_atoms()
        self.show_ray_hits()
        self.show_ray_reflects()
        self.show_deflect()
        self.draw_grid()

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_width(self):
        return self._width

    def set_deflect_color(self, pos, color):
        if self._deflect_color is None:
            self._deflect_color = {}

        if pos not in self._deflect_color:
            self._deflect_color[pos] = color

    def set_end_game(self, ended):
        self._end_game = ended

    def get_end_game(self):
        return self._end_game


class AtomsBox:
    def __init__(self, display):
        self._display = display
        self._atoms_left = 4
        self._pre_guesses = None
        self._invalid_guess = False

    def draw(self, x, y):
        box = pygame.Rect(x - 5, y - 5, tile_size * 4 - 5, tile_size + 5)
        pygame.draw.rect(screen, white, box)
        pygame.draw.rect(screen, black, box, 2)
        if self._pre_guesses is not None:
            self._atoms_left = 4 - len(self._pre_guesses)
        for i in range(self._atoms_left):
            screen.blit(atom, (x, y))
            x += atom.get_width()

    def set_pre_guesses(self, pos):
        if self._pre_guesses is None:
            self._pre_guesses = []

        self._pre_guesses.append(pos)

    def get_pre_guesses(self):
        return self._pre_guesses

    def invalid_guess(self):
        return self._invalid_guess

    def set_invalid_guess(self, validity):
        self._invalid_guess = validity


def get_init_pos():
    """
    generates random flower positions on board
    """
    atoms_pos = []
    while len(atoms_pos) < 4:
        row = random.randint(1, 8)
        col = random.randint(1, 8)
        if (row, col) not in atoms_pos:
            atoms_pos.append((row, col))

    return atoms_pos


def get_rand_color():
    """
    generates a random color
    """
    R = random.randint(0, 256)
    G = random.randint(0, 256)
    B = random.randint(0, 256)
    return (R, G, B)


def get_board_coord(x_or_y, screen_coord):
    """
    takes in screen coordinates and returns position on board
    """
    if x_or_y == "x":
        start = game_board.get_x()
    else:
        start = game_board.get_y()
    stop = start + game_board.get_width() // 10
    found = False
    board_coord = 0
    while not found:
        if screen_coord in range(start, stop):
            found = True
            return board_coord
        else:
            board_coord += 1
            start = stop
            stop += game_board.get_width() // 10


def get_screen_coord(x_or_y, board_coord):
    """ takes board position and returns screen coordinates"""
    if x_or_y == "x":
        screen_coord = game_board.get_x()
    else:
        screen_coord = game_board.get_y()

    start = 0
    stop = 1
    found = False
    while not found:
        if board_coord in range(start, stop):
            found = True
            return screen_coord
        else:
            screen_coord += game_board.get_width() // 10
            start = stop
            stop += 1


def eval_board_click(x, y):
    """evaluates mouse click"""
    row = get_board_coord("y", y)
    col = get_board_coord("x", x)
    guess_box.set_invalid_guess(False)
    deflect_color = get_rand_color()
    print("color", game_board._deflect_color)

    if not game_board.get_end_game() and not show_about:
        if make_guess_b.is_over((x, y)):  # if guess button is clicked
            if guess_box.get_pre_guesses() is None or len(guess_box.get_pre_guesses()) < 4:
                guess_box.set_invalid_guess(True)
            else:
                guess_box.set_invalid_guess(False)
                for guess in guess_box.get_pre_guesses():
                    game.guess_atom(guess[0], guess[1])
                game_board.inactive_hover()  # disable hover
                game_board.set_end_game(True)
        else:
            if x < game_board.get_x() + game_board.get_width() and y < game_board.get_y() + game_board.get_width():
                if game.get_board().is_in_bound((row, col)):
                    guess = (row, col)
                    if guess_box.get_pre_guesses() is None:
                        guess_box.set_pre_guesses(guess)
                    else:
                        if guess not in guess_box.get_pre_guesses():
                            if len(guess_box.get_pre_guesses()) < 4:
                                guess_box.set_pre_guesses(guess)
                        else:
                            guess_box.get_pre_guesses().remove(guess)
                else:
                    shoot = game.shoot_ray(row, col)
                    if shoot[0] != shoot[1] and shoot[1] is not None:  # set color for deflection
                        game_board.set_deflect_color(shoot[0], deflect_color)
                        game_board.set_deflect_color(shoot[1], deflect_color)

    # print(game.get_board().get_atoms_pos())
    # print("guesses ", game.get_guesses())
    # print("hits", game.get_hits())
    # print("reflects", game.get_reflects())
    # print("preguesses", guess_box.get_pre_guesses())


def game_intro():
    intro = True

    while intro:
        screen.blit(w_page, (0, 0))
        pygame.display.update()
        pygame.time.wait(2000)
        intro = False


def message_to_screen(msg, font, color, pos):
    screen_text = font.render(msg, True, color)
    screen.blit(screen_text, pos)


def about_page():
    screen.blit(about_image, (0, 0))
    back_to_game_b.draw(screen, black)


def update_score():
    score = "Score: " + str(game.get_score())
    return score


def draw_buttons():
    new_game_b.draw(screen, button_outline)
    score_b = Button(button_background, button_align_w, button_align_h + 100, 200, 40, font, update_score())
    score_b.draw(screen, button_outline)
    make_guess_b.draw(screen, button_outline)
    about_b.draw(screen, button_outline)


pygame.init()

game = BlackBox.BlackBoxGame(get_init_pos())
game_board = BoardDisplay(50, 50, WIDTH, HEIGHT)

# fonts
font = pygame.font.Font("IndieFlower-Regular.ttf", 25)
guess_font = pygame.font.Font("Raleway-Medium.ttf", 15)
win_font = pygame.font.Font("IndieFlower-Regular.ttf", 30)
about_font = pygame.font.Font("IndieFlower-Regular.ttf", 15)
welcome_font = pygame.font.Font("IndieFlower-Regular.ttf", 75)

# title and icon
pygame.display.set_caption("Black Box Game")
pygame.display.set_icon(icon)

# Buttons
new_game_b = Button(button_background, button_align_w, button_align_h, 200, 40, font, "New Game")
make_guess_b = Button(button_background, button_align_w, button_align_h + 50, 200, 40, font, "Confirm Guesses")
about_b = Button(button_background, WIDTH + 243, 2, 100, 20, about_font, "About")
back_to_game_b = Button(button_background, WIDTH + 243, 2, 100, 20, about_font, "Back to Game")

# Flower box
guess_box = AtomsBox(game_board)

running = True

intro = True
show_about = False

while running:
    screen = pygame.display.set_mode((WIDTH + 345, HEIGHT + 130))

    if intro:
        game_intro()
        intro = False

    game_board.draw_board()
    draw_buttons()
    game_board.show_hover((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))

    if game.get_status() != "started":
        message_to_screen(game.get_status(), win_font, black,
                          (button_align_w - 15, button_align_h + 160))
    else:
        guess_box.draw(button_align_w + 28, button_align_h + 160)

    if guess_box.invalid_guess() is True:
        message_to_screen("Place all four guesses on board before confirming guesses!", guess_font, black,
                          (game_board.get_x(), game_board.get_y() + game_board.get_width() + 10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if pygame.mouse.get_pressed()[0]:
            if new_game_b.is_over(pygame.mouse.get_pos()):
                game = BlackBox.BlackBoxGame(get_init_pos())
                game_board = BoardDisplay(50, 50, WIDTH, HEIGHT)
                guess_box = AtomsBox(game_board)
            elif about_b.is_over(pygame.mouse.get_pos()) or back_to_game_b.is_over(pygame.mouse.get_pos()):
                show_about = not show_about
            else:
                eval_board_click(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

    game_board.update_board()

    if show_about:
        about_page()

    pygame.display.update()
