# Project, DD100N, Linnéa Sandblom, 2022-04-xx
# Makes and views packing lists.

from typing import List, Tuple, Dict


class PackList:
    def __init__(self, name: str, date: str, items: Dict[str, bool] = None):
        """
        constructor of PackList
        :param str name: name of packlist
        :param str date: date of travel
        :param Dict items: items top be packed
        """
        self.name = name
        self.date = date
        self.items = items if items else {}

    def add_item(self, name, packed=False):
        """
        add item to packlist
        :param str name: name of item to be added to packlist
        :param bool packed: true if item is packed when added, else false
        """
        self.items[name]=packed

    def remove_item(self, name):
        """
        remove item from packlist
        :param str name: name of item to be removed
        """
        self.items.pop(name)

    def toggle_item_packed(self, name):
        """
        toggle item "packed"/"not packed"
        :param str name: name of item to be to toggle "packed"/"not packed"
        """
        self.items[name] = not self.items[name]

    def change_date(self, new_date):
        """
        change date of travel for packlist
        :param str new_date: new date of travel
        """
        self.date = new_date

    def change_name(self, new_name):
        """
        change name of packlist
        :param str new_name: new name of packlist
        """
        self.name = new_name


def new_packlist():
    name = input("Name of packlist: ")
    date = input("Date: ")
    packlist = PackList(name, date)
    while True:
        item = input(f'To add an item to {name}, please enter item. Otherwise enter "Q".')
        if item == "Q":
            break
        else:
            packlist.add_item(item)
    print(f"{name} added to packlists.")
    return packlist

def show_lists(lists):
    """
    show all packlists for a specific date and foreward
    :param list lists: list of packlists
    """
    pass

def search_lists(lists):
    """
    search packlist
    :param list lists: list of packlists
    """
    pass

def read_file(filename="lists.txt"):
    """
    reads packlists from textfile
    :param str filename: name of textfile
    """
    pass

def quit_write_to_file(filename, lists):
    """
    writes packlists to text file and quits program
    :param str filename: name of textfile
    :param list lists: list of packlists
    """
    pass

def main():
    """
    main function of program
    """
    packlists: List = read_file()
    print(f"Welcome to Packlist program!")
    while True:
        choice = input(f"Please choose one of the following options: \n\n1. New packlist\n\n2. Show coming packlists\n3. Search packlist\n4. Quit}")
        if choice == "1":
            packlists.append(new_packlist())
        elif choice == "2":
            show_lists()
        elif choice == "3":
            search_lists()
        elif choice == "4":
            quit_write_to_file()
            break
        else:
            print("Unprocessable input. Choose an alternative 1-5.")