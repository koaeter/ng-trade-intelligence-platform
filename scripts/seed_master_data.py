"""Seed deterministic development master data."""
from infrastructure.database.models import CountryModel, HSCodeModel, HSVersionModel, MarketModel, ProductModel
from infrastructure.database.session import SessionLocal

def seed() -> None:
    with SessionLocal() as session:
        for code, name in [("NG","Nigeria"),("DE","Germany"),("GH","Ghana"),("IN","India")]:
            if session.get(CountryModel, code) is None:
                session.add(CountryModel(code=code, name=name))
        for code, name, country in [("NG","Nigeria","NG"),("DE","Germany","DE"),("GH","Ghana","GH"),("IN","India","IN")]:
            if session.get(MarketModel, code) is None:
                session.add(MarketModel(code=code, name=name, country_code=country))
        if session.get(ProductModel, "cocoa") is None:
            session.add(ProductModel(id="cocoa", name="Cocoa"))
        if session.get(HSVersionModel, "HS2022") is None:
            session.add(HSVersionModel(id="HS2022", name="Harmonized System 2022"))
        if session.get(HSCodeModel, ("HS2022","1801")) is None:
            session.add(HSCodeModel(version_id="HS2022", code="1801", description="Cocoa beans, whole or broken, raw or roasted"))
        session.commit()

if __name__ == "__main__":
    seed()
