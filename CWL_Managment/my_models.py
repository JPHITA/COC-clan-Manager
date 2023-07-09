import pandas as pd
from COC_API import COC_API

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
            
            if war_info["clan"]["tag"] == clan_tag or war_info["opponent"]["tag"] == clan_tag:
                break

        ths_clan = pd.DataFrame(war_info["clan"]["members"])
        ths_clan = ths_clan[["mapPosition", "name", "townhallLevel"]]
        ths_clan.set_index("mapPosition", inplace=True, drop=True)

        ths_opponent = pd.DataFrame(war_info["opponent"]["members"])
        ths_opponent = ths_opponent[["mapPosition", "name", "townhallLevel"]]
        ths_opponent.set_index("mapPosition", inplace=True, drop=True)

        print(ths_clan.index.sort_values(), ths_opponent.index.sort_values())
        # print(pd.merge(ths_clan, ths_opponent, left_index=True, right_index=True, suffixes=("_clan", "_opponent")).sort_index())
        # return pd.merge(ths_clan, ths_opponent, left_index=True, right_index=True, suffixes=("_clan", "_opponent")).sort_index()
