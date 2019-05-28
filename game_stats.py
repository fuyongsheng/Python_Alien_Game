class GameStats():
# Track game's status

    def __init__(self, ai_settings):
        # Initialize information
        self.ai_settings = ai_settings
        self.reset_stats()

        # Inactive when game start
        self.game_active = False
        # Do not reset highest score anytime
        self.high_score = 0

    def reset_stats(self):
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1