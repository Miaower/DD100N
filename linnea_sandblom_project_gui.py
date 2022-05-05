# Project, DD100N, Linnéa Sandblom, 2022-05-xx
# Makes, views and edits packing lists.
from tkinter import *
from tkinter import filedialog, messagebox
import ast
from typing import List, Tuple, Dict
import datetime


class App(Tk):

    def __init__(self):
        super().__init__()
        self.title("Packlist program")
        self.packlists = []
        self.filename = ""
        self.packlists_filtered = self.packlists
        self.protocol("WM_DELETE_WINDOW", self.quit_save)

        self.lists = ListsView(self)
        self.itemlists = ItemListsView(self)

        self.quit_btn = Button(text="Quit", command=lambda: self.quit_save()).grid(row=7, column=2)
        self.option_add('*tearOff', FALSE)
        menubar = Menu(self)
        self['menu'] = menubar
        menu_file = Menu(menubar)
        menubar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New file', command=self.new_file)
        menu_file.add_command(label='Open', command=self.open_file)

        # TODO: Fix exit when no listfile opened yet
        # TODO: removeable lists?
        # TODO: remove stuff that isn't used
        # TODO: comment everything
        # TODO: recheck requirements and test the shit out of the program (remove lists??)
        # TODO: recheck requirements and test the shit out of the other non-gui program
        # TODO: Ev visa datum först
        # TODO: Är filtered_lists filtrerad vid lämpliga ställen, t.ex. add och skapande av ny lista?

    def new_file(self):
        self.filename = filedialog.asksaveasfilename()
        self.read_file(self.filename)

    def open_file(self):
        self.filename = filedialog.askopenfilename()
        self.read_file(self.filename)
        self.lists.update_packlist_display(self.packlists)

    def read_file(self, file):
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
                        messagebox.showinfo(message=f"Invalid list! Error in line {index + 1}")
        except FileNotFoundError:
            pass
        self.packlists = packlists

    def quit_save(self):
        quit_write_to_file(self.packlists, file=self.filename)
        self.destroy()

    def search_lists(self, lists, search, show_after=False):
        """
        search packlist
        :param list lists: list of packlists
        """
        self.lists.edit_btn['state'] = DISABLED
        searchlist = []
        print(show_after)
        if show_after:
            if not search:
                search = datetime.date(1, 1, 1)
            else:
                try:
                    searchdate = datetime.datetime.strptime(search, '%Y-%m-%d')
                    search = searchdate.date()
                    print("Date is fixed")
                except ValueError:
                    self.lists.update_packlist_display([])
                    print("ValueError")
                    return
            for packlist in lists:
                #if packlist.date >= search:
                if (datetime.datetime.strptime(str(packlist.date), '%Y-%m-%d').date()) >= (datetime.datetime.strptime(str(search), '%Y-%m-%d').date()):
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

        Label(text="Welcome to Packlist program!\n", width=40).grid(row=0, column=0, columnspan=3)
        Label(text="Search from date:", anchor=W, width=36).grid(row=1, column=0, columnspan=3)
        Entry(textvariable=search_date_entry_var, width=25).grid(row=2, column=0, columnspan=2)
        Button(text="Search", command=lambda: self.root.search_lists(self.root.packlists, search_date_entry_var.get(), show_after=True)).grid(row=2, column=2)
        Label(text="Search by name or date:", anchor=W, width=36).grid(row=3, column=0, columnspan=3)
        Entry(text=search_datename_entry_var, width=25).grid(row=4, column=0, columnspan=2)
        Button(text="Search", command=lambda: self.root.search_lists(self.root.packlists, search_datename_entry_var.get())).grid(row=4, column=2)
        Label(text="", width=40).grid(row=5, column=0, columnspan=3)

        self.packlist_listbox = Listbox(listvariable=self.packlists_listbox_var,  exportselection=0, width=40)
        self.packlist_listbox.bind("<<ListboxSelect>>", lambda e: self.listbox_selection())
        self.packlist_listbox.grid(row=6, column=0, columnspan=3)
        Button(text="New list", command=lambda: self.edit_create(new=True)).grid(row=7, column=0)
        self.edit_btn = Button(text="Edit", command=lambda: self.edit_create(), state=DISABLED)
        self.edit_btn.grid(row=7, column=1)
        self.update_packlist_display(self.root.packlists_filtered)

    def listbox_selection(self):
        self.edit_btn['state'] = ACTIVE
        index = self.packlist_listbox.curselection()[0]
        self.root.itemlists.update_itemlist_display(self.root.packlists_filtered[index])

    def edit_create(self, new=False):
        if new:
            selected_list = None
        else:
            selected_list = self.root.packlists_filtered[self.packlist_listbox.curselection()[0]]
        InputBox(self.root, selected_list=selected_list)

    def update_packlist_display(self, packlists):
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
        self.root = root
        self.selected_packlist = None
        self.packlists_items_box_var = StringVar()
        self.namedate_var = StringVar("")
        self.show_only_unpacked = BooleanVar()

        self.name_date = Label(textvariable=self.namedate_var).grid(row=4, column=4, columnspan=3)
        self.toggle_btn = Checkbutton(text="Show only unpacked items", command=lambda: self.update_itemlist_display(self.selected_packlist), onvalue=True, offvalue=False, variable=self.show_only_unpacked).grid(row=5, column=4, columnspan=3)
        self.packlist_items_box = Listbox(listvariable=self.packlists_items_box_var, width=40)
        self.packlist_items_box.bind("<<ListboxSelect>>", self.packlist_items_box.curselection()) #Testrad, ta bort?
        self.packlist_items_box.grid(row=6, column=4, columnspan=3)
        self.add_item = Button(text="+", command=lambda: self.add_item_func(), state=DISABLED)
        self.add_item.grid(row=7, column=4)
        self.remove_item = Button(text="-", command=lambda: self.remove_item_func(), state=DISABLED)
        self.remove_item.grid(row=7, column=5)
        self.toggle_item = Button(text="Set packed", command=lambda: self.toggle_item_func(), state=DISABLED)
        self.toggle_item.grid(row=7, column=6)
        self.buttons = [self.add_item, self.remove_item, self.toggle_item]


    def update_itemlist_display(self, packlist=None):
        if not packlist:
            if self.selected_packlist:
                packlist = self.selected_packlist
            else:
                for button in self.buttons:
                    button['state'] = DISABLED
                return
        self.selected_packlist = packlist
        if not packlist.items:
            self.packlists_items_box_var.set(["No items found!"])   #TODO: Fix error when "No items found!" is deleted or set packed in listbox
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

    def add_item_func(self):
        InputBox(self.root, selected_list=self.selected_packlist, new_item=True)

    def remove_item_func(self):
        items = [item for item in self.selected_packlist.items.keys()]
        try:
            self.selected_packlist.items.pop(items[self.packlist_items_box.curselection()[0]])
            self.update_itemlist_display(self.selected_packlist)
        except IndexError:
            pass

    def toggle_item_func(self):
        items = [key for key, value in self.selected_packlist.items.items()]
        try:
            selected_item = items[self.packlist_items_box.curselection()[0]]
            self.selected_packlist.items[selected_item] = not self.selected_packlist.items[selected_item]
            self.update_itemlist_display(self.selected_packlist)
        except IndexError:
            pass


