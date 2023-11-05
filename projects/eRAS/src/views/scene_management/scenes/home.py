import tkinter as tk
from networks.access_point import AccessPoint

from views.scene_management.scene import Scene
from views.widgets.close_button import CloseButton
from views.widgets.member_button import MemberButton
from views.widgets.room_access_button import RoomAccessButton
from views.widgets.setting_button import SettingButton

class Home(Scene) :
    def __init__(self, master):
        super().__init__(master)
        login = RoomAccessButton(AccessPoint.ROOM_ENTRY)
        logout = RoomAccessButton(AccessPoint.ROOM_EXIT)
        member = MemberButton()
        setting = SettingButton()
        close = CloseButton()
        login.place(self, 150, 50, tk.NW)        
        logout.place(self, 874, 50, tk.NE)
        member.place(self, 30, 550, tk.SW)
        setting.place(self, 360, 550, tk.SW)
        close.place(self, 690, 550, tk.SW)