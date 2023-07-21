"""
Na podstawie zadania z lekcji 5 (operacje na koncie, sprzedaż/zakup itp.) należy zaimplementować poniższą część:

Saldo konta oraz magazyn mają zostać zapisane do pliku tekstowego, a przy kolejnym uruchomieniu programu ma zostać odczytany.
Zapisać należy również historię operacji (przegląd), która powinna być rozszerzana przy każdym kolejnym uruchomieniu programu.
"""
import json

import praca_domowa_9.praca_domowa_9.funkcje_do_zarzadzania_plikami
from enums import WyborKomendy
from funkcje_do_zarzadzania_plikami import load_history, load_saldo_and_magazyn, save_saldo_and_magazyn_to_file

initial_message = "Witaj w Twoim magazynie. Lista dostępnych komend to:\n" \
                  " 1. Saldo\n 2. Sprzedaż\n 3. Zakup\n 4. Konto\n 5. Lista\n 6. Magazyn\n 7. Przegląd\n 8. Koniec"

end_program = False
saldo, magazyn = load_saldo_and_magazyn(file="saldo_i_magazyn.txt")
history = load_history(file="history.txt")
print(history)
while not end_program:
    print(f"Magazyn: {magazyn}")
    print(f"Saldo: {saldo}")
    print(initial_message)
    operation = input("Podaj operację, którą chcesz wykonać ")
    if operation == WyborKomendy.ZMIEN_SALDO.value:
        changes = input("Chcesz dodać czy odjąć z konta? (-/+)")
        try:
            if changes == "+":
                amount = float(input("Podaj kwotę, którą chcesz dodać"))
                saldo += amount
                history.append(f"Wykonano instrukcję saldo zasilono {amount} \n")
            elif changes == "-":
                amount = float(input("Podaj kwotę, którą chcesz odjąć"))
                saldo -= amount
                history.append(f"Wykonano infstrukcje saldo zmniejszono {amount} \n")
        except:
            print("Wystąpił błąd, musisz wpisać kwotę!")
    if operation == WyborKomendy.SPRZEDAZ.value:
        print(magazyn)
        product = input("Podaj nazwę produktu: ")
        amount = int(input("Podaj ilość, którą chcesz sprzedać: "))
        product_found = False
        for item, item_details in magazyn.items():
            if product == item:
                item_details["ilość"] -= amount
                saldo += (item_details["cena"] * amount)
                product_found = True
                history.append(f"Sprzedano {product} w ilości {amount} \n")
                break
        if not product_found:
            history.append(f"Nie udało się sprzedać towaru {product}, mamy go za mało na magazynie \n")
    if operation == WyborKomendy.ZAKUP.value:
        print(magazyn)
        product = input("Podaj nazwe produktu: ")
        amount = input("Podaj ilość: ")
        for item, item_details in magazyn.items():
            if product == item:
                item_details["ilość"] += amount
                saldo -= (item_details["cena"] * amount)
                history.append(f"Zakupiono {product} w ilości {amount} \n")
                break
    if operation == WyborKomendy.KONTO.value:
        print(saldo)
    if operation == WyborKomendy.LISTA.value:
        print(magazyn)
    if operation == WyborKomendy.MAGAZYN.value:
        choice = input(f"Podaj produkt: ")
        if choice == "rower":
            print(magazyn.get("rower"))
        elif choice == "łódka":
            print(magazyn.get("łódka"))
    if operation == WyborKomendy.PRZEGLAD.value:
        value_from = input("Podaj początkowy zakres")
        value_to = input("Podaj końcowy zakres")
        if not value_to and not value_from:
            print(history)
        if value_from and not value_to:
            print(history[value_from:])

    if operation == WyborKomendy.KONIEC.value:
        end_program = True
        save_saldo_and_magazyn_to_file(file="saldo_i_magazyn.txt", saldo=saldo, magazyn=magazyn)

with open("history.txt", mode="w") as save_history:
    historytxt = "".join(history)
    save_history.write(historytxt)