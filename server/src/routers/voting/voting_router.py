from http.client import HTTPException
from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

from database.database import get_db
from database.models.models import Erste_Stimmen, Zweite_Stimmzettel
from database.scripts.analysis.B6.queries import (
    q1,
    q2,
    q3,
    q4,
    q5,
    q6_winners,
    q6_losers,
    get_stimmzettel,
    get_zweit_stimmzettel,
)
from stimmabgabe.vote import can_vote
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class FirstVote(BaseModel):
    token: str
    code: str
    first_vote: str


class SecondVote(BaseModel):
    token: str
    code: str
    second_vote: str


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
            erste_stimme = Erste_Stimmen(
                KandidatID=vote.first_vote, StimmkreisId=vote.code
            )
            db.add(erste_stimme)

            # Update Zweite_Stimmen
            zweite_stimme = Zweite_Stimmzettel(
                KandidatID=vote.second_vote, StimmkreisId=vote.code
            )
            db.add(zweite_stimme)

            # Commit the changes
            #            db.commit()

            return {"message": "Vote received"}

        except Exception as e:
            # In case of any exception
            db.rollback()
            return {"message": f"An error occurred: {e}"}


@voting_router.post("/first_vote")
async def handle_first_vote(vote: FirstVote):
    # Create a new session
    with get_db() as db:
        try:
            # Update Erste_Stimmen with the first vote
            erste_stimme = Erste_Stimmen(
                KandidatID=vote.first_vote, StimmkreisId=vote.code
            )
            db.add(erste_stimme)

            # Commit the changes
            db.commit()
            return {"message": "First vote received"}

        except Exception as e:
            # In case of any exception
            db.rollback()
            return {"message": f"An error occurred: {e}"}

        finally:
            # Close the session
            db.close()


@voting_router.post("/second_vote")
async def handle_second_vote(vote: SecondVote):
    # Create a new session
    with get_db() as db:
        try:
            # Update Zweite_Stimmen with the second vote
            zweite_stimme = Zweite_Stimmzettel(
                KandidatID=vote.second_vote, StimmkreisId=vote.code
            )
            db.add(zweite_stimme)

            # Commit the changes
            db.commit()

            return {"message": "Second vote received"}

        except Exception as e:
            # In case of any exception
            db.rollback()
            return {"message": f"An error occurred: {e}"}

        finally:
            # Close the session
            db.close()
