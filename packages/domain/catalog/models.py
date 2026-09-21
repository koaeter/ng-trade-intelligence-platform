from dataclasses import dataclass


@dataclass(frozen=True)
class Product:
    id: str
    name: str


@dataclass(frozen=True)
class HSCode:
    version_id: str
    code: str
    description: str


@dataclass(frozen=True)
class Country:
    code: str
    name: str


@dataclass(frozen=True)
class Market:
    code: str
    name: str
    country_code: str | None = None
