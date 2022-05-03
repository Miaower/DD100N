# Project, DD100N, Linnéa Sandblom, 2022-05-xx
# Makes, views and edits packing lists.
from tkinter import *
import ast
from tkinter import messagebox
from typing import List, Tuple, Dict
import datetime

SAVE_FILE = "lists.txt"

class App(Tk):

    def __init__(self):
        super().__init__()
        self.title("Packlist program")
        self.packlists: List = read_file(SAVE_FILE)
        self.packlists_filtered = self.packlists
        self.protocol("WM_DELETE_WINDOW", self.quit_save)

        # TODO: filtrera vid start, efter ny lista och datumbyte
        # TODO: filtrera items på lämpliga ställen, t.ex. add och skapande av ny lista

        self.lists = ListsView(self)
        self.itemlists = ItemListsView(self)

        self.quit_btn = Button(text="Quit", command=lambda: self.quit_save())
        self.quit_btn.grid(row=7, column=2)

        # TODO: new list, change name and change date
        # TODO: choosable lists + show name, date and items
        # TODO: add, remove and toggle
        # TODO: show unpacked
        # TODO: change global variable stuff(?)
        # TODO: remove stuff that isn't used
        # TODO: comment everything
        # TODO: recheck requirements and test the shit out of the program
        # TODO: recheck requirements and test the shit out of the other non-gui program


    def quit_save(self):
        quit_write_to_file(self.packlists, file=SAVE_FILE)
        self.destroy()

    def search_lists(self, lists, search, show_after=False):
        """
        search packlist
        :param list lists: list of packlists
        """
        #self.packlists_filtered = self.packlists
        searchlist = []
        if show_after:
            if not search:
                search = datetime.date(1, 1, 1)
            else:
                try:
                    searchdate = datetime.datetime.strptime(search, '%Y-%m-%d')
                    search = searchdate.date()
                except ValueError:
                    self.lists.update_packlist_display([])
                    return
            for packlist in lists:
                if packlist.date >= search:
                    searchlist.append(packlist)
        else:
            for packlist in lists:
                if search.lower() in packlist.name.lower() or search.lower() in str(packlist.date):
                    searchlist.append(packlist)
        self.lists.update_packlist_display(searchlist)


class ListsView:

    def __init__(self, root):
        self.root = root
        search_date_entry_var = StringVar(value="YYYY-MM-DD")
        search_datename_entry_var = StringVar(value="YYYY-MM-DD or list name")
        self.packlists_listbox_var = StringVar()
        self.update_packlist_display(self.root.packlists_filtered)

        # TODO: Current index matches packlists_filtered. Use that!!

        self.welcome_label = Label(text="Welcome to Packlist program!\n", width=40).grid(row=0, column=0, columnspan=3)
        self.search_date_label = Label(text="Search from date:", anchor=W, width=36).grid(row=1, column=0, columnspan=3)
        self.search_date_entry = Entry(textvariable=search_date_entry_var, width=25).grid(row=2, column=0, columnspan=2)
        self.go_search_date = Button(text="Search", command=lambda: self.root.search_lists(self.root.packlists, search_date_entry_var.get(), show_after=True)).grid(row=2, column=2)
        self.search_datename_label = Label(text="Search by name or date:", anchor=W, width=36).grid(row=3, column=0, columnspan=3)
        self.search_datename_entry = Entry(text=search_datename_entry_var, width=25).grid(row=4, column=0, columnspan=2)
        self.go_search_datename = Button(text="Search", command=lambda: self.root.search_lists(self.root.packlists, search_datename_entry_var.get())).grid(row=4, column=2)
        self.space = Label(text="", width=40).grid(row=5, column=0, columnspan=3)

        self.packlist_listbox = Listbox(listvariable=self.packlists_listbox_var, width=40).grid(row=6, column=0, columnspan=3)
        self.new_list_btn = Button(text="New list", command=lambda: self.edit_create()).grid(row=7, column=0)
        self.edit_btn = Button(text="Edit", command=lambda: self.edit_create()).grid(row=7, column=1)

    def edit_create(self):
        InputBox(self.root)

    def update_packlist_display(self, packlists):
        if not packlists:
            self.packlists_listbox_var.set(["No lists found or invalid input!"])
            return
        packlists_display = [f"{packlist.name} - {packlist.date}" for packlist in packlists]
        self.root.packlists_filtered = packlists
        self.packlists_listbox_var.set(packlists_display)

class ItemListsView:

    def __init__(self, root):
        self.name_date = Label(text="Textvariable w name&date goes here").grid(row=4, column=3, columnspan=3)
        self.toggle_btn = Checkbutton(text="Show only unpacked items", command=lambda: self.dostuff()).grid(row=5, column=3, columnspan=3)
        self.packlist_items_box = Listbox(width=40).grid(row=6, column=3, columnspan=3)
        self.add_item = Button(text="+", command=lambda: self.dostuff()).grid(row=7, column=3)
        self.remove_item = Button(text="-", command=lambda: self.dostuff()).grid(row=7, column=4)
        self.toggle_item = Button(text="Set packed", command=lambda: self.dostuff()).grid(row=7, column=5)


class InputBox:
    def __init__(self, root, selected_list=None):
        self.root = root
        self.selected_list = selected_list

        self.popup = Toplevel(root)
        Label(self.popup, text="New name:").grid()
        Entry(self.popup).grid()  # something to interact with
        Label(self.popup, text="New date:").grid()
        Entry(self.popup).grid()

        Button(self.popup, text="Done", command=self.save).grid()
        self.popup.protocol("WM_DELETE_WINDOW", self.dismiss)  # intercept close button
        self.popup.transient(root)  # dialog window is related to main
        self.popup.wait_visibility()  # can't grab until window appears, so we wait
        self.popup.grab_set()  # ensure all input goes to our window
        self.popup.wait_window()  # block until window is destroyed

    def dismiss(self):
        self.popup.grab_release()
        self.popup.destroy()

    def save(self):  # TODO: Gör olika stuffs här, för att lägga till ny och editera befintlig
        if self.selected_list:
            print(self.root.packlists) # TODO: För edit
        else:
            print(self.root.packlists)  # TODO: För new
        # TODO: sort packlists


class PackList:
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

def sort_lists(lists):
    """
    sort lists by date
    :param list lists: list of lists to be sorted
    :return: lists: sorted by date
    """
    for packlist in lists:
        packlist.items = dict(sorted(packlist.items.items()))
    return sorted(lists, key=lambda packlist: packlist.date)

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
                    messagebox.showinfo(message=f"Invalid list! Error in line {index+1}")
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


def main():
    """
    main function of program
    """
    program = App()
    program.mainloop()

main()