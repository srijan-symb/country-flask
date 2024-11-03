from flask import Blueprint, jsonify, request
from app.models import Country, CountryNeighbour
from app import db

country_bp = Blueprint("country", __name__)


@country_bp.route("/country", methods=["GET"])
def get_countries():
    sort_by = request.args.get("sort_by", "a_to_z")
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))
    name = request.args.get("name", "")
    region = request.args.get("region", "")
    subregion = request.args.get("subregion", "")

    query = Country.query

    # Apply filters
    if name:
        query = query.filter(Country.name.ilike(f"%{name}%"))
    if region:
        query = query.filter(Country.region.ilike(f"%{region}%"))
    if subregion:
        query = query.filter(Country.subregion.ilike(f"%{subregion}%"))

    # Apply sorting
    sort_options = {
        "a_to_z": Country.name.asc(),
        "z_to_a": Country.name.desc(),
        "population_high_to_low": Country.population.desc(),
        "population_low_to_high": Country.population.asc(),
        "area_high_to_low": Country.area.desc(),
        "area_low_to_high": Country.area.asc(),
    }
    query = query.order_by(sort_options.get(sort_by, Country.name.asc()))

    # Pagination
    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    countries = pagination.items

    country_list = [
        {
            "id": country.id,
            "name": country.name,
            "cca3": country.cca,
            "currency_code": country.currency_code,
            "currency": country.currency,
            "capital": country.capital,
            "region": country.region,
            "subregion": country.subregion,
            "area": country.area,
            "map_url": country.map_url,
            "population": country.population,
            "flag_url": country.flag_url,
        }
        for country in countries
    ]

    response = {
        "list": country_list,
        "has_next": pagination.has_next,
        "has_prev": pagination.has_prev,
        "page": pagination.page,
        "pages": pagination.pages,
        "per_page": pagination.per_page,
        "total": pagination.total,
    }

    return jsonify({"message": "Country list", "data": response}), 200


@country_bp.route("/country/<int:country_id>", methods=["GET"])
def get_country_detail(country_id):
    country = Country.query.get(country_id)
    if country:
        country_detail = {
            "id": country.id,
            "name": country.name,
            "cca3": country.cca,
            "currency_code": country.currency_code,
            "currency": country.currency,
            "capital": country.capital,
            "region": country.region,
            "subregion": country.subregion,
            "area": country.area,
            "map_url": country.map_url,
            "population": country.population,
            "flag_url": country.flag_url,
        }
        return (
            jsonify({"message": "Country detail", "data": {"country": country_detail}}),
            200,
        )
    else:
        return jsonify({"message": "Country not found", "data": {}}), 404


@country_bp.route("/country/<int:country_id>/neighbour", methods=["GET"])
def get_country_neighbours(country_id):
    country = Country.query.get(country_id)
    if not country:
        return jsonify({"message": "Country not found", "data": {}}), 404

    neighbours = CountryNeighbour.query.filter_by(country_id=country_id).all()
    if not neighbours:
        return jsonify({"message": "Country neighbours", "data": {"list": []}}), 200

    neighbour_countries = []
    for neighbour in neighbours:
        neighbour_country = Country.query.get(neighbour.neighbour_country_id)
        if neighbour_country:
            neighbour_data = {
                "id": neighbour_country.id,
                "name": neighbour_country.name,
                "cca3": neighbour_country.cca,
                "currency_code": neighbour_country.currency_code,
                "currency": neighbour_country.currency,
                "capital": neighbour_country.capital,
                "region": neighbour_country.region,
                "subregion": neighbour_country.subregion,
                "area": neighbour_country.area,
                "map_url": neighbour_country.map_url,
                "population": neighbour_country.population,
                "flag_url": neighbour_country.flag_url,
            }
            neighbour_countries.append(neighbour_data)

    return (
        jsonify(
            {
                "message": "Country neighbours",
                "data": {"countries": neighbour_countries},
            }
        ),
        200,
    )
