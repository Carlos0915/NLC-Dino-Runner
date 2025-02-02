import pygame

from nlc_dino_runner.components.lives.lives import Live
from nlc_dino_runner.components.lives.livesManager import LiveManager
from nlc_dino_runner.components.powerups.power_up_manager import PowerUpManager
from nlc_dino_runner.utils import text_utils
from nlc_dino_runner.components.dinosaur import Dinosaur
from nlc_dino_runner.components.obstacles.obstaclesManager import ObstaclesManager
from nlc_dino_runner.utils.constants import TITLE, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, BG, FPS, CLOUD, GAME_THEME, \
    GAME_OVER, RESET, GAME_OVER_IMG, DARK_MODE, NORMAL_MODE


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.playing = False
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.game_speed = 20
        self.player = Dinosaur()
        self.obstacle_manager = ObstaclesManager()
        self.power_up_manager = PowerUpManager()
        self.live = Live()
        self.live_manager = LiveManager()
        self.points = 0
        self.running = True
        self.death_count = 0

    def run(self):
        self.obstacle_manager.reset_obstacles()
        self.power_up_manager.reset_power_ups(self.points)
        self.live_manager.reset_lives()
        self.points = 0
        self.playing = True
        GAME_THEME.play()
        while self.playing:
            self.event()
            self.update()
            self.draw()

        self.game_speed = 20
        GAME_OVER.play()

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self, self.screen)
        self.power_up_manager.update(self.points, self.game_speed, self.player)
    def draw(self):
        self.clock.tick(FPS)
        if (self.points // 5000) % 2 == 1:
            self.screen.fill(DARK_MODE)
        else:
            self.screen.fill(NORMAL_MODE)
        self.score()
        self.draw_background()
        self.draw_sky()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.power_up_manager.draw((self.screen))
        self.live_manager.draw(self.screen)
        pygame.display.update()
        pygame.display.flip()

    def score(self):
        self.points += 1
        if self.points % 100 == 0:
            self.game_speed += 1
        score_element, score_element_rect = text_utils.get_score_element(self.points)
        self.screen.blit(score_element, score_element_rect)
        self.player.check_invincibility(self.screen)
        #self.player.check_hammer(self.screen)

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (self.x_pos_bg + image_width, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (self.x_pos_bg + image_width, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def draw_sky(self):
        image_width = CLOUD.get_width()
        self.screen.blit(CLOUD, (self.x_pos_bg + 1100, self.y_pos_bg - 200))
        self.screen.blit(CLOUD, (self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg > +image_width:
            self.screen.blit(CLOUD, (self.x_pos_bg + 1100, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg += self.game_speed - 30

    def execute(self):
        while self.running:
            if not self.playing:
                self.show_menu()
                GAME_THEME.stop()

    def show_menu(self):
        self.running = True
        white_color = (255, 255, 255)
        self.screen.fill(white_color)
        self.print_menu_elements()
        pygame.display.update()
        self.handle_key_events_on_menu()
    def handle_key_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
                pygame.display.quit()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                self.run()
    def print_menu_elements(self):
        half_screen_height = SCREEN_HEIGHT // 2
        if self.death_count < 1:
            text, text_rect = text_utils.get_centered_message("Press any key to Start")
        else:
            pygame.time.delay(800)
            self.screen.blit(GAME_OVER_IMG, ((SCREEN_WIDTH // 2) - 200, (SCREEN_HEIGHT // 2) - 200))

            text, text_rect = text_utils.get_centered_message("Press any key to Restart")
            death_score, death_score_rect = text_utils.get_centered_message("Death count: " + str(self.death_count),
                                                                            height=half_screen_height + 115)
            self.screen.blit(death_score, death_score_rect)
            score, score_rect = text_utils.get_centered_message("FINAL Score: " + str(self.points),
                                                                height=half_screen_height + 165)
            self.screen.blit(score, score_rect)
            self.screen.blit(RESET, ((SCREEN_WIDTH // 2) - 40, (SCREEN_HEIGHT // 2) + 25))
        self.screen.blit(text, text_rect)
        self.screen.blit(ICON, ((SCREEN_WIDTH // 2) - 40, (SCREEN_HEIGHT // 2) - 150))
