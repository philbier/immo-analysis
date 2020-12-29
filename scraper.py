import bs4 as bs
import urllib.request
import time
from datetime import datetime
import pandas as pd
import json
import requests

state = "berlin"
city = "berlin"
page_num = 1
page = "https://www.immobilienscout24.de/Suche/de/"+state+"/"+city+"/wohnung-mieten?pagenumber="+str(page_num)

print(page_num)
print("Aktuelle Seite: "+page)

try:
# soup = bs.BeautifulSoup(urllib.request.urlopen(page).read(),'lxml')
    soup = bs.BeautifulSoup(urllib.request.urlopen(page).read(),'html.parser')

except Exception as e: 
    print(str(datetime.now())+": " + str(e))
#                 l = list(filter(lambda x: x != item, l))
#                 print("ID " + str(item) + " entfernt.")