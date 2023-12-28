# Python script for generating tokens based on user input and storing them in a CSV file

import hashlib
import csv
import os


def generate_token(id, favorite_number):
    """
    Generate a hash token based on the combination of id and favorite number.

    :param id: The user's id
    :param favorite_number: The user's favorite number
    :return: A hashed token
    """
    combined_string = f"{id}{favorite_number}"
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


def input_tokens():
    # Get user input
    while True:
        user_id = input("Enter your ID: ")
        favorite_number = input("Enter your Stimmkreis: ")

        # Generate and store the token
        token = generate_token(user_id, favorite_number)
        store_token_in_csv(token)
        print("Token generated and stored successfully.")


if __name__ == "__main__":
    input_tokens()
