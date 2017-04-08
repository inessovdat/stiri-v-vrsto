from tkinter import *
from igra import *
from clovek import *

class Gui():
    TAG_FIGURA = 'figura'

    TAG_OKVIR = 'okvir'

    VELIKOST_POLJA = 70

    POLMER_KROGCA = VELIKOST_POLJA // 2 - 2

    ODMIK = 2

    def __init__(self, master):
        self.rdeci_igralec = None
        self.rumeni_igralec = None

        master.protocol("WM_DELETE_WINDOW", lambda: self.zapri_okno(master))

        self.plosca = Canvas(master, width = 7 * Gui.VELIKOST_POLJA + Gui.ODMIK, height = 6 * Gui.VELIKOST_POLJA + Gui.ODMIK, bg = 'blue')
        self.plosca.grid(row=1, column=0)
        self.plosca.bind("<Button-1>", self.plosca_klik)
        self.narisi_krogce()
        self.narisi_stiri()
        self.igra = Igra()
        self.napis = StringVar(master, value="Dobrodošli v 4 v vrsto!")

        # self.sporocilo = StringVar(
        #     master,
        #     value='Dobrodosli! Kliknite na Nova igra, da pricnete z igro.')
        # self.sporocevalec = Label(
        #     master,
        #     textvariable = self.sporocilo)
        # self.sporocevalec.grid(row=0, columnspan = 2)


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
        self.plosca.delete(Gui.TAG_FIGURA)
        #self.prekini_igralce()
        # Nastavimo igralce
        self.rdeci_igralec = Clovek(self)
        self.rumeni_igralec = Clovek(self)
        # Ustvarimo novo igro
        #self.igra = Igra()
        # Rdeči je prvi na potezi
        self.napis.set("Na potezi je rdeči igralec.")
        self.rdeci_igralec.igraj()

    def koncaj_igro(self):
        if zmagovalec == RDECI_IGRALEC:
            self.napis.set("Zmagal je rdeči igralec.")
            self.narisi_zmagovalno_trojico(zmagovalec, trojka)
        elif zmagovalec == RUMENI_IGRALEC:
            self.napis.set("Zmagal je rumen igralec.")
            self.narisi_stiri(zmagovalec, stirka)
        else:
            self.napis.set("Neodločeno.")

    def zapri_okno(self, master):
        # TO DO
        master.destroy()

    def narisi_krogce(self):
        for i in range(7):
           for j in range(6):
               self.plosca.create_oval(2 * Gui.ODMIK + i * Gui.VELIKOST_POLJA, 2 * Gui.ODMIK + j * Gui.VELIKOST_POLJA,
                                       (i+1) * Gui.VELIKOST_POLJA, (j+1) * Gui.VELIKOST_POLJA, fill = 'black')

    def narisi_stiri(self, stirka, zmagovalec):
        barva = 'red' if zmagovalec == 'RD' else 'yellow'
        for p in stirka:
            (vrstica, stolpec) = p
            y = vrstica * Gui.VELIKOST_POLJA
            x = stolpec * Gui.VELIKOST_POLJA
            z = Gui.ODMIK
            self.plosca.create_oval(x + z, y + z, x + Gui.VELIKOST_POLJA + z, y + Gui.VELIKOST_POLJA + z, width = 2 * Gui.ODMIK, fill = barva)



    def plosca_klik(self, event):
        stolpec = (event.x - Gui.ODMIK) // Gui.VELIKOST_POLJA
        sredisce_stolpec = stolpec * Gui.VELIKOST_POLJA + Gui.VELIKOST_POLJA // 2 + Gui.ODMIK
        barva = 'gold' if self.igra.na_potezi == RUMENI_IGRALEC else 'tomato'
        vrstica = self.igra.naredi_potezo(stolpec)
        if vrstica != None:
            sredisce_vrstica = vrstica * Gui.VELIKOST_POLJA + Gui.VELIKOST_POLJA // 2 + Gui.ODMIK
            self.plosca.create_oval(sredisce_stolpec - Gui.POLMER_KROGCA, sredisce_vrstica - Gui.POLMER_KROGCA,
                                    sredisce_stolpec + Gui.POLMER_KROGCA, sredisce_vrstica + Gui.POLMER_KROGCA, fill = barva)
            if self.igra.na_potezi == 'RU':
                self.napis.set('Na potezi je rumeni igralec.')
            else:
                self.napis.set('Na potezi je rdeči igralec.')


    def povleci_potezo(self, p):
        """Povleci potezo p, Äe je veljavna. Äe ni veljavna, ne naredi niÄ."""
        # Najprej povleÄemo potezo v igri, ĹĄe pred tem si zapomnimo, kdo jo je povlekel
        # (ker bo self.igra.povleci_potezo spremenil stanje igre).
        # GUI se *ne* ukvarja z logiko igre, zato ne preverja, ali je poteza veljavna.
        # Ta del za njega opravi self.igra.
        igralec = self.igra.na_potezi
        r = self.igra.povleci_potezo(p)
        if r is None:
            # Poteza ni bila veljavna, nič se ni spremenilo
            pass
        else:
            # Poteza je bila veljavna, nariĹĄemo jo na zaslon
            if igralec == RDECI_IGRALEC:
                self.narisi_stiri(p)
            elif igralec == RUMENI_IGRALEC:
                self.narisi_stiri(p)
            # Ugotovimo, kako nadaljevati
            (zmagovalec, stirka) = r
            if zmagovalec == NI_KONEC:
                # Igra se nadaljuje
                if self.igra.na_potezi == RDECI_IGRALEC:
                    self.napis.set("Na potezi je rdeči igralec.")
                    self.rdeci_igralec.igraj()
                elif self.igra.na_potezi == RUMENI_IGRALEC:
                    self.napis.set("Na potezi je rumeni igralec.")
                    self.rumeni_igralec.igraj()
            else:
                # Igre je konec, koncaj
                self.koncaj_igro(zmagovalec, stirka)


if __name__ == "__main__":
    root = Tk()
    root.title("Stiri v vrsto")
    aplikacija = Gui(root)
    root.mainloop()
