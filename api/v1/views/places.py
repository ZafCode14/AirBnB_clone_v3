#!/usr/bin/python3
"""Module with a flask script"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.amenity import Amenity
from models.state import State


@app_views.route('/cities/<city_id>/places', methods=["GET"])
def places_get(city_id):
    """Get all place objects of a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route("/places/<place_id>", methods=["GET"])
def place_get(place_id):
    """Get a place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"])
def place_delete(place_id):
    """Delete a place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def place_create(city_id):
    """Create a new Place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if not request.is_json:
        abort(400, "Not a JSON")

    data = request.get_json()

    if 'user_id' not in data:
        abort(400, "Missing user_id")

    if 'name' not in data:
        abort(400, "Missing name")

    user_id = data['user_id']
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    data['city_id'] = city_id
    new_place = Place(**data)
    new_place.save()

    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def place_update(place_id):
    """Update a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if not request.is_json:
        abort(400, "Not a JSON")

    data = request.get_json()

    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)

    place.save()

    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'])
def places_search():
    """Searches for places based on JSON request"""
    try:
        data = request.get_json()
    except Exception as e:
        abort(400, "Not a JSON")

    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities = data.get('amenities', [])

    places = []

    if not states and not cities and not amenities:
        places = storage.all(Place).values()
    else:
        for state_id in states:
            state = storage.get(State, state_id)
            if state:
                for city in state.cities:
                    if city not in places:
                        places.extend(city.places)

        for city_id in cities:
            city = storage.get(City, city_id)
            if city:
                places.extend(city.places)

        if amenities:
            amenities_objs = [storage.get(Amenity, amenity_id) for amenity_id in amenities]
            places = [place for place in places if all(amenity in place.amenities for amenity in amenities_objs)]

    return jsonify([place.to_dict() for place in places])

