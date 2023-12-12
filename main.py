from fastapi import FastAPI
from login.inciar_Sesion import router as rl


app = FastAPI()

app.include_router(rl)
