# Inlämningsuppgift 4

# Linnéa Sandblom
# 2022-02-27
# DD100N
# Programmet är ett tre-i-rad-spel

# För att rita ut spelplanen används Box Drawing Characters": https: // en.wikipedia.org / wiki / Box - drawing_character

import random

def skrivUtSpelplan(spelplan):
    """
    Visar spelplanen
    :param spelplan: matris innehållandes strängar; ' ', 'X' eller '0'
    """
    print('     A     B     C  ')
    print('  ┏━━━━━┳━━━━━┳━━━━━┓')
    radRäknare = 0
    for rad in spelplan:
        radRäknare += 1
        print(str(radRäknare) + ' ┃', end=' ')
        for ruta in rad:
            print(' ' + ruta, end='  ')
            print('┃', end=' ')
        print()
        if radRäknare < 3:  # Efter sista raden vill vi inte göra detta
            print('  ┣━━━━━╋━━━━━╋━━━━━┫')
    print('  ┗━━━━━┻━━━━━┻━━━━━┛')  # Utan istället detta


def kontrolleraRader(spelplan):
    """Kontrollerar om det finns tre likadana tecken på någon rad och returnerar då True, annars False
    Inparameter: spelplan (matris)
    Returvärde: True om det finns vinnare annars False (booleskt värde)
    """
    for i in range(3):
        if ' ' not in [spelplan[i][0], spelplan[i][1], spelplan[i][2]]:
            if spelplan[i][0] == spelplan[i][1] == spelplan[i][2]:
                return True
            else:
                return False

    return False


def kontrolleraKolumner(spelplan):
    """
    Kollar om tre av samma markering på rad finns längs någon kolumn.
    :param: spelplan: matris innehållandes strängar; ' ', 'X' eller '0'
    :return: True om tre av samma markering på rad finns längs en kolumn, annars False
    """
    for i in range(3):
        if ' ' not in [spelplan[0][i], spelplan[1][i], spelplan[2][i]]:
            if spelplan[0][i] == spelplan[1][i] == spelplan[2][i]:
                return True
            else:
                return False

    return False


def kontrolleraDiagonaler(spelplan):
    """
    Kollar om tre av samma markering på rad finns längs diagonalerna.
    :param spelplan: matris innehållandes strängar; ' ', 'X' eller '0'
    :return: True om tre av samma markering på rad finns längs en diagonal, annars False
    """
    # första diagonalen, uppe till vänster till nere till höger
    if ' ' not in [spelplan[0][0], spelplan[1][1], spelplan[2][2]] and spelplan[0][0] == spelplan[1][1] == spelplan[2][2]:
        return True
    # andra diagonalen, uppe till höger till nere till vänster
    elif ' ' not in [spelplan[0][2], spelplan[1][1], spelplan[2][0]] and spelplan[0][2] == spelplan[1][1] == spelplan[2][0]:
        return True
    else:
        return False


def finnsVinnare(spelplan):
    """
    Kontrollerar om någon spelare vunnit.
    :param spelplan: matris innehållandes strängar; ' ', 'X' eller '0'
    :return: True om någon spelare vunnit, annars False
    """
    if kontrolleraKolumner(spelplan) or kontrolleraDiagonaler(spelplan) or kontrolleraRader(spelplan):
        return True
    else:
        return False


def oavgjort(spelplan):
    """
    Kollar om spelet är oavgjort
    :param spelplan: matris innehållandes strängar; ' ', 'X' eller '0'
    :return: True om oavgjurt, False om ej oavgjort
    """
    if kontrolleraKolumner(spelplan) or kontrolleraDiagonaler(spelplan) or kontrolleraRader(spelplan):
        return False

    for rad in spelplan:
        for element in rad:
            if element == ' ':
                return False

    return True


def tolkaInmatning(inmatning):
    """
    Ser till att markör hamnar i avsedd ruta
    :param str inmatning: A-C för kolumn samt 1-3 för rad, t.ex A1 eller B3.
    :return: tupel rad, kolumn: position för rad och kolumn.
    """
    bokstav = inmatning[0].upper()  # Använder .upper() för att göra om alla inmatade bokstäver till versaler
    rad = int(inmatning[1]) - 1
    if bokstav == 'A':
        kolumn = 0
    elif bokstav == 'B':
        kolumn = 1
    elif bokstav == 'C':
        kolumn = 2
    else:
        raise RuntimeError("Letter has to be 'A', 'B' or 'C'.")
    return rad, kolumn


def vemStartar():
    """
    Slumpar vilken spelare som startar
    :return: int: 1 or 2
    """
    return random.randint(1,2)


def spela(spelarNamn1, spelarNamn2):
    """
    Kör spelet. Tar input från spelare, sätter ut markörer och avgör vem som vinner.
    :param str spelarNamn1: Namn på spelare 1
    :param str spelarNamn2: Namn på spelare 2
    """
    print("Då kör vi!")
    print("Ange de koordinater du vill lägga på på formatet A1, B3 osv.")
    spelplan = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]

    spelarLista = [spelarNamn1, spelarNamn2]
    vemsTur = vemStartar()
    while finnsVinnare(spelplan) == False:
        vemsTur = (vemsTur + 1) % 2  # vemsTur ska aldrig bli 2, utan börja om igen på 0, %-är modul dvs resten vid heltals division.
        skrivUtSpelplan(spelplan)
        if vemsTur == 0:
            markör = 'X'
        else:
            markör = 'O'
        inmatning = input(str(spelarLista[vemsTur]) + "s tur att spela: ")
        rad, kolumn = tolkaInmatning(inmatning)
        if spelplan[rad][kolumn] != ' ':
            print("Rutan är upptagen, turen går över.")
            continue
        spelplan[rad][kolumn] = markör
        if oavgjort(spelplan) == True:
            skrivUtSpelplan(spelplan)
            print("Det blev oavgjort!")
            break

    if not oavgjort(spelplan):
        skrivUtSpelplan(spelplan)
        print("Grattis " + str(spelarLista[vemsTur]) + " du vann!")


def huvudfunktion():
    """
    Huvudfunktion, tar in spelarnamn och startar spelet.
    """
    print("Hej och väkommen till Tre-i-rad!")
    spelarNamn1 = input("Vad heter spelare 1? ")
    spelarNamn2 = input("Vad heter spelare 2? ")
    spela(spelarNamn1, spelarNamn2)


if __name__ == "__main__":
    huvudfunktion()