# Replace 'your_database_url' with the actual database connection URL
from pathlib import Path



def get_auslaender_quote():
    query = """
        select * from auslaender_quote      
         """
    with get_db() as db:
        result = db.execute(text(query))

        # Fetch column names
        column_names = result.keys()

        # Fetch all rows and convert them to dictionaries
        rows = result.fetchall()
        result_list = [dict(zip(column_names, row)) for row in rows]
    return result_list



def get_income_pro_stimmkreis():
    query = """
          
            select g."Gemeineschluessel", s."StimmkreisId", s."Name", e."Kreis",g."Name", e."Einkommen"
            from stimmkreis s, "Einkommen_pro_stimmkreis"  e, gemeinde g
            where g."Kreisschluessel" = e."Kreis" and g."StimmkreisID" = s."StimmkreisId"


         """
    with get_db() as db:
        result = db.execute(text(query))

        # Fetch column names
        column_names = result.keys()

        # Fetch all rows and convert them to dictionaries
        rows = result.fetchall()
        result_list = [dict(zip(column_names, row)) for row in rows]
    return result_list

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
from database.database import get_db
from sqlalchemy.sql import text


def get_income_pro_wahlkreis():
    query = """
        SELECT
    w."WahlkreisId",
    w."Name",
    e."Einkommen",
    SUM(a.anteil) FILTER (WHERE p."ParteiID" = '1') AS "CSU",
    SUM(a.anteil) FILTER (WHERE p."ParteiID" = '2') AS "GRÜNE",
    SUM(a.anteil) FILTER (WHERE p."ParteiID" = '3') AS "FREIE WÄHLER",
    SUM(a.anteil) FILTER (WHERE p."ParteiID" = '4') AS "AfD",
    SUM(a.anteil) FILTER (WHERE p."ParteiID" = '5') AS "SPD"

FROM wahlkreis w
JOIN "Einkommen_pro_wahlkreis" e ON w."WahlkreisId" = e."WahlkreisID"
JOIN anteil_over_five_percent a ON a.wahlkreisid = w."WahlkreisId"
JOIN parteien p ON p."ParteiID" = a.parteiid
GROUP BY w."WahlkreisId", w."Name", e."Einkommen"
ORDER BY w."WahlkreisId"
      
         """
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


def diffference_2023_2018():
    with open(Path(__file__).parent / "difference_2023_2018.sql", "r") as file:
        query = file.read()

    with get_db() as db:
        result = db.execute(text(query))

        # Fetch column names
        column_names = result.keys()

        # Fetch all rows and convert them to dictionaries
        rows = result.fetchall()
        result_list = [dict(zip(column_names, row)) for row in rows]
    return result_list


def reload():
    with open(Path(__file__).parent / "views_code.sql", "r") as file:
        query = file.read()

    with get_db() as db:
        db.execute(text(query))
        db.commit()
    return 'ok'


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



def q6():
    with open(Path(__file__).parent / "q6.sql", "r") as file:
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
            row[1] + " - " + str(row[2]) + " - " + row[0] + "__" + str(row[3])
            for row in result
            if int(row[2]) == int(stimmkreis)
        ]
    return ["-- keine Wahl -- __0"] + result_list


def get_zweit_stimmzettel(stimmkreis):
    with open(Path(__file__).parent / "zweit_stimmzettel_generator.sql", "r") as file:
        query = file.read()

    with get_db() as db:
        result = db.execute(text(query)).all()

        result_list = [
            row[1] + " / " + row[0] + "__" + str(row[2])
            for row in result
            if (row[2] - 9000000) // 10000 == int(stimmkreis) // 100
        ]
        result_list += list(set(row[1] + " __" + str(row[3]) for row in result))
    return ["-- keine Wahl -- __0"] + sorted(result_list)


if __name__ == "__main__":
    result_query = get_stimmzettel(101)
    for row in result_query:
        print(row)
