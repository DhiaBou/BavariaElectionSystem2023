# Python script for generating tokens based on user input and storing them in a CSV file

import csv
import hashlib
import os

from stimmabgabe.stimmkreise import stimmkreise


def generate_token(id, stimmkreis):
    """
    Generate a hash token based on the combination of id and favorite number.

    :param id: The user's id
    :param stimmkreis: The user's favorite number
    :return: A hashed token
    """
    combined_string = f"{id}{stimmkreis}"
    token = hashlib.sha256(combined_string.encode()).hexdigest()
    return token


def store_token_in_csv(token, file_name="token.csv"):
    """
    Store the generated token in a CSV file. If the file does not exist, it creates a new one.

    :param token: The token to be stored
    :param file_name: The name of the CSV file
    """
    file_exists = os.path.isfile(file_name)
    with open(file_name, "a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Token"])  # Write header if file does not exist
        writer.writerow([token])


def is_token_valid(user_id, stimmkreis, file_name="token.csv"):
    """
    Check if a token is valid. A token is valid if the file of tokens does not exist,
    or if it does exist and the token is not already in the file.

    """
    stimmkreis = int(stimmkreis)
    if not stimmkreis in stimmkreise:
        return False
    if not os.path.isfile(file_name):
        return True

    with open(file_name, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            for stimmkreis_i in stimmkreise:
                token = generate_token(user_id, stimmkreis_i)
                if token in row:
                    return False
    return True


def input_tokens():
    # Get user input
    while True:
        user_id = input("Enter your ID: ")
        stimmkreis = input("Enter your Stimmkreis: ")

        # Generate and store the token
        token = generate_token(user_id, stimmkreis)
        if not is_token_valid(user_id, stimmkreis):
            print("Token is not valid")
            continue
        store_token_in_csv(token)
        print("Token generated and stored successfully.")


if __name__ == "__main__":
    input_tokens()
