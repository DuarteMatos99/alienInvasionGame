import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """A class to manage the ship"""

    def __init__(self, ai_game):
        """Initialize the ship and set its starting position"""
        """'ai_game' will reference the current instance of the
        AlienInvasion class. This will give 'Ship'
        access to all game resources defined in AlienInvasion"""
        super().__init__()

        # we assign the screen to an attribute of Ship
        self.screen = ai_game.screen

        """we access the screen's rect attribute using the get_rect()
        method and assign it to 'self.screen_rect'. Doing this allow us
        to place the ship in the correct location on the screen."""
        self.screen_rect = ai_game.screen.get_rect()

        # load the ship image and get its rect.
        """Here we create a new surface with 'pygame.image.load'"""
        self.image = pygame.image.load('Images/red_ship.bmp')

        # we access the image rect attribute using the 'get_rect()'
        self.rect = self.image.get_rect()

        # start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        """when the 'moving_right' flag is False, the ship will be freeze.
        when the player presses the right arrow key, we'll set the flag to
        True, and when the player releases the key, we'll set the flag to
        False again."""
        self.moving_right = False
        self.moving_left = False

        # this attribute give us access to Settings class.
        self.settings = ai_game.settings

        # store a decimal value for the ship's horizontal position because 'rect' only can keep the integer
        self.x = float(self.rect.x)

    def update(self):
        """update the ship's position based on the movement flag(moving_right
        and moving_left)"""

        # update the ship's x value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed

        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # update rect object from self.x for our ship can move
        self.rect.x = self.x

    def blitme(self):
        """draw the ship at its current location."""
        """Pygame has a display Surface. This is basically an image
        that is visible on the screen, and the image is made up of pixels.
        The main way you can change these pixels is by calling the 'blit()'
        function. This copies the pixels from one image onto another."""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center the ship on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom

        """After centering it, we reset the 'self.x' attribute, which allow
        us to track the ship's exact position."""
        self.x = float(self.rect.x)
