from views.widgets.image_button import ImageButton

class MemberButton(ImageButton):
    def __init__(self) -> None:
        super().__init__("member")

    def _on_click(self) -> None:
        pass