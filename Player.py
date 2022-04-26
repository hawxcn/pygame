import time

import pygame
from pygame.locals import *
from HealthBar import HealthBar
from Fireball import Fireball
import random
import xml.dom.minidom
import os

vec = pygame.math.Vector2


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, levelManager):
        super().__init__()
        self.image = pygame.image.load("Images/Player_Sprite_R.png")
        self.rect = pygame.Rect(x, y, 35, 50)
        self.levelManager = levelManager
        self.musicManager = levelManager.musicManager

        if os.path.exists("save.xml"):
            with xml.dom.minidom.parse("save.xml") as domTree:
                player = domTree.getElementsByTagName("player")[0]
                self.maxMana = int(player.getAttribute("maxMana"))
                self.maxManaPotions = int(player.getAttribute("maxManaPotions"))
                self.skillPowerLvl = int(player.getAttribute("skillPowerLvl"))
                self.maxHealth = int(player.getAttribute("maxHealth"))
                self.coins = int(player.getAttribute("coins"))
        else:
            self.maxMana = 100
            self.maxManaPotions = 3
            self.skillPowerLvl = 1
            self.maxHealth = 5
            self.coins = 0

        # tolerance
        self.hpT = 1
        self.manaT = 10
        self.mpT = 1
        self.spT = 1

        # Player Info
        self.pos = vec(x, y)
        self.acc = vec(0, 0)
        self.vel = vec(0, 0)
        self.healthBar = HealthBar(10, 10, self)

        self.mana = self.maxMana
        self.manaPotions = self.maxManaPotions

        # Player Constants
        self.ACC = 0.4
        self.FRIC = -0.1

        # Player Movements
        self.jumping = False
        self.running = False
        self.direction = "RIGHT"
        self.move_frame = 0

        # Player Attacking
        self.attacking = False
        self.attack_frame = 0
        self.attack_counter = 0
        self.attack_range = pygame.Rect(0, 0, 0, 0)
        self.hit_cooldown = False

        # Player Events
        self.hit_cooldown_event = pygame.USEREVENT + 1

    def lvlUp(self):
        r = random.randint(0, 100)
        if r < 30:
            print("add hp")
            # self.maxHealth += self.hpT
            # self.healthBar.reset()
        elif r < 60:
            self.maxMana += self.manaT
            self.mana = self.maxMana
        elif r < 90:
            self.maxManaPotions += self.mpT
            self.manaPotions = self.maxManaPotions
        else:
            self.skillPowerLvl += self.spT

        self.save()
        return

    def save(self):
        doc = xml.dom.minidom.Document()
        root = doc.createElement("games")
        player = doc.createElement("player")
        player.setAttribute("maxHealth", str(self.maxHealth))
        player.setAttribute("maxMana", str(self.maxMana))
        player.setAttribute("maxManaPotions", str(self.maxManaPotions))
        player.setAttribute("skillPowerLvl", str(self.skillPowerLvl))
        player.setAttribute("coins", str(self.coins))
        root.appendChild(player)
        doc.appendChild(root)

        with open('save.xml', 'w') as f:
            # 缩进 - 换行 - 编码
            doc.writexml(f, encoding="utf-8")

    def move(self):
        self.acc = vec(0, 0.5)

        if abs(self.vel.x) > 0.3:
            self.running = True
        else:
            self.running = False

        keys = pygame.key.get_pressed()

        if keys[K_LEFT]:
            self.acc.x = -self.ACC
        if keys[K_RIGHT]:
            self.acc.x = self.ACC

        self.acc.x += self.vel.x * self.FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        lvl = self.levelManager
        if self.pos.x > 800:
            self.pos.x = 0
            if lvl.level == 0:
                self.changeLevel(2)
        elif self.pos.x < -30:
            self.pos.x = 800
            if lvl.level == 0:
                self.changeLevel(2)

        self.rect.topleft = self.pos
        self.rect.x += 32

    def changeLevel(self, n):
        self.healthBar.reset()
        self.mana = self.maxMana
        self.manaPotions = self.maxManaPotions
        self.levelManager.changeLevel(n)

    def walking(self):
        if self.move_frame > 6:
            self.move_frame = 0
            return

        if self.jumping == False and self.running == True:
            if self.vel.x >= 0:
                self.image = self.animation_right[self.move_frame]
                self.direction = "RIGHT"
            elif self.vel.x < 0:
                self.image = self.animation_left[self.move_frame]
                self.direction = "LEFT"
            self.move_frame += 1

        if self.running == False and self.move_frame != 0:
            self.move_frame = 0
            if self.direction == "RIGHT":
                self.image = self.animation_right[self.move_frame]
            elif self.direction == "LEFT":
                self.image = self.animation_left[self.move_frame]

    def attack(self):
        if self.attacking == True:
            if self.direction == "RIGHT":
                self.attack_range = pygame.Rect(self.rect.x + self.rect.width, self.pos.y, 30, self.rect.height)
            elif self.direction == "LEFT":
                self.attack_range = pygame.Rect(self.pos.x, self.pos.y, 30, self.rect.height)

            self.musicManager.loadSound("sword", 0.4)

            if self.attack_frame > 6:
                self.attack_frame = 0
                self.attacking = False
                self.attack_range = pygame.Rect(0, 0, 0, 0)
                return

            if self.direction == "RIGHT":
                self.image = self.attack_animation_right[self.attack_frame]
            elif self.direction == "LEFT":
                self.image = self.attack_animation_left[self.attack_frame]

            self.attack_counter += 1
            if self.attack_counter >= 3:
                self.attack_frame += 1
                self.attack_counter = 0

    def update(self, group, enemyProjectiles):
        self.walking()
        self.move()
        self.attack()
        self.collision(group)
        self.checkProjectiles(enemyProjectiles)

    def checkProjectiles(self, group):
        hits = pygame.sprite.spritecollideany(self, group)

        if hits:
            self.player_hit(1)

    def player_hit(self, damage):
        if self.hit_cooldown == False:
            self.hit_cooldown = True
            self.healthBar.takeDamage(damage)
            if (self.healthBar.health <= 0):
                self.changeLevel(1)
            pygame.time.set_timer(self.hit_cooldown_event, 1000)

    def fireball(self, group):
        if self.mana >= 10:
            if self.skillPowerLvl > 6:
                for i in range(int(self.skillPowerLvl/2)):
                    fireball = Fireball("LEFT", [self.rect.center[0] + i * 10, self.rect.center[1]])
                    group.add(fireball)
                self.musicManager.loadSound("fireball", 0.4)
                for i in range(int(self.skillPowerLvl/2)):
                    fireball = Fireball("RIGHT", [self.rect.center[0] + i * 10, self.rect.center[1]])
                    group.add(fireball)
                self.musicManager.loadSound("fireball", 0.4)
            else:
                for i in range(self.skillPowerLvl):  # "LEFT"
                    fireball = Fireball(self.direction, [self.rect.center[0] + i * 10, self.rect.center[1]])
                    group.add(fireball)
                    self.musicManager.loadSound("fireball", 0.4)
            self.mana -= 10

    def useManaPotion(self):
        if self.mana == self.maxMana:
            return

        if self.manaPotions >= 1:
            self.manaPotions -= 1
            if self.mana + 50 > self.maxMana:
                self.mana = self.maxMana
            else:
                self.mana += 50

    def collision(self, group):
        hits = pygame.sprite.spritecollide(self, group, False)

        if self.vel.y > 0:
            if hits:
                lowest = hits[0]

                if self.rect.bottom < lowest.rect.bottom:
                    self.pos.y = lowest.rect.top - self.rect.height
                    self.rect.y = lowest.rect.top - self.rect.height
                    self.vel.y = 0
                    self.jumping = False

    def jump(self):
        if self.jumping == False:
            self.jumping = True
            self.vel.y = -12

    def jump_cancel(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def render(self, display):
        # pygame.draw.rect(display, (255, 0, 0), self.rect)
        # pygame.draw.rect(display, (0, 255, 0), self.attack_range)
        display.blit(self.image, self.pos)
        self.healthBar.render(display)

        pygame.draw.rect(display, (0, 0, 255), pygame.Rect(10, 70,
                                                           self.mana, 15))

    def load_animations(self):
        self.animation_right = [pygame.image.load("Images/Player_Sprite_R.png").convert_alpha(),
                                pygame.image.load("Images/Player_Sprite2_R.png").convert_alpha(),
                                pygame.image.load("Images/Player_Sprite3_R.png").convert_alpha(),
                                pygame.image.load("Images/Player_Sprite4_R.png").convert_alpha(),
                                pygame.image.load("Images/Player_Sprite5_R.png").convert_alpha(),
                                pygame.image.load("Images/Player_Sprite6_R.png").convert_alpha(),
                                pygame.image.load("Images/Player_Sprite_R.png").convert_alpha()]

        self.animation_left = [pygame.image.load("Images/Player_Sprite_L.png").convert_alpha(),
                               pygame.image.load("Images/Player_Sprite2_L.png").convert_alpha(),
                               pygame.image.load("Images/Player_Sprite3_L.png").convert_alpha(),
                               pygame.image.load("Images/Player_Sprite4_L.png").convert_alpha(),
                               pygame.image.load("Images/Player_Sprite5_L.png").convert_alpha(),
                               pygame.image.load("Images/Player_Sprite6_L.png").convert_alpha(),
                               pygame.image.load("Images/Player_Sprite_L.png").convert_alpha()]

        self.attack_animation_right = [pygame.image.load("Images/Player_Sprite_R.png").convert_alpha(),
                                       pygame.image.load("Images/Player_Attack1_R.png").convert_alpha(),
                                       pygame.image.load("Images/Player_Attack2_R.png").convert_alpha(),
                                       pygame.image.load("Images/Player_Attack3_R.png").convert_alpha(),
                                       pygame.image.load("Images/Player_Attack4_R.png").convert_alpha(),
                                       pygame.image.load("Images/Player_Attack5_R.png").convert_alpha(),
                                       pygame.image.load("Images/Player_Sprite_R.png").convert_alpha()]

        self.attack_animation_left = [pygame.image.load("Images/Player_Sprite_L.png").convert_alpha(),
                                      pygame.image.load("Images/Player_Attack1_L.png").convert_alpha(),
                                      pygame.image.load("Images/Player_Attack2_L.png").convert_alpha(),
                                      pygame.image.load("Images/Player_Attack3_L.png").convert_alpha(),
                                      pygame.image.load("Images/Player_Attack4_L.png").convert_alpha(),
                                      pygame.image.load("Images/Player_Attack5_L.png").convert_alpha(),
                                      pygame.image.load("Images/Player_Sprite_L.png").convert_alpha()]
