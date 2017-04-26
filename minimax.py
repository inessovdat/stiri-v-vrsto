import logging

from igra import RDECI_IGRALEC, RUMENI_IGRALEC, PRAZNO, NEODLOCENO, NI_KONEC, nasprotnik

import random

######################################################################
## Algoritem minimax

class Minimax:
    # Algoritem minimax predstavimo z objektom, ki hrani stanje igre in
    # algoritma, nima pa dostopa do GUI (ker ga ne sme uporabljati, saj deluje
    # v drugem vlaknu kot tkinter).

    def __init__(self, globina):
        self.globina = globina  # do katere globine iščemo?
        self.prekinitev = False # ali moramo končati?
        self.igra = None # objekt, ki opisuje igro (ga dobimo kasneje)
        self.jaz = None  # katerega igralca igramo (podatek dobimo kasneje)
        self.poteza = None # sem napišemo potezo, ko jo najdemo

    def prekini(self):
        """Metoda, ki jo pokliče GUI, če je treba nehati razmišljati, ker
           je uporabnik zaprl okno ali izbral novo igro."""
        self.prekinitev = True

    def izracunaj_potezo(self, igra):
        """Izračunaj potezo za trenutno stanje dane igre."""
        # To metodo pokličemo iz vzporednega vlakna
        self.igra = igra
        self.prekinitev = False # Glavno vlakno bo to nastvilo na True, če moramo nehati
        self.jaz = self.igra.na_potezi
        self.poteza = None # Sem napišemo potezo, ko jo najdemo
        # Poženemo minimax
        (poteza, vrednost) = self.minimax(self.globina, True)
        self.jaz = None
        self.igra = None
        if not self.prekinitev:
            # Potezo izvedemo v primeru, da nismo bili prekinjeni
            logging.debug("minimax: poteza {0}, vrednost {1}".format(poteza, vrednost))
            self.poteza = poteza

    # Vrednosti igre
    ZMAGA = 10000000
    NESKONCNO = ZMAGA + 1 # Več kot zmaga

    def stej(self):
        stevilo_krogcev = 0
        for i in range(6):
            for j in range(5):
                if self.igra.plosca[i][j] != PRAZNO:
                    stevilo_krogcev += 1
        return stevilo_krogcev
                

    def vrednost_pozicije(self):
        """Ocena vrednosti pozicije: sešteje vrednosti vseh trojk na plošči."""
        # Slovar, ki pove, koliko so vredne posamezne trojke, kjer "(x,y) : v" pomeni:
        # če imamo v trojki x znakov igralca in y znakov nasprotnika (in 3-x-y praznih polj),
        # potem je taka trojka za self.jaz vredna v.
        # Trojke, ki se ne pojavljajo v slovarju, so vredne 0.
        vrednost_stirke = {
            (4,0) : Minimax.ZMAGA - 10*self.stej(),
            (0,4) : -Minimax.ZMAGA + 10*self.stej(),
            (3,0) : Minimax.ZMAGA//100 - 10*self.stej(),
            (0,3) : -Minimax.ZMAGA//100 + 10*self.stej(),
            (2,0) : Minimax.ZMAGA//10000 - 10*self.stej(),
            (0,2) : -Minimax.ZMAGA//10000 + 10*self.stej(),
            (1,0) : Minimax.ZMAGA//1000000 - 10*self.stej(),
            (0,1) : -Minimax.ZMAGA//1000000 + 10*self.stej()
        }
        vrednost = 0
        for p in self.igra.stirke:
            x = 0
            y = 0
            for (i,j) in p:
                if self.igra.plosca[i][j] == self.jaz:
                    x += 1
                elif self.igra.plosca[i][j] == nasprotnik(self.jaz):
                    y += 1
            vrednost += vrednost_stirke.get((x,y), 0)
        return vrednost

    def minimax(self, globina, maksimiziramo):
        """Glavna metoda minimax."""
        if self.prekinitev:
            # Sporočili so nam, da moramo prekiniti
            logging.debug ("Minimax prekinja, globina = {0}".format(globina))
            return (None, 0)
        (zmagovalec, stirka) = self.igra.preveri_konec_igre()
        if zmagovalec in (RDECI_IGRALEC, RUMENI_IGRALEC, NEODLOCENO):
            # Igre je konec, vrnemo njeno vrednost
            if zmagovalec == self.jaz:
                return (None, Minimax.ZMAGA)
            elif zmagovalec == nasprotnik(self.jaz):
                return (None, -Minimax.ZMAGA)
            else:
                return (None, 0)
        elif zmagovalec == NI_KONEC:
            # Igre ni konec
            if globina == 0:
                return (None, self.vrednost_pozicije())
            else:
                # Naredimo eno stopnjo minimax
                if maksimiziramo:
                    # Maksimiziramo
                    najboljse_poteze = []
                    vrednost_najboljse = -Minimax.NESKONCNO
                    for stolpec in self.igra.veljavne_poteze():
                        self.igra.povleci_potezo(stolpec)
                        vrednost = self.minimax(globina-1, not maksimiziramo)[1]
                        self.igra.razveljavi()
                        if vrednost > vrednost_najboljse:
                            vrednost_najboljse = vrednost
                            najboljse_poteze = [stolpec]
                        elif vrednost == vrednost_najboljse:
                            najboljse_poteze.append(stolpec)
                else:
                    # Minimiziramo
                    najboljse_poteze = []
                    vrednost_najboljse = Minimax.NESKONCNO
                    for stolpec in self.igra.veljavne_poteze():
                        self.igra.povleci_potezo(stolpec)
                        vrednost = self.minimax(globina-1, not maksimiziramo)[1]
                        self.igra.razveljavi()
                        if vrednost < vrednost_najboljse:
                            vrednost_najboljse = vrednost
                            najboljse_poteze = [stolpec]
                        elif vrednost == vrednost_najboljse:
                            najboljse_poteze.append(stolpec)

                assert (najboljse_poteze is not []), "minimax: izračunana poteza je None"
                return (random.choice(najboljse_poteze), vrednost_najboljse)
        else:
            assert False, "minimax: nedefinirano stanje igre"
