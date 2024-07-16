#!/usr/bin/env python3
"""
Python function that inserts a new document in a collection based on `kwargs`:
    - Prototype: `def insert_school(mongo_collection, **kwargs):
    - `mongo_collection` will be the `pymongo` collection object
    - Return the new `_id`
"""


def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document in a collection based on **kwargs
    """
    document = mongo_collection.insert_one(kwargs)
    return document.inserted_id
