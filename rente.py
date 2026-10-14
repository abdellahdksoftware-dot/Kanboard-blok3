saldo = float(input("Voer het saldo in: "))
def jaarlijkse_rente(saldo, rente_percentage):
    """
    Bereken de jaarlijkse rente op een gegeven saldo.

    Parameters:
    saldo (float): Het saldo waarop de rente wordt berekend.
    rente_percentage (float): Het jaarlijkse rentepercentage.

    Returns:
    float: De jaarlijkse rente.
    """
    if 0 < saldo <= 10000:
        rente_percentage = 0.25
        return  saldo * (rente_percentage / 100)
    elif 25000 < saldo <= 50000:
        rente_percentage = 0.25
        return saldo * (rente_percentage / 100)
    elif 10000 < saldo <= 25000:
        rente_percentage = 0
        return saldo * (rente_percentage / 100)
    elif 50000 < saldo <= 100000:
        rente_percentage = 0.25
        return saldo * (rente_percentage / 100)
    elif 100000 < saldo < 1000000: 
        rente_percentage = 0.5
        return saldo * (rente_percentage / 100)
    else:
        print("Saldo is buiten het toegestane bereik.")

print(f"De jaarlijkse rente op een saldo van {saldo} is: {jaarlijkse_rente(saldo, 0)}")