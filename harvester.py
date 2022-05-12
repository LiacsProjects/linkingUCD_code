#! /usr/bin/python
from sickle import Sickle

URL = 'https://webservices.picturae.com/a2a/20a181d4-c896-489f-9d16-20a3b7306b15/'

'''
0 - Borgbrieven
1 - Bonboeken
2 - Bevolkingsregister, 292.758 records
3 - BS Echtscheidingsakte
4 - BS Geboorte, 307.664 records
5 - BS Huwelijk, 98.000 records
6 - BS Overlijden
7 - DTB Begraven
8 - DTB Dopen
9 - DTB Trouwen, 172.387 records
10 - Militieregisters
11 - Attestaties Doopsgezinden/Buurquesties 1597-1700/Collaterale successie/Crimineel klachtenboek 1533-1811/
        Grafboeken Pieterskerk/Index Notarieel Archief/Kohier Gedwongen Leningen/Legaten gasthuizen/Lijfrente/
        Notariele Akten/Paspoorten/Transportregisters/Vertrokken personen 1924-1929
12 - Poorterboeken
13 - Oud Rechterlijke Akten
'''


# Harvest data per set
def sickleHarvest():
    sickle = Sickle(URL)
    register_set = ['bb_a', 'bn_a', 'br_a', 'bs_e', 'bs_g', 'bs_h', 'bs_o', 'dtb_b', 'dtb_d', 'dtb_t', 'ml_a', 'na_a',
                    'po_a', 'ra_a']
    records = sickle.ListRecords(metadataPrefix='a2a', set=register_set[9])

    count = file_count = 0
    file_location_base = 'data/Erfgoed Leiden/DTBTrouwregister_records'
    while True:
        file_count = file_count + 1
        file_location = file_location_base + str(file_count) + '.xml'
        with open(file_location, 'w', encoding="utf-8") as fp:
            # Assume at least one record is present
            temp = records.next().raw
            # Limit #records to 300.000 per file
            for i in range(300000):
                count = count + 1
                print(count)
                temp = temp[:7] + str(count) + temp[7:]
                temp = temp[:temp.find("/record") + 7] + str(count) + temp[temp.find("/record") + 7:]
                fp.write(temp + '\n')
                try:
                    temp = records.next().raw
                except StopIteration:
                    print("Successfully retrieved all records from \"{}\" set".format(register_set))
                    fp.close()
                    return
            fp.close()


# Main
if __name__ == '__main__':
    sickleHarvest()
