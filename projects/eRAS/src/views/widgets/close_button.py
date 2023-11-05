import sys
from views.widgets.image_button import ImageButton

class CloseButton(ImageButton):
    def __init__(self) -> None:
        super().__init__("close")

    def _on_click(self) -> None:
        sys.exit()