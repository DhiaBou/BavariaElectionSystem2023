import pandas as pd

from src.database.database import get_db
from src.database.models.models import Parteien, Kandidaten

party_name_id = {}
kandidaten = []

with get_db() as db:
    llist: list[Parteien] = db.query(Parteien).all()
    for l in llist:
        party_name_id[l.kurzbezeichnung] = l.ParteiID

path = "/Users/omarbouattour/PycharmProjects/Bayern_Wahl_dbs/server/src/database/scripts/csv/kandidaten/LTW2023_GEWAEHLTE_BEWERBER_UND_LISTENNACHFOLGER_WkrNr_"
for i in range(901, 908, 1):
    file_path = path + str(i) + ".xls"
    xls = pd.ExcelFile(file_path)
    for sheet_name in xls.sheet_names:
        party_id = party_name_id[sheet_name]
        print(party_id)
        df = xls.parse(sheet_name)
        for index, row in df.iterrows():
            if "," in str(row["Name"]):
                name = row["Name"].split(",")[0]
                first_name = row["Name"].split(", ")[1]
                id = row["Nr."]
                print(first_name, name, id)
                kandidat = Kandidaten(
                    KandidatID=i * 10000 + id,
                    Vorname=first_name,
                    Nachname=name,
                    ParteiID=party_id,
                    StimmkreisId=None,
                    ListenNummer=id % 100,
                )
                kandidaten.append(kandidat)

with get_db() as db:
    db.add_all(kandidaten)
    db.commit()
