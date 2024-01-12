from sqlalchemy import text

# Replace 'your_database_url' with the actual database connection URL
from pathlib import Path

from database.database import get_db


def q1():
    with open(Path(__file__).parent / "q1.sql", "r") as file:
        query = file.read()

    with get_db() as db:
        result = db.execute(text(query))

        # Fetch column names
        column_names = result.keys()

        # Fetch all rows and convert them to dictionaries
        rows = result.fetchall()
        result_list = [dict(zip(column_names, row)) for row in rows]

    return result_list


def q2():
    with open(Path(__file__).parent / "q2.sql", "r") as file:
        query = file.read()

    with get_db() as db:
        result = db.execute(text(query))

        # Fetch column names
        column_names = result.keys()

        # Fetch all rows and convert them to dictionaries
        rows = result.fetchall()
        result_list = [dict(zip(column_names, row)) for row in rows]
    return result_list


def q3():
    with open(Path(__file__).parent / "q3.sql", "r") as file:
        query = file.read()

    with get_db() as db:
        result = db.execute(text(query))

        # Fetch column names
        column_names = result.keys()

        # Fetch all rows and convert them to dictionaries
        rows = result.fetchall()
        result_list = [dict(zip(column_names, row)) for row in rows]
    return result_list


def q4():
    with open(Path(__file__).parent / "q4.sql", "r") as file:
        query = file.read()

    with get_db() as db:
        result = db.execute(text(query))

        # Fetch column names
        column_names = result.keys()

        # Fetch all rows and convert them to dictionaries
        rows = result.fetchall()
        result_list = [dict(zip(column_names, row)) for row in rows]
    return result_list


def q5():
    with open(Path(__file__).parent / "q5.sql", "r") as file:
        query = file.read()

    with get_db() as db:
        result = db.execute(text(query))

        # Fetch column names
        column_names = result.keys()

        # Fetch all rows and convert them to dictionaries
        rows = result.fetchall()
        result_list = [dict(zip(column_names, row)) for row in rows]
    return result_list


def q6_losers():
    with open(Path(__file__).parent / "q6-losers.sql", "r") as file:
        query = file.read()

    with get_db() as db:
        result = db.execute(text(query))

        # Fetch column names
        column_names = result.keys()

        # Fetch all rows and convert them to dictionaries
        rows = result.fetchall()
        result_list = [dict(zip(column_names, row)) for row in rows]
    return result_list


def q6_winners():
    with open(Path(__file__).parent / "q6-winners.sql", "r") as file:
        query = file.read()

    with get_db() as db:
        result = db.execute(text(query))

        # Fetch column names
        column_names = result.keys()

        # Fetch all rows and convert them to dictionaries
        rows = result.fetchall()
        result_list = [dict(zip(column_names, row)) for row in rows]
    return result_list


def get_stimmzettel(stimmkreis):
    with open(Path(__file__).parent / "erst_stimmzettel_generator.sql", "r") as file:
        query = file.read()

    with get_db() as db:
        result = db.execute(text(query)).all()

        result_list = [
            row[1] + " / " + str(row[2]) + " / " + row[0] for row in result if int(row[2]) == int(stimmkreis)
        ]
    return result_list


def get_zweit_stimmzettel(stimmkreis):
    with open(Path(__file__).parent / "zweit_stimmzettel_generator.sql", "r") as file:
        query = file.read()

    with get_db() as db:
        result = db.execute(text(query)).all()

        result_list = [
            row[1] + " / " + row[0] for row in result if (row[2] - 9000000) // 10000 == int(stimmkreis) // 100
        ]
        result_list += list(set(row[1] for row in result))
    return sorted(result_list)


if __name__ == "__main__":
    result_query = get_stimmzettel(101)
    for row in result_query:
        print(row)
