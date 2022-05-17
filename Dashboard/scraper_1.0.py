import requests
import urllib.request
import time
from pathlib import Path
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from urllib.request import urlopen
url = 'https://nl.wikipedia.org/wiki/Lijst_van_rectores_magnifici_van_de_Universiteit_Leiden'
html = urlopen(url)
soup = BeautifulSoup(html, 'html.parser')

table = soup.find_all('table', {'class':'wikitable'})

period = []
name = []
picture = []
picture_saved = []
term = []
sources = []

for tab in table:
    rows = tab.find_all('tr')
    for row in rows:
        cells = row.find_all('td')
        if len(cells) > 1:
            #Process period
            per = cells[0]
            period.append(per.text.strip())
            #Process name
            nam = cells[1]
            name.append(nam.text.strip())
            #Process picture
            pic = cells[2]
            pics = pic.find('img')
            if pics is not None:
                src = pics['src']
                picture.append(src)
                if src not in sources:
                    sources.append(src)
                    path = Path('pictures/' + str(nam.text.strip()) + '.jpg')
                    if not path.is_file():
                        imgurl = 'http:' + src
                        try:
                            urllib.request.urlretrieve(imgurl, 'pictures/' + str(nam.text.strip()) + '.jpg')
                        except:
                            time.sleep(1)
                            urllib.request.urlretrieve(imgurl, 'pictures/' + str(nam.text.strip()) + '.jpg')
                picture_saved.append('pictures/' + str(nam.text.strip()) + '.jpg')
            else:
                picture.append('')
                picture_saved.append('')
            #Process term/detail
            ter = cells[3]
            term.append(ter.text.strip())

recmag_list = list(zip(period, name, picture, picture_saved, term))
recmag = pd.DataFrame(recmag_list, columns=('Period', 'Name', 'Picture', 'Picture_saved', 'Term/Details'))
recmag.to_csv('recmag_v1.csv', index=False, encoding='utf-8-sig')