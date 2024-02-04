from fastapi import APIRouter

from database.scripts.analysis.B6.queries import (
    q1,
    q2,
    q3,
    q4,
    q5,
    q6,
    reload,
    get_income_pro_wahlkreis,
)

wahlkreis_router = APIRouter(
    prefix="/wahlkreis",
)


@wahlkreis_router.get("/")
async def get_health():
    return []


@wahlkreis_router.get("/q1")
async def query1():
    return await q1()


@wahlkreis_router.get("/reload")
async def query1():
    return reload()


@wahlkreis_router.get("/q2")
async def query2():
    return await q2()


@wahlkreis_router.get("/q3")
async def query3():
    return await q3()


@wahlkreis_router.get("/q4")
async def query4():
    return await q4()


@wahlkreis_router.get("/q5")
async def query5():
    return await q5()


@wahlkreis_router.get("/q6")
async def query6():
    return await q6()


@wahlkreis_router.get("/einkommen")
async def get_income():
    return get_income_pro_wahlkreis()
