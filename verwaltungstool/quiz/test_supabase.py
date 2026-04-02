from verwaltungstool.login import login
from verwaltungstool.config import settings
from verwaltungstool.supabase_client import supabase



if __name__ == "__main__":
    login()

    try: 
        response = (supabase.table("quiz_fragen")
        .select("id, frage_text")
        .execute())
    except Exception as e:
        print(" fehler in daten bank abfrage ")

    print(response.data)
    print(type(response.data))


    for row in response.data:
        print(type(row))
        print(row['id'] , row['frage_text'])




