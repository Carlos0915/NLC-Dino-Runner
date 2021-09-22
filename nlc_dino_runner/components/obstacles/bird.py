import random

from nlc_dino_runner.components.obstacles.obstacles import Obstacles


class Bird(Obstacles):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.FPS = 0

    def draw(self, screen):
        if self.FPS > 5:
            self.rect.y = 236
            screen.blit(self.image[1], self.rect)
        else:
            self.rect.y = 250
            screen.blit(self.image[0], self.rect)

        if self.FPS >= 9:
            self.FPS = 0

        self.FPS += 1.2