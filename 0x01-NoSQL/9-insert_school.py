#!/usr/bin/env python3
"""
Module 9-insert_school
"""


def insert_school(mongo_collection, **kwargs):
    """
    inserts a new document in a collection based on kwargs
    Returns the new _id
    """
    n_ew = mongo_collection.insert_one(kwargs)
    return n_ew.inserted_id
