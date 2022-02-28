# Inlämningsuppgift 5, DD100N, Linnéa Sandblom, 2022-xx-xx
# Programmet håller koll på och visar poäng för en pilkastningstävling.
# Det läser in och sparar poängställningen till en textfil.
import ast


def read_file(in_file="results2022.txt"):
    competitors = []
    with open(in_file, "r+", encoding="utf-8") as file:
        for line in file:
            competitors.append(ast.literal_eval(line.strip()))
    return competitors

def view_results(competitors):
    for element in competitors:
        print(element)


def enter_results(competitors):
    input()
    return competitors


def save_quit(competitors=None):
    if competitors is None:
        competitors = [["Kalle", 3], ["Lisa", 50]]
    with open("results2022.txt", "w") as file:
        for element in competitors:
            file.write(str(element) + "\n")
    print("Saved, welcome back!")


def main():
    competitors = read_file()
    print("1. View results \n2. Enter new result \n3. Save and quit")
    while True:
        choice = input("Choose an alternative 1-3: ")
        if choice == "1":
            view_results(competitors)
        elif choice == "2":
            enter_results(competitors)
        elif choice == "3":
            save_quit()
            break


if __name__ == "__main__":
    main()