"""Transacties berekenen: storten en opnemen, het nieuwe saldo uitrekenen en opslaan.

Dit bestand kent geen Flask of HTML. Het werkt alleen met Python en de database,
dus je kunt het ook los testen.
"""

from datetime import datetime

from database import maak_verbinding

STORTING = "storting"
OPNAME = "opname"


def haal_saldo_op(rekening_id):
    """Geef het huidige saldo van een rekening."""
    verbinding = maak_verbinding()
    rij = verbinding.execute(
        "SELECT saldo FROM rekening WHERE rekening_id = ?", (rekening_id,)
    ).fetchone()
    verbinding.close()

    if rij is None:
        raise ValueError("Deze rekening bestaat niet.")
    return rij["saldo"]


def controleer_bedrag(bedrag):
    """Het bedrag moet een getal groter dan 0 zijn."""
    if not isinstance(bedrag, (int, float)) or bedrag <= 0:
        raise ValueError("Het bedrag moet groter zijn dan 0.")


def bereken_nieuw_saldo(saldo, type_transactie, bedrag):
    """Reken het saldo uit na een storting of opname."""
    if type_transactie == STORTING:
        return round(saldo + bedrag, 2)

    if type_transactie == OPNAME:
        if bedrag > saldo:
            raise ValueError("Onvoldoende saldo voor deze opname.")
        return round(saldo - bedrag, 2)

    raise ValueError(f"Onbekend type transactie: {type_transactie}")


def verwerk_transactie(rekening_id, type_transactie, bedrag):
    """Bereken het nieuwe saldo, werk de rekening bij en bewaar de transactie.

    Geeft het nieuwe saldo terug. Bij een fout verandert er niets in de database.
    """
    controleer_bedrag(bedrag)

    verbinding = maak_verbinding()
    try:
        with verbinding:  # slaat alles samen op, of draait alles terug bij een fout
            rij = verbinding.execute(
                "SELECT saldo FROM rekening WHERE rekening_id = ?", (rekening_id,)
            ).fetchone()
            if rij is None:
                raise ValueError("Deze rekening bestaat niet.")

            nieuw_saldo = bereken_nieuw_saldo(rij["saldo"], type_transactie, bedrag)

            verbinding.execute(
                "UPDATE rekening SET saldo = ? WHERE rekening_id = ?",
                (nieuw_saldo, rekening_id),
            )
            verbinding.execute(
                """INSERT INTO transactie
                       (rekening_id, type, bedrag, datum, saldo_na_transactie)
                   VALUES (?, ?, ?, ?, ?)""",
                (
                    rekening_id,
                    type_transactie,
                    bedrag,
                    datetime.now().strftime("%Y-%m-%d %H:%M"),
                    nieuw_saldo,
                ),
            )
    finally:
        verbinding.close()

    return nieuw_saldo


def stort(rekening_id, bedrag):
    return verwerk_transactie(rekening_id, STORTING, bedrag)


def neem_op(rekening_id, bedrag):
    return verwerk_transactie(rekening_id, OPNAME, bedrag)


def haal_transacties_op(rekening_id):
    """Geef alle transacties van een rekening, nieuwste eerst."""
    verbinding = maak_verbinding()
    transacties = verbinding.execute(
        """SELECT type, bedrag, datum, saldo_na_transactie
           FROM transactie
           WHERE rekening_id = ?
           ORDER BY transactie_id DESC""",
        (rekening_id,),
    ).fetchall()
    verbinding.close()
    return transacties