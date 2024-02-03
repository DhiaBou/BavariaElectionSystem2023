from fastapi import APIRouter

from database.scripts.analysis.B6.queries import get_income_pro_wahlkreis, get_income_pro_stimmkreis,get_auslaender_quote

other = APIRouter(
    prefix="/other",
)

@other.get("/")
async def get_():
    return ["3asba"]
@other.get("/wahlkreis")
async def wahlkreis():
    return get_income_pro_wahlkreis()

@other.get("/stimmkreis")
async def stimmkreis():
    return get_income_pro_stimmkreis()

@other.get("/auslaender")
async def auslaender_quote():
    return get_auslaender_quote()



