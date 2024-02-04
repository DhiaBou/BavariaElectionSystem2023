import logging
from asyncio import create_task
from http.client import HTTPException

from fastapi import APIRouter
from pydantic import BaseModel

from database.database import get_db
from database.models.models import Erste_Stimmen, Zweite_Stimmzettel, Zweite_Stimme_Ohne_Kandidaten
from database.scripts.analysis.B6.queries import (
    get_stimmzettel,
    get_zweit_stimmzettel, reload,
)
from stimmabgabe.vote import can_vote, remove_token_from_csv


class Vote(BaseModel):
    token: str
    code: str
    first_vote: str
    second_vote: str


voting_router = APIRouter(
    prefix="/vote",
)


@voting_router.get("/")
async def get_candidates(voter_id: str, code: str):
    print(voter_id, code)
    vote = can_vote(voter_id, code)
    if not vote:
        raise HTTPException()
    return [vote, get_stimmzettel(code), get_zweit_stimmzettel(code)]


@voting_router.post("/submit_vote")
async def submit_vote(vote: Vote):
    # Create a new session
    with get_db() as db:
        try:
            # Assuming 'vote' has attributes like 'first_vote', 'second_vote', etc.
            # Update Erste_Stimmen
            if vote.first_vote != '0':
                erste_stimme = Erste_Stimmen(
                    KandidatID=vote.first_vote, StimmkreisId=vote.code
                )
                db.add(erste_stimme)

            if vote.second_vote != '0':
                if len(vote.second_vote) <= 2:
                    # Update Zweite_Stimmen
                    zweite_stimme = Zweite_Stimme_Ohne_Kandidaten(
                        ParteiID=vote.second_vote, StimmkreisId=vote.code
                    )
                else:
                    zweite_stimme = Zweite_Stimmzettel(
                        KandidatID=vote.second_vote, StimmkreisId=vote.code
                    )
                db.add(zweite_stimme)

            # Commit the changes
            db.commit()
            remove_token_from_csv(vote.token)

            async def r():
                reload()

            create_task(r())
            return {"message": "Vote received"}

        except Exception as e:
            # In case of any exception
            db.rollback()
            logging.info("Error")
            return {"message": f"An error occurred: {e}"}
