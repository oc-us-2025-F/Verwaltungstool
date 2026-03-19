import requests

Superbaseurl = "https://fburyyzzewkdqxutuayl.supabase.co/rest/v1/quotes?select=text"
API_KEY = "sb_publishable_rRavetQ4CoLx_I29JkWOsQ_SvgyuP2u"

HEADER = {
    "apikey": API_KEY,
    "Authorization": f"Bearer {API_KEY}"
    
}

response = requests.get(Superbaseurl, headers=HEADER)

text_list = []
for row in response.json():
    text_list.append(row['text'])

print(text_list)