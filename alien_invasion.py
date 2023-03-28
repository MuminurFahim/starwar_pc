import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


def run_game():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('Alien Invasion')

    ship = Ship(ai_settings, screen)

    bullets = Group()
    aliens = Group()
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    play_button = Button(screen, 'Play')
    gf.create_fleet(ai_settings, screen, aliens)

    while True:
        gf.check_events(ai_settings, screen, ship, bullets, stats, play_button, aliens, sb)
        if stats.game_active:
            ship.update_ship()
            gf.update_bullets(ai_settings, screen, bullets, aliens, sb, stats, ship)
            gf.update_aliens(ai_settings, screen, bullets, aliens, ship, stats, sb)
        gf.update_screen(ai_settings, screen, ship, aliens, bullets, play_button, stats, sb)


run_game()
