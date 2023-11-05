import tkinter as tk
from abc import ABCMeta
from utils.config import Config

from utils.misc_helper import MiscHelper

class Scene(tk.Canvas, metaclass=ABCMeta):
    def __init__(self, master: tk.Misc):
        image_path = f"../resources/{Config().layout}/images/backgrounds/{self.__class__.__name__.lower()}.png"
        self.__background = tk.PhotoImage(file=image_path)
        tk.Canvas.__init__(
            self, 
            MiscHelper.get_root(master), 
            width=master.winfo_screenwidth(), 
            height=master.winfo_screenheight()
        )
        self.create_image(0, 0, anchor=tk.NW, image=self.__background, tags="background")

    def on_load(self) -> None:
        pass

    def on_show(self) -> None:
        pass

    def on_hide(self) -> None:
        pass

    def on_destroy(self) -> None:
        pass