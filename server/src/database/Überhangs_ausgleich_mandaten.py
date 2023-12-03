from src.database.test_algo import sainte_lague_iterative_dict


def allocate_final_seats_in_wahlkreis(votes, total_seats, erste_stimme):
    erste_verteilung = sainte_lague_iterative_dict(votes, total_seats)
    difference_dict = {key: erste_verteilung[key] - erste_stimme[key] for key in erste_verteilung if key in erste_stimme}

    positive_dict = {}
    negative_dict = {}

    # Iterate through the original dictionary
    for key, value in difference_dict.items():
        if value > 0:
            positive_dict[key] = value
        elif value < 0:
            negative_dict[key] = value

    number_of_überhangsmandate = 0

    for key, value in difference_dict.items():
        if value < 0:
            number_of_überhangsmandate += abs(value)

    votes_without_überhangs = {}

    # Iterate through the keys in dict1
    for key in votes:
        # Check if the value in dict2 is positive
        if difference_dict.get(key, 0) > 0:
            # Add the key and value from dict1 to the result_dict
            votes_without_überhangs[key] = votes[key]

    zweite_alloc = sainte_lague_iterative_dict(votes_without_überhangs, number_of_überhangsmandate)

    final_alloc = {
        key: (erste_verteilung[key] - negative_dict[key]) if key in negative_dict else (
                    erste_verteilung[key] + zweite_alloc[key])
        for key in erste_verteilung
    }
    return final_alloc



votes = {1: 487487, 2: 122291, 3: 228057, 4: 223034, 5: 95537}


direct_candidates =  {1: 8, 2: 0, 3: 0, 4: 0, 5: 0}


x =allocate_final_seats_in_wahlkreis(votes, 16, direct_candidates)
print(x)