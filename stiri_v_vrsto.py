from tkinter import *
from igra import *
from clovek import *
from racunalnik import *
import argparse
import logging

ALFABETA_GLOBINA = 4

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

        # Animacija padanja krogcev
        self.animacija_v_teku = False
        self.animacija_trenutna_vrstica = 0
        self.animacija_koncna_vrstica = 0
        self.animacija_stolpec = 0
        self.animacija_barva = ""
        self.animacija_id = None
        self.animacija_zmagovalec = None

        master.protocol("WM_DELETE_WINDOW", lambda: self.zapri_okno(master))

        # Igralna plošča
        self.plosca = Canvas(master, width = 7 * Gui.VELIKOST_POLJA + 4 * Gui.ODMIK, height = 6 * Gui.VELIKOST_POLJA + 4 * Gui.ODMIK, bg = 'blue')
        self.plosca.grid(row=1, column=0)
        
        self.narisi_igralno_plosco()

        # Napis ob začetku igre
        self.napis = StringVar(master, value = "Dobrodošli v 4 v vrsto!")
        Label(master, textvariable = self.napis).grid(row=0, column=0)

        # Glavni menu
        menu = Menu(master)
        master.config(menu=menu)

        # Podmenu
        menu_igra = Menu(menu, tearoff = 0)
        menu.add_cascade(label="Igra", menu=menu_igra)
        menu_igra.add_command(label="Človek : Človek",
                              command=lambda: self.zacni_igro(Clovek(self), Clovek(self)))
        menu_igra.add_command(label="Rdeči=Človek : Rumeni=Računalnik",
                              command=lambda: self.zacni_igro(Clovek(self), Racunalnik(self, AlfaBeta(globina))))
        menu_igra.add_command(label="Rdeči=Računalnik : Rumeni=Človek",
                              command=lambda: self.zacni_igro(Racunalnik(self, AlfaBeta(globina)), Clovek(self)))
        menu_igra.add_command(label="Računalnik : Računalnik",
                              command=lambda: self.zacni_igro(Racunalnik(self, AlfaBeta(globina)), Racunalnik(self, AlfaBeta(globina))))
        
        # Z zamikom začne igro človek(rdeči) proti računalniku(rumeni)
        self.plosca.after(1000,
                          lambda:
                          self.zacni_igro(Clovek(self), Racunalnik(self, AlfaBeta(globina))))

    def zacni_igro(self, rdeci_igralec, rumeni_igralec):
        '''Stanje igre nastavi na začetek.'''
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
        self.plosca.bind("<Button-1>", self.plosca_klik)
        self.rdeci_igralec.igraj()

    def koncaj_igro(self, zmagovalec, stirka):
         '''Preveri kdo je zmagal, ustrezno spremeni napis in nariše zmagovalno štirko.'''
         # Zmagal je rdeči
         if zmagovalec == RDECI_IGRALEC:
            self.napis.set("Zmagal je rdeči igralec.")
            self.narisi_zmagovalne_stiri(zmagovalec, stirka)
        # Zmagal je rumeni
         elif zmagovalec == RUMENI_IGRALEC:
            self.napis.set("Zmagal je rumeni igralec.")
            self.narisi_zmagovalne_stiri(zmagovalec, stirka)
        # Igra je neodločena
         else:
            self.napis.set("Neodločeno.")

    def prekini_igralce(self):
        '''Pove igralcem naj nehajo z razmišljanjem.'''
        logging.debug ("prekinjam igralce")
        if self.rdeci_igralec: self.rdeci_igralec.prekini()
        if self.rumeni_igralec: self.rumeni_igralec.prekini()


    def zapri_okno(self, master):
        '''Ko uporabnik zapre aplikacijo, ta metoda zapre okno.'''
        self.prekini_igralce()
        master.destroy()

    def narisi_igralno_plosco(self):
        '''Nariše igralno ploščo.'''
        for i in range(7):
           for j in range(7):
               self.plosca.create_oval(koordinate_krogca(i, j), fill = 'black', tag = Gui.TAG_OKVIR)

    def narisi_krogec(self, stolpec, vrstica, barva):
        '''Na ustrezno mesto spusti krogec ustrezne barve.'''
        self.animacija_v_teku = True
        self.animacija_koncna_vrstica = vrstica
        self.animacija_stolpec = stolpec
        self.animacija_barva = barva
        self.animacija_id = self.plosca.create_oval(koordinate_krogca(self.animacija_trenutna_vrstica, stolpec), fill = self.animacija_barva, tag = Gui.TAG_FIGURA)
        
        self.animiraj_krogec()

    def animiraj_krogec(self):
        '''Animira padanje krogca.'''
        stolpec = self.animacija_stolpec
        vrstica = self.animacija_koncna_vrstica

        # Animira krogec
        if self.animacija_trenutna_vrstica < vrstica:
            self.plosca.coords(self.animacija_id, koordinate_krogca(self.animacija_trenutna_vrstica, stolpec))
            self.animacija_trenutna_vrstica += 1
            self.plosca.after(150,self.animiraj_krogec)

        # Konca animacijo krogca
        else:
            self.plosca.coords(self.animacija_id, koordinate_krogca(vrstica, stolpec))
            # Ponastavi spremenljivke
            self.animacija_v_teku = False
            self.animacija_trenutna_vrstica = 0
            self.animacija_id = None
            # Preveri, če je konec igre
            r = self.animacija_zmagovalec
            (zmagovalec, stirka) = r
            # Igre ni konec
            if zmagovalec == NI_KONEC:
                # Izvede se naslednja poteza in zamenja napis
                if self.igra.na_potezi == RDECI_IGRALEC:
                    self.napis.set('Na potezi je rdeči igralec.')
                    self.rdeci_igralec.igraj()
                elif self.igra.na_potezi == RUMENI_IGRALEC:
                    self.napis.set('Na potezi je rumeni igralec.')
                    self.rumeni_igralec.igraj()
            # Igre je konec
            else:
                self.koncaj_igro(zmagovalec, stirka)

    def plosca_klik(self, event):
        '''Izvede se ob kliku na ploščo. '''
        stolpec = (event.x - Gui.ODMIK) // Gui.VELIKOST_POLJA
        # Preveri, če poteka animacija
        if self.animacija_v_teku:
            # Če poteka, ne sprejema klikov
            return
        # Če animacija ne poteka, obdela klik
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
        vrstica = self.igra.vrni_vrstico(stolpec)
        r = self.igra.povleci_potezo(stolpec)
        self.animacija_zmagovalec = r
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

    def narisi_zmagovalne_stiri(self, zmagovalec, stirka):
        '''Z bolj živo barvo obarva in z belo obrobi zmagovalno štirko.'''
        barva = 'red' if zmagovalec == RDECI_IGRALEC else 'yellow'
        for p in stirka:
            (vrstica, stolpec) = p
            self.plosca.create_oval(koordinate_krogca(vrstica, stolpec), width = 2 * Gui.ODMIK, fill = barva, outline = 'white', tag = Gui.TAG_FIGURA)

def koordinate_krogca(vrstica, stolpec):
    '''Iz vrstice in stolpca izračuna koordinate krogca na plošči.'''
    odmik = Gui.ODMIK
    polje = Gui.VELIKOST_POLJA
    return 5 * odmik + stolpec * polje, 5 * odmik + vrstica * polje, (stolpec + 1) * polje, (vrstica + 1) * polje

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Igrica štiri v vrsto")
    parser.add_argument('--globina',
                        default=ALFABETA_GLOBINA,
                        type=int,
                        help='globina iskanja za alfabeta algoritem')
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

