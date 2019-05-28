import sys

import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
import game_functions as gf

def run_game():
	# Initialze game & create an screen object
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Create play button
    play_button = Button(ai_settings, screen, "Play")
    # Create an instance for stat & scoreboard
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    # Create a ship
    ship = Ship(ai_settings, screen)
    # Create a group of storing bullet
    bullets = Group()
    # Create a group of alien
    aliens = Group()

    gf.create_fleet(ai_settings, screen, ship, aliens)

	# Loop of start game
    while True:
		# Monitor keyboard and mouse events
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)


        if stats.game_active:
            # Update the position of ship
            ship.update()

            # Update and delete bullets
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)

            # Update position of alien
            gf.update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets)

        # Draw the screen each time & Make the screen visiable
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)

run_game()