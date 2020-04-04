import sys
from time import sleep

"""SYS MODULE - provides functions that allow us to interact with interpreter
directly like exit the game when the player quits"""

import pygame  # contains the functionality we need to make a game
import json

from ProjetoAlienInvasion.Projeto.settings import Settings
from ProjetoAlienInvasion.Projeto.game_stats import GameStats
from ProjetoAlienInvasion.Projeto.scoreboard import Scoreboard
from ProjetoAlienInvasion.Projeto.button import Button
from ProjetoAlienInvasion.Projeto.ship import Ship
from ProjetoAlienInvasion.Projeto.bullet import Bullet
from ProjetoAlienInvasion.Projeto.alien import Alien


class AlienInvasion:
    """Overall class to manage game assets and behavior"""

    def __init__(self):
        """Initialize the game, and create game resources"""

        # This function initializes the background settings that Pygame needs to work properly
        pygame.init()

        # Here we create a instance of Settings
        self.settings = Settings()

        """self.screen - create a display window, on which we'll draw all the game's 
           graphical elements. The argument (1200, 800) is a tuple that defines the dimensions
           of the game window. pygame.display.set_mode represents the entire game window
           - Surface is like a blank piece of paper, we create a special surface with:"""
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))

        """full screen mode, the (0, 0) tells pygame to figure out a window
        size that fill the screen."""
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        """We use the 'width' and 'height' attributes of the screen's
        rect to update the 'settings' object"""
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height

        # set the pygame window name
        pygame.display.set_caption('Alien Invasion')

        """We make the instance after creating the game window but before
        defining other game elements, such as the ship."""
        # Create an instance to store game statistics,
        #  and create a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        """we create a instance of Ship after the screen has been created.
        The call to Ship() requires one argument, an instance of 
        AlienInvasion."""
        self.ship = Ship(self)

        """-This group will be an instance of the 'pygame.sprite.Group()'
        class, which behaves like a list with some extra functionality that's
        helpful when building games. Store all the live bullets so we can
        manage the bullets that have already been fired.
        -I cannot add sprites to sprite groups unless they inherit from the
        Sprite class. This is useful because I can now do things like update
        all the sprites in the group and them all with one function."""
        self.bullets = pygame.sprite.Group()  # define a group

        # We create a group to hold the fleet of aliens
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Make buttons.
        self.easy_button = Button(self, 'Easy')
        self.medium_button = Button(self, 'Medium')
        self.hard_button = Button(self, 'Hard')

    def run_game(self):
        """The game is controlled by this method.
        Start the main loop for the game"""
        while True:
            """To call a method from within a class, use dot notation
            with the variable 'self' and the name of the method. We call
            the method from inside the 'while' loop in 'run_game()'."""
            # Main Program
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            
            self._update_screen()

    """A 'helper method' does work inside a class but isn't meant to be 
    called through an instance. In python, a single leading underscore 
    indicates a helper method."""
    def _check_events(self):
        """Respond to key presses and mouse events"""
        """-A event is an action that the user performs while playing the game,
        such as pressing a key or moving the mouse.
        -We write this 'event loop' to 'listen' for events and perform appropriate
        tasks depending on the kinds of events that occur. The 'for' loop is an
        event loop.
        -To access the events that pygame detects, we'll use the
        'pygame.event.get()' function. This function returns a list of
        events that have taken place since the last time this function was called."""
        for event in pygame.event.get():  # watch for keyboard and mouse events
            if event.type == pygame.QUIT:  # when the player clicks the game window's close button is 'pygame.QUIT'
                if self.stats.score >= self.stats.high_score:
                    with open('highscore.json', 'w') as f:
                        json.dump(self.stats.high_score, f)
                sys.exit()  # the interpreter will close the game

            # Each keypress is registered as a KEYDOWN event.
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            # when the player releases the right arrow key
            elif event.type == pygame.KEYUP:  # type event
                self._check_keyup_events(event)

            # when the player clicks anywhere on the screen.
            # we want to restrict our game to respond to mouse clicks only on the PLAY button.
            elif event.type == pygame.MOUSEBUTTONDOWN:
                """We use 'pygame.mouse.get_pos()' which returns a tuple 
                containing the mouse cursor's x- and y-coordinates when the
                mouse button is clicked"""
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the players selects a certain difficulty."""

        """We use the 'rect' method 'collidepoint()' to check whether the
        point of the mouse click overlaps the region defined by the PLAY 
        button's 'rect'"""
        easy_clicked = self.easy_button.rect.collidepoint(mouse_pos)
        medium_clicked = self.medium_button.rect.collidepoint(mouse_pos)
        hard_clicked = self.hard_button.rect.collidepoint(mouse_pos)

        self._check_difficulty(easy_clicked, medium_clicked, hard_clicked)

    def _check_difficulty(self, easy_clicked, medium_clicked, hard_clicked):
        """Increases speedup_scale consonant difficulty selected."""
        if easy_clicked and not self.stats.game_active:
            self.settings.speedup_scale = 1.1
            self.settings.initialize_dynamic_settings()
            self._start_game()

        if medium_clicked and not self.stats.game_active:
            self.settings.speedup_scale = 1.2
            self.settings.initialize_dynamic_settings()
            self._start_game()

        if hard_clicked and not self.stats.game_active:
            self.settings.speedup_scale = 1.3
            self.settings.initialize_dynamic_settings()
            self._start_game()

    def _start_game(self):
        """Reset Alien Invasion and activate the game"""
        # Reset the game statistics.
        self.stats.reset_status()

        self.stats.game_active = True
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()

        # get rid of any remaining aliens and bullets.
        self.aliens.empty()
        self.bullets.empty()

        # Create a new fleet and center the ship.
        self._create_fleet()
        self.ship.center_ship()

        # Hide the mouse cursor
        pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """responds to key presses"""
        if event.key == pygame.K_RIGHT:  # if right arrow key was pressed
            self.ship.moving_right = True

        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True

        elif event.key == pygame.K_q:  # if I press the 'q' key the game closes
            sys.exit()

        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

        elif event.key == pygame.K_p:
            self._start_game()

    def _check_keyup_events(self, event):
        """responds to key releases"""
        if event.key == pygame.K_RIGHT:  # key event
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # update bullet positions.
        self.bullets.update()  # calls the update function on all sprites in group

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.

        """- The 'sprite.groupcollide()' function compares the rects of each
        element in one group with the rects of each element in another group.
        - The two 'True' arguments tell Pygame to delete the bullets and aliens
        that have collided."""
        # Check for any bullets that have hit aliens.
        #  If so, get rid of the bullet and the alien.
        # Bullets are KEYS and aliens are values.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        """We'll perform th is check at the end of _update_bullets(),
        because that's where individual aliens are destroyed.
        An empty group evaluates to 'False', so this is a simple way to check
        whether the group is empty."""
        # Repopulating the fleet.
        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level.
            self.stats.level += 1
            self.sb.prep_level()

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and find the number of aliens in a row.
        # Spacing between each alien is equal to one alien width.
        alien = Alien(self)

        # Attribute 'size', contains a tuple with the width and height of a rect object.
        alien_width, alien_height = alien.rect.size

        ship_height = self.ship.rect.height

        """To figure out how many aliens fit in a row, let's look at how 
        much space we have. The screen width is stored in 'settings.screen.
        width', but we need an empty margin on either side of the screen.
        We'll make this margin the width of one alien. Because we have two
        margins, the available space for aliens is the screen width minus 
        two alien widths."""
        # Calculate the horizontal space available for aliens
        available_space_x = self.settings.screen_width - (2 * alien_width)

        """We also need to set the spacing between aliens; We'll make it one
        alien width. The space needed to display one alien is twice its 
        width: one width for the alien and one width for the empty space to
        its right. To find the number of aliens that fit across the screen,
        we divide the available space by two times the width of an alien.
        We use 'floor division (//)', which divides two numbers and drops
        any reminder, so we'll get an integer number of aliens."""
        # Number of aliens that can fit into that space.
        number_aliens_x = available_space_x // (2 * alien_width)

        """To determine the number of rows, we find the available vertical
        space by subtracting the alien height from the top, the ship height
        from the bottom, and two alien heights from the bottom of the screen"""
        # determine height screen available for we can know the number of rows available
        # calculations with more over two lines is recommended use parentheses.
        available_space_y = (self.settings.screen_height -
                             (3 * alien_height) - ship_height)

        """Each row needs some empty space below it, which we'll make equal
        to the height of one alien. To find the number of rows, we divide 
        the available space by two times the height of an alien."""
        number_rows = available_space_y // (2 * alien_height)

        # create a full fleet of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        """We multiply the alien width by 2 to account for the space
        each alien takes up, including the empty space to its right,
        and we multiply this amount by the alien's position in the row."""
        alien.x = alien_width + 2 * alien_width * alien_number

        # We use the alien's 'x' attribute to set the position of its rect
        alien.rect.x = alien.x

        alien.rect.y = alien_height + 2 * alien_height * row_number

        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_aliens(self):
        """Check if the fleet is at an edge,
        then update the positions of all aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()

        """The 'spritecollideany()' takes two arguments: a sprite and a 
        group. The functions looks for any member of the group that has
        collided with the sprite and stops looping through the group as
        soon as it finds one member that has collided with the sprite.
        Here, it loops through the group aliens and returns the first 
        alien it finds that has collided with ship.
        If no collisions occur, 'spritecollideany()' returns 'None' and
        the 'if' block at won't execute."""
        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # Decrement ships_left, and update scoreboard.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause.
            sleep(0.5)
        else:
            self.stats.game_active = False

            # Show the mouse cursor.
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Check if any aliens have reached"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _update_screen(self):
        """update images on the screen, and flip to the new screen"""
        # redraw the screen during each pass through the loop
        self.screen.fill(self.settings.bg_color)

        # Here we call blitme() to draw the ship on the screen
        self.ship.blitme()

        # Draw the bullets on the screen
        """bullets.sprites returns a list of all sprites in the group bullets"""
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        """When we call draw() on a group, Pygame draws each element in the
        group at the position defined by its rect attribute. The draw() 
        method requires one argument: a surface on which to draw the elements
        from the group."""
        self.aliens.draw(self.screen)

        # Draw the score information.
        self.sb.show_score()

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.easy_button.draw_button()
            self.medium_button.draw_button()
            self.hard_button.draw_button()

        # update the contents of the entire display
        pygame.display.flip()


if __name__ == '__main__':
    # make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()
