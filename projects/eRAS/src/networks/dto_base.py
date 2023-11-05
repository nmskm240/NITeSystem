from abc import ABCMeta
from dataclasses import  dataclass
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class DTO(metaclass=ABCMeta):
    def __new__(cls, *args, **kwargs):
        dataclass(cls)
        return super().__new__(cls)

    @classmethod
    def from_json(cls, json) -> "DTO":
        return dataclass_json.from_json(json)