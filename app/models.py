from . import db
from datetime import datetime


class Country(db.Model):
    __tablename__ = "countries"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    cca = db.Column(db.String, nullable=False, unique=True)
    currency_code = db.Column(db.String, nullable=True)
    currency = db.Column(db.String, nullable=True)
    capital = db.Column(db.String, nullable=True)
    region = db.Column(db.String, nullable=False)
    subregion = db.Column(db.String, nullable=True)
    area = db.Column(db.Float, nullable=True)
    map_url = db.Column(db.String, nullable=True)
    population = db.Column(db.BigInteger, nullable=False)
    flag_url = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    neighbours = db.relationship(
        "CountryNeighbour", back_populates="country", cascade="all, delete-orphan"
    )


class CountryNeighbour(db.Model):
    __tablename__ = "country_neighbours"

    id = db.Column(db.Integer, primary_key=True)
    country_id = db.Column(db.Integer, db.ForeignKey("countries.id"), nullable=False)
    neighbour_country_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    country = db.relationship("Country", back_populates="neighbours")
