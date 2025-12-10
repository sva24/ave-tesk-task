from pydantic import BaseModel, Field
from pydantic_extra_types.phone_numbers import PhoneNumber
from pydantic_extra_types.phone_numbers import PhoneNumberValidator
from typing import Annotated, Union

RUNumberType = Annotated[
    Union[str, PhoneNumber],
    PhoneNumberValidator(supported_regions=["RU"], number_format="E164")
]


class ContactResponse(BaseModel):
    phone: str = Field(..., example="+78005553535", description="Нормализованный номер телефона")
    address: str = Field(..., min_length=10, example="Москва, ул. Ленина 1", description="Адрес контакта")


class ContactCreate(BaseModel):
    phone: RUNumberType = Field(..., example="+78005553535", description="Номер телефона")
    address: str = Field(..., min_length=10, example="Москва, ул. Ленина 1", description="Адрес контакта")


class ContactUpdate(BaseModel):
    address: str = Field(..., min_length=10, example="Москва, ул. Ленина, дом 20", description="Новый адрес контакта")
