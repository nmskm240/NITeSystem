from views.scene_management.scene_manager import SceneManager
from views.widgets.image_button import ImageButton

class BackButton(ImageButton):
    def __init__(self) -> None:
        super().__init__("back")

    def _on_click(self) -> None:
        SceneManager.back()