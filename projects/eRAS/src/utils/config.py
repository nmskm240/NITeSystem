import configparser

class Config():
    @property
    def campus(self) -> str:
        return self.__config.get(self.__section, "campus")

    @campus.setter
    def campus(self, name: str) -> None:
        self.__config.set(self.__section, "campus", name)

    @property
    def layout(self) -> str:
        return self.__config.get(self.__section, "layout")

    @layout.setter
    def layout(self, name: str) -> None:
        self.__config.set(self.__section, "layout", name)
    

    def __init__(self, section: str = "USER"):
        self.__config = configparser.ConfigParser()
        self.__config.read('../config.ini')
        self.__section = section

    def reset(self) -> None:
        for option in self.__config.options(self.__section):
            self.__config.remove_option(self.__section, option)