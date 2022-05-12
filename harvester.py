#! /usr/bin/python
from sickle import Sickle

URL = 'https://webservices.picturae.com/a2a/20a181d4-c896-489f-9d16-20a3b7306b15/'

'''
0 - Borgbrieven, 4.206 records
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
def sickleHarvest(register_number):
    if register_number < 0 or register_number > 13:
        print("Invalid register number")
        return

    sickle = Sickle(URL)
    register_set = ['bb_a', 'bn_a', 'br_a', 'bs_e', 'bs_g', 'bs_h', 'bs_o', 'dtb_b', 'dtb_d', 'dtb_t', 'ml_a', 'na_a',
                    'po_a', 'ra_a']
    records = sickle.ListRecords(metadataPrefix='a2a', set=register_set[register_number])

    count = file_count = 0
    if register_number is 0:
        file_location_base = 'data/Erfgoed Leiden/Borgbrieven_records'
    elif register_number is 1:
        file_location_base = 'data/Erfgoed Leiden/Bonboeken_records'
    elif register_number is 2:
        file_location_base = 'data/Erfgoed Leiden/Bevolkingsregister_records'
    elif register_number is 3:
        file_location_base = 'data/Erfgoed Leiden/BS Echtscheidingsakte_records'
    elif register_number is 4:
        file_location_base = 'data/Erfgoed Leiden/BS Geboorte_records'
    elif register_number is 5:
        file_location_base = 'data/Erfgoed Leiden/BS Huwelijk_records'
    elif register_number is 6:
        file_location_base = 'data/Erfgoed Leiden/BS Overlijden_records'
    elif register_number is 7:
        file_location_base = 'data/Erfgoed Leiden/DTB Begraven_records'
    elif register_number is 8:
        file_location_base = 'data/Erfgoed Leiden/DTB Dopen_records'
    elif register_number is 9:
        file_location_base = 'data/Erfgoed Leiden/DTB Trouwen_records'
    elif register_number is 10:
        file_location_base = 'data/Erfgoed Leiden/Militieregisters_records'
    elif register_number is 11:
        file_location_base = 'data/Erfgoed Leiden/NA_records'
    elif register_number is 12:
        file_location_base = 'data/Erfgoed Leiden/Poorterboeken_records'
    elif register_number is 13:
        file_location_base = 'data/Erfgoed Leiden/Oud Rechterlijke Akten_records'
    else:
        return

    while True:
        file_count = file_count + 1
        file_location = file_location_base + str(file_count) + '.xml'
        with open(file_location, 'w', encoding="utf-8") as fp:
            # Assume at least one record is present
            record = records.next().raw
            # Limit #records to 300.000 per file
            for i in range(300000):
                count = count + 1
                print(count)
                record = record[:7] + str(count) + record[7:]
                record = record[:record.find("/record") + 7] + str(count) + record[record.find("/record") + 7:]
                fp.write(record + '\n')
                try:
                    record = records.next().raw
                except StopIteration:
                    print("Successfully retrieved all " + str(count) + " records from \"{}\" set".format(
                        register_set[register_number]))
                    fp.close()
                    return
            fp.close()


# Main
if __name__ == '__main__':
    sickleHarvest(0)
    sickleHarvest(1)
