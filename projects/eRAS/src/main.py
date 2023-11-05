import tkinter as tk

from dotenv import load_dotenv
load_dotenv()

from views.scene_management.scenes.home import Home
from views.scene_management.scene_manager import SceneManager

app = tk.Tk()
app.wm_attributes("-topmost", True)
app.geometry("1024x600")
app.attributes("-fullscreen", True)
app.resizable(False, False)
app.title("NITeRAS")

SceneManager.load(Home(app))

app.mainloop()