import sys

import pygame

from bullet import Bullet
from alien import Alien
from time import sleep

def ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets):
    # Respone to aliens hit the ship
    if stats.ships_left > 0:
        stats.ships_left -= 1

        # Refresh scoreboard
        sb.prep_ships()

        # Empty aliens and bullet list
        aliens.empty()
        bullets.empty()

        # Create new group of aliens and put ship on the bottom of screen
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Sleep
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    # Respone to press key
    if event.key == pygame.K_RIGHT:
        # Move ship to right
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        # Move ship to left
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        # Create a bullet, and put it into group
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()
        

def fire_bullet(ai_settings, screen, ship, bullets):
    # If not reach allowed numer, launch one more bullet and add it to group
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def check_keyup_events(event, ship):
    # Respone to release key
    if event.key == pygame.K_RIGHT:
        #  Stop moving
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        # Stop moving
        ship.moving_left = False

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    # Respone to keyboard and mouse event
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                check_keydown_events(event, ai_settings, screen, ship, bullets)

            elif event.type == pygame.KEYUP:
                check_keyup_events(event, ship)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    # Start the game when player click play button
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset game settings
        ai_settings.initialize_dynamic_settings()
        # Invisible mouse
        pygame.mouse.set_visible(False)
        # Reset stats information
        stats.reset_stats()
        stats.game_active = True
        # Reset image of scoreboard
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Empty aliens and bullets list
        aliens.empty()
        bullets.empty()

        # Create a new group of aliens, and make them in the middle
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
                
def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    # Update image on screen
    # Draw the screen each time
    screen.fill(ai_settings.bg_color)
    # Draw all bullets
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    # Show score
    sb.show_score()

    # If the game is inactive, draw play button
    if not stats.game_active:
        play_button.draw_button()

    # Make the screen visiable
    pygame.display.flip()

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # Update bullets' position and delete bullets
    bullets.update()

    # Delete all bullets outside the screen
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # Check wether meet with alien, if yes take out both of them from screen
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # Delete all bullets and create a new group of aliens
        bullets.empty()
        ai_settings.increase_speed()

        # Level up
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)

def check_fleet_edges(ai_settings, aliens):
    # Take action when alien reach edge
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    # Move down the whole group alien and change their direction
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets):
    # Check wether there are aliens reach bottom
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
            break

def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets):
    # Update all aliens' position
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Detect wether alien is hit with ship
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)

    # Check wether there are aliens reach bottom
    check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets)

def get_number_aliens_x(ai_settings, alien_width):
    # Compute how many aliens can show up in each row
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x/(2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    # Compute how many rows of aliens can show up
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    # Create firt alien and put it to current row
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    # Create a group of alien
    # Create an alien and compute how many aliens can show up in this row
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows( ai_settings, ship.rect.height, alien.rect.height)
    
    # Create firt row of alien
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def check_high_score(stats, sb):
    # Check wether it is new record of highest score
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
