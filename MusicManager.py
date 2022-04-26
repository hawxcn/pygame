import pygame


class MusicManager:
    def __init__(self):
        self.sounds = {}
        self.loadSounds()

    def loadSounds(self):
        self.sounds["background"] = "Sound/background_village.wav"
        self.sounds["battle"] = "Sound/battle_music.wav"
        self.sounds["enemyhit"] = "Sound/enemy_hit.wav"
        self.sounds["fireball"] = "Sound/fireball_sound.wav"
        self.sounds["gameover"] = "Sound/gameover.wav"
        self.sounds["sword"] = "Sound/sword1.wav"

    def loadSound(self, name, volume):
        soundEffect = pygame.mixer.Sound(self.sounds[name])
        soundEffect.set_volume(volume)
        soundEffect.play()

    def loadMusic(self, name, volume, num = -1):
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.load(self.sounds[name])
        pygame.mixer.music.play(num)

    def stop(self):
        pygame.mixer.music.stop()
