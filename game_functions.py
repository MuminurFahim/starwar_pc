import sys
import pygame
from bullets import Bullet
from alien import Alien
from time import sleep


def fire_bullets(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_keydown_events(event, ai_settings, screen, ship, bullets, stats, aliens, sb):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullets(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_p and not stats.game_active:
        start_game(stats, aliens, bullets, ai_settings, screen, ship, sb)


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_play_button(stats, play_button, mouse_x, mouse_y, aliens, bullets, ai_settings, screen, ship, sb):
    if play_button.rect.collidepoint(mouse_x, mouse_y) and not stats.game_active:
        start_game(stats, aliens, bullets, ai_settings, screen, ship, sb)


def start_game(stats, aliens, bullets, ai_settings, screen, ship, sb):
    ai_settings.dynamic_settings()
    pygame.mouse.set_visible(False)
    stats.reset_stats()
    stats.game_active = True
    sb.prep_score()
    sb.prep_level()
    sb.prep_ships()
    aliens.empty()
    bullets.empty()
    create_fleet(ai_settings, screen, aliens)
    ship.center_ship()


def check_events(ai_settings, screen, ship, bullets, stats, play_button, aliens, sb):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets, stats, aliens, sb)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(stats, play_button, mouse_x, mouse_y, aliens, bullets, ai_settings, screen, ship, sb)


def update_screen(ai_settings, screen, ship, aliens, bullets, play_button, stats, sb):
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    sb.show_score()
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()


def update_bullets(ai_settings, screen, bullets, aliens, sb, stats, ship):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    collisions(ai_settings, screen, bullets, aliens, sb, stats, ship)


def collisions(ai_settings, screen, bullets, aliens, sb, stats, ship):
    cl = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if cl:
        for alns in cl.values():
            stats.score += ai_settings.alien_points * len(alns)
            sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, aliens)
        ship.center_ship()


def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def get_number_of_aliens_x(ai_settings, alien):
    number_of_aliens_x = int(ai_settings.screen_width / (2 * alien.rect.width)) - 1
    return number_of_aliens_x


def get_number_of_aliens_y(ai_settings, alien):
    number_of_aliens_y = int(ai_settings.screen_height / alien.rect.height) - 3
    return number_of_aliens_y


def create_alien(ai_settings, screen, aliens, alien_number_x, alien_number_y):
    alien = Alien(ai_settings, screen)
    alien.rect.x = alien.rect.width * (1 + 2 * alien_number_x)
    alien.rect.y = alien.rect.height * alien_number_y
    aliens.add(alien)


def create_fleet(ai_settings, screen, aliens):
    alien = Alien(ai_settings, screen)
    number_of_aliens_x = get_number_of_aliens_x(ai_settings, alien)
    number_of_aliens_y = get_number_of_aliens_y(ai_settings, alien)
    for alien_number_y in range(number_of_aliens_y):
        for alien_number_x in range(number_of_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number_x, alien_number_y)


def if_hit_edges_do(ai_settings, screen, aliens):
    for alien in aliens.sprites():
        if alien.rect.right >= screen.get_rect().right or alien.rect.left <= 0:
            ai_settings.direction *= -1
            drop_fleet(ai_settings, aliens)
            break


def drop_fleet(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed


def update_aliens(ai_settings, screen, bullets, aliens, ship, stats, sb):
    if_hit_edges_do(ai_settings, screen, aliens)
    aliens.update()
    check_bottom(ai_settings, screen, bullets, aliens, ship, stats, sb)
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, bullets, aliens, ship, stats, sb)


def ship_hit(ai_settings, screen, bullets, aliens, ship, stats, sb):
    if stats.ships_left > 1:
        stats.ships_left -= 1
        sb.prep_ships()
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, aliens)
        ship.center_ship()
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_bottom(ai_settings, screen, bullets, aliens, ship, stats, sb):
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen.get_rect().bottom:
            ship_hit(ai_settings, screen, bullets, aliens, ship, stats, sb)
            break
