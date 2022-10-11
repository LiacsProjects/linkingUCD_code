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
country = []
b_place = []
b_day = []
d_place = []
d_day = []
o_place = []
o_day = []
subject = []
job = []
t_prof = []
thesis = []
doc_advisor = []
fam_from = []
fam_works = []

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
            #print(name[-1])
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
            #Process extra information
            nam_link = nam.find('a')
            if nam_link is not None:
                nam_url = nam_link['href']
                html = urlopen(url)
                soup = BeautifulSoup(html, 'html.parser')
                nam_html = urlopen('https://nl.wikipedia.org/' + nam_url)
                nam_soup = BeautifulSoup(nam_html, 'html.parser')
                info_table = nam_soup.find('table', {'class': 'infobox'})
                if info_table is not None:
                    nam_rows = info_table.find_all('tr')
                    for nam_row in nam_rows:
                        nam_cells = nam_row.find_all('td')
                        if len(nam_cells) > 1:
                            #Process nationality
                            if nam_cells[0].text.strip() == 'Nationaliteit':
                                nat = nam_cells[1].text.strip()
                                country.append(nat)
                            #Process birth/death details
                            if nam_cells[0].text.strip() == 'Geboren':
                                bir_cell = nam_cells[1].text.strip()
                                try:
                                    bir = bir_cell[1].split(',')
                                    bir_p = bir[0]
                                    b_place.append(bir_p)
                                    bir_d = bir[1]
                                    b_day.append(bir_d)
                                except:
                                    bir_d = bir_cell
                                    b_day.append(bir_d)
                            if nam_cells[0].text.strip() == 'Geboortedatum':
                                try:
                                    bir_cell = nam_cells[1].text.strip()
                                    bir = bir_cell[1].split(' te ')
                                    bir_d = bir[0]
                                    b_day.append(bir_d)
                                    bir_p = bir[1]
                                    b_place.append(bir_p)
                                except:
                                    bir_d = nam_cells[1].text.strip()
                                    b_day.append(bir_d)
                            if nam_cells[0].text.strip() == 'Geboorteplaats':
                                bir_p = nam_cells[1].text.strip()
                                b_place.append(bir_p)
                            if nam_cells[0].text.strip() == 'Overleden':
                                ovr_cell = nam_cells[1].text.strip()
                                try:
                                    ovr = ovr_cell[1].split(',')
                                    ovr_p = ovr[0]
                                    o_place.append(ovr_p)
                                    ovr_d = ovr[1]
                                    o_day.append(ovr_d)
                                except:
                                    ovr_d = ovr_cell
                                    o_day.append(ovr_d)
                            if nam_cells[0].text.strip() == 'Overlijdensdatum':
                                try:
                                    ovr_cell = nam_cells[1].text.strip()
                                    ovr = ovr_cell[1].split(' te ')
                                    ovr_d = ovr[0]
                                    o_day.append(ovr_d)
                                    ovr_p = ovr[1]
                                    o_place.append(ovr_p)
                                except:
                                    ovr_d = nam_cells[1].text.strip()
                                    o_day.append(ovr_d)
                            if nam_cells[0].text.strip() == 'Overlijdensplaats':
                                ovr_p = nam_cells[1].text.strip()
                                o_place.append(ovr_p)
                            if nam_cells[0].text.strip() == 'Datum van overlijden':
                                ovr_d = nam_cells[1].text.strip()
                                o_day.append(ovr_d)
                            if nam_cells[0].text.strip() == 'Plaats van overlijden':
                                ovr_p = nam_cells[1].text.strip()
                                o_place.append(ovr_p)
                            #Process Subject area
                            if nam_cells[0].text.strip() == 'Vakgebied':
                                sub = nam_cells[1].text.strip()
                                subject.append(sub)
                            #Process Job
                            if nam_cells[0].text.strip() == 'Beroep':
                                j = nam_cells[1].text.strip()
                                job.append(j)
                            #Type of professor
                            if nam_cells[0].text.strip() == 'Soort hoogleraar':
                                prof = nam_cells[1].text.strip()
                                t_prof.append(prof)
                            #Thesis
                            if nam_cells[0].text.strip() == 'Proefschrift':
                                the = nam_cells[1].text.strip()
                                thesis.append(the)
                            #doctoral advisor
                            if nam_cells[0].text.strip() == 'Promotor':
                                doc = nam_cells[1].text.strip()
                                doc_advisor.append(doc)
                            #famous from
                            if nam_cells[0].text.strip() == 'Bekend van':
                                fro = nam_cells[1].text.strip()
                                fam_from.append(fro)
                            #famous works
                            if nam_cells[0].text.strip() == 'Bekende werken':
                                work = nam_cells[1].text.strip()
                                fam_works.append(work)
                else:
                    country.append('')
                    b_place.append('')
                    b_day.append('')
                    o_place.append('')
                    o_day.append('')
                    subject.append('')
                    job.append('')
                    t_prof.append('')
                    thesis.append('')
                    doc_advisor.append('')
                    fam_from.append('')
                    fam_works.append('')

            else:
                name[-1] = ''

recmag_list = list(zip(period, name, picture, picture_saved, term, country, b_place, b_day, o_place, o_day, subject,
                       job, t_prof, thesis, doc_advisor, fam_from, fam_works))
recmag = pd.DataFrame(recmag_list, columns=('Period', 'Name', 'Picture', 'Picture_saved', 'Term/Details', 'Country',
                                            'Birth place', 'Birth date', 'Death place', 'Death date', 'Subject',
                                            'Job', 'Type of professor', 'Thesis', 'Doctoral advisor', 'Familiar from',
                                            'Familiar works'))
recmag.to_csv('recmag_v2.csv', index=False, encoding='utf-8-sig')