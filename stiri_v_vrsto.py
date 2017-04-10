from tkinter import *
from igra import *
from clovek import *
import argparse
import logging

class Gui():
    TAG_FIGURA = 'figura'

    TAG_OKVIR = 'okvir'

    VELIKOST_POLJA = 70

    # Odmik od roba polja
    ODMIK = 2

    POLMER_KROGCA = VELIKOST_POLJA // 2 - 2


    def __init__(self, master):
        self.rdeci_igralec = None
        self.rumeni_igralec = None

        master.protocol("WM_DELETE_WINDOW", lambda: self.zapri_okno(master))

        # Igralna plošča
        self.plosca = Canvas(master, width = 7 * Gui.VELIKOST_POLJA + Gui.ODMIK, height = 6 * Gui.VELIKOST_POLJA + Gui.ODMIK, bg = 'blue')
        self.plosca.grid(row=1, column=0)
        self.plosca.bind("<Button-1>", self.plosca_klik)
        self.narisi_igralno_plosco()

        self.igra = Igra()

        # Napis ob začetku igre
        self.napis = StringVar(master, value="Dobrodošli v 4 v vrsto!")
        self.w = Label(master, textvariable = self.napis)
        self.w.grid(row=0, column=0)

        # Glavni menu
        menu = Menu(master)
        master.config(menu=menu)

        # Podmenu
        menu_igra = Menu(menu, tearoff = 0)
        menu.add_cascade(label="Igra", menu=menu_igra)
        menu_igra.add_command(label = "Nova igra", command = self.zacni_igro)

        self.zacni_igro()


    def zacni_igro(self):
        ''' Stanje igre nastavi na začetek.'''
        # Ustavimo vsa vlakna, ki trenutno razmišljajo
        self.prekini_igralce()
        self.plosca.delete(Gui.TAG_FIGURA)
         # Ustvarimo novo igro
        self.igra = Igra()
        # Nastavimo igralce
        self.rdeci_igralec = Clovek(self)
        self.rumeni_igralec = Clovek(self)
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

    def narisi_krogec(self, p, barva):
        '''Na ustrezno mesto nariše krogec ustrezne barve.'''
        (stolpec, sredisce_stolpec, vrstica) = p
        sredisce_vrstica = vrstica * Gui.VELIKOST_POLJA + Gui.VELIKOST_POLJA // 2 + Gui.ODMIK
        self.plosca.create_oval(sredisce_stolpec - Gui.POLMER_KROGCA, sredisce_vrstica - Gui.POLMER_KROGCA,
                                        sredisce_stolpec + Gui.POLMER_KROGCA, sredisce_vrstica + Gui.POLMER_KROGCA, fill = barva, tag = Gui.TAG_FIGURA)

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
        sredisce_stolpec = stolpec * Gui.VELIKOST_POLJA + Gui.VELIKOST_POLJA // 2 + Gui.ODMIK
        vrstica = self.igra.vrni_vrstico(stolpec)
        if self.igra.na_potezi == RDECI_IGRALEC or self.igra.na_potezi == RUMENI_IGRALEC:
            self.povleci_potezo((stolpec, sredisce_stolpec, vrstica))
        else:
            pass

    def povleci_potezo(self, p):
        (stolpec, sredisce_stolpec,vrstica) = p
        igralec = self.igra.na_potezi
        r = self.igra.shrani_poteze(stolpec)
        (zmagovalec, stirka) = r
        if r is None:
            # Neveljavna poteza, nič se ne spremeni
            pass
        else:
            # Veljavna poteza znotraj igralne plošče
            if vrstica != None:
                # Na zaslon narišemo krogec ustrezne barve
                if igralec == RDECI_IGRALEC:
                    self.narisi_krogec(p, 'tomato')
                else:
                    self.narisi_krogec(p, 'gold')
                # Igre še ni konec
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
    parser = argparse.ArgumentParser(description="Igrica stiri v vrsto")
    parser.add_argument('--debug',
                        action='store_true',
                        help='vklopi sporoÄila o dogajanju')
    args = parser.parse_args()
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    root = Tk()
    root.title("Stiri v vrsto")
    aplikacija = Gui(root)
    root.mainloop()
