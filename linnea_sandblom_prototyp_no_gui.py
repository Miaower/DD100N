# Project, DD100N, Linnéa Sandblom, 2022-05-09
# This is the version of the program WITHOUT GUI.
# Makes, views and edits packing lists.
import ast
from typing import List, Dict
import datetime

SAVE_FILE = "lists.txt"

class PackList:
    """
    Class that constructs object containing packlists.
    The data structure of each list in a PackList object consists of a str name, a datetime.date date and a dict of items.
    Each item is a dict entry that consists of a str name of the item and a bool that states if the item is packed or not.
    """
    def __init__(self, name: str, date: datetime.date, items: Dict[str, bool] = None):
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
        add item to PackList
        :param str name: name of item to be added to PackList
        :param bool packed: true if item is packed when added, else false
        """
        while not name:
            name = input("Input name of item:  ")
        name = name[0].upper() + name[1:]
        self.items[name] = packed
        self.items = dict(sorted(self.items.items()))

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
        change date of travel for PackList
        :param str new_date: new date of travel
        """
        self.date = new_date

    def change_name(self, new_name):
        """
        change name of PackList
        :param str new_name: new name of PackList
        """
        self.name = new_name

    def __repr__(self):
        """
        create string from PackList object
        :return: string of PackList object
        """
        return str((self.name, self.date.year, self.date.month, self.date.day, self.items))

    def print_list(self):
        """
        print list date, name and items
        """
        print(f"{self.date} - {self.name}")
        self.print_list_items()

    def print_list_items(self, only_unpacked=False):
        """
        print list items, enumerated
        :param only_unpacked: if only unpacked items True, otherwise false
        """
        for index, (item, packed) in enumerate(self.items.items()):
            if packed and not only_unpacked:
                print(f"{index}: X {item}")
            else:
                print(f"{index}:   {item}")


def new_packlist():
    """
    create new packlist
    :return: packlist created
    """
    name = ""
    while not name:
        name = input("Name of packlist: ")
    name = name[0].upper() + name[1:]
    print("Enter date of travel: ")
    date = None
    while not date:
        date = ask_for_date()
    packlist = PackList(name, date)
    while True:
        item = input(f'To add an item to {name}, please enter item. Otherwise enter "Q": ')
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
    print("Enter a date from when to show packlists: ")
    date = ask_for_date()
    if date is None:
        date = datetime.date(1, 1, 1)
    for packlist in lists:
        if packlist.date >= date:
            packlist.print_list()

def search_lists(lists):
    """
    search packlist
    :param list lists: list of packlists
    """
    searchlist = []
    while True:
        search = input("Search for packlist by name or date (YYYY-MM-DD): ")
        for packlist in lists:
            if search.lower() in packlist.name.lower() or search.lower() in str(packlist.date):
                searchlist.append(packlist)
        if not searchlist:
            print("No lists found.")
        elif len(searchlist) == 1:
            list_menu(searchlist[0])
            break
        else:
            print("Multiple lists found.")
            for index, packlist in enumerate(searchlist):
                print(f"{index}: {packlist.name} - {packlist.date}")
            while True:
                list_number = input("Choose a list by entering it's number: ")
                try:
                    list_number = int(list_number)
                    chosen_list = searchlist[list_number]
                except (ValueError, IndexError):
                    print(f"No such list number. Enter a number between 0 and {len(searchlist)-1}.")
                else:
                    list_menu(chosen_list)
                    break
                print("")
            break


