# Project, DD100N, Linnéa Sandblom, 2022-04-xx
# Makes and views packing lists.

from typing import List, Tuple, Dict


class PackList:
    def __init__(self, name: str, date: str, items: Dict[str, bool]):
        self.name = name
        self.date = date
        self.items = items

    def add_item(self, name, packed=False):
        self.items[name]=packed

    def remove_item(self, name):
        self.items.pop(name)

    def toggle_item_packed(self, name):
        self.items[name] = not self.items[name]

    def change_date(self, new_date):
         self.date = new_date

    def change_name(self, new_name):
        self.name = new_name
