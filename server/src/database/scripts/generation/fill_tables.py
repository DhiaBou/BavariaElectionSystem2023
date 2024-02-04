from pathlib import Path

from sqlalchemy import text

from database.database import get_db
from database.scripts.analysis.B6.queries import reload
from database.scripts.generation.create_candidates import create_candidates
from database.scripts.generation.generate_votes import generate_votes


def fill_tables():
    with open(Path(__file__).parent / "insert_data.sql", "r", encoding="utf-8") as file:
        query = file.read()

    with get_db() as db:
        db.execute(text(query))
        db.commit()
    return 'ok'


fill_tables()
create_candidates()
generate_votes()
reload()
