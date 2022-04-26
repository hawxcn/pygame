import pygame
from Level import Level
from Ground import Ground
from Building import Building
from Item import Item


class LevelManager:
    def __init__(self, musicManager):

        self.musicManager = musicManager
        self.levels = []
        self.level = 0
        self.generatedEnemies = 0
        self.Number_of_kills = 0
        self.finish = False

        self.enemy_generation = pygame.USEREVENT + 2
        self.enemyGroup = pygame.sprite.Group()

        # Level 0 
        L0 = Level()
        L0.addBackGround("Images/ControlGuide.png")
        L0.addGround(Ground(900, 120, -20, 340, "Images/Ground.png"))
        L0.addBuilding(Building(50, 200, "Images/Building044.png"))
        self.levels.append(L0)

        # Level 1
        L1 = Level()
        L1.addGround(Ground(900, 120, -20, 340, "Images/Ground.png"))
        # L1.addBuilding(Building(500, 120, "Images/Building01.png"))
        L1.addBackGround("Images/GameOver.png")
        self.levels.append(L1)

        # Level 2
        L2 = Level(5)
        L2.addGround(Ground(900, 120, -20, 340, "Images/Ground.png"))
        L2.addGround(Ground(100, 20, 300, 200, "Images/Ground.png"))
        L2.addGround(Ground(120, 20, 100, 150, "Images/Ground.png"))
        L2.addGround(Ground(80, 20, 500, 100, "Images/Ground.png"))
        self.levels.append(L2)

        # Level 3
        L3 = Level(8)
        L3.addGround(Ground(900, 120, -20, 340, "Images/Ground.png"))
        L3.addGround(Ground(100, 20, 200, 200, "Images/Ground.png"))
        L3.addGround(Ground(120, 20, 300, 120, "Images/Ground.png"))
        L3.addGround(Ground(80, 20, 400, 200, "Images/Ground.png"))
        L3.generationGap = 1500
        self.levels.append(L3)

        # Level 4
        L4 = Level(45)
        L4.addGround(Ground(900, 120, -20, 340, "Images/Ground.png"))
        L4.addGround(Ground(100, 20, 200, 200, "Images/Ground.png"))
        L4.addGround(Ground(120, 20, 300, 120, "Images/Ground.png"))
        L4.addGround(Ground(80, 20, 400, 200, "Images/Ground.png"))
        L4.generationGap = 300
        self.levels.append(L4)

    def getLevel(self):
        return self.level

    def nextLevel(self):
        self.level += 1

    def changeLevel(self, n):
        prevlevel = self.level
        self.level = n
        self.generatedEnemies = 0
        self.Number_of_kills = 0
        self.enemyGroup.empty()
        self.finish = False
        pygame.time.set_timer(self.enemy_generation, self.levels[self.level].generationGap)

        if (self.levels[prevlevel].enemyCount != self.levels[self.level].enemyCount):
            if (self.levels[self.level].enemyCount == 0):
                self.musicManager.loadMusic("background", 0.3)
            else:
                self.musicManager.loadMusic("battle", 0.3)

    def update(self, itemGroup):
        enemyCount = self.levels[self.level].enemyCount
        if (self.generatedEnemies == enemyCount):
            pygame.time.set_timer(self.enemy_generation, 0)
        self.Number_of_kills += len(pygame.event.get(pygame.USEREVENT + 3))
        if enemyCount > 0 and enemyCount == self.Number_of_kills and not self.finish:
            self.finish = True
            item = Item(400, 300, 0, "Images/coin.png")
            itemGroup.add(item)
