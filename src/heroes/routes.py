from fastapi import APIRouter, HTTPException, status, Query
from sqlmodel import select
from src.database import SessionDep

from typing import Annotated
from src.heroes.models import Hero


heroes_router = APIRouter()


@heroes_router.get("/heroes")
async def read_heroes(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Hero]:
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes


@heroes_router.post("/", status_code=status.HTTP_201_CREATED)
async def hero_create(session: SessionDep, hero: Hero) -> Hero:
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero


@heroes_router.get("/{hero_id}")
async def hero_get(hero_id: int, session: SessionDep) -> Hero:
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found")
    return hero
