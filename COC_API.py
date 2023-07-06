import requests
import pandas as pd

class COC_API:
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImJjNTE4OGZjLTJiYzYtNDBmNy04YjQzLTExZjk1ODExNGVkYiIsImlhdCI6MTY4NzI5MDU1Miwic3ViIjoiZGV2ZWxvcGVyL2NkYmZkYzE1LTZkM2YtYjVlNi02OWY1LWI0ZWQ3MTNkYTRlOSIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjE4MS41MC4zMi4xNCJdLCJ0eXBlIjoiY2xpZW50In1dfQ.cjoxcQyVyvAaLC_nbeHKCELQBPHWWHjH_aeSh6DE80r1gsu4blPgwvc8zCXuMVMLi8N9IYbMriiburOSiiuNDg"

    @classmethod
    def get_clan_info_members(cls, clan_tag):
        clan_tag = clan_tag.replace("#", "%23")

        res = requests.get(f"https://api.clashofclans.com/v1/clans/{clan_tag}", headers={"Authorization": f"Bearer {cls.token}"})
        res = res.json()

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
        res = res.json()["items"]

        return res