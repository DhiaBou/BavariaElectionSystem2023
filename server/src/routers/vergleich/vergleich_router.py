from fastapi import APIRouter

from database.scripts.analysis.B6.queries import diffference_2023_2018

vrgleich_router = APIRouter(
    prefix="/vergleich",
)


@vrgleich_router.get("/")
async def get_wahlkreis():
    return diffference_2023_2018()
