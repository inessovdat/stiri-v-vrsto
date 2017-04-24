from tkinter import *
from igra import *
from clovek import *
from racunalnik import *
import argparse
import logging

MINIMAX_GLOBINA = 4

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

        # Za animacijo
        self.anim_id = None # ID krogca, ki pada, None, ce ne animiramo
        self.anim_stolpec = None
        self.anim_vrstica = None # ko je to celo število, pomeni, da animiramo in da je krogec v tej vrstici
        self.anim_koncna = None # vrstica, do katere mora priti padajoci krogec
        self.anim_stanje = None # Sem spravimo podatek o tem, kaj se mora zgoditi, ko je animacije konec

        master.protocol("WM_DELETE_WINDOW", lambda: self.zapri_okno(master))

        # Igralna plošča
        self.plosca = Canvas(master, width = 7 * Gui.VELIKOST_POLJA + 4 * Gui.ODMIK, height = 6 * Gui.VELIKOST_POLJA + 4 * Gui.ODMIK, bg = 'blue')
        self.plosca.grid(row=1, column=0)
        self.plosca.bind("<Button-1>", self.plosca_klik)
        self.narisi_igralno_plosco()

        # Napis ob začetku igre
        self.napis = StringVar(master, value = "Dobrodošli v 4 v vrsto!")#zakaj ne dela
        Label(master, textvariable = self.napis).grid(row=0, column=0)

        # Glavni menu
        menu = Menu(master)
        master.config(menu=menu)

        # Podmenu
        menu_igra = Menu(menu, tearoff = 0)
        menu.add_cascade(label="Igra", menu=menu_igra)
        menu_igra.add_command(label="Rdeči=Človek, Rumeni=Človek",
                              command=lambda: self.zacni_igro(Clovek(self), Clovek(self)))
        menu_igra.add_command(label="Rdeči=Človek, Rumeni=Računalnik",
                              command=lambda: self.zacni_igro(Clovek(self), Racunalnik(self, Minimax(globina))))
        menu_igra.add_command(label="Rdeči=Računalnik, Rumeni=Človek",
                              command=lambda: self.zacni_igro(Racunalnik(self, Minimax(globina)), Clovek(self)))
        menu_igra.add_command(label="Rdeči=Računalnik, Rumeni=Računalnik",
                              command=lambda: self.zacni_igro(Racunalnik(self, Minimax(globina)), Racunalnik(self, Minimax(globina))))

        self.plosca.after(1000,
                          lambda:
                          self.zacni_igro(Clovek(self), Racunalnik(self, Minimax(globina))))

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
               odmik = Gui.ODMIK
               polje = Gui.VELIKOST_POLJA
               self.plosca.create_oval(5 * odmik + i * polje, 5 * odmik + j * polje, (i+1) * polje, (j+1) * polje, fill = 'black', tag = Gui.TAG_OKVIR)

    def narisi_zmagovalne_stiri(self, zmagovalec, stirka):
        '''S temnejšo barvo obarva in obrobi zmagovalno štirko.'''
        barva = 'red' if zmagovalec == RDECI_IGRALEC else 'yellow'
        for p in stirka:
            (vrstica, stolpec) = p
            odmik = Gui.ODMIK
            polje = Gui.VELIKOST_POLJA
            y = vrstica * polje
            x = stolpec * polje
            self.plosca.create_oval(x + 5 * odmik, y + 5 * odmik, x + polje, y + polje, width = 2 * odmik, fill = barva, outline = 'white', tag = Gui.TAG_FIGURA)

    def plosca_klik(self, event):
        '''Izvede se ob kliku na ploščo. '''
        stolpec = (event.x - Gui.ODMIK) // Gui.VELIKOST_POLJA
        if self.igra.na_potezi == RDECI_IGRALEC:
            logging.debug("plosca_klik: rdeci igralec {0}".format(stolpec))
            self.rdeci_igralec.klik(stolpec)
        elif self.igra.na_potezi == RUMENI_IGRALEC:
            logging.debug("plosca_klik: rdeci igralec {0}".format(stolpec))
            self.rumeni_igralec.klik(stolpec)
        else:
            # Nihče ni na potezi, ne naredimo nič
            logging.debug("plosca_klik: ignoriramo klik")
            pass

    def povleci_potezo(self, stolpec):
        '''Spremeni napis trenutnega igralca in nariše krogec.'''
        igralec = self.igra.na_potezi
        self.anim_stanje = self.igra.shrani_poteze(stolpec)
        if self.anim_stanje is None:
            # Neveljavna poteza, nič se ne spremeni
            pass
        else:
            # Veljavna poteza znotraj igralne plošče
            self.anim_stolpec = stolpec
            self.anim_vrstica = 0
            self.anim_koncna = self.igra.vrni_vrstico(stolpec)
            odmik = Gui.ODMIK
            polje = Gui.VELIKOST_POLJA
            barva = ('brown1' if igralec == RDECI_IGRALEC else 'Darkgoldenrod1')
            self.anim_id = self.plosca.create_oval(self.anim_stolpec * polje + 5 * odmik,
                                                       (self.anim_vrstica) * polje + 5 * odmik,
                                                       (self.anim_stolpec + 1) * polje ,
                                                       (self.anim_vrstica + 1) * polje,
                                                       fill = barva, tag = Gui.TAG_FIGURA)
            self.plosca.after(200, self.spusti_krogec)

    def spusti_krogec(self):
        if self.anim_vrstica <= self.anim_koncna:
            # padamo
            self.anim_vrstica += 1
            odmik = Gui.ODMIK
            polje = Gui.VELIKOST_POLJA
            self.plosca.coords(self.anim_id,
                              self.anim_stolpec * polje + 5 * odmik,
                                                       (self.anim_vrstica) * polje + 5 * odmik,
                                                       (self.anim_stolpec + 1) * polje ,
                                                       (self.anim_vrstica + 1) * polje)
            self.plosca.after(200, self.spusti_krogec)
        else:
            # smo prisli do konca
            (zmagovalec, stirka) = self.anim_stanje
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
