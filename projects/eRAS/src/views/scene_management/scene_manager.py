from views.scene_management.scene import Scene

class SceneManager():
    __stack: list[Scene] = list()
    __currentScene: Scene = None

    @classmethod
    def load(cls, scene: Scene) -> None:
        if(cls.__currentScene is not None):
            cls.__stack.append(cls.__currentScene)
            cls.__currentScene.pack_forget()
            cls.__currentScene.on_hide()
        cls.__currentScene = scene
        scene.pack()
        scene.on_load()
        scene.on_show()

    @classmethod
    def back(cls) -> None:
        if(len(cls.__stack) == 0):
            raise "can't go back any further."
        scene = cls.__stack.pop()
        cls.__currentScene.on_hide()
        cls.__currentScene.on_destroy()
        cls.__currentScene.destroy()
        cls.__currentScene = scene
        scene.pack()
        scene.on_show()
    
    @classmethod
    def back_root(cls) -> None:
        scene = cls.__currentScene
        scene.on_hide()
        while 0 < len(cls.__stack):
            scene.on_destroy()
            scene.destroy()
            scene = cls.__stack.pop()
        cls.__currentScene = scene
        scene.pack()
        scene.on_show()