def list_menu(chosen_list):
    """
    menu for options on chosen_list
    :param chosen_list: list to be handled in function
    """
    chosen_list.print_list()
    while True:
        choice = input(f"\nPlease choose one of the following options for {chosen_list.name}: \n\n"
                       f"1. Change name\n2. Change travel date\n3. Add item\n4. Remove item\n5. Toggle packed/unpacked item\n6. Show unpacked items\n7. Back to main menu\n")
        if choice == "1":
            new_name = input(f"Enter a new name for {chosen_list.name}: ")
            chosen_list.change_name(new_name)
        elif choice == "2":
            print(f"Enter a new travel date for {chosen_list.name}, {chosen_list.date}: ")
            chosen_list.change_date(ask_for_date())
        elif choice == "3":
            new_item = input(f"Add new item to list {chosen_list.name}: ")
            chosen_list.add_item(new_item)
        elif choice in ["4", "5"]:
            chosen_list.print_list_items()
            list_item = ask_for_int(f"Enter list item to change: ")
            chosen_item = list(chosen_list.items)[list_item]
            if choice == "4":
                chosen_list.remove_item(chosen_item)
                print(f"{chosen_item} removed.")
            if choice == "5":
                chosen_list.toggle_item_packed(chosen_item)
                print(f"{chosen_item} packed.") if chosen_list.items[chosen_item] else print(f"{chosen_item} unpacked.")
        elif choice == "6":
            chosen_list.print_list_items(only_unpacked=True)
        elif choice == "7":
            break
        else:
            print("Unprocessable input. Choose an alternative 1-6.")


def read_file(file=SAVE_FILE):
    """
    reads packlists from textfile
    :param str file: name of textfile
    :return list packlists made from textfile data
    """
    packlists = []
    try:
        with open(file, "r+", encoding="utf-8") as file:
            for index, line in enumerate(file):
                try:
                    evaluated_line = ast.literal_eval(line.strip())
                    name, year, month, day, lists = evaluated_line
                    packlists.append(PackList(name, datetime.date(year, month, day), lists))
                except (SyntaxError, ValueError):
                    print(f"Invalid list! Error in line {index+1}\n")
    except FileNotFoundError:
        print(f"File not found. New file {file} will be created for your lists")
    return packlists


def quit_write_to_file(lists, file=SAVE_FILE):
    """
    writes packlists to text file and quits program
    :param str file: name of textfile
    :param list lists: list of packlists
    """
    with open(file, "w", encoding="utf-8") as file:
        for packlist in lists:
            file.write(repr(packlist) + "\n")
    print("Saved, welcome back!")


def ask_for_date():
    """
    take date input from user as a datetime.date object
    :return: date as datetime.date object if there is a date input, otherwise None
    """
    while True:
        try:
            year_str = input("Enter year (1-9999): ")
            if year_str.strip():
                year = int(year_str)
            else:
                return None
            month = int(input("Enter month (1-12): "))
            day = int(input("Enter day (1-31): "))
            date = datetime.date(year, month, day)
            return date
        except ValueError:
            print("Non-valid date, try again!")


def ask_for_int(message):
    """
    check that input is int
    :param str message: message for input
    :return: value: int value input
    """
    while True:
        try:
            value = int(input(message))
        except ValueError:
            continue
        else:
            return value


def sort_lists(lists):
    """
    sort lists by date
    :param list lists: list of lists to be sorted
    :return: lists: sorted by date
    """
    for packlist in lists:
        packlist.items = dict(sorted(packlist.items.items()))
    return sorted(lists, key=lambda packlist: packlist.date)


def main():
    """
    main function of program
    """
    in_file = input("Enter file name. Empty for default: ")
    packlists: List = read_file(in_file) if in_file else read_file()
    print(f"Welcome to Packlist program!")
    while True:
        packlists = sort_lists(packlists)
        choice = input("\nPlease choose one of the following options: \n\n1. New packlist\n2. Show coming packlists\n3. Search and edit packlist\n4. Quit\n")
        if choice == "1":
            packlists.append(new_packlist())
            packlists = sort_lists(packlists)
        elif choice == "2":
            show_lists(packlists)
        elif choice == "3":
            search_lists(packlists)
        elif choice == "4":
            quit_write_to_file(packlists, in_file) if in_file else quit_write_to_file(packlists)
            break
        else:
            print("Unprocessable input. Choose an alternative 1-4.")


if __name__ == "__main__":
    main()