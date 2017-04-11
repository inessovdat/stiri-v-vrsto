from tkinter import *
from igra import *
from clovek import *
from racunalnik import *
import argparse
import logging

MINIMAX_GLOBINA = 3

class Gui():
    TAG_FIGURA = 'figura'

    TAG_OKVIR = 'okvir'

    VELIKOST_POLJA = 70

    # Odmik od roba polja
    ODMIK = 2
    
    def __init__(self, master, globina):
        self.rdeci_igralec = None
        self.rumeni_igralec = None
        self.igra = None

        master.protocol("WM_DELETE_WINDOW", lambda: self.zapri_okno(master))

        # Igralna plošča
        self.plosca = Canvas(master, width = 7 * Gui.VELIKOST_POLJA + Gui.ODMIK, height = 6 * Gui.VELIKOST_POLJA + 2 * Gui.ODMIK, bg = 'blue')#barva roba
        self.plosca.grid(row=1, column=0)
        self.plosca.bind("<Button-1>", self.plosca_klik)
        self.narisi_igralno_plosco()

        # Napis ob začetku igre
        self.napis = StringVar(master, value="Dobrodošli v 4 v vrsto!")#zakaj ne dela
        Label(master, textvariable = self.napis).grid(row=0, column=0)

        # Glavni menu
        menu = Menu(master)
        master.config(menu=menu)

        # Podmenu
        menu_igra = Menu(menu, tearoff = 0)
        menu.add_cascade(label="Igra", menu=menu_igra)
        #menu_igra.add_command(label = "Nova igra", command = self.zacni_igro)
        menu_igra.add_command(label="Rdeči=Človek, Rumeni=Človek",
                              command=lambda: self.zacni_igro(Clovek(self), Clovek(self)))
        menu_igra.add_command(label="Rdeči=Človek, Rumeni=Računalnik",
                              command=lambda: self.zacni_igro(Clovek(self), Racunalnik(self, Minimax(globina))))
        menu_igra.add_command(label="Rdeči=Računalnik, Rumeni=Človek",
                              command=lambda: self.zacni_igro(Racunalnik(self, Minimax(globina)), Clovek(self)))
        menu_igra.add_command(label="Rdeči=Računalnik, Rumeni=Računalnik",
                              command=lambda: self.zacni_igro(Racunalnik(self, Minimax(globina)), Racunalnik(self, Minimax(globina))))

        self.zacni_igro(Clovek(self), Racunalnik(self, Minimax(globina)))

    def zacni_igro(self, rdeci_igralec, rumeni_igralec):
        ''' Stanje igre nastavi na začetek.'''
        # Ustavimo vsa vlakna, ki trenutno razmišljajo
        self.prekini_igralce()
        self.plosca.delete(Gui.TAG_FIGURA)
         # Ustvarimo novo igro
        self.igra = Igra()
        # Nastavimo igralce
        self.rdeci_igralec = rdeci_igralec
        self.rumeni_igralec = rumeni_igralec
        # Rdeči igralec je prvi na potezi
        self.napis.set("Na potezi je rdeči igralec.")
        self.rdeci_igralec.igraj()

    def koncaj_igro(self, zmagovalec, stirka):
         ''' Stanje igre nastavi na konec. '''
         if zmagovalec == RDECI_IGRALEC:
            self.napis.set("Zmagal je rdeči igralec.")
            self.narisi_zmagovalne_stiri(zmagovalec, stirka)
         elif zmagovalec == RUMENI_IGRALEC:
            self.napis.set("Zmagal je rumeni igralec.")
            self.narisi_zmagovalne_stiri(zmagovalec, stirka)
         else:
            self.napis.set("Neodločeno.")

    def prekini_igralce(self):
        ''' Pove igralcem naj nehajo z razmišljanjem. '''
        logging.debug ("prekinjam igralce")
        if self.rdeci_igralec: self.rdeci_igralec.prekini()
        if self.rumeni_igralec: self.rumeni_igralec.prekini()


    def zapri_okno(self, master):
        ''' Ko uporabnik zapre aplikacijo, ta metoda zapre okno.'''
        self.prekini_igralce()
        master.destroy()

    def narisi_igralno_plosco(self):
        ''' Nariše igralno ploščo.'''
        for i in range(7):
           for j in range(6):
               self.plosca.create_oval(2 * Gui.ODMIK + i * Gui.VELIKOST_POLJA, 2 * Gui.ODMIK + j * Gui.VELIKOST_POLJA,
                                       (i+1) * Gui.VELIKOST_POLJA, (j+1) * Gui.VELIKOST_POLJA, fill = 'black', tag = Gui.TAG_OKVIR)

    def narisi_krogec(self, stolpec, vrstica, barva):
        '''Na ustrezno mesto nariše krogec ustrezne barve.'''
        self.plosca.create_oval(stolpec * Gui.VELIKOST_POLJA + 2 * Gui.ODMIK, (vrstica) * Gui.VELIKOST_POLJA + 2 * Gui.ODMIK,
                                (stolpec + 1)* Gui.VELIKOST_POLJA, (vrstica + 1) * Gui.VELIKOST_POLJA, fill = barva, tag = Gui.TAG_FIGURA)

    def narisi_zmagovalne_stiri(self, zmagovalec, stirka):
        '''S temnejšo barvo obarva in obrobi zmagovalno štirko.'''
        barva = 'red' if zmagovalec == RDECI_IGRALEC else 'yellow'
        for p in stirka:
            (vrstica, stolpec) = p
            y = vrstica * Gui.VELIKOST_POLJA
            x = stolpec * Gui.VELIKOST_POLJA
            z = Gui.ODMIK
            self.plosca.create_oval(x + z, y + z, x + Gui.VELIKOST_POLJA + z, y + Gui.VELIKOST_POLJA + z, width = 2 * Gui.ODMIK, fill = barva, tag = Gui.TAG_FIGURA)

    def plosca_klik(self, event):
        '''Izvede se ob kliku na ploščo. '''
        stolpec = (event.x - Gui.ODMIK) // Gui.VELIKOST_POLJA
        #if vrstica != None:
           # if 0<=vrstica<=5 and 0<=stolpec<=6:
        if self.igra.na_potezi == RDECI_IGRALEC or self.igra.na_potezi == RUMENI_IGRALEC:
            self.povleci_potezo(stolpec)
        else:
            # Nihče ni na potezi, ne naredimo nič
            pass
        #else:
            # Neveljavna poteza
          #  pass

    def povleci_potezo(self, stolpec):
        igralec = self.igra.na_potezi
        vrstica = self.igra.vrni_vrstico(stolpec)
        r = self.igra.shrani_poteze(stolpec)
        if r is None:
            # Neveljavna poteza, nič se ne spremeni
            pass
        else:
            # Veljavna poteza znotraj igralne plošče
            if vrstica != None:
                # Na zaslon narišemo krogec ustrezne barve
                if igralec == RDECI_IGRALEC:
                    self.narisi_krogec(stolpec, vrstica, 'brown1')
                else:
                    self.narisi_krogec(stolpec, vrstica, 'Darkgoldenrod1')
                # Igre še ni konec
                (zmagovalec, stirka) = r
                if zmagovalec == NI_KONEC:
                    # Izvede se naslednja poteza in zamenja napis
                    if self.igra.na_potezi == RDECI_IGRALEC:
                        self.napis.set('Na potezi je rdeči igralec.')
                        self.rdeci_igralec.igraj()
                    elif self.igra.na_potezi == RUMENI_IGRALEC:
                        self.napis.set('Na potezi je rumeni igralec.')
                        self.rumeni_igralec.igraj()
                else:
                    # Igre je konec
                    self.koncaj_igro(zmagovalec, stirka)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Igrica štiri v vrsto")
    parser.add_argument('--globina',
                        default=MINIMAX_GLOBINA,
                        type=int,
                        help='globina iskanja za minimax algoritem')
    parser.add_argument('--debug',
                        action='store_true',
                        help='vklopi sporočila o dogajanju')
    args = parser.parse_args()
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    root = Tk()
    root.title("Stiri v vrsto")
    aplikacija = Gui(root, args.globina)
    root.mainloop()
