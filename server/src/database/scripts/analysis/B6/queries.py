from sqlalchemy import create_engine, text


# Replace 'your_database_url' with the actual database connection URL
from src.database.database import get_db



def q1():
    with open('q1.sql', 'r') as file:
        query = file.read()

    with get_db() as db:
        result = db.execute(text(query))
        return result.fetchall()

def q2():
    with open('q2.sql', 'r') as file:
        query = file.read()

    with get_db() as db:
        result = db.execute(text(query))
        return result.fetchall()
def q3():
    with open('q3.sql', 'r') as file:
        query = file.read()

    with get_db() as db:
        result = db.execute(text(query))
        return result.fetchall()


def q4():
    with open('q4.sql', 'r') as file:
        query = file.read()

    with get_db() as db:
        result = db.execute(text(query))
        return result.fetchall()

def q5():
    with open('q5.sql', 'r') as file:
        query = file.read()

    with get_db() as db:
        result = db.execute(text(query))
        return result.fetchall()
def q6_losers():
    with open('q6-losers.sql', 'r') as file:
        query = file.read()

    with get_db() as db:
        result = db.execute(text(query))
        return result.fetchall()

def q6_winners():
    with open('q6-winners.sql', 'r') as file:
        query = file.read()

    with get_db() as db:
        result = db.execute(text(query))
        return result.fetchall()


if __name__ == "__main__":
    result_query = q6_winners()
    for row in result_query:
        print(row)
