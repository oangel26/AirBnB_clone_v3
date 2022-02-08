#!/usr/bin/python3
""" New view for the  link between Place objects and Amenity
objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models.place import Place
from models.city import City
from models.user import User
from models.review import Review
from models.amenity import Amenity
from models import storage
from os import getenv


storage_t = getenv("HBNB_TYPE_STORAGE")


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def get_all_amenities(place_id):
    """ Retrieves the list of all Amenity objects of a Place """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    all_amenities = storage.all(Amenity).values()
    amenity_list = []

    for amenity in all_amenities:
        if place_id == amenity.to_dict()['place_id']:
            if storage_t == "db":
                amenity_list.append(amenity.to_dict())
            else:
                amenity_list.append(amenity.amenity_ids)
    return jsonify(amenity_list)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(place_id, amenity_id):
    """ Deletes a Amenity object to a Place """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if amenity.to_dict()['place_id'] != place_id:
        abort(404)

    if storage_t == "db":
        storage.delete(amenity)
    else:
        amenity.amenity_ids = []
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def create_amenity_in_place(place_id):
    """ Link a Amenity object to a Place """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if amenity.to_dict()['place_id'] == place_id:
        return make_response(jsonify(amenity.to_dict()), 200)
    new_amenity = Amenity()
    if storage_t == "db":
        new_amenity.place_id = place_id
    else:
        new_amenity.amenity_ids = place_id
    storage.new(new_amenity)
    storage.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)
