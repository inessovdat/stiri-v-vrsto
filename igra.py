RDECI_IGRALEC = 'RD'
RUMENI_IGRALEC = 'RU'
PRAZNO = ""
NI_KONEC = "ni konec igre"
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
        pozicija = [self.plosca[i][:] for i in range(6)]
        self.zgodovina.append((pozicija, self.na_potezi))

    def kopija(self):
        kopirano = Igra()
        kopirano.plosca = [self.plosca[i][:] for i in range(6)]
        kopirano.na_potezi = self.na_potezi
        return kopirano

    def razveljavi(self):
        (self.plosca, self.na_potezi) = self.zgodovina.pop()

    def veljavne_poteze(self):
        mozne_poteze = []
        for i in range (7):
            if self.plosca[0][i] == PRAZNO:
                mozne_poteze.append(i)
        return mozne_poteze

    def vrni_vrstico(self, p):
        if p not in self.veljavne_poteze():
            return None
        elif self.na_potezi == None:
            return None
        else:
            a = 5
            while a >= 0 and self.plosca[a][p] != PRAZNO:
                a -= 1
            return a

    def shrani_poteze(self, p):
        if p not in self.veljavne_poteze():
            return None
        elif self.na_potezi == None:
            return None
        else:
            self.shrani_pozicijo()
            a = 5
            while a >= 0 and self.plosca[a][p] != PRAZNO:
                a -= 1
            self.plosca[a][p] = self.na_potezi
            (zmagovalec, stirka) = self.preveri_konec_igre()
            if zmagovalec == NI_KONEC:
                # Igre ni konec, zdaj je na potezi nasprotnik
                self.na_potezi = nasprotnik(self.na_potezi)
            else:
                # Igre je konec
                self.na_potezi = None
            return (zmagovalec, stirka)


    stirke =[
        #vrstice
            [((i,0), (i,1), (i,2), (i,3)) for i in range(6)],
            [((i,1), (i,2), (i,3), (i,4)) for i in range(6)],
            [((i,2), (i,3), (i,4), (i,5)) for i in range(6)],
            [((i,3), (i,4), (i,5), (i,6)) for i in range(6)],
        #stolpci
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



    def preveri_konec_igre(self):
        '''(RDECI_IGRALEC, stirka) če je igre konec in je zmagal RDECI_IGRALEC z dano zmagovalno štirko.
           (RUMENI_IGRALEC, stirka) če je igre konec in je zmagal RUMENI_IGRALEC z dano zmagovalno štirko.
           (NEODLOCENO, None), če je igre konec in je neodločeno.
           (NI_KONEC, None), če igre še ni konec'''

        for stirka in Igra.stirke:
            for j in stirka:
                ((i1,j1),(i2,j2),(i3,j3),(i4,j4)) = j
                p = self.plosca[i1][j1]
                if p != PRAZNO and p == self.plosca[i2][j2] == self.plosca[i3][j3] == self.plosca[i4][j4]:
                # zmagovalna štirka
                    print((p, [j[0], j[1], j[2], j[3]]))
                    return (p, [j[0], j[1], j[2], j[3]])
        # Ni zmagovalca, ali je igre konec?
        for i in range(7):
            if self.plosca[0][i] is PRAZNO:
                # Našli smo prazno plosca, igre ni konec
                return (NI_KONEC, None)
        # Vsa polja so polna, rezultat je neodločen
        return (NEODLOCENO, None)