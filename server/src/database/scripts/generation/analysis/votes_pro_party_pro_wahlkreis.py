from sqlalchemy.sql import text, func

from database.models.models import Wahlkreis, Stimmkreis
from src.database.database import get_db


wahlkreise_dict = {}

with get_db() as db:
    wahlkreise = db.query(
        Wahlkreis.WahlkreisId,
        Wahlkreis.Abgeordnetenmandate,
    ).all()
    for wahlkreis in wahlkreise:
        wahlkreise_dict[wahlkreis[0]] = {
            "parties": {},
            "nb_seats": wahlkreis[1],
            "direct_candidates": [],
        }

with get_db() as db:
    res = db.execute(text("select * from gesamt_stimmen_pro_partei_pro_wahlkreis_view"))
    for r in res:
        if r[4] > 0:
            wahlkreise_dict[r[0]]["parties"][r[2]] = r[4]

with get_db() as db:
    res = db.execute(text("select * from direct_candidates"))
    for r in res:
        wahlkreise_dict[r[0]]["direct_candidates"].append(r[6])
print(wahlkreise_dict)
x = {
    907: {
        "parties": {
            1: 706704,
            2: 245253,
            3: 328583,
            4: 328165,
            5: 134399,
            6: 55016,
            7: 24694,
            8: 17031,
            9: 29511,
            10: 24072,
            11: 14086,
            12: 6326,
            14: 22250,
        },
        "nb_seats": 26,
        "direct_candidates": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    },
    905: {
        "parties": {
            1: 733528,
            2: 295591,
            3: 172099,
            4: 249643,
            5: 192782,
            6: 43749,
            7: 39929,
            8: 10354,
            9: 27712,
            11: 15361,
            13: 6252,
            14: 17574,
        },
        "nb_seats": 24,
        "direct_candidates": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    },
    906: {
        "parties": {
            1: 611164,
            2: 198158,
            3: 179068,
            4: 228188,
            5: 137383,
            6: 38401,
            7: 25233,
            8: 12326,
            9: 23669,
            14: 14043,
        },
        "nb_seats": 19,
        "direct_candidates": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    },
    904: {
        "parties": {
            1: 481744,
            2: 120644,
            3: 178045,
            4: 207627,
            5: 121592,
            6: 26780,
            7: 18422,
            8: 9435,
            9: 17998,
            14: 8651,
            15: 4852,
        },
        "nb_seats": 16,
        "direct_candidates": [1, 1, 1, 1, 1, 1, 1, 1],
    },
    902: {
        "parties": {
            1: 429120,
            2: 96504,
            3: 402629,
            4: 242784,
            5: 71833,
            6: 32099,
            7: 12605,
            8: 19533,
            9: 36818,
            12: 4177,
            14: 5911,
        },
        "nb_seats": 18,
        "direct_candidates": [1, 1, 1, 3, 1, 1, 1, 1, 1],
    },
    901: {
        "parties": {
            1: 1609824,
            2: 894284,
            3: 675368,
            4: 520994,
            5: 387227,
            6: 190047,
            7: 64332,
            8: 48350,
            9: 83003,
            10: 40082,
            11: 40345,
            12: 9182,
            13: 7774,
            14: 40539,
            15: 31923,
        },
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
    },
    903: {
        "parties": {
            1: 487487,
            2: 122291,
            3: 228057,
            4: 223034,
            5: 95537,
            6: 27795,
            7: 15663,
            8: 12451,
            9: 26513,
            12: 3140,
            14: 10521,
            15: 4919,
        },
        "nb_seats": 16,
        "direct_candidates": [1, 1, 1, 1, 1, 1, 1, 1],
    },
}


def sainte_lague_iterative(votes, total_seats):
    total_votes = sum(votes)
    divisor = total_votes / total_seats
    seats_allocated = [0] * len(votes)
    remainders = [0] * len(votes)

    while True:
        for i in range(len(votes)):
            allocation = votes[i] / divisor
            seats_allocated[i] = round(allocation)
            remainders[i] = allocation - seats_allocated[i]

        allocated_seats = sum(seats_allocated)
        print(seats_allocated)
        if allocated_seats == total_seats:
            break
        elif allocated_seats < total_seats:
            for _ in range(total_seats - allocated_seats):
                max_index = remainders.index(max(remainders))
                seats_allocated[max_index] += 1
                remainders[max_index] = -1
        elif allocated_seats > total_seats:
            for _ in range(allocated_seats - total_seats):
                min_index = remainders.index(min(remainders))
                seats_allocated[min_index] -= 1
                remainders[min_index] = 1

        break

    return seats_allocated
