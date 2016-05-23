# get a key from http://api.reimaginebanking.com
# assign your key to an environement variable
from bge import logic

import os, requests

def fetch_merchants():
    api_key = os.environ['NESSIE_API_KEY'] # assign this in your bash profile or hard-code the string
    url = 'http://api.reimaginebanking.com/enterprise/merchants?key=%s' % api_key
    r = requests.get(url)
    print(r.json())
    return r.json()

def render_merchants():
    merchants = fetch_merchants()
    print(len(merchants), type(merchants), merchants.keys())
    for m in merchants['results']:
        try:
            lat = m['geocode']['lat']
            lng = m['geocode']['lng']
            if(lat != 0 and lng != 0):
                spawn_prefab('merchant_prefab', (lng, lat, 0))
            else:
                print('no geo, try geocoding it')
                #TODO see https://github.com/geopy/geopy
        except Exception as e:
            print(e)

def spawn_prefab(prefab_name=None, location=(0,0,0), orientation=(0,0,0)):
    scene = logic.getCurrentScene()
    spawnpoint = scene.objects["spawnpoint"]
    if(prefab_name):
        scene.addObject(prefab_name, spawnpoint)
    else:
        #TODO add cube as default
        pass

def run():
    controller = logic.getCurrentController()
    obj = controller.owner
    if not obj['hasInitialized']:
        print('trying to fetch merchants')
        render_merchants()
        obj['hasInitialized'] = True
