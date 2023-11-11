import tkinter as tk
from abc import ABCMeta
from utils.config import Config

from utils.misc_helper import MiscHelper

class Scene(tk.Canvas, metaclass=ABCMeta):
    def __init__(self, master: tk.Misc):
        tk.Canvas.__init__(
            self, 
            MiscHelper.get_root(master), 
            width=master.winfo_screenwidth(), 
            height=master.winfo_screenheight()
        )

    def on_load(self) -> None:
        pass

    def on_show(self) -> None:
        pass

    def on_hide(self) -> None:
        pass

    def on_destroy(self) -> None:
        pass