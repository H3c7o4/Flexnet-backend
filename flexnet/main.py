from fastapi import FastAPI
from .models import Base
from .database import engine
from .routers import user, authentication, movie, score

from starlette.responses import JSONResponse

app = FastAPI(title='Flexnet API', version='V1.0.0')

Base.metadata.create_all(engine)

app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(movie.router)
app.include_router(score.router)

@app.get('/')
async def hello_world():
    return 'Hello friends !'