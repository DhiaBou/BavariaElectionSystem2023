from src.database.seat_alloc_EStimme import get_direct_candidates
from src.database.seat_alloc_ZStimme import zweite_stimme_alloc


def seat_alloc_partei(erste, zweite):
    result = {}

    # Using a for loop
    for key in set(erste.keys()) | set(zweite.keys()):
        result[key] = erste.get(key, 0) + zweite.get(key, 0)

    # Using a dictionary comprehension (Python 3.6+)
    result_dict = {key: erste.get(key, 0) + zweite.get(key, 0) for key in set(erste) | set(zweite)}

    return result_dict
database_url = "postgresql://username:password@localhost:5433/dbname"

erste = get_direct_candidates(database_url)
zweite = zweite_stimme_alloc(database_url, 89)
seat_alloc = seat_alloc_partei(erste, zweite)
print(seat_alloc)
