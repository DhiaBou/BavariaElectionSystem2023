from sqlalchemy.sql import text

from database.database import get_db
from database.models.models import (
    Wahlkreis,
    Abgeordnete,
    Ueberhangsmandate,
    Ausgleichsmandate,
)
from database.scripts.analysis.Überhangs_ausgleich_mandaten import (
    allocate_final_seats_in_wahlkreis,
)


def create_abgeordnete():
    def get_wahlkreise():
        with get_db() as db:
            return db.query(Wahlkreis.WahlkreisId, Wahlkreis.Abgeordnetenmandate).all()

    def get_party_votes():
        query = """
            SELECT g.* 
            FROM gesamt_stimmen_pro_partei_pro_wahlkreis_view g, anteil_over_five_percent a 
            WHERE g.wahlkreisid = a.wahlkreisid AND g.parteiid = a.parteiid
        """
        with get_db() as db:
            return db.execute(text(query))

    def get_direct_candidates():
        with get_db() as db:
            return db.execute(text("SELECT * FROM direct_candidates"))

    def get_total_votes():
        with get_db() as db:
            return db.execute(text("SELECT * FROM kandidat_gasammt_stimmen"))

    def process_wahlkreise():
        wahlkreise_dict = {}
        for wahlkreis_id, nb_seats in get_wahlkreise():
            wahlkreise_dict[wahlkreis_id] = {
                "parties": {},
                "nb_seats": nb_seats,
                "direct_candidates": [],
                "direct_candidates_ids": [],
            }

        for vote_record in get_party_votes():
            if vote_record[4] > 0:
                wahlkreise_dict[vote_record[0]]["parties"][vote_record[2]] = vote_record[4]

        for candidate in get_direct_candidates():
            wahlkreis_info = wahlkreise_dict[candidate[0]]
            wahlkreis_info["direct_candidates"].append(candidate[6])
            wahlkreis_info["direct_candidates_ids"].append(candidate[3])

        return wahlkreise_dict

    def allocate_seats(wahlkreise_dict):
        kandidaten_gesammt_stimmen = list(get_total_votes())
        kandidaten_erstestimme = [candidate[3] for candidate in get_direct_candidates()]
        kandidaten_zweitestimme = []
        ueberhangs_mandate = []
        ausgleichmandate = []
        for wahlkreis, data in wahlkreise_dict.items():
            direct_candidates_count = {
                party: data["direct_candidates"].count(party) for party in data["parties"]
            }
            allocated_seats, erste_verteilung = allocate_final_seats_in_wahlkreis(
                data["parties"], data["nb_seats"], direct_candidates_count
            )

            for party, allocated_seat_count in allocated_seats.items():
                if direct_candidates_count[party] > erste_verteilung[party]:
                    ueberhangs_mandate += [(wahlkreis, party)] * (
                            direct_candidates_count[party] - erste_verteilung[party]
                    )
                elif allocated_seat_count > erste_verteilung[party]:
                    ausgleichmandate += [(wahlkreis, party)] * (
                            allocated_seat_count - erste_verteilung[party]
                    )
                remaining_seats = allocated_seat_count - direct_candidates_count[party]
                for kandidat in kandidaten_gesammt_stimmen:
                    if should_allocate_seat(
                            wahlkreis,
                            party,
                            kandidat,
                            kandidaten_erstestimme,
                            kandidaten_zweitestimme,
                            remaining_seats,
                    ):
                        kandidaten_zweitestimme.append(kandidat[0])
                        remaining_seats -= 1
                        if remaining_seats == 0:
                            break

        return (
            kandidaten_erstestimme,
            kandidaten_zweitestimme,
            ueberhangs_mandate,
            ausgleichmandate,
        )

    def should_allocate_seat(
            wahlkreis,
            party,
            kandidat,
            kandidaten_erstestimme,
            kandidaten_zweitestimme,
            remaining_seats,
    ):
        return (
                kandidat[0] // 10000 == wahlkreis
                and kandidat[3] == party
                and kandidat[0] not in kandidaten_erstestimme + kandidaten_zweitestimme
                and remaining_seats >= 1
        )

    def save_allocated_seats(kandidaten_erstestimme, kandidaten_zweitestimme):
        with get_db() as db:
            for k in kandidaten_zweitestimme:
                db.add(Abgeordnete(KandidatID=k, Erststimme=False))
            for k in kandidaten_erstestimme:
                db.add(Abgeordnete(KandidatID=k, Erststimme=True))
            db.commit()

    def save_uberhangs_ausgleichs_mandate(ueberhangs_mandate, ausgleichmandate):
        with get_db() as db:
            for m in ueberhangs_mandate:
                db.add(Ueberhangsmandate(WahlkreisId=m[0], ParteiID=m[1]))
            for m in ausgleichmandate:
                db.add(Ausgleichsmandate(WahlkreisId=m[0], ParteiID=m[1]))
            db.commit()

    wahlkreise_dict = process_wahlkreise()
    erstestimme, zweitestimme, ueberhangs_mandate, ausgleichmandate = allocate_seats(
        wahlkreise_dict
    )
    save_allocated_seats(erstestimme, zweitestimme)
    save_uberhangs_ausgleichs_mandate(ueberhangs_mandate, ausgleichmandate)
