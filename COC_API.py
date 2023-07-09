import requests
import pandas as pd

class COC_API:
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImVkNDE3ZWRkLTMwOTgtNGQ3Zi1hYTYzLTg1NWJiOGViNDc1NSIsImlhdCI6MTY4ODgzNzI3OSwic3ViIjoiZGV2ZWxvcGVyL2NkYmZkYzE1LTZkM2YtYjVlNi02OWY1LWI0ZWQ3MTNkYTRlOSIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjE4MS41MS4zMi4yMjYiXSwidHlwZSI6ImNsaWVudCJ9XX0.FWx8b7jGauw137L8H4YdGGJhTbHCgq0jzJ1ek3ib0K0fKmYbAcgCjek1DSQsbtY2Yg3jL9QNO6fjDx3PLi2kgw"

    @classmethod
    def get_clan_info_members(cls, clan_tag):
        clan_tag = clan_tag.replace("#", "%23")

        res = requests.get(f"https://api.clashofclans.com/v1/clans/{clan_tag}", headers={"Authorization": f"Bearer {cls.token}"})
        res = res.json()
        
        if "reason" in res:
            raise Exception("Error en la API de Clash of Clans\n" + res.__str__())

        clan_members = res["memberList"]
        del res["memberList"]

        clan_info = res

        # seleccionar columnas relevantes
        clan_members = pd.DataFrame(clan_members)
        clan_members = clan_members[["tag", "name", "role"]]
        clan_members = clan_members.to_dict("records")

        return clan_info, clan_members
    

    @classmethod
    def get_raid_info(cls, clan_tag, limit=1):
        clan_tag = clan_tag.replace("#", "%23")

        res = requests.get(f"https://api.clashofclans.com/v1/clans/{clan_tag}/capitalraidseasons?limit={limit}", headers={"Authorization": f"Bearer {cls.token}"})
        res = res.json()

        if "reason" in res:
            raise Exception("Error en la API de Clash of Clans\n" + res.__str__())

        return res["items"]
    
    @classmethod
    def get_CWL_info(cls, clan_tag):
        clan_tag = clan_tag.replace("#", "%23")

        res = requests.get(f"https://api.clashofclans.com/v1/clans/{clan_tag}/currentwar/leaguegroup", headers={"Authorization": f"Bearer {cls.token}"})
        res = res.json()

        return res
    
    @classmethod
    def CWL_specificwar_info(cls, war_tag):
        war_tag = war_tag.replace("#", "%23")

        res = requests.get(f"https://api.clashofclans.com/v1/clanwarleagues/wars/{war_tag}", headers={"Authorization": f"Bearer {cls.token}"})
        res = res.json()

        return res
    
    @classmethod
    def get_clan_war_info(cls, clan_tag):
        clan_tag = clan_tag.replace("#", "%23")

        res = requests.get(f"https://api.clashofclans.com/v1/clans/{clan_tag}/currentwar", headers={"Authorization": f"Bearer {cls.token}"})
        res = res.json()

        return res