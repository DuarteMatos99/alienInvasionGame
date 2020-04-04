import json


class GameStats:
    """Track statistics for Alien Invasion"""

    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_status()

        # Start Alien Invasion in an inactive state.
        self.game_active = False

        # High score should never be reset.
        with open('highscore.json') as f:
            self.high_score = json.load(f)

    def reset_status(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1