from http.client import HTTPException
from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

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
    print("Received Vote:")
    print("token:", vote.token)
    print("Stimmkreis ID:", vote.code)
    print("First Vote Candidate ID:", vote.first_vote)
    print("Second Vote Candidate ID:", vote.second_vote)

    return {"message": "Vote received"}
