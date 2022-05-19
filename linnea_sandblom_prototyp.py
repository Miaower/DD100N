# Project, DD100N, Linnéa Sandblom, 2022-05-09
# This is the version of the program WITH GUI.
# Makes, views and edits packing lists.
from tkinter import *
from tkinter import filedialog, messagebox, ttk
import ast
from typing import Dict, Union
import datetime


class App(Tk):
    def __init__(self):
        """
        Constructor of App class
        """
        super().__init__()
        self.title("Packlist program")
        self.packlists = []
        self.filename = ""
        self.packlists_filtered = self.packlists
        self.protocol("WM_DELETE_WINDOW", self.quit_save)

        self.lists = ListsView(self)
        self.itemlists = ItemListsView(self)

        self.quit_btn = Button(text="Save & Quit", command=lambda: self.quit_save()).grid(row=7, column=2)
        self.option_add('*tearOff', FALSE)
        menubar = Menu(self)
        self['menu'] = menubar
        menu_file = Menu(menubar)
        menubar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New file', command=self.new_file)
        menu_file.add_command(label='Open', command=self.open_file)

        if not self.filename:
            self.update_idletasks()
            while not self.filename:
                open_action = messagebox.askyesnocancel(title="No file loaded", message="You need to open or create a file to run the program. Open file?", detail="Click yes to open an existing file, no to create a new one, or cancel to exit the app")
                if open_action is None:
                    self.destroy()
                    break
                elif open_action:
                    self.open_file()
                else:
                    self.new_file()

        # If excess time:
        # TODO: Make lists removable?
        # TODO: Either dont reset filters on new list, or empty filter input box when lists are reset to all

        # TODO: Fix set packed when toggling first item multiple times with showing only unpacked (index problems)

    def new_file(self):
        """
        Create new file
        """
        self.filename = filedialog.asksaveasfilename()
        self.read_file(self.filename)

    def open_file(self):
        """
        Open existing file
        """
        self.filename = filedialog.askopenfilename()
        self.read_file(self.filename)
        self.lists.update_packlist_display(self.packlists)

    def read_file(self, file):
        """
        Reads packlists from textfile
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
                        messagebox.showinfo(message=f"Invalid list! Error in line {index + 1}")
        except FileNotFoundError:
            pass
        self.packlists = packlists

    def quit_save(self):
        """
        Write the list of packlists to file and quit program
        """
        try:
            with open(self.filename, "w", encoding="utf-8") as file:
                for packlist in self.packlists:
                    file.write(repr(packlist) + "\n")
        except FileNotFoundError:
            pass
        self.destroy()

    def search_lists(self, lists, search, show_after=False):
        """
        Search packlists
        :param list lists: list of packlists
        :param str search: input from user
        :param bool show_after: show lists with a later date if True, otherwise show only lists matching search
        """
        self.lists.edit_btn['state'] = DISABLED
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
                if (datetime.datetime.strptime(str(packlist.date), '%Y-%m-%d').date()) >= (datetime.datetime.strptime(str(search), '%Y-%m-%d').date()):
                    searchlist.append(packlist)
        else:
            for packlist in lists:
                if search.lower() in packlist.name.lower() or search.lower() in str(packlist.date):
                    searchlist.append(packlist)
        self.lists.update_packlist_display(searchlist)

    def sort_lists(self):
        """
        sort lists by date
        :param list lists: list of lists to be sorted
        :return: lists: sorted by date
        """
        for packlist in self.packlists:
            packlist.items = dict(sorted(packlist.items.items()))
        self.packlists = sorted(self.packlists, key=lambda packlist: str(packlist.date))


class ListsView:
    def __init__(self, root):
        """
        Constructor for ListsView class
        :param root: Tk root instance
        """
        self.root = root
        search_date_entry_var = StringVar(value="YYYY-MM-DD")
        search_datename_entry_var = StringVar(value="Enter name or date")
        self.packlists_listbox_var = StringVar()
        self.welcome_lbl = StringVar(value="Welcome to Packlist program!\n")

        Label(textvariable=self.welcome_lbl, width=40).grid(row=0, column=0, columnspan=3)
        Label(text="Search from date:", anchor=W, width=36).grid(row=1, column=0, columnspan=3)
        Entry(textvariable=search_date_entry_var, width=26).grid(row=2, column=0, columnspan=2)
        Button(text="Search", command=lambda: self.root.search_lists(self.root.packlists, search_date_entry_var.get(), show_after=True)).grid(row=2, column=2)
        Label(text="Search by name or date:", anchor=W, width=36).grid(row=3, column=0, columnspan=3)
        Entry(text=search_datename_entry_var, width=26).grid(row=4, column=0, columnspan=2)
        Button(text="Search", command=lambda: self.root.search_lists(self.root.packlists, search_datename_entry_var.get())).grid(row=4, column=2)
        Label(text="", width=40).grid(row=5, column=0, columnspan=3)

        self.packlist_listbox = Listbox(listvariable=self.packlists_listbox_var,  exportselection=0, width=48)
        self.packlist_listbox.bind("<<ListboxSelect>>", lambda e: self.listbox_selection())
        self.packlist_listbox.grid(row=6, column=0, columnspan=3)
        self.scrollbar = ttk.Scrollbar(root, orient=VERTICAL, command=self.packlist_listbox.yview)
        self.scrollbar.grid(column=3, row=6, sticky=(N,S))
        self.packlist_listbox.configure(yscrollcommand=self.scrollbar.set)
        Button(text="New list", command=lambda: self.edit_create(new=True)).grid(row=7, column=0)
        self.edit_btn = Button(text="Edit", command=lambda: self.edit_create(), state=DISABLED)
        self.edit_btn.grid(row=7, column=1)
        self.update_packlist_display(self.root.packlists_filtered)

    def listbox_selection(self):
        """
        Select list and update item display
        """
        self.edit_btn['state'] = ACTIVE
        index = self.packlist_listbox.curselection()[0]
        self.root.itemlists.update_itemlist_display(self.root.packlists_filtered[index])

    def edit_create(self, new=False):
        """
        Edit or create a list
        :param bool new: True if creating new list, otherwise False
        """
        if new:
            selected_list = None
        else:
            selected_list = self.root.packlists_filtered[self.packlist_listbox.curselection()[0]]
        InputBox(self.root, selected_list=selected_list)

    def update_packlist_display(self, packlists):
        """
        Update display that shows packlists
        :param packlists: list of lists
        :return: return if input is invalid or no lists found
        """
        self.packlist_listbox['state'] = NORMAL
        if not packlists:
            self.packlist_listbox['state'] = DISABLED
            self.packlists_listbox_var.set(["No lists found or invalid input!", "Dates must be on format YYYY-MM-DD"])
            return
        packlists_display = [f"{packlist.date} - {packlist.name}" for packlist in packlists]
        self.root.packlists_filtered = packlists
        self.packlists_listbox_var.set(packlists_display)

class ItemListsView:
    def __init__(self, root):
        """
        Constructor of ItemListsView
        :param root: Tk root instance
        """
        self.root = root
        self.selected_packlist = None
        self.packlists_items_box_var = StringVar()
        self.namedate_var = StringVar()
        self.show_only_unpacked = BooleanVar()

        self.name_date = Label(textvariable=self.namedate_var).grid(row=4, column=5, columnspan=3)
        self.toggle_btn = Checkbutton(text="Show only unpacked items", command=lambda: self.update_itemlist_display(self.selected_packlist), onvalue=True, offvalue=False, variable=self.show_only_unpacked).grid(row=5, column=5, columnspan=3)
        self.packlist_items_box = Listbox(listvariable=self.packlists_items_box_var, width=40)
        self.packlist_items_box.grid(row=6, column=5, columnspan=3)
        self.scrollbar = ttk.Scrollbar(root, orient=VERTICAL, command=self.packlist_items_box.yview)
        self.scrollbar.grid(column=8, row=6, sticky=(N,S))
        self.packlist_items_box.configure(yscrollcommand=self.scrollbar.set)
        self.add_item = Button(text="+", command=lambda: InputBox(self.root, selected_list=self.selected_packlist, new_item=True), state=DISABLED)
        self.add_item.grid(row=7, column=5)
        self.remove_item = Button(text="-", command=lambda: self.remove_item_func(), state=DISABLED)
        self.remove_item.grid(row=7, column=6)
        self.toggle_item = Button(text="Set packed", command=lambda: self.toggle_item_func(), state=DISABLED)
        self.toggle_item.grid(row=7, column=7)
        self.buttons = [self.add_item, self.remove_item, self.toggle_item]

    def update_itemlist_display(self, packlist=None):
        """
        Update display that shows items of a packlist
        :param packlist packlist: list from which to show items
        :return: return if no packlist input or not self.selected_packlist, return if packlist has no items
        """
        if not packlist:
            if self.selected_packlist:
                packlist = self.selected_packlist
            else:
                for button in self.buttons:
                    button['state'] = DISABLED
                return
        self.selected_packlist = packlist
        if not packlist.items:
            self.packlists_items_box_var.set(["No items found!"])
            self.packlist_items_box['state'] = DISABLED
            self.toggle_item['state'] = DISABLED
            self.remove_item['state'] = DISABLED
            self.add_item['state'] = ACTIVE
            return
        for button in self.buttons:
            button['state'] = ACTIVE
        self.packlist_items_box['state'] = NORMAL
        if self.show_only_unpacked.get():
            items_display = [f"{'    '}  {key}" for key, value in packlist.items.items() if not value]
        else:
            items_display = [f"{' X' if value else '    '}  {key}" for key, value in packlist.items.items()]
        self.packlists_items_box_var.set(items_display)
        namedate_display = (f"{packlist.name} - {packlist.date}")
        self.namedate_var.set(namedate_display)

    def remove_item_func(self):
        """
        Remove item from packlist
        """
        items = [item for item in self.selected_packlist.items.keys()]
        try:
            self.selected_packlist.items.pop(items[self.packlist_items_box.curselection()[0]])
            self.update_itemlist_display(self.selected_packlist)
        except IndexError:
            pass

    def toggle_item_func(self):
        """
        Toggle item packed/unpacked
        """
        items = [key for key, value in self.selected_packlist.items.items()]
        try:
            selected_item = items[self.packlist_items_box.curselection()[0]]
            self.selected_packlist.items[selected_item] = not self.selected_packlist.items[selected_item]
            self.update_itemlist_display(self.selected_packlist)
        except IndexError:
            pass


class InputBox:
    def __init__(self, root, selected_list=None, new_item=False):
        """
        Constructor of InputBox class
        :param root: Tk root instance
        :param packlist selected_list: packlist to be edited
        :param bool new_item: show window for adding item if True, otherwise show window for create/edit list
        """
        self.root = root
        self.selected_list = selected_list
        self.popup = Toplevel(root)
        self.new_item = new_item
        self.item_entry_var = StringVar()
        self.name_entry_var = StringVar()
        self.date_entry_var = StringVar()
        if selected_list:
            self.name_entry_var.set(selected_list.name)
            self.date_entry_var.set(selected_list.date)
        if self.new_item:
            Label(self.popup, text="New item:").grid()
            Entry(self.popup, textvariable=self.item_entry_var).grid()
        else:
            Label(self.popup, text="New name:").grid()
            Entry(self.popup, textvariable=self.name_entry_var).grid()
            Label(self.popup, text="New date:").grid()
            Entry(self.popup, textvariable=self.date_entry_var).grid()
        Button(self.popup, text="Done", command=self.save).grid()
        root_geom = self.root.geometry().split('+')
        self.popup.geometry(f"+{root_geom[1]}+{root_geom[2]}")
        self.popup.protocol("WM_DELETE_WINDOW", self.dismiss)
        self.popup.transient(root)
        self.popup.wait_visibility()
        self.popup.grab_set()
        self.popup.wait_window()

    def dismiss(self):
        """
        Allow clicking on windows other than InputBox popup window and close popup window
        """
        self.popup.grab_release()
        self.popup.destroy()

    def save(self):
        """
        Save new list, new item or save edits on list.
        """
        error = False
        if self.new_item:
            if entry := self.item_entry_var.get():
                self.selected_list.add_item(entry)
            else:
                messagebox.showwarning(title="Empty item!", message="Please input item to add")
                error = True
        else:
            new_name = self.name_entry_var.get()
            if not new_name:
                messagebox.showerror(title="Invalid name", message="Please provide a valid, non-null name")
                error = True
            try:
                new_date = datetime.datetime.strptime(self.date_entry_var.get(), '%Y-%m-%d').date()
            except ValueError:
                messagebox.showerror(title="Invalid date", message="Please provide a valid date",
                                     detail="Format: YYYY-MM-DD")
                error = True
            if not error:
                if not self.selected_list:
                    self.root.packlists.append(PackList(self.name_entry_var.get(), new_date))
                else:
                    self.selected_list.name = self.name_entry_var.get()
                    self.selected_list.change_date(new_date)
        if not error:
            self.root.sort_lists()
            self.root.lists.update_packlist_display(self.root.packlists)
            self.root.itemlists.update_itemlist_display()
            self.dismiss()


class PackList:
    """
    Main PackList class.
    The data structure of each list in a PackList object consists of a str name, a datetime.date date and a dict of items.
    Each item is a dict entry that consists of a str name of the item and a bool that states if the item is packed or not.
    """
    def __init__(self, name: str, date: Union[datetime.date, str], items: Dict[str, bool] = None):
        """
        constructor of PackList
        :param str name: name of packlist
        :param str date: date of travel
        :param Dict items: items top be packed
        """
        self.name = name[0].upper() + name[1:]
        if isinstance(date, str):
            self.date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        else:
            self.date = date
        self.items = items if items else {}

    def remove_item(self, name):
        """
        remove item from packlist
        :param str name: name of item to be removed
        """
        self.items.pop(name)

    def change_date(self, new_date):
        """
        change date of travel for PackList
        :param str new_date: new date of travel
        """
        self.date = new_date

    def __repr__(self):
        """
        create string from PackList object
        :return: string of PackList object
        """
        return str((self.name, self.date.year, self.date.month, self.date.day, self.items))

    def add_item(self, name, packed=False):
        """
        add item to PackList
        :param str name: name of item to be added to PackList
        :param bool packed: true if item is packed when added, else false
        """
        name = name[0].upper() + name[1:]
        self.items[name] = packed
        self.items = dict(sorted(self.items.items()))


def main():
    """
    main function of program
    """
    program = App()
    program.mainloop()

main()