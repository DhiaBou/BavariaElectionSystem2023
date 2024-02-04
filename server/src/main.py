from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.vergleich.vergleich_router import vrgleich_router
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


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


app.include_router(wahlkreis_router)
app.include_router(voting_router)
app.include_router(vrgleich_router)
