from fastapi import APIRouter

from database.scripts.analysis.B6.queries import (
    q1,
    q2,
    q3,
    q4,
    q5,
    q6,
    reload,
)

wahlkreis_router = APIRouter(
    prefix="/wahlkreis",
)


@wahlkreis_router.get("/")
async def get_wahlkreis():
    return ["3asba"]


@wahlkreis_router.get("/q1")
async def query1():
    return q1()


@wahlkreis_router.get("/reload")
async def query1():
    return reload()


@wahlkreis_router.get("/q2")
async def query2():
    return q2()


@wahlkreis_router.get("/q2")
async def query2():
    return q2()


@wahlkreis_router.get("/q3")
async def query3():
    return q3()


@wahlkreis_router.get("/q4")
async def query4():
    return q4()


@wahlkreis_router.get("/q5")
async def query5():
    return q5()


@wahlkreis_router.get("/q6")
async def query6():
    return q6()


@wahlkreis_router.get("/1")
async def get_q1():
    return ["3asbbbba"]