class InputBox:
    def __init__(self, root, selected_list=None, new_item=False):
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
        self.popup.protocol("WM_DELETE_WINDOW", self.dismiss)  # intercept close button
        self.popup.transient(root)  # dialog window is related to main
        self.popup.wait_visibility()  # can't grab until window appears, so we wait
        self.popup.grab_set()  # ensure all input goes to our window
        self.popup.wait_window()  # block until window is destroyed

    def dismiss(self):
        self.popup.grab_release()
        self.popup.destroy()

    def save(self):
        if self.new_item:
            self.selected_list.items[self.item_entry_var.get()] = False
        else:
            if not self.selected_list:
                self.root.packlists.append(new_packlist(self.name_entry_var.get(), self.date_entry_var.get())) #TODO: felhantering input, datum!!
            else:
                self.selected_list.name = self.name_entry_var.get()
                self.selected_list.change_date(datetime.datetime.strptime(self.date_entry_var.get(), '%Y-%m-%d').date())
        self.root.packlists = sort_lists(self.root.packlists)
        self.root.lists.update_packlist_display(self.root.packlists)
        self.root.itemlists.update_itemlist_display()
        self.dismiss()


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

def new_packlist(name, date):
    """
    create new packlist
    :return: packlist created
    """
    name = name[0].upper() + name[1:]
    date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    packlist = PackList(name, date)
    return packlist

def sort_lists(lists):
    """
    sort lists by date
    :param list lists: list of lists to be sorted
    :return: lists: sorted by date
    """
    for packlist in lists:
        packlist.items = dict(sorted(packlist.items.items()))
    return sorted(lists, key=lambda packlist: str(packlist.date))

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



def quit_write_to_file(lists, file):
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