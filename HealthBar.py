import pygame

vec = pygame.math.Vector2


class HealthBar(pygame.sprite.Sprite):
    def __init__(self, x, y,player):
        super().__init__()
        self.load_animations()
        self.player = player
        self.health = player.maxHealth
        self.image = self.health_animations[self.health]
        self.pos = vec(x, y)

    def reset(self):
        self.health = self.player.maxHealth
        self.image = self.health_animations[self.health]

    def render(self, display):
        display.blit(self.image, self.pos)

    def takeDamage(self, damage):
        self.health -= damage
        if self.health < 0: self.health = 0

        self.image = self.health_animations[self.health]

    def Heal(self, heal):
        self.health += heal
        if self.health > 5: self.health = 5

        self.image = self.health_animations[self.health]

    def load_animations(self):

        self.health_animations = [pygame.image.load("Images/heart0.png").convert_alpha(),
                                  pygame.image.load("Images/heart1.png").convert_alpha(),
                                  pygame.image.load("Images/heart2.png").convert_alpha(),
                                  pygame.image.load("Images/heart3.png").convert_alpha(),
                                  pygame.image.load("Images/heart4.png").convert_alpha(),
                                  pygame.image.load("Images/heart5.png").convert_alpha()]
