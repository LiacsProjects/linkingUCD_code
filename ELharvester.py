#! /usr/bin/python
from sickle import Sickle

URL = 'https://webservices.picturae.com/a2a/20a181d4-c896-489f-9d16-20a3b7306b15/'

'''
0 - Borgbrieven, 4.206 records
1 - Bonboeken, 144.262 records
2 - Bevolkingsregister, 292.758 records
3 - BS Echtscheidingsakte, 1.618 records
4 - BS Geboorte, 307.664 records
5 - BS Huwelijk, 98.000 records
6 - BS Overlijden, 333.573 records
7 - DTB Begraven, 179.995 records
8 - DTB Dopen, 399.351 records
9 - DTB Trouwen, 172.387 records
10 - Militieregisters, 36.312 records
11 - Attestaties Doopsgezinden/Buurquesties 1597-1700/Collaterale successie/Crimineel klachtenboek 1533-1811/
        Grafboeken Pieterskerk/Index Notarieel Archief/Kohier Gedwongen Leningen/Legaten gasthuizen/Lijfrente/
        Notariele Akten/Paspoorten/Transportregisters/Vertrokken personen 1924-1929, 693.785 records
12 - Poorterboeken, 21.839 records
13 - Oud Rechterlijke Akten, 18.422 records
Totaal - 2.704.172 records
'''


# Returns base for file location
def baseSelector(register_number):
    match register_number:
        case 0:
            return 'data/Erfgoed Leiden/Borgbrieven_records'
        case 1:
            return 'data/Erfgoed Leiden/Bonboeken_records'
        case 2:
            return 'data/Erfgoed Leiden/Bevolkingsregister_records'
        case 3:
            return 'data/Erfgoed Leiden/BS Echtscheidingsakte_records'
        case 4:
            return 'data/Erfgoed Leiden/BS Geboorte_records'
        case 5:
            return 'data/Erfgoed Leiden/BS Huwelijk_records'
        case 6:
            return 'data/Erfgoed Leiden/BS Overlijden_records'
        case 7:
            return 'data/Erfgoed Leiden/DTB Begraven_records'
        case 8:
            return 'data/Erfgoed Leiden/DTB Dopen_records'
        case 9:
            return 'data/Erfgoed Leiden/DTB Trouwen_records'
        case 10:
            return 'data/Erfgoed Leiden/Militieregisters_records'
        case 11:
            return 'data/Erfgoed Leiden/NA_records'
        case 12:
            return 'data/Erfgoed Leiden/Poorterboeken_records'
        case 13:
            return 'data/Erfgoed Leiden/Oud Rechterlijke Akten_records'
        case _:
            print("No base selected")
            return


# TODO add "from" statement to retrieve only newly added records
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
    file_location_base = baseSelector(register_number)
    print("Start harvesting \"" + register_set[register_number] + "\" set")
    while True:
        file_count = file_count + 1
        file_location = file_location_base + str(file_count) + '.xml'
        with open(file_location, 'w', encoding="utf-8") as fp:
            # Assume at least one record is present
            record = records.next().raw
            # Limit number of records to 300.000 per file so files don't exceed ~1.3GB
            for i in range(300000):
                count = count + 1
                # print(count)
                record = record[:7] + str(count) + record[7:]
                record = record[:record.find("/record") + 7] + str(count) + record[record.find("/record") + 7:]
                fp.write(record + '\n')
                try:
                    record = records.next().raw
                except StopIteration:
                    print("Successfully harvested all " + str(count) + " records from \"" + register_set[
                        register_number] + "\" set")
                    fp.close()
                    return
            fp.close()


# Main
if __name__ == '__main__':
    # Fill in number of register
    sickleHarvest(13)
