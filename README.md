## Štiri v vrsto

Projekt pri predmetu Programiranje 2

Štiri v vrsto je igra za dva igralca (oba ali eden od njiju je lahko tudi raèunalnik). Namen igre je postaviti štiri žetone v zaporedna polja(vertikalno, horizontalno ali diagonalno) preden to stori nasprotnik.

#Pravila igre:

- igro zaène igralec z rdeèimi žetoni
- vsak igralec vstavi po en žeton v katerikoli stolpec (žeton zasede najnižje mesto v danem stolpcu)
- igra se izmenièno, dokler eden od igralcev ne postavi štiri žetone v zaporedna polja
- zmaga tisti, ki uspe prvi postaviti štiri žetone v zaporedna polja

#Struktura igre: 

Igra je sestavljena iz veè datotek:

- stiri_v_vrsto.py:
To je uporabniški vmesnik, ki nariše igralno plošèo in vsebuje funkcije za izrisovanje krogcev na zaslon. Igralcu omogoèi izbiro med razliènimi kombinacijami igralcev (oba igralca sta èloveka, oba raèunalnik ali èlovek igra proti raèunalniku) in razlièno težavnostjo igre.  Zaèetna izbira ob prvem zagonu programa je èlovek proti raèunalniku z najveèjo težavnostjo(raèunalnik skoraj nepremagljiv). Ko igralec klikne na plošèo, na najnižje možno mesto v stolpcu pade krogec ustrezne barve. Igralec zmaga, ko ima v štirih zaporednih 	poljih svoje krogce. Zmagovalni krogci se pobarvajo z bolj živo barvo in obrobijo z belo.

- igra.py:
To je logika igre. Igralna plošèa je predstavljena z matriko velikosti 6x7, v kateri so shranjeni krogci na plošèi( 'RU' : èe se na danem mestu nahaja krogec rumene barve, 'RD' : èe se na danem mestu nahaja krogec rdeèe barve in '' : èe se na danem mestu ne nahaja noben krogec). Logika igre tudi menja igralca in preverja veljavnost poteze.

- clovek.py:
Ta datoteka sprejema klike èloveka kot igralca.

- minimax.py
V tej datoteki se nahaja funkcija minimax, ki po principu minimax ugotovi naboljšo potezo, ki jo lahko odigra raèunalnik.
Cenilka ima najveèjo vrednost v poljih, kjer je v okolici najveè žetonov ustrezne barve (najveè 4 – to pomeni zmago) in pada z manjšanjem žetonov. Poleg tega, koliko žetonov je v okolici, upošteva še število žetonov na plošèi, torej je cenilka takšna, da poteze, kjer raèunalnik zmaga takoj, ko je možno, oceni boljše.

- alfabeta.py
V tej datoteki se nahaja funkcija alfa-beta, ki po principu alfa-beta rezanja ugotovi naboljšo potezo, ki jo lahko odigra raèunalnik. Cenilka je takšna kot pri minimax metodi.

- racunalnik.py
Ta datoteka predstavlja raèunalnik kot igralca in uporablja metodo minimax ali alfabeta za igranje raèunalnika. 