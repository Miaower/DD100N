# Project, DD100N, Linnéa Sandblom, 2022-04-xx
# Makes and views packing lists.

from typing import List, Tuple, Dict


class PackList:
    def __init__(self, name: str, date: str, items: Dict[str, bool]):
        """
        constructor of PackList
        :param str name: name of packlist
        :param str date: date of travel
        :param Dict items: items top be packed
        """
        pass

    def add_item(self, name, packed=False):
        """
        add item to packlist
        :param str name: name of item to be added to packlist
        :param bool packed: true if item is packed when added, else false
        """
        pass

    def remove_item(self, name):
        """
        remove item from packlist
        :param str name: name of item to be removed
        """
        pass

    def toggle_item_packed(self, name):
        """
        toggle item "packed"/"not packed"
        :param str name: name of item to be to toggle "packed"/"not packed"
        """
        pass

    def change_date(self, new_date):
        """
        change date of travel for packlist
        :param str new_date: new date of travel
        """
        pass

    def change_name(self, new_name):
        """
        change name of packlist
        :param str new_name: new name of packlist
        """
        pass