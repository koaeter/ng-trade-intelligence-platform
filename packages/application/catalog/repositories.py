from abc import ABC, abstractmethod

from packages.domain.catalog.models import Country, HSCode, Market, Product


class ProductRepository(ABC):
    @abstractmethod
    def get(self, product_id: str) -> Product | None:
        raise NotImplementedError


class HSCodeRepository(ABC):
    @abstractmethod
    def get(self, version_id: str, code: str) -> HSCode | None:
        raise NotImplementedError


class CountryRepository(ABC):
    @abstractmethod
    def get(self, code: str) -> Country | None:
        raise NotImplementedError


class MarketRepository(ABC):
    @abstractmethod
    def get(self, code: str) -> Market | None:
        raise NotImplementedError
