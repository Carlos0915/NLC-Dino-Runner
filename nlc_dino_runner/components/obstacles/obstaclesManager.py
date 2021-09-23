import pygame
import random

from nlc_dino_runner.components.obstacles.bird import Bird
from nlc_dino_runner.components.obstacles.cactus import Cactus
from nlc_dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS, BIRD, LOSE_LIFE, POWER_UP_SHIELD_OBSTACLES


class ObstaclesManager:
    def __init__(self):
        self.obstacles_list = []


    def update(self, game, screen):
        obstacles_type = [Cactus(SMALL_CACTUS), Cactus(LARGE_CACTUS), Bird(BIRD)]
        if len(self.obstacles_list) == 0:
            self.obstacles_list.append(random.choice(obstacles_type))
        for obstacle in self.obstacles_list:
            obstacle.update(game.game_speed, self.obstacles_list)

            if game.player.hammer and game.player.hammer.rect.colliderect(obstacle.rect):
                self.obstacles_list.remove(obstacle)
                POWER_UP_SHIELD_OBSTACLES.play()

            if game.player.dino_rect.colliderect(obstacle.rect):
                if game.player.shield:
                    self.obstacles_list.remove(obstacle)


                elif game.live_manager.lives > 1:
                    LOSE_LIFE.play()
                    game.live_manager.reduce_lives()
                    game.player.shield = True
                    start_time = pygame.time.get_ticks()
                    game.player.shield_time_up = start_time + 1000

                else:
                    game.player.draw_dead(screen)
                    pygame.time.delay(500)
                    game.playing = False
                    game.death_count += 18
                    break



    def draw(self, screen):
        for obstacle in self.obstacles_list:
            obstacle.draw(screen)
    def reset_obstacles(self):
        self.obstacles_list = []
