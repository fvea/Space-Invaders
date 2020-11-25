import pygame
from pygame.sprite import Group 

from settings import Settings
from ship import Ship
import game_functions as gf
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


def run_game(): 
    
    # Initialize pygame, clock, settings, and screen object.
    pygame.init()
    clock = pygame.time.Clock()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_icon(ai_settings.icon)
    pygame.display.set_caption(ai_settings.title)

    # Make a Play Button
    play_button = Button(screen)
    # Create an instance to store game statistics and create a scoreboard.
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings,screen,stats)

    # Make a ship, a group of bullets, and a group of aliens.
    ship = Ship(ai_settings,screen)
    bullets = Group()
    aliens = Group()

    # Create the fleet of aliens.
    gf.create_fleet(ai_settings,aliens,screen,ship)

    # Start the main loop for the game.
    while True:
        clock.tick(ai_settings.FPS) 
        gf.check_events(ai_settings,aliens,bullets,screen,ship,stats,play_button,sb)

        if stats.game_active: 
            ship.update()
            gf.update_bullets(ai_settings,aliens,bullets,sb,screen,ship,stats)
            gf.update_aliens(ai_settings,aliens,bullets,screen,ship,stats,sb)
            
        gf.update_screen(ai_settings,aliens,bullets,sb,screen,ship,stats,play_button)


run_game()