import tkinter as tk

from marshmallow.fields import Function
from threading import Thread
from views.scene_management.scene import Scene

class Loading(Scene):
    __task: Thread

    def __init__(self, master, task: Function):
        super().__init__(master)
        self.__task = Thread(target=task)

    def on_load(self) -> None:
        self.__task.start()

    def on_destroy(self) -> None:
        self.__task.join()