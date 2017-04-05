RDECI_IGRALEC = 'RD'
RUMENI_IGRALEC = 'RU'
PRAZNO = ""

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

    def zamenjaj_igralca(self):
        self.na_potezi = nasprotnik(self.na_potezi)

    def shrani_pozicijo(self):
        pozicija = [self.plosca[i][:] for i in range(6)]
        self.zgodovina.append((pozicija, self.na_potezi))

    def kopija(self):
        kopirano = Igra()
        kopirano.plosca = [self.plosca[i][:] for i in range(6)]
        kopirano.na_potezi = self.na_potezi
        return kopirano

    #def razveljavi(self):
        #(self.plosca, self.na_potezi) = self.zgodovina.pop()

    def veljavne_poteze(self):
        mozne_poteze = []
        for i in range (7):
            if self.plosca[0][i] == PRAZNO:
                mozne_poteze.append(i)
        return mozne_poteze

    def naredi_potezo(self, p):
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
            print(self.plosca)
            self.zamenjaj_igralca()
            return a

    def preveri_konec_igre(self):
        stirke =[
        #vrstice
            [((i,0), (i,1), (i,2), (i,3)) for i in range(6)] +
            [((i,1), (i,2), (i,3), (i,4)) for i in range(6)] +
            [((i,2), (i,3), (i,4), (i,5)) for i in range(6)] +
            [((i,3), (i,4), (i,5), (i,6)) for i in range(6)] +
        #stolpci
            [((0,j), (1,j), (2,j), (3,j)) for j in range(7)] +
            [((1,j), (2,j), (3,j), (4,j)) for j in range(7)] +
            [((2,j), (3,j), (4,j), (5,j)) for j in range(7)] +
        #diagonale /
            [((0,j), (1,j-1), (2,j-2),(3,j-3))for j in range(3,7)] +
            [((1,j), (2,j-1), (3,j-2),(4,j-3))for j in range(3,7)] +
            [((2,j), (3,j-1), (4,j-2),(5,j-3))for j in range(3,7)] +
        #diagonale \
            [((0,j), (1,j+1), (2,j+2),(3,j+3))for j in range(4)] +
            [((1,j), (2,j+1), (3,j+2),(4,j+3))for j in range(4)] +
            [((2,j), (3,j+1), (4,j+2),(5,j+3))for j in range(4)]]