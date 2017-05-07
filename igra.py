RDECI_IGRALEC = 'RD'
RUMENI_IGRALEC = 'RU'
PRAZNO = ""
NI_KONEC = "igre ni konec"
NEODLOCENO = "neodločeno"

def nasprotnik(igralec):
    '''Vrne nasprotnika od igralca.'''
    if igralec == RDECI_IGRALEC:
        return RUMENI_IGRALEC
    elif igralec == RUMENI_IGRALEC:
        return RDECI_IGRALEC
    else:
        assert False, 'neveljaven nasprotnik'


class Igra():
    def __init__(self):
        self.na_potezi = RDECI_IGRALEC
        self.plosca = [[PRAZNO for i in range(7)] for j in range(6)]
        self.zgodovina = []

    def shrani_pozicijo(self):
        '''Igralca, ki je postavil krogec, shrani na mesto, kamor ga je postavil.'''
        pozicija = [self.plosca[i][:] for i in range(6)]
        self.zgodovina.append((pozicija, self.na_potezi))

    def kopija(self):
        '''Naredi kopijo plošče.'''
        kopirano = Igra()
        kopirano.plosca = [self.plosca[i][:] for i in range(6)]
        kopirano.na_potezi = self.na_potezi
        return kopirano

    def razveljavi(self):
        '''Razveljavi potezo.'''
        if self.na_potezi != None:
            (self.plosca, self.na_potezi) = self.zgodovina.pop()
        else:
            pass

    def veljavne_poteze(self):
        '''Vrne vse možne stolpce, v katere lahko postavimo krogec.'''
        mozne_poteze = []
        for i in range (7):
            if self.plosca[0][i] == PRAZNO:
                mozne_poteze.append(i)
        return mozne_poteze

    def vrni_vrstico(self, stolpec):
        '''Vrne vrstico, v katero mora pasti krogec.'''
        if stolpec in self.veljavne_poteze():
            vrstica = 5
            while self.plosca[vrstica][stolpec] != PRAZNO:
                vrstica -= 1
            return vrstica
        else:
            pass

    def povleci_potezo(self, stolpec):
        '''Če je poteza neveljavna se ne zgodi nič, vrne None. Sicer vrne preveri_konec_igre().'''
        if (stolpec not in self.veljavne_poteze()) or (self.na_potezi == None):
            # Neveljavna poteza
            return None
        else:
            self.shrani_pozicijo()
            self.plosca[self.vrni_vrstico(stolpec)][stolpec] = self.na_potezi
            (zmagovalec, stirka) = self.preveri_konec_igre()
            if zmagovalec == NI_KONEC:
                # Igre ni konec, na potezi je nasprotnik
                self.na_potezi = nasprotnik(self.na_potezi)
            else:
                # Igre je konec
                self.na_potezi = None
            return (zmagovalec, stirka)

    # Seznam vseh zmagovalnih štirk
    stirke =[
        #vrstice -
            [((i,0), (i,1), (i,2), (i,3)) for i in range(6)],
            [((i,1), (i,2), (i,3), (i,4)) for i in range(6)],
            [((i,2), (i,3), (i,4), (i,5)) for i in range(6)],
            [((i,3), (i,4), (i,5), (i,6)) for i in range(6)],
        #stolpci |
            [((0,j), (1,j), (2,j), (3,j)) for j in range(7)],
            [((1,j), (2,j), (3,j), (4,j)) for j in range(7)],
            [((2,j), (3,j), (4,j), (5,j)) for j in range(7)],
        #diagonale /
            [((0,j), (1,j-1), (2,j-2),(3,j-3))for j in range(3,7)],
            [((1,j), (2,j-1), (3,j-2),(4,j-3))for j in range(3,7)],
            [((2,j), (3,j-1), (4,j-2),(5,j-3))for j in range(3,7)],
        #diagonale \
            [((0,j), (1,j+1), (2,j+2),(3,j+3))for j in range(4)],
            [((1,j), (2,j+1), (3,j+2),(4,j+3))for j in range(4)],
            [((2,j), (3,j+1), (4,j+2),(5,j+3))for j in range(4)]]
    stirke = [s for l in stirke for s in l]

    def preveri_konec_igre(self):
        '''(RDECI_IGRALEC, štirka), če je igre konec in je zmagal RDECI_IGRALEC z dano zmagovalno štirko.
           (RUMENI_IGRALEC, štirka), če je igre konec in je zmagal RUMENI_IGRALEC z dano zmagovalno štirko.
           (NEODLOCENO, None), če je igre konec in je neodločeno.
           (NI_KONEC, None), če igre še ni konec'''

        for j in Igra.stirke:
            ((i1,j1),(i2,j2),(i3,j3),(i4,j4)) = j
            p = self.plosca[i1][j1]
            if p != PRAZNO and p == self.plosca[i2][j2] == self.plosca[i3][j3] == self.plosca[i4][j4]:
            # zmagovalna štirka
                return (p, [j[0], j[1], j[2], j[3]])
        # Ni zmagovalca, preverimo, ali je konec igre
        for i in range(7):
            if self.plosca[0][i] is PRAZNO:
                # Našli smo prazno mesto v prvi vrstici, igre ni konec
                return (NI_KONEC, None)
        # Vsa polja so polna, rezultat je neodločen
        return (NEODLOCENO, None)
