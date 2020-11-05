from typing import Any
from pydantic import BaseModel
from pydantic.utils import GetterDict
import peewee

class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res

class forRegister(BaseModel):
    name: str
    email: str
    password: str

    class Config:
        orm_mode = True
        GetterDict = PeeweeGetterDict

class forLogin(BaseModel):
    email: str
    password: str
    token: str = None

    class Config:
        orm_mode = True
        GetterDict = PeeweeGetterDict

class forUpdateCredentials(BaseModel):
    name: str
    email: str
    password: str

    class Config:
        orm_mode = True
        GetterDict = PeeweeGetterDict

class forUpdatePassword(BaseModel):
    token: str
    password: str

    class Config:
        orm_mode = True
        GetterDict = PeeweeGetterDict

class forRegisterSecret(BaseModel):
    title: str
    description: str
    monetary_value: int
    place: str
    latitude: int
    longitude: int
    token: str = None

    class Config:
        orm_mode = True
        GetterDict = PeeweeGetterDict

class forDeleteSecret(BaseModel):
    token: str = None

    class Config:
        orm_mode = True
        GetterDict = PeeweeGetterDict







