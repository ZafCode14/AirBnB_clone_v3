#!/usr/bin/python3
"""Module with a flask script"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review 


@app_views.route('/places/<place_id>/reviews/', methods=["GET"])
def reviews_get(place_id):
    """Get all review objects"""
    array = []

    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    for review in place.reviews:
        array.append(review.to_dict())

    return jsonify(array)


@app_views.route('/reviews/<review_id>/', methods=["GET"])
def review_get(review_id):
    """Get review object"""
    review = storage.get(Review, review_id)

    if review is None:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>/', methods=["DELETE"])
def reviews_delete(review_id):
    """delete review object"""
    review = storage.get(Review, reivew_id)

    if review is None:
        abort(404)

    storage.delete(review)

    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def review_create(place_id):
    """Create a new Review"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if not request.is_json:
        abort(400, "Not a JSON")

    data = request.get_json()

    if 'user_id' not in data:
        abort(400, "Missing user_id")

    user_id = data['user_id']
    if storage.get(User, user_id) is None:
        abort(404)

    if 'text' not in data:
        abort(400, "Missing text")

    data['place_id'] = place_id
    new_review = Review(**data)
    new_review.save()

    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def review_update(review_id):
    """Update a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    if not request.is_json:
        abort(400, "Not a JSON")

    data = request.get_json()

    for key, value in data.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, key, value)

    review.save()

    return jsonify(review.to_dict()), 200
