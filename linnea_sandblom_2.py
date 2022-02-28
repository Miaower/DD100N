# Inlämningsuppgift 2, DD100N, Linnéa Sandblom, 2022-02-02
# The program takes input from the user and converts centimetres to inches,
# kilometres to miles and kilograms to pounds.

print("Welcome to the Converter")
CM_PER_INCH: float = 2.54
MILES_PER_KM: float = 0.621371192237334
POUNDS_PER_KG: float = 2.2046226218487757
while True:
    try:
        print("\nChoose one of the following conversions: \n1. centimetres to inches \n"
              "2. kilometres to miles \n3. kilograms to pounds \n4. quit")
        choice_nr = int(input("Choose mode [1-4]: "))
        if choice_nr == 1:
            cm_input = float(input("Enter value in cm: "))
            print(cm_input, "cm equals", cm_input/CM_PER_INCH, "inches.")
        elif choice_nr == 2:
            km_input = float(input("Enter value in km: "))
            print(km_input, "km equals", km_input*MILES_PER_KM, "miles.")
        elif choice_nr == 3:
            kg_input = float(input("Enter value in kg: "))
            print(kg_input, "km equals", kg_input*POUNDS_PER_KG, "pounds.")
        elif choice_nr == 4:
            break
        else:
            print("Input must be between 1-4. Please try again.")
    except ValueError:
        print("Please input a number")
        continue
print("Welcome back!")