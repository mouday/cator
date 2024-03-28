# -*- coding: utf-8 -*-
"""
@File    : collection.py
@Date    : 2024-03-28
"""


class Collection(object):
    def __init__(self, items: list):
        self.items = items or []

    def is_empty(self):
        return self.count() == 0

    def count(self):
        return len(self.items)

    def first(self, default=None):
        if self.is_empty():
            return default
        else:
            return self.items[0]
