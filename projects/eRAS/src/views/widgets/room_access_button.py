from networks.access_point import AccessPoint
from views.scene_management.scene_manager import SceneManager
from views.scene_management.scenes.login import Login
from views.widgets.image_button import ImageButton

class RoomAccessButton(ImageButton):
    def __init__(self, access_point: AccessPoint) -> None:
        image_file_name = "login" if access_point == AccessPoint.ROOM_ENTRY else "logout"
        super().__init__(image_file_name)
        self.__access_point = access_point

    def _on_click(self) -> None:
        SceneManager.load(Login(self._master, self.__access_point))