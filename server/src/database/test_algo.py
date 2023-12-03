



def sainte_lague_iterative(votes, total_seats):
    total_votes = sum(votes)
    divisor = total_votes / total_seats
    seats_allocated = [0] * len(votes)
    allocation = [0] * len(votes)
    divisors_ = [0] * len(votes)

    while True:
        for i in range(len(votes)):
            allocation[i] = votes[i] / divisor
            seats_allocated[i] = round(allocation[i])

        allocated_seats = sum(seats_allocated)
        print(seats_allocated)
        if allocated_seats == total_seats:
            break
        elif allocated_seats > total_seats:
            for i in range(len(votes)):
                divisors_[i] = votes[i] / (round(allocation[i]) - 0.5)
            divisor = sum(sorted(divisors_)[:2]) / 2
        else:
            for i in range(len(votes)):
                divisors_[i] = votes[i] / (round(allocation[i]) + 0.5)
            divisor = sum(sorted(divisors_)[:-2]) / 2

    return seats_allocated








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
        print(seats_allocated)
        if allocated_seats == total_seats:
            break
        elif allocated_seats > total_seats:
            for parteiID in votes.keys():
                divisors_[parteiID] = votes[parteiID] / (round(allocation[parteiID]) - 0.5)
            divisor = sum(sorted(divisors_.values())[:2]) / 2
        else:
            for parteiID in votes.keys():
                divisors_[parteiID] = votes[parteiID] / (round(allocation[parteiID]) + 0.5)
            divisor = sum(sorted(divisors_.values())[:-2]) / 2

    return seats_allocated

# Example usage
votes = {'PartyA': 10000, 'PartyB': 6000, 'PartyC': 1500}  # Example vote counts for three parties
total_seats = 8  # Total seats to allocate
result = sainte_lague_iterative_dict(votes, total_seats)
print(result)
