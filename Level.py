import pygame


class Level:
    def __init__(self, enemyCount=0):
        self.data = []
        self.backgroundData = None
        self.groundData = pygame.sprite.Group()
        self.buildingData = pygame.sprite.Group()
        self.enemyCount = enemyCount
        self.generationGap = 2000

    def add(self, data):
        self.data.append(data)

    def addGround(self, data):
        self.data.append(data)
        self.groundData.add(data)

    def addBackGround(self, name):
        self.backgroundData = pygame.image.load(name)

    def addBuilding(self, data):
        self.data.append(data)
        self.buildingData.add(data)
