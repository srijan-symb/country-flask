import requests
from app import create_app, db
from app.models import Country, CountryNeighbour

app = create_app()


def fetch_and_populate():
    response = requests.get("https://restcountries.com/v3.1/all")
    countries_data = response.json()

    with app.app_context():
        db.create_all()

        for country in countries_data:
            new_country = Country(
                name=country.get("name", {}).get("common"),
                cca=country.get("cca3"),
                currency_code=(
                    list(country.get("currencies", {}).keys())[0]
                    if country.get("currencies")
                    else None
                ),
                currency=(
                    list(country.get("currencies", {}).values())[0].get("name")
                    if country.get("currencies")
                    else None
                ),
                capital=country.get("capital", [None])[0],
                region=country.get("region"),
                subregion=country.get("subregion"),
                area=country.get("area"),
                map_url=country.get("maps", {}).get("googleMaps"),
                population=country.get("population"),
                flag_url=country.get("flags", {}).get("png"),
            )
            db.session.add(new_country)
        db.session.commit()


if __name__ == "__main__":
    fetch_and_populate()
