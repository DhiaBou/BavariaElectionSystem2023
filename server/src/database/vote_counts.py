from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlalchemy as sa


def get_vote_counts(database_url):
    # Create an engine and bind it to a session
    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    # SQL query to get vote counts
    sql = """WITH TotalVotes AS (
    SELECT
        COUNT(*) AS TotalSecondVotes
    FROM
        zweite_stimmzettel
),
PartyVotes AS (
    SELECT
        p."ParteiID",
        COUNT(*) AS "Votes"
    FROM
        zweite_stimmzettel s
    JOIN
        Kandidaten k ON s."KandidatID" = k."KandidatID"
    JOIN
        Parteien p ON k."ParteiID" = p."ParteiID"
    GROUP BY
        p."ParteiID"
),
ValidParties AS (
    SELECT
        pv."ParteiID",
        pv."Votes"
    FROM
        PartyVotes pv
    WHERE
        (pv."Votes" / (SELECT TotalSecondVotes FROM TotalVotes)) * 100 >= 5 -- Assuming a 5% threshold
)
SELECT
    p."ParteiID", p."Name",
    COUNT(*) AS Votes
FROM
    zweite_stimmzettel s
JOIN
    Kandidaten k ON s."KandidatID" = k."KandidatID"
JOIN
    Parteien p ON k."ParteiID" = p."ParteiID"
GROUP BY
    p."ParteiID"

"""

    # Execute the query
    try:
        vote_counts = {}
        results = session.execute(sa.text(sql))

        for row in results:
            print(row)
            vote_counts[row[0]] = row[2]

        return vote_counts
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        session.close()


# Replace with your database URL
database_url = "postgresql://username:password@localhost:5433/dbname"

# Get vote counts
vote_counts = get_vote_counts(database_url)

# Print the vote counts (or proceed with seat allocation)
print(vote_counts)
