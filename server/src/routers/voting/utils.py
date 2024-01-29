from sqlalchemy import text

from database.database import get_db


def parse_id_first_vote(first_vote):
    query = ''
    with get_db() as db:
        result = db.execute(text('select k.ka'))

    return ''


def parse_id_second_vote(second_vote: str):
    if '/' in second_vote:
        pass
    else:
        pass
    return ''
