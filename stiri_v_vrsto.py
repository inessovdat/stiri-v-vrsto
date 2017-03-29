from tkinter import *
from igra import *

class Gui():
    TAG_FIGURA = 'figura'

    TAG_OKVIR = 'okvir'

    VELIKOST_POLJA = 50

    POLMER_KROGCA = VELIKOST_POLJA // 2 - 2

    ODMIK = 2

    def __init__(self, master):
        master.protocol("WM_DELETE_WINDOW", lambda: self.zapri_okno(master))

        self.plosca = Canvas(master, width= 7 * Gui.VELIKOST_POLJA + Gui.ODMIK, height= 6 * Gui.VELIKOST_POLJA + Gui.ODMIK)
        self.plosca.pack()
        self.narisi_crte()
        self.plosca.bind("<Button-1>", self.plosca_klik)

        self.igra = Igra()

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

    def koncaj_igro(self):
        self.napis.set("Konec igre.")

    def zapri_okno(self, master):
        # TO DO
        master.destroy()

    def narisi_crte(self):
        """Nariši črte v igralnem polju"""
        self.plosca.delete(Gui.TAG_OKVIR)
        d = Gui.VELIKOST_POLJA
        r = Gui.ODMIK
        for vrstica in range(0,7):
            self.plosca.create_line(r , r + vrstica*d ,r + 7*d,r + vrstica*d, tag=Gui.TAG_OKVIR)
        for stolpec in range(0,8):
            self.plosca.create_line(r + stolpec * d, r,r + stolpec*d,r + 6*d, tag=Gui.TAG_OKVIR)

    def plosca_klik(self, event):
        stolpec = (event.x - Gui.ODMIK) // Gui.VELIKOST_POLJA
        vrstica = (event.y - Gui.ODMIK) // Gui.VELIKOST_POLJA
        sredisce_stolpec = stolpec * Gui.VELIKOST_POLJA + Gui.VELIKOST_POLJA // 2 + Gui.ODMIK
        #spremeniti vrstico
        sredisce_vrstica = vrstica * Gui.VELIKOST_POLJA + Gui.VELIKOST_POLJA // 2 + Gui.ODMIK
        barva = 'yellow' if self.igra.na_potezi == RUMENI_IGRALEC else 'red'
        self.plosca.create_oval(sredisce_stolpec - Gui.POLMER_KROGCA, sredisce_vrstica - Gui.POLMER_KROGCA, sredisce_stolpec + Gui.POLMER_KROGCA, sredisce_vrstica + Gui.POLMER_KROGCA, fill = barva)

    #def povleci_potezo():


if __name__ == "__main__":
    root = Tk()
    root.title("Stiri v vrsto")
    aplikacija = Gui(root)
    root.mainloop()