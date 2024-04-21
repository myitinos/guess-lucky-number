import datetime
import secrets
import string

import sqlmodel

NUMBER_LEN = 6
HINT_LEN = 4


def random_number_generator():
    return "".join([secrets.choice(string.digits) for _ in range(NUMBER_LEN)])


class CardCreate(sqlmodel.SQLModel):
    name: str


class CardPublic(CardCreate):
    id: int | None = sqlmodel.Field(default=None, primary_key=True)
    remaining_hint: int = sqlmodel.Field(default=HINT_LEN)


class CardHint(CardPublic):
    pos: int
    number: str = sqlmodel.Field(max_length=1, min_length=1)


class Card(CardPublic, table=True):
    number: str = sqlmodel.Field(
        max_length=NUMBER_LEN,
        min_length=NUMBER_LEN,
        default_factory=random_number_generator,
    )
    created_at: datetime.datetime = sqlmodel.Field(
        default_factory=datetime.datetime.now,
        index=True,
    )
