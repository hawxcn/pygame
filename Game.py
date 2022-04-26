import pygame
from pygame.locals import *
import sys
import random

from Ground import Ground
from Player import Player
from Enemy import Enemy
from RangedEnemy import RangedEnemy
from UserInterface import UserInterface
from LevelManager import LevelManager
from MusicManager import MusicManager

# Begin Pygame
pygame.init()

WIDTH = 800
HEIGHT = 400
FPS = 60
CLOCK = pygame.time.Clock()

display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bugs Free")

background = pygame.image.load("Images/Background.png")

musicManager = MusicManager()
levelManager = LevelManager(musicManager)
player = Player(200, 200, levelManager)
player.load_animations()
UI = UserInterface(player)

Items = pygame.sprite.Group()
PlayerProjectiles = pygame.sprite.Group()
EnemyProjectiles = pygame.sprite.Group()
playerGroup = pygame.sprite.Group()
playerGroup.add(player)

musicManager.loadMusic("background", 0.3)

while 1:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == player.hit_cooldown_event:
            player.hit_cooldown = False
            pygame.time.set_timer(player.hit_cooldown_event, 0)

        if event.type == levelManager.enemy_generation:
            choice = random.randint(0, 1)
            enemy = None

            if choice == 0:
                enemy = Enemy()
            elif choice == 1:
                enemy = RangedEnemy(EnemyProjectiles)

            levelManager.enemyGroup.add(enemy)
            levelManager.generatedEnemies += 1

        if event.type == MOUSEBUTTONDOWN:
            pass

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                player.jump()
            if event.key == K_RETURN:
                player.attacking = True
                player.attack()
            if event.key == K_1:
                levelManager.changeLevel(0)
            if event.key == K_2:
                levelManager.changeLevel(1)
            if event.key == K_3:
                levelManager.changeLevel(2)
            if event.key == K_4:
                levelManager.changeLevel(3)
            if event.key == K_5:
                    levelManager.changeLevel(4)
            if event.key == K_h:
                UI.toggleInventory()
            if event.key == K_m:
                player.fireball(PlayerProjectiles)
            if event.key == K_p:
                player.useManaPotion()

        if event.type == KEYUP:
            if event.key == K_SPACE:
                player.jump_cancel()

    # Update Functions
    for enemy in levelManager.enemyGroup:
        enemy.update(levelManager.levels[levelManager.getLevel()].groundData, player, PlayerProjectiles, Items)

    player.update(levelManager.levels[levelManager.getLevel()].groundData, EnemyProjectiles)
    UI.update(CLOCK.get_fps())

    levelManager.update(Items)

    # Render Functions
    newBg = levelManager.levels[levelManager.getLevel()].backgroundData
    if newBg is not None:
        display.blit(newBg, (0, 0))
    else:
        display.blit(background, (0, 0))

    for data in levelManager.levels[levelManager.getLevel()].data:
        data.render(display)

    for enemy in levelManager.enemyGroup:
        enemy.render(display)

    for item in Items:
        item.render(display)
        item.update(player)

    for projectile in PlayerProjectiles:
        projectile.render(display)
        projectile.update(levelManager.enemyGroup)

    for projectile in EnemyProjectiles:
        projectile.render(display)
        projectile.update(playerGroup)

    player.render(display)
    UI.render(display)

    pygame.display.update()
    CLOCK.tick(FPS)
