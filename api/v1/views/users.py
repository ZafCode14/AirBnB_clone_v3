#!/usr/bin/python3
"""Module with a flask script"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users/', methods=["GET"])
def users_get():
    """Get all user objects"""
    array = []

    all_obj = storage.all(User)

    for obj in all_obj.values():
        dictionary = obj.to_dict()
        array.append(dictionary)

    return jsonify(array)


@app_views.route("/users/<obj_id>", methods=["GET"])
def user_get(obj_id):
    """Get a user object"""
    obj = storage.get(User, obj_id)

    if obj is None:
        abort(404)

    return jsonify(obj.to_dict())


@app_views.route("/users/<obj_id>", methods=["DELETE"])
def user_delete(obj_id):
    """Delete a user object"""
    obj = storage.get(User, obj_id)
    if obj is None:
        abort(404)

    storage.delete(obj)
    storage.save()

    return jsonify({}), 200


@app_views.route('/users/', methods=['POST'])
def user_create():
    """Create a new User"""
    if not request.is_json:
        abort(400, "Not a JSON")

    data = request.get_json()

    if 'name' not in data:
        abort(400, "Missing name")

    new_obj = User(**data)
    new_obj.save()

    return jsonify(new_obj.to_dict()), 201


@app_views.route('/users/<obj_id>', methods=['PUT'])
def user_update(obj_id):
    """Update a User object"""
    obj = storage.get(User, obj_id)
    if obj is None:
        abort(404)

    if not request.is_json:
        abort(400, "Not a JSON")

    data = request.get_json()

    for key, value in data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(obj, key, value)

    obj.save()

    return jsonify(obj.to_dict()), 200
