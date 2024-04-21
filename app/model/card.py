import datetime
import secrets
import string

import sqlmodel


def random_number_generator():
    return "".join([secrets.choice(string.digits) for _ in range(16)])


class CardCreate(sqlmodel.SQLModel):
    name: str


class CardPublic(CardCreate):
    id: int | None = sqlmodel.Field(default=None, primary_key=True)
    remaining_hint: int = sqlmodel.Field(default=8)


class CardHint(CardPublic):
    pos: int
    number: str = sqlmodel.Field(max_length=1, min_length=1)


class Card(CardPublic, table=True):
    number: str = sqlmodel.Field(
        max_length=16,
        min_length=16,
        default_factory=random_number_generator,
    )
    created_at: datetime.datetime = sqlmodel.Field(
        default_factory=datetime.datetime.now
    )
