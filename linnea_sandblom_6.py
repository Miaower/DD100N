# Inlämningsuppgift 6, DD100N, Linnéa Sandblom, 2022-03-14
# Controls a pet care robot. Finds pets, feeds and pets them. Loads and saves pet-data from text-file.
import ast

class Pet:
    def __init__(self, species, name, hunger, need_of_pats):
        """
        Constructor for objects of class Pet
        :param str species: type of animal
        :param str name: name of pet
        :param int hunger: represents hunger level
        :param int need_of_pats: represents need-of-pats-level
        """
        self.species: str = species
        self.name: str = name
        self.hunger: int = hunger
        self.need_of_pats: int = need_of_pats

    def feed(self):
        """
        Lowers self.hunger with -3 or to 0
        """
        if (self.hunger - 3) >= 0:
            self.hunger = self.hunger - 3
        else:
            self.hunger = 0

    def pet(self):
        """
        Lowers self.hunger with -3 or to 0
        """
        self.need_of_pats = self.need_of_pats - 3
        if (self.need_of_pats - 3) >= 0:
            self.need_of_pats = self.need_of_pats - 3
        else:
            self.need_of_pats = 0

    def __repr__(self):
        """
        :return: String representation of a pet
        """
        return str((self.name, self.species, self.hunger, self.need_of_pats))


    def __str__(self):
        """
        :return: String representation of a pet formatted for human eyes
        """
        return f"{self.name} the {self.species}: Hunger: {self.hunger}, Need for pats: {self.need_of_pats}"

    def __lt__(self, other: "Pet"):
        """
        Is self less than other
        :param other: Object of class Pet
        :return: True if attributes in comparison is lees for self, otherwise False
        """
        if other.hunger*2 + other.need_of_pats/2 > self.hunger*2 + self.need_of_pats/2:
            return True
        return False


def print_pets(pet_list):
    """
    Sorts the pets in pet_list by need of care
    :param pet_list: List of objects of class Pet
    """
    sorted_pets = sorted(pet_list, reverse=True)
    for pet in sorted_pets:
        print(pet)


def find_pet(pet_list):
    """
    Find a pet. Go to pet care menu (pet_care())
    :param pet_list: List of objects of class Pet
    """
    pet_name = input("Which pet do you want me to find? ")
    pet_found = False
    for pet in pet_list:
        if pet.name == pet_name:
            pet_found = True
            pet_care(pet)
            break  # Don't loop more than needed
    if not pet_found:
        print(f"Could not find {pet_name} in pet list. Returning to main menu.")


def pet_care(pet):
    """
    Feeds and/or pets the @pet
    :param pet: Pet to be fed and/or petted
    """
    print(f"Found {pet.name}.")
    while True:
        print(f"What should I do now?\n1. Pet {pet.name} \n2. Feed {pet.name} \n3. Main menu")
        choice = input("Choose an alternative 1-3: ")
        if choice == "1":
            pet.pet()
            print(f"feeding {pet.name}")
        elif choice == "2":
            pet.feed()
            print(f"Petting {pet.name}")
        elif choice == "3":
            break


def read_file(in_file="pets.txt"):
    """
    Reads from the text file(in_file) into the list pet_list
    :param in_file: text-file containing pets
    :return: competitors: list containing pets
    """
    pet_list = []
    with open(in_file, "r+", encoding="utf-8") as file:
        for line in file:
            evaluated_line = ast.literal_eval(line.strip())
            name, species, hunger, num_of_pats = evaluated_line
            pet_list.append(Pet(species, name, hunger, num_of_pats))
    return pet_list


def save_quit(pet_list, file="pets.txt"):
    """
    Saves list of pets to text file.
    :param pet_list: list containing pets
    :param file: file to save to
    """
    with open(file, "w") as file:
        for pet in pet_list:
            file.write(repr(pet) + "\n")
    print("Saved, welcome back!")


def main():
    """
    Main function. Runs main menu.
    """
    #animal_1 = Pet('cat', 'Mira', 2, 4)
    #animal_2 = Pet('dog', 'Virre', 2, 3)
    #animal_3 = Pet('chinchilla', 'Lio', 4, 1)
    #pet_list = [animal_1, animal_2, animal_3]
    pet_list = read_file()
    while True:
        print("\n1. List pets and their statuses \n2. Find pet \n3. Quit")
        choice = input("Choose an alternative 1-3: ")
        print()
        if choice == "1":
            print_pets(pet_list)
        elif choice == "2":
            find_pet(pet_list)
        elif choice == "3":
            save_quit(pet_list)
            break


if __name__ == "__main__":
    main()