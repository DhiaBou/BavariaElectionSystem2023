from sqlalchemy.sql import text, func

from database.models.models import Wahlkreis, Stimmkreis
from database.Überhangs_ausgleich_mandaten import allocate_final_seats_in_wahlkreis, \
    allocate_final_seats_in_wahlkreis_nico
from src.database.database import get_db


# wahlkreise_dict = {}
#
# with get_db() as db:
#     wahlkreise = db.query(
#         Wahlkreis.WahlkreisId,
#         Wahlkreis.Abgeordnetenmandate,
#     ).all()
#     for wahlkreis in wahlkreise:
#         wahlkreise_dict[wahlkreis[0]] = {
#             "parties": {},
#             "nb_seats": wahlkreis[1],
#             "direct_candidates": [],
#         }
#
# with get_db() as db:
#     res = db.execute(
#         text(
#             "select g.* from gesamt_stimmen_pro_partei_pro_wahlkreis_view g, anteil_over_five_percent a where g.wahlkreisid = a.wahlkreisid and  g.parteiid = a.parteiid"
#         )
#     )
#     for r in res:
#         if r[4] > 0:
#             wahlkreise_dict[r[0]]["parties"][r[2]] = r[4]
#
# with get_db() as db:
#     res = db.execute(text("select * from direct_candidates"))
#     for r in res:
#         wahlkreise_dict[r[0]]["direct_candidates"].append(r[6])

wahlkreise_dict = {
    907: {
        "parties": {1: 706704, 2: 245253, 3: 328583, 4: 328165, 5: 134399},
        "nb_seats": 26,
        "direct_candidates": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        "direct_candidates_dict": {1: 13, 2: 0, 3: 0, 4: 0, 5: 0},
    },
    905: {
        "parties": {1: 733528, 2: 295591, 3: 172099, 4: 249643, 5: 192782},
        "nb_seats": 24,
        "direct_candidates": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        "direct_candidates_dict": {1: 12, 2: 0, 3: 0, 4: 0, 5: 0},
    },
    906: {
        "parties": {1: 611164, 2: 198158, 3: 179068, 4: 228188, 5: 137383},
        "nb_seats": 19,
        "direct_candidates": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        "direct_candidates_dict": {1: 10, 2: 0, 3: 0, 4: 0, 5: 0},
    },
    904: {
        "parties": {1: 481744, 2: 120644, 3: 178045, 4: 207627, 5: 121592},
        "nb_seats": 16,
        "direct_candidates": [1, 1, 1, 1, 1, 1, 1, 1],
        "direct_candidates_dict": {1: 8, 2: 0, 3: 0, 4: 0, 5: 0},
    },
    902: {
        "parties": {1: 429120, 2: 96504, 3: 402629, 4: 242784, 5: 71833},
        "nb_seats": 18,
        "direct_candidates": [1, 1, 1, 3, 1, 1, 1, 1, 1],
        "direct_candidates_dict": {1: 8, 2: 0, 3: 1, 4: 0, 5: 0},
    },
    901: {
        "parties": {1: 1609824, 2: 894284, 3: 675368, 4: 520994, 5: 387227},
        "nb_seats": 61,
        "direct_candidates": [
            1,
            1,
            2,
            2,
            1,
            1,
            1,
            2,
            2,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            3,
            1,
            1,
            1,
            1,
            1,
            1,
        ],
        "direct_candidates_dict": {1: 26, 2: 4, 3: 1, 4: 0, 5: 0},
    },
    903: {
        "parties": {1: 487487, 2: 122291, 3: 228057, 4: 223034, 5: 95537},
        "nb_seats": 16,
        "direct_candidates": [1, 1, 1, 1, 1, 1, 1, 1],
        "direct_candidates_dict": {1: 8, 2: 0, 3: 0, 4: 0, 5: 0},
    },
}

for wahlkreis in wahlkreise_dict:
    print(wahlkreis)
    wahlkreise_dict[wahlkreis]["direct_candidates_dict"] = {}
    for party in wahlkreise_dict[wahlkreis]["parties"]:
        print("\t", party, " ", wahlkreise_dict[wahlkreis]["parties"][party])
        number_direct_candidates = len(
            [1 for t in wahlkreise_dict[wahlkreis]["direct_candidates"] if t == party]
        )
        print(number_direct_candidates)
        wahlkreise_dict[wahlkreis]["direct_candidates_dict"][
            party
        ] = number_direct_candidates


for wahlkreis in wahlkreise_dict:
    votes = wahlkreise_dict[wahlkreis]["parties"]

    direct_candidates = wahlkreise_dict[wahlkreis]["direct_candidates_dict"]
    nb_seats = wahlkreise_dict[wahlkreis]["nb_seats"]
    x = allocate_final_seats_in_wahlkreis_nico(votes, nb_seats, direct_candidates)
    print(wahlkreis)
    print(x)