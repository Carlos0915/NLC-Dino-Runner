import random
import pygame

from nlc_dino_runner.components.powerups import hammer
from nlc_dino_runner.components.powerups.shield import Shield
from nlc_dino_runner.components.powerups.hammer_power_up import HammerPowerUp
from nlc_dino_runner.utils.constants import SHIELD_TYPE, HAMMER_TYPE, POWER_UP_SOUND_SHIELD, POWER_UP_SOUND_HAMMER


class PowerUpManager:

    def __init__(self):
        self.power_ups = []
        self.when_appears = 0
        self.points = 0
        self.option_numbers = list(range(1, 10))
        self.hammer = hammer


    def reset_power_ups(self, points):
        self.power_ups = []
        self.points = points
        self.when_appears = random.randint(100, 110) + self.points

    def generate_power_ups(self, points):
        self.points = points
        if len(self.power_ups) == 0:
            if self.when_appears == self.points:
                print("generating powerup")
                self.when_appears = random.randint(self.when_appears + 200, 500 + self.when_appears)
                if random.randint(0, 10) < 5:
                    self.power_ups.append(Shield())
                else:
                    self.power_ups.append(HammerPowerUp())
        return self.power_ups

    def update(self, points, game_speed, player):
        self.generate_power_ups(points)
        for power_up in self.power_ups:
            power_up.update(game_speed, self.power_ups)
            if player.dino_rect.colliderect(power_up.rect):
                if power_up.type == SHIELD_TYPE:
                    player.shield = True
                    player.show_text = True
                    POWER_UP_SOUND_SHIELD.play()
                    player.type = power_up.type
                    power_up.start_time = pygame.time.get_ticks()
                    time_random = random.randrange(5, 8)
                    player.shield_time_up = power_up.start_time + (time_random * 1000)
                    self.power_ups.remove(power_up)


                elif power_up.type == HAMMER_TYPE:
                    player.hammer_available = True
                    player.show_hammer_text = True
                    POWER_UP_SOUND_HAMMER.play()
                    player.type = power_up.type
                    power_up.start_time = pygame.time.get_ticks()
                    time_random = random.randrange(5, 8)
                    player.shield_time_up = power_up.start_time + (time_random * 1000)
                    self.power_ups.remove(power_up)


    def draw(self, screen):
        for power_up in self.power_ups:
            power_up.draw(screen)
