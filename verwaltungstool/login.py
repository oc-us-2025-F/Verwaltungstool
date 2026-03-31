'''

In die Tabellen, die die userbezüglichen Daten halten sollen, 
muss zwingend eine Spalte mit der UserID (user_id), die einen Fremdschlüssel auf die Usertabelle hat. 
Damit funktioniert dann diese Row-Level-Security, die von supabase bereitgestellt wird und nur das anschauen/ändern usw. 
von Datensätzen ermöglicht, die zur eigenen userID gehören.

Was man überlegen könnte, ist (zur allgemeinen Vereinfachung) - das JSON-Format beizubehalten und in 
den Tabelln jeweils eine Spalte für das JSON anzulegen. 

'''



from supabase import create_client, Client
from verwaltungstool.config import settings
import os
from dotenv import load_dotenv

from verwaltungstool.supabase_client import supabase

load_dotenv()


def login():

    try: 
        response = supabase.auth.sign_in_with_password({
            "email": os.getenv("USER_EMAIL"),
            "password": os.getenv("USER_PASSWORD")

        })
        user = supabase.auth.get_user()
        settings.USER = user
        return user

    except Exception as e:
        print("Fehler!", e)
        raise e


