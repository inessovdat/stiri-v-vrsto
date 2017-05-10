# �tiri v vrsto

Projekt pri predmetu Programiranje 2

�tiri v vrsto je igra za dva igralca (oba ali eden od njiju je lahko tudi ra�unalnik). Namen igre je postaviti �tiri �etone v zaporedna polja (vertikalno, horizontalno ali diagonalno), preden to stori nasprotnik.

## Pravila igre:

- igro za�ne rde�i igralec
- vsak igralec vstavi po en krogec v katerikoli stolpec (krogec zasede najni�je mesto v danem stolpcu)
- igra se izmeni�no, dokler eden od igralcev ne postavi �tiri krogce v zaporedna polja
- zmaga tisti, ki uspe prvi postaviti �tiri krogce v zaporedna polja

## Struktura igre: 

Igra je sestavljena iz ve� datotek:

- `stiri_v_vrsto.py`:
To je uporabni�ki vmesnik, ki nari�e igralno plo��o in izrisuje krogce na zaslon. Igralcu omogo�i izbiro med razli�nimi kombinacijami igralcev (oba igralca sta �loveka, �lovek igra proti ra�unalniku ali ra�unalnik proti ra�unalniku) in razli�no te�avnostjo igre. Za�etna izbira ob prvem zagonu programa je nastavljena na �lovek proti ra�unalniku z najve�jo te�avnostjo (ra�unalnik skoraj nepremagljiv). Ko igralec klikne na plo��o, na najni�je mo�no mesto v stolpcu pade krogec ustrezne barve. Igralec zmaga, ko ima v �tirih zaporednih poljih svoje krogce. Zmagovalni krogci se obrobijo belo in pobarvajo z bolj �ivo barvo.

- `igra.py`:
To je logika igre. Igralna plo��a je predstavljena z matriko velikosti 6x7, v kateri so shranjeni krogci na plo��i ('RU' : �e se na danem mestu nahaja krogec rumene barve, 'RD' : �e se na danem mestu nahaja krogec rde�e barve in '' : �e se na danem mestu ne nahaja noben krogec). Logika igre shranjuje pozicijo krogcev, izmenjuje igralca in preverja veljavnost poteze.

- `clovek.py`:
Ta datoteka sprejema klike �loveka kot igralca.

- `minimax.py`:
V tej datoteki se nahaja funkcija minimax, ki po principu minimax ugotovi nabolj�o potezo, ki jo lahko odigra ra�unalnik, tako da za prvega igralca izbira poteze z maksimalno, za drugega pa z minimalno vrednostjo. �e ima ve� potez enako vrednost, minimax naklju�no izbere eno izmed njih, torej ra�unalnik v enakih okoli��inah ne odigra vedno isto, saj bi sicer igra postala predvidljiva.
Cenilka ima najve�jo vrednost v poljih, kjer je v okolici najve� �etonov ustrezne barve (najve� 4 � to pomeni zmago) in pada z manj�anjem �etonov. Poleg tega, koliko �etonov je v okolici, upo�teva �e �tevilo �etonov na plo��i, torej je cenilka tak�na, da poteze, kjer ra�unalnik zmaga takoj, ko je mo�no, oceni bolj�e. 

- `alfabeta.py`:
V tej datoteki se nahaja funkcija alfa-beta, ki po principu alfa-beta rezanja ugotovi nabolj�o potezo, ki jo lahko odigra ra�unalnik, tako da poteze s slab�o vrednostjo od vrednosti alfa oz. beta presko�i. Ker algoritem izra�una najbolj�o potezo hitreje kot metoda minimax, lahko ra�una na ve�ji globini, ne da bi za to porabila ve� �asa. Cenilka je tak�na kot pri minimax metodi.

- `racunalnik.py`:
Ta datoteka predstavlja ra�unalnik kot igralca in uporablja metodo minimax ali alfabeta za igranje ra�unalnika. 


### [Na�rt dela](./Na�rt_dela.md)