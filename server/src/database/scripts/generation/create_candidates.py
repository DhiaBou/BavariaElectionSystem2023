import os

import pandas as pd

from database.database import get_db
from database.models.models import Parteien, Kandidaten


def create_candidates():
    party_name_id = {}
    kandidaten = []

    with get_db() as db:
        llist: list[Parteien] = db.query(Parteien).all()
        for l in llist:
            party_name_id[l.kurzbezeichnung] = l.ParteiID

    current_directory = os.getcwd()

    relative_path = "csv/kandidaten/LTW2023_GEWAEHLTE_BEWERBER_UND_LISTENNACHFOLGER_WkrNr_"

    path = os.path.join(current_directory, relative_path)

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
