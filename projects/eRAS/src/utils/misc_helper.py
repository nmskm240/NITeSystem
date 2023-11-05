import tkinter as tk

class MiscHelper():
    @staticmethod
    def get_root(target: tk.Misc) -> tk.Misc:
        node = target
        while not node.master is None:
            node = node.master
        return node