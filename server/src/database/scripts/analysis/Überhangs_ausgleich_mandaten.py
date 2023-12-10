def sainte_lague_iterative_dict(votes, total_seats):
    total_votes = sum(votes.values())
    divisor = total_votes / total_seats
    seats_allocated = {parteiID: 0 for parteiID in votes.keys()}
    allocation = {parteiID: 0 for parteiID in votes.keys()}
    divisors_ = {parteiID: 0 for parteiID in votes.keys()}

    while True:
        for parteiID in votes.keys():
            allocation[parteiID] = votes[parteiID] / divisor
            seats_allocated[parteiID] = round(allocation[parteiID])

        allocated_seats = sum(seats_allocated.values())

        if allocated_seats == total_seats:
            break
        elif allocated_seats > total_seats:
            for parteiID in votes.keys():
                divisors_[parteiID] = votes[parteiID] / (round(allocation[parteiID]) - 0.5)
            divisor = sum(sorted(divisors_.values())[:2]) / 2
        else:
            for parteiID in votes.keys():
                divisors_[parteiID] = votes[parteiID] / (round(allocation[parteiID]) + 0.5)
            divisor = sum(sorted(divisors_.values(), reverse=True)[:2]) / 2

    return seats_allocated


def allocate_final_seats_in_wahlkreis(votes, total_seats, erste_stimme):
    erste_verteilung = sainte_lague_iterative_dict(votes, total_seats)
    divisor = -1
    for party in erste_verteilung:
        if erste_stimme[party] > erste_verteilung[party]:
            divisor = votes[party] / (erste_stimme[party] - 0.5)
            print(divisor)
    if divisor != -1:
        allocation = {parteiID: 0 for parteiID in votes.keys()}
        for parteiID in votes.keys():
            allocation[parteiID] = votes[parteiID] / divisor
            erste_verteilung[parteiID] = round(allocation[parteiID])

    return erste_verteilung
