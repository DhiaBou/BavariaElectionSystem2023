import pandas as pd

from src.database.database import get_db
from src.database.models.models import (
    Parteien,
    Kandidaten,
    Erste_Stimmen,
    Zweite_Stimmzettel,
    Zweite_Stimme_Ohne_Kandidaten,
    Stimmkreis,
)

kandidaten = {}
stimmKreise = {}
erststimmen = []
zweitstimmen = []
zweitstimmenohnekandidaten = []

with get_db() as db:
    llist: list[Kandidaten] = db.query(Kandidaten).all()
    stimmkreise_res: list[Stimmkreis] = db.query(Stimmkreis).all()
    stimmkreise_res = sorted(stimmkreise_res, key=lambda x: -x.StimmkreisId)

    for l in llist:
        kandidaten[l.KandidatID] = l
    for l in stimmkreise_res:
        if l.WahlkreisId not in stimmKreise:
            stimmKreise[l.WahlkreisId] = [l.StimmkreisId]
        else:
            stimmKreise[l.WahlkreisId].append(l.StimmkreisId)


def get_value(value):
    try:
        return int(value), True
    except:
        return int(value[:-1]), False


path = "/Users/omarbouattour/PycharmProjects/Bayern_Wahl_dbs/server/src/database/scripts/csv/LTW2023_BEWERBER_UND_ABGEORDNETE_WkrNr_"
for i in range(907, 900, -1):
    print(i)
    file_path = path + str(i) + ".xls"
    xls = pd.ExcelFile(file_path)
    for sheet_name in xls.sheet_names:
        if sheet_name == "Combined Data":
            df = xls.parse(sheet_name)
            for index, row in df.iterrows():
                id = i * 10000 + row["Unnamed: 0"]
                print(id)
                erststimmen = []
                zweitstimmen = []
                zweitstimmenohnekandidaten = []
                for stimmkreis in stimmKreise[i]:
                    value, flag = get_value(row[stimmkreis])
                    if id in kandidaten:
                        if flag:
                            print("1++" + str(value))
                            for k in range(value):
                                zweitstimmen.append(Zweite_Stimmzettel(KandidatID=id, StimmkreisId=stimmkreis))
                            with get_db() as db:
                                db.bulk_save_objects(zweitstimmen)
                                db.commit()
                                zweitstimmen = []

                        else:
                            print("2++" + str(value))
                            for k in range(value):
                                erststimmen.append(Erste_Stimmen(KandidatID=id, StimmkreisId=stimmkreis))

                    else:
                        print("--" + str(value))
                        for k in range(value):
                            zweitstimmenohnekandidaten.append(
                                Zweite_Stimme_Ohne_Kandidaten(
                                    ParteiID=kandidaten[id - 1].ParteiID,
                                    StimmkreisId=stimmkreis,
                                )
                            )

                with get_db() as db:
                    db.bulk_save_objects(erststimmen)
                    db.bulk_save_objects(zweitstimmenohnekandidaten)
                    db.commit()
