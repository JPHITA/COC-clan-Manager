from Members_Managment.my_models import Member
import pandas as pd
from COC_API import COC_API

class Raid:

    @classmethod
    def get_last_raid_info(cls, clan_tag):
        membersBD = Member.get_active_membersBD(clan_tag)
        success, msg, raid_info = COC_API.get_raid_info(clan_tag)

        attacks_info = None
        if success:
            raid_info = raid_info[0]
            raid_info.pop("attackLog")
            raid_info.pop("defenseLog")

            # combinar con los celulares
            membersBD = membersBD[["tag", "name","cel"]]
            attacks_info = pd.DataFrame(raid_info.pop("members"))        
            attacks_info = attacks_info.merge(membersBD, on="tag", how="right", suffixes=("_API", "_BD"))

            attacks_info["total_attack_limit"] = attacks_info["attackLimit"] + attacks_info["bonusAttackLimit"]
            attacks_info.drop(columns=["attackLimit", "bonusAttackLimit"], inplace=True)

            attacks_info = attacks_info[["tag", "name_BD", "attacks", "total_attack_limit", "capitalResourcesLooted", "cel"]]
            attacks_info["attacks"].fillna(0, inplace=True)
            attacks_info["total_attack_limit"].fillna(5, inplace=True)
            attacks_info["capitalResourcesLooted"].fillna(0, inplace=True)

        return success, msg, raid_info, attacks_info