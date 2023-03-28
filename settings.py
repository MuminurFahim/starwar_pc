class Settings():
    """all settings for game"""

    def __init__(self):
        self.screen_width = 1100
        self.screen_height = 680
        self.bg_color = (222, 222, 222)

        self.ship_speed_factor = 2
        self.ship_limit = 3

        self.bullet_speed_factor = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3

        self.alien_speed_factor = 1
        self.fleet_drop_speed = 10

        # self.direction = 1 means going right
        # self.direction = -1 means going left
        self.direction = 1

        self.speedup_scale = 1.1
        self.score_scale = 10

        self.dynamic_settings()

    def dynamic_settings(self):
        self.ship_speed_factor = 2
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 10
        self.direction = 1
        self.alien_points = 10

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.fleet_drop_speed *= self.speedup_scale
        self.alien_points += self.score_scale
