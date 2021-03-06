import os
import json
import requests
import logging as log
from dotenv import load_dotenv


class Rest:
    attribute: dict = {"titel": "round_name", "setting": "setting",
                       "regelwerk": "ruleset", "zeitblock": "round_tb", "spielleiter": "round_gm",
                       "gewünschte spielerzahl": "round_max_pl", "vorbereitete charaktere": "own_char",
                       "beschreibung": "round_desc"}
    headers = {
        'Content-Type': 'application/json',
    }

    def __init__(self):
        load_dotenv()
        self.URL = os.getenv('WEB_API')
        self.headers["auth"] = os.getenv('API_TOKEN')

    def makeRequest(self, msg: str) -> bool:
        response = requests.request(
            "POST",
            self.URL,
            headers=self.headers,
            data=json.dumps(self.preparePayload(msg))
        )
        if(response.status_code == 200):
            log.error("created new Entry")
            return True
        else:
            log.error(response.content)
            return False

    def preparePayload(self, msg: str) -> dict:
        """
        builds from a string a dictionary to be consumed as a payload
        """
        msg_dict: dict = {}
        split_msg = msg.split("\n")
        for line in split_msg:
            for key in self.attribute:
                if key in line.lower():
                    msg_dict[self.attribute[key]
                             ] = line[len(key) + 1:].lstrip().rstrip()
        msg_dict["round_max_pl"] = int(msg_dict["round_max_pl"][-1:])
        if msg_dict["own_char"].lower() == "ja":
            msg_dict["own_char"] = True
        else:
            msg_dict["own_char"] = False
        return msg_dict
