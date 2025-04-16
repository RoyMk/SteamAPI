from pprint import pprint
from typing import Any, Dict, Union

import requests
from endpoints import Endpoints



class Steam:
    elden_ring_id = 1245620

    def __init__(self):
        pass
    @staticmethod
    def make_request(endpoint_url,params: dict | None = None):
        if endpoint_url:
            request = requests.get(endpoint_url,params=params)
            response = request.json()
            return response


    @staticmethod
    def get_all_apps(search_name: str = None) -> str | list[dict]:
        json_response = Steam.make_request(endpoint_url=Endpoints.all_apps).get('applist', []).get('apps', [])
        if not search_name:
            return json_response
        for app in json_response:
            result = app.get("name")
            if result.lower() == search_name.lower():
                return app.get("appid")


    @classmethod
    def multi_app_search(cls,apps : list[str]) -> list[str]:
        matches = []
        """
        Grab all user inserted names and make them lowercase, we use a
        set to avoid duplicates.
        """
        target_names = set([app.lower() for app in apps])
        if "elden ring" in target_names:
            matches.append(cls.elden_ring_id)
            """
            Remove elden ring once we append into the match list, this is to avoid re-adding
            it to the list
            """
            target_names.remove("elden ring")
        json_response = Steam.make_request(endpoint_url=Endpoints.all_apps).get('applist', []).get('apps', [])
        # Parse the response and get any matching name from the applist.
        for application in json_response:
            game_name = application.get("name")

            # Simple match case, if we do get a match we append the id corresponding to the name to the list.
            if game_name and game_name.lower() in target_names:
                matches.append(application.get("appid"))
        return matches





    @staticmethod
    def player_count(appid: int = None, apps: list[str] = None):
        p_count = []
        if apps:
            query = Steam.multi_app_search(apps)
            for game in query:
                json_response = Steam.make_request(endpoint_url=Endpoints.player_count, params={"appid": game})
                p_count.append(json_response.get('response').get("player_count"))
        return p_count




a = Steam.player_count(apps=["elden ring","path of exile 2","path of exile"])
print(a)



