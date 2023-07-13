from COC_API import COC_API
import pandas as pd
from Members_Managment.my_models import Member

class ClanWar:

    @classmethod
    def get_ClanWar_info(cls, clan_tag):
        success, msg, clanwar_info = COC_API.get_clan_war_info(clan_tag)
        
        clanwar_members_API = None
        if success:
            if clanwar_info["state"] == "inWar":
                clanwar_members_API = pd.DataFrame(clanwar_info["clan"]["members"])
                
                clanwar_members_API["attacks"] = clanwar_members_API["attacks"].apply(lambda x: len(x) if isinstance(x, list) else 0)
                clanwar_members_API = clanwar_members_API[["tag", "name", "attacks"]]

                # combinar con la base de datos de miembros
                membersBD = Member.get_active_membersBD(clan_tag)[["tag", "cel"]]

                clanwar_members_API = pd.merge(clanwar_members_API, membersBD, on="tag", how="left")
                clanwar_members_API = clanwar_members_API.to_dict("records")

        
            clanwar_info.pop("clan")
            clanwar_info.pop("opponent")

        return success, msg, clanwar_info, clanwar_members_API