import pygame.font  # This module lets Pygame render text to the screen.


class Button:
    """A class to manage an button"""

    def __init__(self, ai_game, msg):
        """Initialize button attributes."""
        self.settings = ai_game.settings
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the button.
        self.width, self.height = 200, 50

        # Text color.
        self.text_color = (0, 0, 0)

        """The 'None' argument tells Pygame to use the default font, and
        48 specifies the size of the text."""
        self.font = pygame.font.SysFont(None, 40)

        # Build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)

        if msg == 'Easy':
            self._button_easy()
        elif msg == 'Medium':
            self._button_medium()
        elif msg == 'Hard':
            self._button_hard()

        """Pygame works with text by rendering the string you want to 
        display as an image.
        We call _prep_msg() to handle this rendering."""
        # The button message needs to be prepped only once.
        self._prep_msg(msg)

    def _button_easy(self):
        """Set colors and set easy button in position."""
        self.button_color = (0, 255, 0)
        self.rect.x = (self.settings.screen_width / 2) - (2 * self.width)
        self.rect.y = (self.settings.screen_height / 2)

    def _button_medium(self):
        """Set colors and set medium button in position."""
        self.button_color = (255, 255, 0)
        self.rect.x = (self.settings.screen_width / 2) - (2 * self.height)
        self.rect.y = (self.settings.screen_height / 2)

    def _button_hard(self):
        """Set colors and set hard button in position."""
        self.button_color = (255, 0, 0)
        self.rect.x = (self.settings.screen_width / 2) + (4 * self.height)
        self.rect.y = (self.settings.screen_height / 2)

    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""

        """The call to 'font.render()' turns the text stored in 'msg' into
        an image, which we then store in 'self.msg_image'. 
        The 'font.render()' method also takes a Boolean value to turn 
        antialiasing on or off (antialiasing makes the edges of the text 
        smoother). 
        We set antaliasing to True and set the text background to the same 
        color as the button. (If you dont include a background color, Pygame
        will try to render the font with a transparent background)."""
        self.msg_image = self.font.render(msg, True, self.text_color,
                                          self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Draw blank button and then draw message."""

        # fill() - fill surface with a solid color
        self.screen.fill(self.button_color, self.rect)

        # blit() - draw image
        self.screen.blit(self.msg_image, self.msg_image_rect)
