import pandas as pd
from COC_API import COC_API
from Members_Managment.my_models import Member

class CWL:

    @classmethod
    def ResumenClanes(cls, CWL_clans_info):
        clanes = {}
        for clan in CWL_clans_info:
            clanes[clan["name"]] = pd.DataFrame(clan["members"])["townHallLevel"].value_counts().to_dict()
        
        return clanes


    @classmethod
    def Info_GuerraEspecifica(cls, clan_tag, war_tags):
        
        for wat_tag in war_tags:
            war_info = COC_API.CWL_specificwar_info(wat_tag)
            print(war_info["clan"]["name"], war_info["opponent"]["name"])
            if war_info["clan"]["tag"] == clan_tag or war_info["opponent"]["tag"] == clan_tag:
                break

        Members_API = None
        if war_info["clan"]["tag"] == clan_tag:
            Members_API = pd.DataFrame(war_info["clan"]["members"])
        else:
            Members_API = pd.DataFrame(war_info["opponent"]["members"])

        Members_API = Members_API[Members_API["attacks"].isna()]

        Members_BD = Member.get_active_membersBD(clan_tag)

        Members_API = Members_API.merge(Members_BD, how="left", on="tag", suffixes=("_API", "_BD"))
        Members_API = Members_API[["name_API", "cel"]]
        Members_API = Members_API.rename(columns={"name_API": "name"})
        Members_API["cel"].fillna("no lo tengo", inplace=True)

        return Members_API.to_dict("records")
