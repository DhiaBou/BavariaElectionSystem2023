from src.database.sainte_lague_iterative import sainte_lague_iterative_dict


def allocate_final_seats_in_wahlkreis(votes, total_seats, erste_stimme):
    erste_verteilung = sainte_lague_iterative_dict(votes, total_seats)
    for party in erste_verteilung:
        erste_verteilung[party] = max(erste_verteilung[party], erste_stimme[party])

    total_votes = sum(votes.values())
    print("starting")
    while True:
        maxx = 0
        p = None
        for party in votes:
            anteil_votes = votes[party] / total_votes
            anteil_chairs = erste_verteilung[party] / sum(erste_verteilung.values())
            if anteil_votes - anteil_chairs > maxx:
                maxx = anteil_votes - anteil_chairs
                p = party
        if maxx < 0.018:
            break
        print("adding 1")
        erste_verteilung[p] += 1
    return erste_verteilung
