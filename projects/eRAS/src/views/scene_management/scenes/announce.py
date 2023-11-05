import pygame.mixer

from abc import ABCMeta
from utils.config import Config
from views.scene_management.scene import Scene
from views.scene_management.scene_manager import SceneManager

class Announce(Scene, metaclass=ABCMeta):
    def __init__(self, master, message: str):
        super().__init__(master)
        self._message = message
        sound_path = f"../resources/{Config().layout}/sounds/{self.__class__.__name__.lower()}.mp3"
        pygame.mixer.init()
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play()

    def on_load(self) -> None:
        self.after(2500, func=lambda: SceneManager.back_root())

    def on_destroy(self) -> None:
        pygame.mixer.music.stop()