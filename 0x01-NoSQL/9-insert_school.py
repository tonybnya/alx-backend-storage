#!/usr/bin/env python3
"""
Python function that inserts a new document in a collection based on kwargs

- Prototype: def insert_school(mongo_collection, **kwargs):
- mongo_collection will be the pymongo collection object
- Returns the new _id
"""

import pymongo


def insert_school(mongo_collection, **kwargs):
    """
    Function
    """
    if len(kwargs) == 0:
        return None

    return mongo_collection.insert(kwargs)
