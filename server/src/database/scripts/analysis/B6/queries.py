from sqlalchemy import create_engine, text


# Replace 'your_database_url' with the actual database connection URL
from src.database.database import get_db



def q1():
    with open('/database/scripts/analysis/B6/q1.sql', 'r') as file:
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
    with open('/database/scripts/analysis/B6/q2.sql', 'r') as file:
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
    with open('/database/scripts/analysis/B6/q3.sql', 'r') as file:
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
    with open('/database/scripts/analysis/B6/q4.sql', 'r') as file:
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
    with open('/database/scripts/analysis/B6/q5.sql', 'r') as file:
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
    with open('/database/scripts/analysis/B6/q6-losers.sql', 'r') as file:
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
    with open('/database/scripts/analysis/B6/q6-winners.sql', 'r') as file:
        query = file.read()

    with get_db() as db:
        result = db.execute(text(query))

        # Fetch column names
        column_names = result.keys()

        # Fetch all rows and convert them to dictionaries
        rows = result.fetchall()
        result_list = [dict(zip(column_names, row)) for row in rows]
    return result_list


if __name__ == "__main__":
    result_query = q1()
    print(result_query)
    for row in result_query:
        print(row)
