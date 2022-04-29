# Inlämningsuppgift 5, DD100N, Linnéa Sandblom, 2022-03-01
# The program keeps count of the score of a dart competition.
# It reads the score from, and saves the score to a text file.
import ast


def read_file(in_file="results2022.txt"):
    """
    Reads from the text file(in_file) into the list competitors
    :param in_file: name of text-file containing competitors and their scores
    :return: competitors: list containing competitors and their scores
    """
    competitors = []
    with open(in_file, "r+", encoding="utf-8") as file:
        for line in file:
            competitors.append(ast.literal_eval(line.strip()))
    return competitors


def view_results(competitors):
    """
    Sorts and views results in order of highest to lowest scores
    :param competitors: list containing competitors and their scores
    """
    results = sorted(competitors, key=lambda person: person[1], reverse=True)
    for element in results:
        print(f" {element[0]}: {element[1]} points")


def enter_results(competitors):
    """
    Enters new player and score to the list
    :param competitors: list containing competitors and their scores
    :return: competitors: list containing competitors and their scores, with added player and score
    """
    new_name = input("Name of competitor: ")
    while not check_name(competitors, new_name):
        new_name = input("This name is already taken or invalid. Enter new name of competitor: ")

    new_result = input(f"How many points did {new_name} get? ")
    while not check_result(new_result):
        new_result = input(f"Invalid input. Enter a result between 0-50. How many points did {new_name} get? ")

    competitors.append([new_name, int(new_result)])
    return competitors


def check_name(competitors, new_name):
    """
    Checks if name is taken
    :param competitors: list containing competitors and their scores
    :param new_name: name to check
    :return: False if name is already taken, else True
    """
    for element in competitors:
        if element[0] == new_name or not element[0]:
            return False
    return True


def check_result(new_result):
    """
    Checks if score is int and if it is in the requested range 0-50.
    :param new_result: score to be checked
    :return: False if new_result is not an int or not in range 0-50, else True
    """
    try:
        new_result = int(new_result)
    except ValueError:
        return False
    if new_result not in range(0, 51):
        return False
    return True


def save_quit(competitors, file="results2022.txt"):
    """
    Saves list of competitors to text file.
    :param competitors: list containing competitors and their scores
    :param file: filename to save to
    """
    with open(file, "w") as file:
        for element in competitors:
            file.write(str(element) + "\n")
    print("Saved, welcome back!")


def main():
    """
    Calls function to read text file with competition data. Let's user choose between the actions
    "View results", "Enter new result" and "Save and quit"
    """
    competitors = read_file()
    while True:
        print("\n1. View results \n2. Enter new result \n3. Save and quit")
        choice = input("Choose an alternative 1-3: ")
        print()
        if choice == "1":
            view_results(competitors)
        elif choice == "2":
            enter_results(competitors)
        elif choice == "3":
            save_quit(competitors)
            break


if __name__ == "__main__":
    main()
