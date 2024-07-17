#!/usr/bin/env python3
"""
Module contains Python Function that returns the list of school having
a specific topic:
    - Prototype: `def schools_by_topic(mongo_collection, topic):`
    - `mongo_collection` will be the `pymongo` collection object
    - `topic` (string) will be topic searched
"""


def schools_by_topic(mongo_collection, topic):
    """
    Gets the schools having a specific topic.
    """
    return list(mongo_collection.find({"topics": topic}))
