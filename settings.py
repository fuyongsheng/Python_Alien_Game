class Settings():
    # Class for store all settings of alien invasion

    def __init__(self):
        # initialize game's settings
        # screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Settings of ship
        self.ship_speed_factor = 7
        self.ship_limit = 3

        # Settings of bullet
        self.bullet_speed_factor = 3
        self.bullet_width = 1200
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 99999

        # Settings of aliens
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 100
        # fleet_direction == 1 denotes right, 0 denotes left
        self.fleet_direction = 1

        # Speed up
        self.speedup_scale = 1.1
        # Score scale as speed up
        self.score_scale = 2

        self.initialize_dynamic_settings()


    def initialize_dynamic_settings(self):
        # Dynamic changing as game going
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 10
        self.alien_speed_factor = 1

        # fleet_direction == 1 denotes right, 0 denotes left
        self.fleet_direction = 1

        # Count score
        self.alien_points = 50

    def increase_speed(self):
        # Increase speed settings and score
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)

