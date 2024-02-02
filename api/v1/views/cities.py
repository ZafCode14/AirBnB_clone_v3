#!/usr/bin/python3
"""Module with a flask script"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities/', methods=["GET"])
def cities_get(state_id):
    """Get all city objects"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    list_of_cities = [city.to_dict() for city in state.cities]
    return jsonify(list_of_cities)


@app_views.route("/cities/<city_id>", methods=["GET"])
def city_get(city_id):
    """Get a city object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"])
def city_delete(city_id):
    """Delete a city object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    storage.delete(city)
    storage.save()

    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def city_create(state_id):
    """Create a new City"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    if not request.is_json:
        abort(400, "Not a JSON")

    data = request.get_json()

    if 'name' not in data:
        abort(400, "Missing name")

    data['state_id'] = state_id
    new_city = City(**data)
    new_city.save()

    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def city_update(city_id):
    """Update a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if not request.is_json:
        abort(400, "Not a JSON")

    data = request.get_json()

    for key, value in data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)

    city.save()

    return jsonify(city.to_dict()), 200
