import tkinter as tk
import uuid
from abc import ABCMeta, abstractmethod

from utils.config import Config

class ImageButton(metaclass=ABCMeta):
    def __init__(self, image_file_name: str) -> None:
        image_path = f"../resources/{Config().layout}/images/widgets/{image_file_name}.png"
        self.__image = tk.PhotoImage(file=image_path)
        self.__uuid = str(uuid.uuid4())

    def place(self, canvas: tk.Canvas, x: int, y: int, anchor: tk.ANCHOR) -> None:
        canvas.create_image(x, y, anchor=anchor, image=self.__image, tags=self.__uuid)
        canvas.tag_bind(self.__uuid, "<ButtonPress-1>", func=lambda event: self._on_click())
        self._master = canvas

    @abstractmethod
    def _on_click(self) -> None:
        pass