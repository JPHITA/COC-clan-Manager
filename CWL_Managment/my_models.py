import pandas as pd

class CWL:

    @classmethod
    def ResumenClanes(cls, CWL_clans_info):
        clanes = {}
        for clan in CWL_clans_info:
            clanes[clan["name"]] = pd.DataFrame(clan["members"])["townHallLevel"].value_counts().to_dict()
        
        return clanes       
