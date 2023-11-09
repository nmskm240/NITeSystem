import tkinter as tk
import uuid
from abc import ABCMeta, abstractmethod

from utils.config import Config

class ImageButton(metaclass=ABCMeta):
    def __init__(self, image_file_name: str) -> None:
        self.__uuid = str(uuid.uuid4())

    def place(self, canvas: tk.Canvas, x: int, y: int, anchor: tk.ANCHOR) -> None:
        canvas.tag_bind(self.__uuid, "<ButtonPress-1>", func=lambda event: self._on_click())
        self._master = canvas

    @abstractmethod
    def _on_click(self) -> None:
        pass