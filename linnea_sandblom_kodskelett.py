# Project, DD100N, Linnéa Sandblom, 2022-04-24
# Makes, views and edits packing lists.

from typing import List, Tuple, Dict
import datetime


class PackList:
    def __init__(self, name: str, date: datetime.date, items: Dict[str, bool] = None):
        """
        constructor of PackList
        :param str name: name of packlist
        :param str date: date of travel
        :param Dict items: items top be packed
        """

    def add_item(self, name, packed=False):
        """
        add item to PackList
        :param str name: name of item to be added to PackList
        :param bool packed: true if item is packed when added, else false
        """

    def remove_item(self, name):
        """
        remove item from packlist
        :param str name: name of item to be removed
        """

    def toggle_item_packed(self, name):
        """
        toggle item "packed"/"not packed"
        :param str name: name of item to be to toggle "packed"/"not packed"
        """

    def change_date(self, new_date):
        """
        change date of travel for PackList
        :param str new_date: new date of travel
        """

    def change_name(self, new_name):
        """
        change name of PackList
        :param str new_name: new name of PackList
        """

    def __repr__(self):
        """
        create string from PackList object
        :return: string of PackList object
        """

    def print_list(self):
        """
        print list date, name and items
        """

    def print_list_items(self, only_unpacked=False):
        """
        print list items, enumerated
        :param only_unpacked: if only unpacked items True, otherwise false
        """


def new_packlist():
    """
    create new packlist
    :return: packlist created
    """


def show_lists(lists):
    """
    show all packlists for a specific date and foreward
    :param list lists: list of packlists
    """


def search_lists(lists):
    """
    search packlist
    :param list lists: list of packlists
    """


def list_menu(chosen_list):
    """
    menu for options on chosen_list
    :param chosen_list: list to be handled in function
    """


def read_file(file):
    """
    reads packlists from textfile
    :param str file: name of textfile
    :return list packlists made from textfile data
    """


def quit_write_to_file(lists, file):
    """
    writes packlists to text file and quits program
    :param str file: name of textfile
    :param list lists: list of packlists
    """


def ask_for_date():
    """
    take date input from user as a datetime.date object
    :return: date as datetime.date object if there is a date input, otherwise None
    """


def ask_for_int(message):
     """
    check that input is int
     :param str message: message for input
     :return: value: int value input
     """


def sort_lists(lists):
    """
    sort lists by date
    :param list lists: list of lists to be sorted
    :return: lists: sorted by date
    """


def main():
    """
    main function of program
    Program reads data from file and loops main menu. The data is saved into a list "packlists"
    The user chooses to create a new packlist, show packlists, search and edit packlists or quit.
    For "Search and edit packlist", a  packlist is chosen and a function loops a menu with the following optios:
    "Change name", "Change travel date", "Add item", "Remove item", "Toggle packed/unpacked item", "Show unpacked items" and "Back to main menu".
    The main loop continues until user selects "Quit" where the list "packlists" is saved back into the file that was read in the start of the program.
    """



if __name__ == "__main__":
    main()