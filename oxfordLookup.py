import requests

app_id = "d90fc163"
app_key = "6a9b97fb3679828caf97206643bfb475"
language = "en-gb"

def getDefinitions(word_id):
    url = "https://od-api.oxforddictionaries.com:443/api/v2/entries/" + language + "/" + word_id.lower()
    r = requests.get(url, headers={"app_id": app_id, "app_key": app_key})
    res = r.json()

    if 'error' in res.keys():
         return False
    
    output = {}
    senses = res['results'][0]['lexicalEntries'][0]['entries'][0]['senses']
    definations = []
    for sense in senses:
        definations.append(f"{sense['definitions'][0]}")
    output['definitions'] = "\n".join(definations)

    if res['results'][0]['lexicalEntries'][0]['entries'][0]['pronunciations'][0].get('audioFile'):
        output['audio'] = res['results'][0]['lexicalEntries'][0]['entries'][0]['pronunciations'][0]['audioFile']

    return output