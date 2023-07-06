from Members_Managment.my_models import Member
import pandas as pd
from COC_API import COC_API

class Raid:

    @classmethod
    def get_last_raid_info(cls, clan_tag):
        membersBD = Member.get_active_membersBD(clan_tag)
        raid_info = COC_API.get_raid_info(clan_tag)[0]
        raid_info.pop("attackLog")
        raid_info.pop("defenseLog")

        # combinar con los celulares
        membersBD = membersBD[["tag", "cel"]]
        attacks_info = pd.DataFrame(raid_info.pop("members"))        
        attacks_info = attacks_info.merge(membersBD, on="tag", how="left")

        attacks_info["total_attack_limit"] = attacks_info["attackLimit"] + attacks_info["bonusAttackLimit"]
        attacks_info.drop(columns=["attackLimit", "bonusAttackLimit"], inplace=True)

        return raid_info, attacks_info