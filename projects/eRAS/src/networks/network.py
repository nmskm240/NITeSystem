from cgi import test
import json
import os
import socket
from typing import Dict
import requests
from networks.access_point import AccessPoint
from networks.dto_base import DTO

class Network():
    @staticmethod
    def get_token() -> str:
        res = requests.get(os.environ["OAUTH_API"])
        return json.loads(res.text)["token"] if res.status_code == 200 else ""

    @staticmethod
    def is_connection() -> bool:
        ip = socket.gethostbyname(socket.gethostname())
        return not ip == "127.0.0.1"

    @staticmethod
    def get(access_point: AccessPoint, parameters: DTO) -> str:
        if(not Network.is_connection()):
            raise Exception("ネットワークに接続されていません")
        token = Network.get_token()
        query: Dict = parameters.to_dict()
        query["access_token"] = token
        base_url = os.environ["MAIN_API"]
        res = requests.get(f"{base_url}/{access_point.value.path}", query)
        return res.text if res.status_code == 200 else None

    @staticmethod
    def post(access_point: AccessPoint, req: DTO) -> str:
        if(not Network.is_connection()):
            raise Exception("ネットワークに接続されていません")
        token = Network.get_token()
        query = { "access_token": token }
        base_url = os.environ["MAIN_API"]
        res = requests.post(f"{base_url}/{access_point._value_.path}", json= req.to_dict(), params= query)
        return res.text if res.status_code == 200 else None