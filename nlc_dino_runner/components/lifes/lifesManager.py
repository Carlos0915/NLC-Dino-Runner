from nlc_dino_runner.components.lives.lives import Live
from  nlc_dino_runner.components.game import Game

class LivesManager():

    def __init__(self):
        self.lifes = 4

    def draw(self, screen):
        for live in range(self.lives):
            heart = Live(POS_X)
