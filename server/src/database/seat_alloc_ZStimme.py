from vote_counts import get_vote_counts


def allocate_seats_sainte_lague(vote_counts, total_seats):
    """
    Allocate seats using the Sainte-Laguë/Schepers method.

    :param vote_counts: Dictionary with ParteiID as keys and vote counts as values.
    :param total_seats: Total number of seats to allocate.
    :return: Dictionary with ParteiID as keys and allocated seat counts as values.
    """
    # Initialize the seat allocation with zero seats for each party
    seat_allocation = {party_id: 0 for party_id in vote_counts}

    # Calculate quotients for each party and each divisor, and store them with their respective party and divisor
    quotients = []
    for party_id, votes in vote_counts.items():
        for divisor in range(1, total_seats * 2, 2):  # Divisors are 1, 3, 5, 7, ...
            quotients.append((votes / divisor, party_id))

    # Sort the quotients in descending order
    quotients.sort(reverse=True)

    # Allocate seats based on the highest quotients
    for i in range(total_seats):
        _, party_id = quotients[i]
        seat_allocation[party_id] += 1

    return seat_allocation


database_url = "postgresql://username:password@localhost:5433/dbname"


# Example vote counts

def zweite_stimme_alloc(database_url, total_seats):
    vote_counts = get_vote_counts(database_url)

    # Allocate seats for the example vote counts
    seat_allocation_result = allocate_seats_sainte_lague(vote_counts, total_seats)
    return seat_allocation_result
