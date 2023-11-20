from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlalchemy as sa

def get_direct_candidates(database_url):
    # Create an engine and bind it to a session
    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    # SQL query to get direct candidates
    sql = """
WITH CandidateVotes AS (
    SELECT
        Erste_Stimmzettel."StimmkreisId",
        Kandidaten."KandidatID",
        Kandidaten."Vorname",
        Kandidaten."Nachname",
        COUNT(Erste_Stimmzettel."KandidatID") AS Stimmenzahl
    FROM
        Erste_Stimmzettel
    JOIN
        Kandidaten ON Erste_Stimmzettel."KandidatID" = Kandidaten."KandidatID"
    GROUP BY
        Erste_Stimmzettel."StimmkreisId", Kandidaten."KandidatID"
),
RankedCandidates AS (
    SELECT
        cv."StimmkreisId",
        cv."KandidatID",
        cv."Vorname",
        cv."Nachname",
        Stimmenzahl,
        RANK() OVER (PARTITION BY cv."StimmkreisId" ORDER BY Stimmenzahl DESC) AS Rank
    FROM
        CandidateVotes cv
),
 direct_candidates as (
     SELECT
        rc."StimmkreisId",
        sk."Name" AS StimmkreisName,
        rc."KandidatID",
        rc."Vorname",
        rc."Nachname",
        rc.Stimmenzahl
    FROM
        RankedCandidates rc
    JOIN
        Stimmkreis sk ON rc."StimmkreisId" = sk."StimmkreisId"
    WHERE
        rc.Rank = 1
    )

select * from direct_candidates"""

    # Execute the query
    try:
        direct_candidates = {}
        results = session.execute(sa.text(sql))
        index = 0
        for row in results:
            direct_candidates[index] = row.KandidatID
            index += 1
        return direct_candidates
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        session.close()

# Replace with your database URL
database_url = "postgresql://username:password@localhost:5433/dbname"

# Get vote counts
direct_candidates = get_direct_candidates(database_url)

