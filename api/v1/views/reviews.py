#!/usr/bin/python3
"""Module with a flask script"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review


@app_views.route('/reviews/', methods=["GET"])
def reviews_get():
    """Get all review objects"""
    array = []

    all_obj = storage.all(Review)

    for obj in all_obj.values():
        dictionary = obj.to_dict()
        array.append(dictionary)

    return jsonify(array)


@app_views.route("/reviews/<obj_id>", methods=["GET"])
def review_get(obj_id):
    """Get a review object"""
    obj = storage.get(Review, obj_id)

    if obj is None:
        abort(404)

    return jsonify(obj.to_dict())


@app_views.route("/reviews/<obj_id>", methods=["DELETE"])
def review_delete(obj_id):
    """Delete a review object"""
    obj = storage.get(Review, obj_id)
    if obj is None:
        abort(404)

    storage.delete(obj)
    storage.save()

    return jsonify({}), 200


@app_views.route('/reviews/', methods=['POST'])
def review_create():
    """Create a new Review"""
    if not request.is_json:
        abort(400, "Not a JSON")

    data = request.get_json()

    if 'text' not in data:
        abort(400, "Missing text")

    new_obj = Review(**data)
    new_obj.save()

    return jsonify(new_obj.to_dict()), 201


@app_views.route('/reviews/<obj_id>', methods=['PUT'])
def review_update(obj_id):
    """Update a Review object"""
    obj = storage.get(Review, obj_id)
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
