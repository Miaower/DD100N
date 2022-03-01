# Inlämningsuppgift 6, DD100N, Linnéa Sandblom, 2022-xx-xx
# Controls a pet care robot. Finds pets, feeds and pets them.

def list_pets():
    return True


def find_pet():
    pet = input("Which pet do you want me to find? ")
    pet_care(pet)


def pet_pet():
    return True


def feed_pet():
    return True


def pet_care(pet):
    print(f"Found {pet}. What should I do now?\n1. Pet {pet} \n2. Feed {pet} \n3. Main menu")
    choice = input("Choose an alternative 1-3: ")
    if choice == "1":
        pet_pet()
    elif choice == "2":
        feed_pet()
    elif choice == "3":
        break

def main():
    while True:
        print("\n1. List pets and their statuses \n2. Find pet \n3. Quit")
        choice = input("Choose an alternative 1-3: ")
        print()
        if choice == "1":
            list_pets()
        elif choice == "2":
            find_pet()
        elif choice == "3":
            print("Welcome back!")
            break


if __name__ == "__main__":
    main()