from views.widgets.image_button import ImageButton

class SettingButton(ImageButton):
    def __init__(self) -> None:
        super().__init__("setting")

    def _on_click(self) -> None:
        pass