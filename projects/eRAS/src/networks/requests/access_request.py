from networks.dto_base import DTO

class AccessRequest(DTO):
    class Place(DTO):
        campus: str = ""
        name: str = ""
    id: str = ""
    place: Place = None