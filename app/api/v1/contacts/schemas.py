from typing import Annotated, Union

from pydantic import BaseModel, Field
from pydantic_extra_types.phone_numbers import (PhoneNumber,
                                                PhoneNumberValidator)

RUNumberType = Annotated[
    Union[str, PhoneNumber],
    PhoneNumberValidator(supported_regions=["RU"], number_format="E164"),
]


class ContactResponse(BaseModel):
    phone: str = Field(
        ..., description="Номер телефона", json_schema_extra={"example": "+78005553535"}
    )
    address: str = Field(
        ...,
        min_length=10,
        description="Адрес контакта",
        json_schema_extra={"example": "Москва, ул. Ленина 1"},
    )


class ContactCreate(BaseModel):
    phone: RUNumberType = Field(
        ..., description="Номер телефона", json_schema_extra={"example": "+78005553535"}
    )
    address: str = Field(
        ...,
        min_length=10,
        description="Адрес контакта",
        json_schema_extra={"example": "Москва, ул. Ленина 1"},
    )


class ContactUpdate(BaseModel):
    address: str = Field(
        ...,
        min_length=10,
        description="Новый адрес контакта",
        json_schema_extra={"example": "Москва, ул. Ленина, дом 20"},
    )
