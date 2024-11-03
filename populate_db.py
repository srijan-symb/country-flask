import requests
from app import create_app, db
from app.models import Country, CountryNeighbour

app = create_app()


def fetch_and_populate():
    response = requests.get("https://restcountries.com/v3.1/all")
    countries_data = response.json()

    with app.app_context():
        db.create_all()

        # Dictionary to store country codes and their IDs to handle neighbors
        country_dict = {}

        # First, populate the Country table
        for country in countries_data:
            cca3_code = country.get("cca3")

            # Check if the country already exists in the database
            existing_country = Country.query.filter_by(cca=cca3_code).first()
            if existing_country:
                print(f"Country with cca3 {cca3_code} already exists. Skipping.")
                country_dict[cca3_code] = existing_country.id
                continue

            # Create and add the new country if it doesn't already exist
            new_country = Country(
                name=country.get("name", {}).get("common"),
                cca=cca3_code,
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
            db.session.flush()  # Allows new_country.id to be available immediately
            country_dict[cca3_code] = new_country.id

        db.session.commit()

        # Next, populate the CountryNeighbour table
        for country in countries_data:
            country_id = country_dict.get(country.get("cca3"))
            if not country_id:
                continue

            borders = country.get("borders", [])
            for border_code in borders:
                neighbour_country_id = country_dict.get(border_code)
                if neighbour_country_id:
                    # Check if this neighbor relationship already exists
                    existing_neighbour = CountryNeighbour.query.filter_by(
                        country_id=country_id, neighbour_country_id=neighbour_country_id
                    ).first()
                    if existing_neighbour:
                        print(
                            f"Neighbor relationship already exists between country {country_id} and {neighbour_country_id}. Skipping."
                        )
                        continue

                    # Add new neighbor relationship
                    new_neighbour = CountryNeighbour(
                        country_id=country_id, neighbour_country_id=neighbour_country_id
                    )
                    db.session.add(new_neighbour)

        db.session.commit()


if __name__ == "__main__":
    fetch_and_populate()
