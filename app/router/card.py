import os
import typing

import fastapi
import fastapi.dependencies
import pydantic
import sqlmodel

import app.db
import app.model.card

router = fastapi.APIRouter(
    prefix="/card",
    tags=["card"],
)


@router.post("")
def create_card(card: app.model.card.CardCreate) -> app.model.card.CardPublic:
    db_card = app.model.card.Card.model_validate(card)
    with sqlmodel.Session(app.db.ENGINE) as session:
        session.add(db_card)
        session.commit()
        session.refresh(db_card)
        return db_card


@router.get("")
def view_card() -> typing.Sequence[app.model.card.CardPublic]:
    with sqlmodel.Session(app.db.ENGINE) as session:
        result = session.exec(sqlmodel.select(app.model.card.Card)).all()
    return result


def get_single_card(id: int) -> app.model.card.Card:
    with sqlmodel.Session(app.db.ENGINE) as session:
        card = session.get(entity=app.model.card.Card, ident=id)
        if not card:
            raise fastapi.HTTPException(
                status_code=404,
                detail="Card not found",
            )
    return card


@router.get("/{id}")
def view_card_single(
    card: typing.Annotated[
        app.model.card.Card,
        fastapi.Depends(get_single_card),
    ],
) -> app.model.card.CardPublic:
    return card


@router.get("/{id}/hint")
def view_card_hint(
    card: typing.Annotated[
        app.model.card.Card,
        fastapi.Depends(get_single_card),
    ],
    pos: int = fastapi.Query(ge=0, le=16),
) -> app.model.card.CardHint:
    card.remaining_hint = card.remaining_hint - 1
    if card.remaining_hint <= 0:
        raise fastapi.HTTPException(
            status_code=403,
            detail="You don't have remaining hint",
        )
    with sqlmodel.Session(app.db.ENGINE) as session:
        session.add(card)
        session.commit()
        session.refresh(card)
    return app.model.card.CardHint(
        **card.model_dump(exclude={"number"}),
        pos=pos,
        number=card.number[pos],
    )


class CardGuess(pydantic.BaseModel):
    number: str = pydantic.Field(
        min_length=app.model.card.NUMBER_LEN,
        max_length=app.model.card.NUMBER_LEN,
    )


@router.post("/{id}/guess")
def guess_card_number(
    card: typing.Annotated[
        app.model.card.Card,
        fastapi.Depends(get_single_card),
    ],
    guess: CardGuess,
):
    correct = card.number == guess.number
    with sqlmodel.Session(app.db.ENGINE) as session:
        session.delete(card)
        session.commit()
    return os.getenv("FLAG", "CORRECT") if correct else "WRONG"
