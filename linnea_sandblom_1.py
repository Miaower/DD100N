# Inlämningsuppgift 1, DD100N, Linnéa Sandblom, 2022-01-29
# The program prints out a presentation made from the variables declared.
import typing

def print_presentation():
    # variables
    NAME: typing.Final = "Linnéa"
    BF_NAME: typing.Final = "Simon"
    age: int = 28
    bf_age: int = 32
    age_difference: int = bf_age - age
    nr_of_cats: int = 2
    shoe_size: float = 37.5
    combined_age: int = age + bf_age

    # printout
    print(NAME + " is", age, "years old and has", nr_of_cats, "cats. Her shoe size is " + str(shoe_size) + ". "
          + NAME + "'s boyfriends name is", BF_NAME, "and he is", bf_age, "years old. \nTogether, " + NAME +
          " and " + BF_NAME + " is", combined_age, "years old. When " + NAME + " was born, " + BF_NAME +
          " was", age_difference, "years old.")

    # Nicer way to create string for printing
    #print(
    #    f"{NAME} is {age} years old and has {nr_of_cats} cats. Her shoe size is {shoe_size}. {NAME}'s boyfriends name "
    #    f"is {BF_NAME} and he is {bf_age} years old. \nTogether {NAME} and {BF_NAME} is {combined_age} years old. "
    #    f"When {NAME} was born, {BF_NAME} was {age_difference} years old."
    #)


# run print_presentation()
if __name__ == "__main__":
    print_presentation()