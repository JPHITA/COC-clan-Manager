import requests
import pandas as pd
from Config.models import Constantes

class COC_API:
    token = Constantes.objects.get(nombre="token COC_API").valor

    @classmethod
    def get_clan_info_members(cls, clan_tag):
        clan_tag = clan_tag.replace("#", "%23")

        res = requests.get(f"https://api.clashofclans.com/v1/clans/{clan_tag}", headers={"Authorization": f"Bearer {cls.token}"})
        res = res.json()
        
        if "reason" in res:
            return False, "Error en la API de Clash of Clans: " + res.__str__(), None, None

        clan_members = res["memberList"]
        del res["memberList"]

        clan_info = res

        # seleccionar columnas relevantes
        clan_members = pd.DataFrame(clan_members)
        clan_members = clan_members[["tag", "name", "role"]]
        clan_members = clan_members.to_dict("records")

        return True, "", clan_info, clan_members
    

    @classmethod
    def get_raid_info(cls, clan_tag, limit=1):
        clan_tag = clan_tag.replace("#", "%23")

        res = requests.get(f"https://api.clashofclans.com/v1/clans/{clan_tag}/capitalraidseasons?limit={limit}", headers={"Authorization": f"Bearer {cls.token}"})
        res = res.json()

        if "reason" in res:
            return False, "Error en la API de Clash of Clans: " + res.__str__(), None

        return True, "", res["items"]
    
    @classmethod
    def get_CWL_info(cls, clan_tag):
        clan_tag = clan_tag.replace("#", "%23")

        res = requests.get(f"https://api.clashofclans.com/v1/clans/{clan_tag}/currentwar/leaguegroup", headers={"Authorization": f"Bearer {cls.token}"})
        res = res.json()

        if "reason" in res:
            return False, "Error en la API de Clash of Clans: " + res.__str__(), None

        return True, "", res
    
    @classmethod
    def CWL_specificwar_info(cls, war_tag):
        war_tag = war_tag.replace("#", "%23")

        res = requests.get(f"https://api.clashofclans.com/v1/clanwarleagues/wars/{war_tag}", headers={"Authorization": f"Bearer {cls.token}"})
        res = res.json()

        if "reason" in res:
            return False, "Error en la API de Clash of Clans: " + res.__str__(), None

        return True, "", res
    
    @classmethod
    def get_clan_war_info(cls, clan_tag):
        clan_tag = clan_tag.replace("#", "%23")

        res = requests.get(f"https://api.clashofclans.com/v1/clans/{clan_tag}/currentwar", headers={"Authorization": f"Bearer {cls.token}"})
        res = res.json()

        if "reason" in res:
            return False, "Error en la API de Clash of Clans: " + res.__str__(), None

        return True, "", res