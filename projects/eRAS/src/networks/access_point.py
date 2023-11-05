from dataclasses import dataclass
from enum import Enum

@dataclass(frozen= True)
class AccessPointData():
    path: str

class AccessPoint(Enum):
    ROOM_ENTRY = AccessPointData("room/entry")
    ROOM_EXIT = AccessPointData("room/exit")