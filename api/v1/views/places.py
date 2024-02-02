#!/usr/bin/python3
"""Module with a flask script"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place


@app_views.route('/places/', methods=["GET"])
def places_get():
    """Get all place objects"""
    array = []

    all_obj = storage.all(Place)

    for obj in all_obj.values():
        dictionary = obj.to_dict()
        array.append(dictionary)

    return jsonify(array)


@app_views.route("/places/<obj_id>", methods=["GET"])
def place_get(obj_id):
    """Get a place object"""
    obj = storage.get(Place, obj_id)

    if obj is None:
        abort(404)

    return jsonify(obj.to_dict())


@app_views.route("/places/<obj_id>", methods=["DELETE"])
def place_delete(obj_id):
    """Delete a place object"""
    obj = storage.get(Place, obj_id)
    if obj is None:
        abort(404)

    storage.delete(obj)
    storage.save()

    return jsonify({}), 200


@app_views.route('/places/', methods=['POST'])
def place_create():
    """Create a new Place"""
    if not request.is_json:
        abort(400, "Not a JSON")

    data = request.get_json()

    if 'name' not in data:
        abort(400, "Missing name")

    new_obj = Place(**data)
    new_obj.save()

    return jsonify(new_obj.to_dict()), 201


@app_views.route('/places/<obj_id>', methods=['PUT'])
def place_update(obj_id):
    """Update a Place object"""
    obj = storage.get(Place, obj_id)
    if obj is None:
        abort(404)

    if not request.is_json:
        abort(400, "Not a JSON")

    data = request.get_json()

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(obj, key, value)

    obj.save()

    return jsonify(obj.to_dict()), 200
