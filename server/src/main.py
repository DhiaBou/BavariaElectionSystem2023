from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.voting.voting_router import voting_router
from routers.wahlkreis.wahlkreis_router import wahlkreis_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allows all origins from localhost:3000
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
async def root():
    return ["o World", "OMARRRRR"]


@app.get("/list")
async def roott():
    return [
        {"product_id": "prod_1", "timestamp": "2023-12-01T12:00:00Z"},
        {"product_id": "prod_1", "timestamp": "2023-12-02T15:30:00Z"},
        {"product_id": "prod_2", "timestamp": "2023-12-01T10:00:00Z"},
        {"product_id": "prod_3", "timestamp": "2023-12-03T08:45:00Z"},
    ]


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


app.include_router(wahlkreis_router)
app.include_router(voting_router)
