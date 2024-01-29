import csv
import hashlib
from pathlib import Path


def generate_token(id, favorite_number):
    combined_string = id + favorite_number
    hashed_token = hashlib.sha256(combined_string.encode()).hexdigest()
    return hashed_token


def read_tokens_from_csv():
    tokens = []
    try:
        with open(Path(__file__).parent / "token.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header
            for row in reader:
                tokens.append(row[0])  # The first element is the token
        return tokens
    except FileNotFoundError:
        print("Token file not found.")
        return None


def remove_token_from_csv(token):
    rows = []
    with open(Path(__file__).parent / "token.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] != token:
                rows.append(row)

    with open(Path(__file__).parent / "token.csv", "w", newline='') as file:
        writer = csv.writer(file)
        for row in rows:
            writer.writerow(row)


def can_vote(id, favorite_number):
    token = generate_token(id, favorite_number)
    tokens = read_tokens_from_csv()
    if tokens and token in tokens:
        return token
    else:
        return False


def vote(token, stimmkreis_id, first_vote, second_vote):
    tokens = read_tokens_from_csv()
    if tokens and token in tokens:
        remove_token_from_csv(token)

        return True
    else:
        return False

# if __name__ == "__main__":
#     while True:
#         id = input("Enter your ID: ")
#         favorite_number = input("Enter your favorite number: ")
#         token = generate_token(id, favorite_number)
#
#         tokens = read_tokens_from_csv()
#
#         if tokens and token in tokens:
#             vote = input("Enter your vote: ")
#             print(f"Your vote '{vote}' has been recorded.")
#             remove_token_from_csv(token)
#         else:
#             print("You cannot vote.")
