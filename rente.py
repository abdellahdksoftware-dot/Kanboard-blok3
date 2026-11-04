# Spaarsysteem SparenVoorIedereen
# Rente wordt elke dag berekend en per kwartaal uitgekeerd.

import calendar
from datetime import date, timedelta

# Rente van de bank voor het wegzetten van geld, vanaf een datum
bank_rente = {date(2025, 1, 1): 2.05}

# Saldoklassen: (saldo lager dan, afwijking op de spaarrente)
klassen = [(10000, -0.25), (25000, 0), (50000, -0.15), (100000, -0.25), (1000000, -0.5)]

saldo = 0.0
opgebouwde_rente = 0.0
transacties = []      # (datum, soort, bedrag)
rente_per_dag = []    # (datum, bedrag)
vandaag = date(2025, 1, 1)


def rentepercentage(saldo, dag):
    laatste_wijziging = max(d for d in bank_rente if d <= dag)
    spaarrente = bank_rente[laatste_wijziging] - 0.25   # spaarders krijgen 0,25% minder
    if saldo <= 0:
        return 0
    for grens, afwijking in klassen:
        if saldo < grens:
            return spaarrente + afwijking
    return 0   # boven 1.000.000 geen rente


def einde_dag():
    global saldo, opgebouwde_rente, vandaag
    dagen = 366 if calendar.isleap(vandaag.year) else 365
    rente = saldo * rentepercentage(saldo, vandaag) / 100 / dagen
    opgebouwde_rente += rente
    rente_per_dag.append((vandaag, rente))

    morgen = vandaag + timedelta(days=1)
    if morgen.day == 1 and morgen.month in (1, 4, 7, 10):   # einde kwartaal
        uitkering = round(opgebouwde_rente, 2)
        saldo += uitkering
        transacties.append((vandaag, "rente", uitkering))
        opgebouwde_rente = 0
    vandaag = morgen


def vraag_datum(tekst):
    invoer = input(tekst + " (jjjj-mm-dd): ")
    return date.fromisoformat(invoer) if invoer else None


while True:
    print(f"\n--- Datum: {vandaag} | Saldo: € {saldo:.2f} ---")
    print("1 Storten  2 Opnemen  3 Saldo  4 Rente dit kwartaal  5 Rente dit jaar")
    print("6 Rente laatste 12 maanden  7 Transacties  8 Naar datum  9 Rente wijzigen  0 Stop")
    keuze = input("Keuze: ")

    try:
        if keuze == "1":
            bedrag = float(input("Bedrag: "))
            if bedrag <= 0:
                print("Bedrag moet positief zijn.")
            else:
                saldo += bedrag
                transacties.append((vandaag, "storting", bedrag))

        elif keuze == "2":
            bedrag = float(input("Bedrag: "))
            if bedrag <= 0 or bedrag > saldo:
                print("Ongeldig bedrag of te weinig saldo.")
            else:
                saldo -= bedrag
                transacties.append((vandaag, "opname", -bedrag))

        elif keuze == "3":
            print(f"Saldo: € {saldo:.2f} (rente {rentepercentage(saldo, vandaag):.2f}%)")

        elif keuze == "4":
            print(f"Opgebouwde rente dit kwartaal: € {opgebouwde_rente:.2f}")

        elif keuze == "5":
            totaal = sum(b for d, s, b in transacties if s == "rente" and d.year == vandaag.year)
            print(f"Uitgekeerde rente {vandaag.year}: € {totaal:.2f}")

        elif keuze == "6":
            per_maand = {}
            for d, b in rente_per_dag:
                if d > vandaag - timedelta(days=365):
                    maand = d.strftime("%m-%Y")
                    per_maand[maand] = per_maand.get(maand, 0) + b
            for maand, b in per_maand.items():
                print(f"{maand}: € {b:.2f}")

        elif keuze == "7":
            van = vraag_datum("Van (leeg = vanaf start)") or date(2025, 1, 1)
            tot = vraag_datum("Tot en met (leeg = vandaag)") or vandaag
            for d, s, b in transacties:
                if van <= d <= tot:
                    print(f"{d}  {s:<9} € {b:.2f}")

        elif keuze == "8":
            doel = vraag_datum("Naar datum")
            while doel and vandaag < doel:
                einde_dag()

        elif keuze == "9":
            vanaf = vraag_datum("Geldig vanaf")
            if vanaf:
                bank_rente[vanaf] = float(input("Nieuwe bankrente in %: "))

        elif keuze == "0":
            break

    except ValueError:
        print("Ongeldige invoer.")
