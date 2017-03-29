RDECI_IGRALEC = 'rdeci'
RUMENI_IGRALEC = 'rumeni'
PRAZNO = "."

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
        self.plosca = [[PRAZNO for i in range(1,8)] for j in range(1,7)]             
        self.zgodovina = []
        

    def naredi_potezo(self, p):
        self.na_potezi = nasprotnik(self.na_potezi)

    def shrani_pozicijo(self):
        pozicija = [self.plosca[i][:] for i in range(1, 8)]
        self.zgodovina.append((pozicija, self.na_potezi))

    def kopija(self):
        kopirano = Igra()
        kopirano.plosca = [self.plosca[i][:] for i in range(1, 8)]
        kopirano.na_potezi = self.na_potezi
        return kopirano
    
    def razveljavi(self):
        (self.plosca, self.na_potezi) = self.zgodovina.pop()

    def veljavne_poteze(self):
        poteze = []
        #TO DO
        return poteze
