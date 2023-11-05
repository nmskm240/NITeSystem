import tkinter as tk
from views.scene_management.scenes.announce import Announce

class Error(Announce):
    def __init__(self, master, message: str):
        super().__init__(master, message)
        self.create_text(
            (50, 250), 
            anchor=tk.NW, 
            font=("", 30), 
            text=self._message,
            width=700
        )