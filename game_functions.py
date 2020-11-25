import sys
from time import sleep

import pygame

from bullet import Bullet
from alien import Alien


def check_events(ai_settings,aliens,bullets,screen,ship,stats,play_button,sb):
    """Respond to keypresses and mouse events.""" 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(ai_settings,aliens,bullets,event,screen,ship,stats,sb)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)
        elif event.type == pygame.MOUSEBUTTONDOWN: 
            mouse_X, mouse_Y = pygame.mouse.get_pos()
            check_play_button(ai_settings,aliens,bullets,
                    mouse_X,mouse_Y,play_button,stats,ship,screen,sb)

def check_keydown_events(ai_settings,aliens,bullets,event,screen,ship,stats,sb):
    """Respond to keypresses.""" 
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT: 
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings,bullets,screen,ship)
    elif event.key == pygame.K_q: 
        sys.exit()
    elif event.key == pygame.K_p: 
        start_game(ai_settings,aliens,bullets,stats,ship,screen,sb)
    
def check_keyup_events(event,ship):
    """Respond to key releseases."""
    if event.key == pygame.K_RIGHT: 
        ship.moving_right = False
    elif event.key == pygame.K_LEFT: 
        ship.moving_left = False

def start_game(ai_settings,aliens,bullets,stats,ship,screen,sb):
    """Start a new game when the player clicks Play or Press P."""
    if not stats.game_active:
        # Reset the game settings.
        ai_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        # Reset the game statistics.
        stats.reset_stats()
        stats.game_active = True
        # Reset the scoreboard images.
        sb.prep_score()
        sb.prep_level()
        sb.prep_ships()
        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()
        # Create a new fleet and center the ship.
        create_fleet(ai_settings,aliens,screen,ship)
        ship.center_ship()
 
def check_play_button(ai_settings,aliens,bullets,
            mouse_X,mouse_Y,play_button,stats,ship,screen,sb): 
    """Start a new game when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_X,mouse_Y)
    if button_clicked:
        start_game(ai_settings,aliens,bullets,stats,ship,screen,sb)

def fire_bullet(ai_settings,bullets,screen,ship):
    """Fire a bullet if limit not reached yet.""" 
    #Create a new bullet and add it to the bullets group.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings,screen,ship)
        bullets.add(new_bullet)

def check_high_score(sb,stats):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score: 
        stats.high_score = stats.score
        sb.prep_high_score()
        with open('highscore.txt', 'w') as f_obj: 
            f_obj.write(str(stats.high_score))

def check_bullet_alien_collision(ai_settings,aliens,bullets,sb,screen,ship,stats):

    collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)

    if collisions:
        for aliens in collisions.values(): 
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(sb,stats)

    if len(aliens) == 0:
        # If the entire fleet is destroyed, start a new level.
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings,aliens,screen,ship)
        # Increase level.
        stats.level += 1
        sb.prep_level()

def update_bullets(ai_settings,aliens,bullets,sb,screen,ship,stats):
    """Update position of bullets and get rid of old bullets."""
    # Update bullet positions. 
    bullets.update()

    # Check for any bullets that have hit aliens.
    check_bullet_alien_collision(ai_settings,aliens,bullets,sb,screen,ship,stats)

    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy(): 
        if bullet.rect.bottom <= 0: 
            bullets.remove(bullet)
            
def check_fleet_edges(ai_settings,aliens):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges(): 
            change_fleet_direction(ai_settings,aliens)
            break

def change_fleet_direction(ai_settings,aliens):
    """Drop the entire fleet and change the fleet's direction."""
    for alien in aliens.sprites(): 
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings,aliens,bullets,screen,ship,stats,sb):
    """Respond to ship being hit by alien."""

    if stats.ship_left > 0: 
        # Decrement ships_left.
        stats.ship_left -= 1
        # Update scoreboard.
        sb.prep_ships()
        # Empty the list of aliens and bullets.
        bullets.empty()
        aliens.empty()
        # Create a new fleet and center the ship.
        create_fleet(ai_settings,aliens,screen,ship)
        ship.center_ship()
        # Pause.
        sleep(0.5)
    else: 
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings,aliens,bullets,screen,ship,stats,sb): 
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites(): 
        if alien.rect.bottom >= screen_rect.bottom: 
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings,aliens,bullets,screen,ship,stats,sb)
     
def update_aliens(ai_settings,aliens,bullets,screen,ship,stats,sb): 
    """
    Check if the fleet is at an edge,
    and then update the postions of all aliens in the fleet.
    """
    check_fleet_edges(ai_settings,aliens)
    aliens.update()
    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(ai_settings,aliens,bullets,screen,ship,stats,sb)
    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship,aliens): 
        ship_hit(ai_settings,aliens,bullets,screen,ship,stats,sb)

def get_number_alien_x(ai_settings,alien_width):
    """Determine the number of aliens that fit in a row."""
    available_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_x / (2*alien_width))
    return number_aliens_x

def create_alien(ai_settings,aliens,alien_number,screen,row_number):
    """Create an alien and place it in the row."""
    alien = Alien(ai_settings,screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_number * alien_width
    alien.rect.y = alien.rect.height + 25 + 2 * row_number * alien.rect.height
    alien.rect.x = alien.x 
    aliens.add(alien)

def get_number_rows(ai_settings,ship_height,alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_y = ai_settings.screen_height - 7 * alien_height - ship_height
    number_of_rows = int(available_y / (2*alien_height))
    return number_of_rows

def create_fleet(ai_settings,aliens,screen,ship): 
    """Create a full fleet of aliens."""
    # Create an alien and find the number of aliens in a row.
    # Spacing between each alien is equal to one alien width.
    alien = Alien(ai_settings,screen)
    number_aliens_x = get_number_alien_x(ai_settings,alien.rect.width)
    number_of_rows = get_number_rows(ai_settings,ship.rect.height,
    alien.rect.height)

    # Create the fleet of aliens.
    for number_row in range(number_of_rows): 
        for alien_number in range(number_aliens_x): 
            create_alien(ai_settings,aliens,alien_number,screen,number_row)

def update_screen(ai_settings,aliens,bullets,sb,screen,ship,stats,play_button):
    """Update images on the screen and flip to the new screen."""
    # Redraw the screen during each pass through the loop.
    screen.fill(ai_settings.bg_color)
    # Draw the score information.
    sb.show_score()
    # Redraw all bullets behind ship and aliens.
    for bullet in bullets.sprites(): 
        bullet.draw_bullet()
    aliens.draw(screen)
    ship.blitme()
    # Draw the play button if the game is inactive.
    if not stats.game_active:
        play_button.blitme()
    # Make the most recently drawn screen visible.
    pygame.display.flip() 