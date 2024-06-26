import contextlib

import fastapi

from . import router


@contextlib.asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    import sqlmodel

    from . import db

    sqlmodel.SQLModel.metadata.create_all(bind=db.ENGINE)

    yield


app = fastapi.FastAPI(
    title="Guess Lucky Number",
    version="0.1.0",
    description="guess your lucky number and win the flag if you can guess it right!",
    lifespan=lifespan,
)
app.include_router(router=router.router)
