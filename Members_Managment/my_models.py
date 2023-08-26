import pandas as pd
from django.db import connection
from datetime import datetime


class Member:

    membersBD = None
       

    @classmethod
    def get_active_membersBD(cls, clan_tag):
        sql = """
            SELECT
                tag, name, cel, role, clan, comments
            FROM
                Members_Managment_member
            WHERE
                current_member = 1
            AND
                clan = %s;"""

        with connection.cursor() as cursor:
            cursor.execute(sql, [clan_tag])
            members = cursor.fetchall()
            cols = [col[0] for col in cursor.description]

        cls.membersBD = pd.DataFrame(members, columns=cols)

        return cls.membersBD
    
    @classmethod
    def get_historical_memberBD(cls, tag_name):
        tag_name = tag_name.upper()
        sql = """
            SELECT
                tag, name, clan, role, cel, comments, date_created, date_updated,
                CASE WHEN current_member = 1 THEN 'Si' ELSE 'No' END AS current_member
            FROM
                Members_Managment_member
            WHERE
                UPPER(tag) = %s
            OR
                UPPER(name) LIKE %s;"""

        with connection.cursor() as cursor:
            cursor.execute(sql, [tag_name, f"%{tag_name}%"])
            member = cursor.fetchone()
            cols = [col[0] for col in cursor.description]

        if member is None:
            return "no encontrado", None
        else:
            return "ok", dict(zip(cols, member))

    @classmethod
    def verify_modified_fields(cls, clan_tag, members):
        if not isinstance(cls.membersBD, pd.DataFrame):
            cls.membersBD = cls.get_active_membersBD(clan_tag)

        membersAPI = pd.DataFrame(members)

        # verificar nombres y roles
        res = pd.merge(cls.membersBD, membersAPI, on="tag", how='inner', suffixes=("_BD", "_API"))

        res["actualizar_name"] = res["name_API"] != res["name_BD"]
        res["actualizar_role"] = res["role_API"] != res["role_BD"]
        # actualizar nombres y roles
        for i, row in res.query("actualizar_name == True or actualizar_role == True").iterrows():
            member_update = Member(
                tag = row["tag"],
                name = row["name_API"],
                role = row["role_API"],
                date_updated=datetime.now().strftime('%Y-%m-%d')
            )
            member_update.update(campos=["name", "role", "date_updated"])

    @classmethod
    def verify_new_and_leaving_members(cls, clan_tag, members):
        if not isinstance(cls.membersBD, pd.DataFrame):
            cls.membersBD = cls.get_active_membersBD(clan_tag)

        membersAPI = pd.DataFrame(members)

        # verificar nuevos miembros (estan en la API pero no en la BD)
        with connection.cursor() as cursor:
            news = membersAPI[~membersAPI['tag'].isin(cls.membersBD['tag'])]
            for i, row in news.iterrows():
                # verificar si ya estaban en la BD como inactivos
                cursor.execute("SELECT COUNT(tag) from Members_Managment_member WHERE tag = %s AND clan = %s AND current_member = 0", [row["tag"], clan_tag])

                if cursor.fetchone()[0] >= 1: # si estan en la BD como inactivos
                    memb = Member(
                        tag = row["tag"],
                        name = row["name"],
                        role = row["role"],
                        current_member = True,
                        date_updated = datetime.now().strftime('%Y-%m-%d')
                    )
                    memb.update(campos=["name", "role", "current_member", "date_updated"])

                else:
                    memb = Member(
                        tag = row["tag"],
                        name = row["name"],
                        clan = clan_tag,
                        role = row["role"],
                        cel = None,
                        comments = None,
                        current_member = True,
                        date_created = datetime.now().strftime('%Y-%m-%d'),
                        date_updated = datetime.now().strftime('%Y-%m-%d')
                    )
                    
                    memb.save()

        # verificar miembros que ya no estan (estan en la BD pero no en la API)
        leaving = cls.membersBD[~cls.membersBD['tag'].isin(membersAPI['tag'])]

        for i, row in leaving.iterrows():
            member_update = Member(
                tag = row["tag"],
                current_member = False,
                date_updated = datetime.now().strftime('%Y-%m-%d')
            )
            member_update.update(campos=["current_member", "date_updated"])
                

    def __init__(self, tag=None, name=None, clan=None, role=None, cel=None, comments=None, current_member=None, date_created=None, date_updated=None):
        self.tag = tag
        self.name = name
        self.clan = clan
        self.role = role
        self.cel = cel
        self.comments = comments
        self.current_member = current_member
        self.date_created = date_created
        self.date_updated = date_updated


    def update(self, campos = None):
        # si no se especifican campos, se actualizan todos
        if campos == None:
            campos = list(self.__dict__.keys())
            campos.remove("date_created")

        params = []
        sql = "UPDATE Members_Managment_member SET "
        for c in campos:
            params.append(self.__dict__[c])
            sql += f"{c} = %s,"
        
        sql = sql[:-1] + " WHERE tag = %s;"
        params.append(self.tag)

        with connection.cursor() as cursor:
            cursor.execute(sql, params)

            return cursor.rowcount >= 1


    def save(self):
        sql = """
            INSERT INTO Members_Managment_member
                (tag, name, clan, role, cel, current_member, date_created, date_updated)
            VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s);"""
        
        with connection.cursor() as cursor:
            cursor.execute(sql, [self.tag, self.name, self.clan, self.role, self.cel, self.current_member, self.date_created, self.date_updated])        

            return cursor.rowcount >= 1
            