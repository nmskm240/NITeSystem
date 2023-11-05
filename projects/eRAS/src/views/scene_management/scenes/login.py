import json
import os
import tkinter as tk
from networks.access_point import AccessPoint
from networks.network import Network
from networks.requests.access_request import AccessRequest

from views.scene_management.scene import Scene
from views.scene_management.scene_manager import SceneManager
from views.scene_management.scenes.complete import Complete
from views.scene_management.scenes.error import Error
from views.scene_management.scenes.loading import Loading
from views.widgets.back_button import BackButton


class Login(Scene):
    def __init__(self, master, access_point: AccessPoint):
        super().__init__(master)
        self.__access_point = access_point
        sv = tk.StringVar()
        entry = tk.Entry(self, textvariable=sv)
        entry.focus_set()
        entry.bind("<Return>", func=lambda event: SceneManager.load(
            Loading(self.master, lambda: self.__login_process(sv.get()))
        ))
        entry.place(x=0, y=0, height=0)
        back = BackButton()
        back.place(self, 0, 600, tk.SW)

    def __login_process(self, id: str) -> None:
        id = id.replace("A", "")
        if(id.isdigit()):
            req = AccessRequest(id, AccessRequest.Place(
                os.environ["CAMPUS"], os.environ["ROOM"]))
            result = json.loads(Network.post(self.__access_point, req))
            if("message" in result):
                SceneManager.load(Error(self.master, result["message"]))
            else:
                SceneManager.load(Complete(self.master, ""))
        else:
            SceneManager.load(Error(self.master, "このバーコードは使用できません"))
