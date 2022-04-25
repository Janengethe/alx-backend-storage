#!/usr/bin/env python3
"""
Module 8-all
"""


def list_all(mongo_collection):
    """
    lists all documents in a collection
    Return an empty list if no document in the collection
    """
    if not mongo_collection:
        return []
    coll_ections = mongo_collection.find()
    return [docs for docs in coll_ections]
