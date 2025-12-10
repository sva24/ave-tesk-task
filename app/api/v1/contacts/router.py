from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, HTTPException, status

from app.api.v1.contacts.schemas import (ContactCreate, ContactResponse,
                                         ContactUpdate, RUNumberType)
from app.repositories.contact_repository import ContactRepository

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ContactResponse)
@inject
async def create_contact(
    payload: ContactCreate,
    repo: FromDishka[ContactRepository],
):
    phone_normalized = str(payload.phone)
    existing = await repo.get(phone_normalized)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Контакт уже существует"
        )

    await repo.create(phone_normalized, payload.address)
    return {"phone": phone_normalized, "address": payload.address}


@router.get("/{phone}", status_code=status.HTTP_200_OK, response_model=ContactResponse)
@inject
async def get_contact(
    phone: RUNumberType,
    repo: FromDishka[ContactRepository],
):
    address = await repo.get(phone)

    if not address:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Контакт не найден")

    return {"phone": phone, "address": address}


@router.put("/{phone}", status_code=status.HTTP_200_OK, response_model=ContactResponse)
@inject
async def update_contact(
    payload: ContactUpdate,
    phone: RUNumberType,
    repo: FromDishka[ContactRepository],
):
    existing = await repo.get(phone)
    if not existing:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Контакт не найден")
    await repo.update(phone, payload.address)
    return {"phone": phone, "address": payload.address}


@router.delete("/{phone}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_contact(
    phone: RUNumberType,
    repo: FromDishka[ContactRepository],
):
    existing = await repo.get(phone)
    if not existing:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Контакт не найден")

    await repo.delete(phone)
    return
