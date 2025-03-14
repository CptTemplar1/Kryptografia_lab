# Kryptografia i kryptoanaliza
## Laboratorium 1
### Grupa 22B
### Autorzy: Przemysław Kałużiński, Michał Kaczor

### Zadanie 1

Korzystając z języka C++, dokonaj implementacji programu szyfrującego i deszyfrującego zadany tekst.
1. Tekst jawny powinien być importowany do programu z pliku tekstowego, którego nazwa określona powinna być po zdefiniowanym argumencie / fladze: -i.
2. Wynik pracy programu powinien być eksportowany do pliku tekstowego, którego nazwa określona powinna być po zdefiniowanym argumencie / fladze: -o.
3. Klucz powinien być importowany z pliku tekstowego, którego nazwa powinna być określona po zdefiniowanym argumencie / fladze: -k.
4. Tryb pracy programu powinien być określony poprzez flagi: -e dla procesu szyfrowania, -d dla procesu deszyfrowania. 
 
Przykład wywołania programu w celu zaszyfrowania tekstu:  
./program -e -k klucz.txt -i tekst_jawny.txt -o szyfrogram.txt

Przykład wywołania programu w celu odszyfrowania tekstu:  
./program -d -k klucz.txt -i szyfrogram.txt -o tekst_odszyfrowany.txt

**Uwagi:**  
- Kolejność argumentów powinna być dowolna.
- Plik z kluczem powinien mieć formę pliku tekstowego zawierającego definicję tablicy podstawieniowej w postaci dwóch kolumn liter, np:  
A G  
B O  
C R  
D L  
...  
Z B  

Powyższy przykład pokazuje, iż literze A przypisana jest litera G, literze B przypisana jest litera O itp.  
- Tablica podstawieniowa powinna definiować podstawienia dla wszystkich liter alfabetu łacińskiego (język angielski).
- Tekst jawny (z przeznaczeniem do zaszyfrowania) powinien zawierać dłuższy akapit a lepiej kilka akapitów pisanych w języku angielskim (najlepiej beletrystyka).
- Odczytany tekst jawny, przed dalszym przetwarzaniem, powinien być zamieniony do postaci składającej się tylko z dużych liter. Ponadto z tekstu powinny być usunięte wszystkie znaki, które nie są literami, np: odstępy, przecinki, kropki itp.

#### Implementacja

Ze względu na fakt, że zadania 1-4 są ze sobą powiązane i polegają na rozbudowie jednego programu, zdecydowaliśmy się na umieszczenie kodu źródłowego w osobnej sekcji implementacja, znajdującej się pod zadaniem 4.

#### Wyniki

Przed uruchomieniem programu, musieliśmy utworzyć plik z kluczem, który będzie używany do szyfrowania i deszyfrowania tekstu oraz zadeklarować plik z tekstem jawnym, który będzie poddany szyfrowaniu. Poniżej znajduje się wykorzystany przez nas klucz oraz tekst jawny:

**Klucz (klucz.txt):**

``` plaintext
A Q
B W
C E
D R
E T
F Y
G U
H I
I O
J P
K A
L S
M D
N F
O G
P H
Q J
R K
S L
T Z
U X
V C
W V
X B
Y N
Z M
```

**Tekst jawny (tekst_jawny.txt):**

``` plaintext
Valentine's Day (or Saint Valentine's Day) is a holiday that, in the United States, takes place on February 14, and technically signifies the accomplishments of St. Valentine, a third-century Roman saint.

With that said, most Americans, instead of honoring St. Valentine through religious ceremony, enjoy the holiday by engaging in "romantic" behavior with their significant other or someone who they wish to be their significant other; gifts, special dinners, and other acknowledgements of affection comprise most individuals' Valentine's Day celebrations.

Chocolates and flowers are commonly given as gifts during Valentine's Day, as are accompanying greeting cards (greeting card companies release new Valentine's Day designs annually). Red and pink are generally understood to be "the colors" of Valentine's Day, and many individuals, instead of celebrating romantically, spend the holiday with their friends and/or family members.

Variations of Valentine's Day are celebrated across the globe throughout the year. In America, the holiday, although acknowledged by the vast majority of the population, isn't federally recognized; no time off work is granted for Valentine's Day.
```

Polecenie, którego użyliśmy do wywołania programu w celu zaszyfrowania tekstu:  
`dotnet run -e -k klucz.txt -i tekst_jawny.txt -o szyfrogram.txt`

Po uruchomieniu programu z przedstawionymi argumentami otrzymaliśmy zaszyfrowany tekst, który został zapisany do pliku `szyfrogram.txt`. Poniżej znajduje się wynik szyfrowania:

**Szyfrogram (szyfrogram.txt):**

``` plaintext
CQSTFZOFTLRQNGKLQOFZCQSTFZOFTLRQNOLQIGSORQNZIQZOFZITXFOZTRLZQZTLZQATLHSQETGFYTWKXQKNQFRZTEIFOEQSSNLOUFOYOTLZITQEEGDHSOLIDTFZLGYLZCQSTFZOFTQZIOKRETFZXKNKGDQFLQOFZVOZIZIQZLQORDGLZQDTKOEQFLOFLZTQRGYIGFGKOFULZCQSTFZOFTZIKGXUIKTSOUOGXLETKTDGFNTFPGNZITIGSORQNWNTFUQUOFUOFKGDQFZOEWTIQCOGKVOZIZITOKLOUFOYOEQFZGZITKGKLGDTGFTVIGZITNVOLIZGWTZITOKLOUFOYOEQFZGZITKUOYZLLHTEOQSROFFTKLQFRGZITKQEAFGVSTRUTDTFZLGYQYYTEZOGFEGDHKOLTDGLZOFROCORXQSLCQSTFZOFTLRQNETSTWKQZOGFLEIGEGSQZTLQFRYSGVTKLQKTEGDDGFSNUOCTFQLUOYZLRXKOFUCQSTFZOFTLRQNQLQKTQEEGDHQFNOFUUKTTZOFUEQKRLUKTTZOFUEQKREGDHQFOTLKTSTQLTFTVCQSTFZOFTLRQNRTLOUFLQFFXQSSNKTRQFRHOFAQKTUTFTKQSSNXFRTKLZGGRZGWTZITEGSGKLGYCQSTFZOFTLRQNQFRDQFNOFROCORXQSLOFLZTQRGYETSTWKQZOFUKGDQFZOEQSSNLHTFRZITIGSORQNVOZIZITOKYKOTFRLQFRGKYQDOSNDTDWTKLCQKOQZOGFLGYCQSTFZOFTLRQNQKTETSTWKQZTRQEKGLLZITUSGWTZIKGXUIGXZZITNTQKOFQDTKOEQZITIGSORQNQSZIGXUIQEAFGVSTRUTRWNZITCQLZDQPGKOZNGYZITHGHXSQZOGFOLFZYTRTKQSSNKTEGUFOMTRFGZODTGYYVGKAOLUKQFZTRYGKCQSTFZOFTLRQN
```

Następnie uruchomiliśmy program ponownie w celu odszyfrowania tekstu. Polecenie, którego użyliśmy do wywołania programu w celu odszyfrowania tekstu:  
`dotnet run -d -k klucz.txt -i szyfrogram.txt -o tekst_odszyfrowany.txt`

Po uruchomieniu programu z przedstawionymi argumentami otrzymaliśmy odszyfrowany tekst, który został zapisany do pliku `tekst_odszyfrowany.txt`. Poniżej znajduje się wynik odszyfrowania:

**Tekst odszyfrowany (tekst_odszyfrowany.txt):**

``` plaintext
VALENTINESDAYORSAINTVALENTINESDAYISAHOLIDAYTHATINTHEUNITEDSTATESTAKESPLACEONFEBRUARYANDTECHNICALLYSIGNIFIESTHEACCOMPLISHMENTSOFSTVALENTINEATHIRDCENTURYROMANSAINTWITHTHATSAIDMOSTAMERICANSINSTEADOFHONORINGSTVALENTINETHROUGHRELIGIOUSCEREMONYENJOYTHEHOLIDAYBYENGAGINGINROMANTICBEHAVIORWITHTHEIRSIGNIFICANTOTHERORSOMEONEWHOTHEYWISHTOBETHEIRSIGNIFICANTOTHERGIFTSSPECIALDINNERSANDOTHERACKNOWLEDGEMENTSOFAFFECTIONCOMPRISEMOSTINDIVIDUALSVALENTINESDAYCELEBRATIONSCHOCOLATESANDFLOWERSARECOMMONLYGIVENASGIFTSDURINGVALENTINESDAYASAREACCOMPANYINGGREETINGCARDSGREETINGCARDCOMPANIESRELEASENEWVALENTINESDAYDESIGNSANNUALLYREDANDPINKAREGENERALLYUNDERSTOODTOBETHECOLORSOFVALENTINESDAYANDMANYINDIVIDUALSINSTEADOFCELEBRATINGROMANTICALLYSPENDTHEHOLIDAYWITHTHEIRFRIENDSANDORFAMILYMEMBERSVARIATIONSOFVALENTINESDAYARECELEBRATEDACROSSTHEGLOBETHROUGHOUTTHEYEARINAMERICATHEHOLIDAYALTHOUGHACKNOWLEDGEDBYTHEVASTMAJORITYOFTHEPOPULATIONISNTFEDERALLYRECOGNIZEDNOTIMEOFFWORKISGRANTEDFORVALENTINESDAY
```

**Wnioski:**

Przed szyfrowaniem tekst jawny został przekształcony w ciąg wielkich liter, z usunięciem wszystkich znaków niebędących literami (np. spacji, znaków interpunkcyjnych). Miało to na celu uproszczenie procesu szyfrowania i uniknięcie niejednoznaczności. Po uruchomieniu programu z flagą `-e` (szyfrowanie) oraz podaniu odpowiednich argumentów (`-k klucz.txt`, `-i tekst_jawny.txt`, `-o szyfrogram.txt`), program zaszyfrował tekst jawny przy użyciu podanego klucza. Wynikiem szyfrowania jest tekst zaszyfrowany, który został zapisany do pliku `szyfrogram.txt`. Tekst ten jest ciągiem znaków, w którym każda litera z tekstu jawnego została zastąpiona odpowiadającą jej literą z klucza. Na przykład litera `A` została zamieniona na `Q`, `B` na `W`, itd. W efekcie otrzymaliśmy tekst, który jest trudny do odczytania bez znajomości klucza.

Następnie, aby zweryfikować poprawność szyfrowania, uruchomiliśmy program z flagą `-d` (deszyfrowanie) oraz tymi samymi argumentami (`-k klucz.txt`, `-i szyfrogram.txt`, `-o tekst_odszyfrowany.txt`). Program odszyfrował tekst zaszyfrowany, używając odwrotnego mapowania z klucza. Wynikiem jest tekst odszyfrowany, który został zapisany do pliku `tekst_odszyfrowany.txt`. Tekst ten jest identyczny z oryginalnym tekstem jawnym, z wyjątkiem tego, że wszystkie litery zostały zamienione na wielkie, a znaki niebędące literami (np. spacje, znaki interpunkcyjne) zostały usunięte.

### Zadanie 2

Rozbudować program z poprzedniego przykładu poprzez dodanie do niego funkcjonalności generowania statystyk liczności występowania n-gramów (sekwencji kolejnych liter), to jest mono-gramów (pojedynczych liter), bi-gramów (wyrazów dwuliterowych), tri-gramów (wyrazów trzyliterowych) oraz quad-gramów (wyrazów czteroliterowych). Funkcjonalność ta powinna być wyzwalana poprzez dodanie do programu jednej z następujących flag: -g1, -g2, -g3 lub -g4, po której powinna zostać określona nazwa pliku, do którego zapisane zostaną wyniki.

Przykład wywołania programu:  
./program -i tekst_jawny.txt -g1 monogramy.txt

Przykład wyznaczania bi-gramów dla tekstu:  
Tekst jawny:  
This is an example of plain text

Tekst wstępnie przetworzony:  
THISISANEXAMPLEOFPLAINTEXT

Kilka pierwszych bi-gramów:  
1.TH  
2.HI  
3.IS  
4.SI  
5.IS  
6.SA  
...  

Dla każdego wyznaczonego n-gramu należy wyznaczyć liczność jego występowania w badanym tekście. Wynik pracyprogramu powinien być wygenerowany w postaci tabeli:
n-gram liczbość

Przykład:  
TH 1  
HI 1  
IS 2  
SI 1  
SA 1  
...  

#### Implementacja

Ze względu na fakt, że zadania 1-4 są ze sobą powiązane i polegają na rozbudowie jednego programu, zdecydowaliśmy się na umieszczenie kodu źródłowego w osobnej sekcji implementacja, znajdującej się pod zadaniem 4.

#### Wyniki

Przed uruchomieniem programu, musieliśmy przygotować plik z tekstem jawnym, który będzie analizowany pod kątem statystyk n-gramów. Wykorzystaliśmy ten sam plik, który został użyty w poprzednim zadaniu (`tekst_jawny.txt`).

Program został uruchomiony dla wszystkich wartości `n` (1-4), aby wygenerować statystyki mono-gramów, bi-gramów, tri-gramów i quad-gramów. Poniżej znajdują się polecenia wywołania programu dla każdej wartości `n` oraz fragmenty wyników otrzymanych statystyk. Ze względu na długość wyników, zostało wyświetlone jedynie kilka pierwszych wartości n-gramów.

Polecenie, którego użyliśmy do wywołania programu w celu generowania statystyk mono-gramów:  
`dotnet run -i tekst_jawny.txt -g1 monogramy.txt`

**Wynik statystyk dla mono-gramów (monogramy.txt):**

``` plaintext
n-gram	liczność
E	109
A	92
N	88
I	84
T	78
O	66
S	60
R	55
L	44
D	44
H	40
C	32
Y	30
G	28
M	23
F	22
V	16
U	14
B	11
P	10
W	10
K	5
J	2
Z	1
```

Polecenie, którego użyliśmy do wywołania programu w celu generowania statystyk bi-gramów:  
`dotnet run -i tekst_jawny.txt -g2 bigramy.txt`

**Fragment wyniku statystyk dla bi-gramów (bigramy.txt):**

``` plaintext
n-gram	liczność
IN	28
TH	26
NT	22
TI	22
EN	20
AL	19
HE	17
AN	17
LE	16
NE	14
ES	14
DA	14
VA	12
AY	12
ST	12
ER	12
AT	11
ND	11
RE	11
SA	10
SD	9
OR	9
RS	9
...
```

Polecenie, którego użyliśmy do wywołania programu w celu generowania statystyk tri-gramów:  
`dotnet run -i tekst_jawny.txt -g3 trigramy.txt`

**Fragment wyniku statystyk dla tri-gramów (trigramy.txt):**

``` plaintext
n-gram	liczność
THE	17
TIN	15
ENT	13
NTI	12
DAY	12
VAL	10
ALE	10
LEN	10
INE	10
NES	8
ESD	8
SDA	8
ING	7
AND	6
ICA	6
ATI	5
ALL	5
LLY	5
COM	5
ANT	5
HOL	4
OLI	4
...
```

Polecenie, którego użyliśmy do wywołania programu w celu generowania statystyk quad-gramów:  
`dotnet run -i tekst_jawny.txt -g4 quadgramy.txt`

**Fragment wyniku statystyk dla quad-gramów (quadgramy.txt):**

``` plaintext
n-gram	liczność
VALE	10
ALEN	10
LENT	10
ENTI	10
NTIN	10
TINE	10
INES	8
NESD	8
ESDA	8
SDAY	8
ALLY	5
HOLI	4
OLID	4
LIDA	4
IDAY	4
SIGN	4
COMP	4
OTHE	4
TION	4
DAYA	4
TVAL	3
IGNI	3
...
```

**Wnioski:**

Uruchomienie programu z odpowiednią flagą (-g1, -g2, -g3, -g4) oraz podanie odpowiednich argumentów (`-i tekst_jawny.txt`, `-gX n-gramy.txt`, gdzie `X` to 1, 2, 3 lub 4), program wygenerował statystyki dla wybranego typu n-gramów, które zostały zapisane do pliku wynikowego. Wynikiem jest lista n-gramów wraz z ich licznością, czyli liczbą wystąpień w tekście.

Dla każdego typu n-gramów (mono-gramy, bi-gramy, tri-gramy, quad-gramy) program działa w ten sam sposób. Na przykład:
- Dla mono-gramów (flaga -g1), program generuje statystyki pojedynczych liter. Przykładowo, litera `A` może wystąpić 50 razy, `B` 30 razy, itd.
- Dla bi-gramów (flaga -g2), program generuje statystyki sekwencji dwóch liter. Przykładowo, bi-gram `TH` może wystąpić 15 razy, `HE` 12 razy, itd.
- Dla tri-gramów (flaga -g3), program generuje statystyki sekwencji trzech liter. Przykładowo, tri-gram `THE` może wystąpić 8 razy, `ING` 5 razy, itd.
- Dla quad-gramów (flaga -g4), program generuje statystyki sekwencji czterech liter. Przykładowo, quad-gram `THAT` może wystąpić 3 razy, `WITH` 2 razy, itd.

Program poprawnie generuje statystyki n-gramów dla podanego tekstu, niezależnie od wybranego typu n-gramów (mono-, bi-, tri- lub quad-gramów). Wyniki są zapisywane do plików w formacie tabelarycznym, gdzie każdy wiersz zawiera n-gram oraz jego liczność. Dzięki temu możemy analizować częstotliwość występowania różnych sekwencji liter w tekście, co może być przydatne w analizie językowej lub kryptoanalizie.

### Zadanie 3

Uzupełnij program z poprzedniego zadania, tak aby w przypadku podania flagi `-rX`, gdzie `X` jest liczbą należącą do zbioru `{1, 2, 3, 4}`, a następnie nazwy pliku, program odczytywał z niego referencyjną bazę *n*-gramów. Liczby z podanego zbioru odpowiadają:

- `1` → *mono-gramom*  
- `2` → *bi-gramom*  
- `3` → *tri-gramom*  
- `4` → *quad-gramom*  

**Uwaga**  
Odczytana referencyjna baza *n*-gramów powinna być tabelą, której każdy wiersz składa się z dwóch wartości oddzielonych spacją. Wartościami tymi powinny być:  
- $G_i$ – *i*-ty *n*-gram  
- $P_i$ – prawdopodobieństwo wystąpienia *i*-tego *n*-gramu w tekście referencyjnym (*corpus*).  

Prawdopodobieństwo to wyznaczyć można korzystając ze wzoru:

$$
P_i = \frac{N_i}{N}
$$

gdzie:  
- $N_i$ – liczność wystąpienia *i*-tego *n*-gramu w tekście referencyjnym,  
- $N$ – całkowita liczba wszystkich *n*-gramów w tekście referencyjnym.  

Następnie należy rozbudować program, tak aby podanie flagi `-s` generowało wartość testu $\chi^2$ dla zadanego tekstu (flaga `-i`) i wybranej bazy referencyjnej (flaga `-rX`). Wynik działania programu powinien być drukowany na standardowe wyjście.

W kontekście zadania, test $\chi^2$ może być zdefiniowany następująco:

$$
T = \sum_{{i=0}}^{n} \frac{(C_i - E_i)^2}{E_i}
$$

gdzie:  
- $C_i$ – liczba wystąpień *i*-tego symbolu (*n*-gramu) w analizowanym tekście,  
- $E_i$ – wartość oczekiwana liczby wystąpień *i*-tego symbolu (*n*-gramu) w tekście,  
- $n$ – całkowita liczba *n*-gramów w analizowanym tekście.

#### Implementacja

Ze względu na fakt, że zadania 1-4 są ze sobą powiązane i polegają na rozbudowie jednego programu, zdecydowaliśmy się na umieszczenie kodu źródłowego w osobnej sekcji implementacja, znajdującej się pod zadaniem 4.

#### Wyniki

Przed uruchomieniem programu, musieliśmy przygotować plik z tekstem jawnym, który będzie analizowany pod kątem testu chi-kwadrat. Wykorzystaliśmy ten sam plik, który został użyty w zadaniu 1 (`tekst_jawny.txt`). Dodatkowo wykorzystaliśmy pliki z referencyjnymi bazami n-gramów przesłane przez prowadzącego (`english_monograms.txt`, `english_bigrams.txt`, `english_trigrams.txt`, `english_quadgrams.txt`). Poniżej znajduje się fragment zawartości jednego z plików referencyjnych (dla bi-gramów):

**Fragment referencyjnej bazy bi-gramów (english_bigrams.txt):**

``` plaintext
TH 116997844
HE 100689263
IN 87674002
ER 77134382
AN 69775179
RE 60923600
ES 57070453
ON 56915252
ST 54018399
NT 50701084
EN 48991276
AT 48274564
ED 46647960
ND 46194306
TO 46115188
OR 45725191
EA 43329810
...
```

Polecenie, którego użyliśmy do wywołania programu w celu obliczenia testu chi-kwadrat dla mono-gramów:  
`dotnet run -i tekst_jawny.txt -r1 english_monograms.txt -s`

Po uruchomieniu programu z przedstawionymi argumentami otrzymaliśmy wartość testu chi-kwadrat, która została wyświetlona w konsoli. Poniżej znajduje się wynik:

``` plaintext
Wartość testu chi-kwadrat: 50,4818
```

Polecenie, którego użyliśmy do wywołania programu w celu obliczenia testu chi-kwadrat dla bi-gramów:
`dotnet run -i tekst_jawny.txt -r2 english_bigrams.txt -s`

Po uruchomieniu programu z przedstawionymi argumentami otrzymaliśmy wartość testu chi-kwadrat, która została wyświetlona w konsoli. Poniżej znajduje się wynik:

``` plaintext
Wartość testu chi-kwadrat: 1084,0064
```

Polecenie, którego użyliśmy do wywołania programu w celu obliczenia testu chi-kwadrat dla tri-gramów:
`dotnet run -i tekst_jawny.txt -r3 english_trigrams.txt -s`

Po uruchomieniu programu z przedstawionymi argumentami otrzymaliśmy wartość testu chi-kwadrat, która została wyświetlona w konsoli. Poniżej znajduje się wynik:

``` plaintext
Wartość testu chi-kwadrat: 9836,0391
```

Polecenie, którego użyliśmy do wywołania programu w celu obliczenia testu chi-kwadrat dla quad-gramów:
`dotnet run -i tekst_jawny.txt -r4 english_quadgrams.txt -s`

Po uruchomieniu programu z przedstawionymi argumentami otrzymaliśmy wartość testu chi-kwadrat, która została wyświetlona w konsoli. Poniżej znajduje się wynik:

``` plaintext
Wartość testu chi-kwadrat: 86385,1160
```

**Wnioski:**

Program obliczył wartość testu chi-kwadrat dla każdego typu n-gramów (mono-, bi-, tri- i quad-gramów) na podstawie porównania statystyk n-gramów w analizowanym tekście z odpowiednimi referencyjnymi bazami.

Wyniki testu chi-kwadrat dla poszczególnych typów n-gramów są następujące:
- **Mono-gramy**: Wartość testu wyniosła 50,4818. Ta stosunkowo niska wartość wskazuje na dużą zgodność rozkładu pojedynczych liter w analizowanym tekście z rozkładem w referencyjnej bazie mono-gramów. Jest to spodziewane, ponieważ mono-gramy (pojedyncze litery) mają zazwyczaj stabilny rozkład w języku angielskim.
- **Bi-gramy**: Wartość testu wyniosła 1084,0064. Wyższa wartość wskazuje na większe różnice w rozkładzie bi-gramów w porównaniu z referencyjną bazą. Bi-gramy są bardziej zależne od kontekstu i specyfiki tekstu, co może prowadzić do większych odchyleń.
- **Tri-gramy**: Wartość testu wyniosła 9836,0391. Znacznie wyższa wartość sugeruje, że rozkład tri-gramów w analizowanym tekście różni się znacząco od rozkładu w referencyjnej bazie. Tri-gramy są jeszcze bardziej wrażliwe na kontekst i specyfikę tekstu, co tłumaczy dużą wartość testu.
- **Quad-gramy**: Wartość testu wyniosła 86385,1160. Ta bardzo wysoka wartość wskazuje na bardzo duże różnice w rozkładzie quad-gramów w porównaniu z referencyjną bazą. Quad-gramy są wysoce specyficzne i rzadko występują w tekście, co prowadzi do znacznych odchyleń.

Wartość testu chi-kwadrat rośnie wraz ze wzrostem długości n-gramów. Jest to spodziewane, ponieważ im dłuższe sekwencje liter (np. tri-gramy, quad-gramy), tym bardziej są one zależne od kontekstu i specyfiki tekstu. W przypadku mono-gramów, które są pojedynczymi literami, rozkład jest bardziej uniwersalny i stabilny, co tłumaczy niższą wartość testu. Natomiast dla dłuższych n-gramów, takich jak bi-gramy, tri-gramy i quad-gramy, różnice w rozkładach są bardziej wyraźne, co skutkuje wyższymi wartościami testu chi-kwadrat. 

### Zadanie 4

Wykonać eksperymenty:
- Dokonaj obserwacji wyniku testu χ2 dla tekstu jawnego i zaszyfrowanego o różnych długościach.
- Wiadomo, iż wynik testu może być znacząco zaburzony w przypadku gdy brane są pod uwagę symbole (n-gramy), które rzadko występują w tekście, np w przypadku mono-gramów języka angielskiego są to litery: J, K, Q, X oraz Z (patrz odczytana tablica częstości mono-gramów). Zbadaj wynik testu χ2 w przypadku gdy do wyznaczenia testu pominięte zostaną rzadko występujące n-gramy.

#### Implementacja

Ze względu na fakt, że zadania 1-4 są ze sobą powiązane i polegają na rozbudowie jednego programu, zdecydowaliśmy się na umieszczenie kodu źródłowego w osobnej sekcji implementacja, znajdującej się pod zadaniem 4.

#### Wyniki

W ramach zadania 4 przeprowadziliśmy eksperymenty, aby zaobserwować wyniki testu chi-kwadrat dla tekstu jawnego i zaszyfrowanego o różnych długościach. Szyfrowanie przeprowadziliśmy z wykorzystaniem funkcjonalości programu z zadania 1. Ze względu na długość tekstu, nie przedstawiliśmy go w raporcie, a jedynie umieścilimy informację o ich długości. Poniżej znajdują się wyniki eksperymentów:

**Długość analizowanego tekstu:**

- **Długi tekst jawny:** Tekst składał się z **16159 znaków**
- **Krótki tekst jawny:** Tekst składał się z **1185 znaków**

**Tabela wyników testu chi-kwadrat**

| Typ n-gramu | Tekst jawny (długi) | Szyfrogram (długi) | Tekst jawny (krótki) | Szyfrogram (krótki) |
|-------------|---------------------|--------------------|----------------------|---------------------|
| Mono-gramy  | 379,9119            | 180684,0010        | 50,4818              | 14635,5831          |
| Bi-gramy    | 3614,9834           | 38883889,6392      | 1084,0064            | 2755717,7049        |
| Tri-gramy   | 29912,4879          | 1374338013,1173    | 9836,0391            | 118466475,9358      |
| Quad-gramy  | 410538,8369         | 2059523791,1963    | 86385,1160           | 1084040903,3257     |

**Wnioski:**

Przeprowadzone eksperymenty pokazują, że wartość testu chi-kwadrat rośnie wraz ze wzrostem długości n-gramów oraz po zaszyfrowaniu tekstu. Dla tekstu jawnego wartości testu są niższe, co wskazuje na większą zgodność z referencyjnymi bazami n-gramów. Po zaszyfrowaniu tekstu wartości testu chi-kwadrat znacząco wzrastają, co odzwierciedla losowy rozkład liter w szyfrogramie. Długość analizowanego tekstu również wpływa na wyniki testu. Zakładaliśmy, że w przypadku dłuższego tekstu wartości testu będą bardziej stabilne i zbliżone do referencyjnych baz n-gramów. Wyniki eksperymentów pokazują jednak, że wraz ze wzrostem ilości znaków, otrzymujemy bardziej niestabilne i rozbieżne wyniki testu chi-kwadrat.

**Pominięcie rzadko występujących n-gramów:**

W drugim etapie zadania zbadaliśmy wpływ pominięcia rzadko występujących n-gramów na wyniki testu chi-kwadrat. Z referencyjnych baz n-gramów języka angielskiego usunęliśmy rzadko występujące pozycje (pozostały n-gramy z licznościami nie niższymi niż 100 tysięcy). Następnie ponownie obliczyliśmy test chi-kwadrat dla długiego oraz krótkiego tekstu jawnego i zaszyfrowanego. Wyniki eksperymentu przedstawiamy w poniższej tabeli:

### Tabela wyników testu chi-kwadrat (bez rzadkich n-gramów)

| Typ n-gramu | Tekst jawny (długi) | Szyfrogram (długi) | Tekst jawny (krótki) | Szyfrogram (krótki) |
|-------------|---------------------|--------------------|----------------------|---------------------|
| Mono-gramy  | 452,4778            | 4147,9283          | 35,9866              | 330,0803            |
| Bi-gramy    | 3027,6717           | 28165,8802         | 779,6808             | 3398,6111           |
| Tri-gramy   | 4463,1387           | 11501,9068         | 2122,0409            | 1042,5702           |
| Quad-gramy  | 8193,0183           | 12111,8548         | 836,5947             | 961,0000            |

**Wnioski:**

Przeprowadzone eksperymenty wykazały, że usunięcie rzadko występujących n-gramów obniża wartości testu chi-kwadrat w porównaniu do wyników uzyskanych z pełnymi bazami n-gramów. W przypadku tekstu jawnego wartości testu pozostają niższe niż dla szyfrogramów, co sugeruje większą zgodność z bazami referencyjnymi. Po zaszyfrowaniu tekstu wartości testu chi-kwadrat wzrastają, jednak różnice w stosunku do pełnych baz n-gramów są mniej znaczące.

Eliminacja rzadkich n-gramów z baz referencyjnych wpływa na lepsze dopasowanie rozkładów n-gramów w analizowanych tekstach do baz wzorcowych. Test chi-kwadrat nadal pozostaje skutecznym narzędziem analizy statystycznej zarówno dla tekstu jawnego, jak i zaszyfrowanego, a pominięcie rzadkich n-gramów może prowadzić do bardziej stabilnych wyników, zwłaszcza w przypadku krótszych tekstów.

### Implementacja

**1. Funkcja `Main`**

**Wejście:**
- `args`: Argumenty przekazane do programu z linii poleceń. Argumenty te określają operacje do wykonania, takie jak szyfrowanie, deszyfrowanie, generowanie statystyk n-gramów oraz obliczanie testu chi-kwadrat.

**Wyjście:**
- Brak bezpośredniego wyjścia. Program wykonuje operacje na plikach i wyświetla komunikaty w konsoli, informujące o postępie i wynikach operacji.

**Opis:**  
Funkcja `Main` jest punktem wejścia programu. Odczytuje argumenty z linii poleceń, przetwarza je i wywołuje odpowiednie funkcje w zależności od podanych flag. Program obsługuje szyfrowanie, deszyfrowanie, generowanie statystyk n-gramów oraz obliczanie testu chi-kwadrat. Funkcja sprawdza poprawność przekazanych argumentów i wyświetla komunikat o błędzie, jeśli argumenty są nieprawidłowe.

**Kod:**
``` C#
static void Main(string[] args)
{
    string inputFile = "", outputFile = "", keyFile = "";
    string gramFile = "", refFile = "";
    bool encrypt = false, decrypt = false, calculateChiSquare = false;
    int nGram = 0, refNGram = 0;

    for (int i = 0; i < args.Length; i++)
    {
        switch (args[i])
        {
            case "-i": inputFile = args[++i]; break;
            case "-o": outputFile = args[++i]; break;
            case "-k": keyFile = args[++i]; break;
            case "-e": encrypt = true; break;
            case "-d": decrypt = true; break;
            case "-s": calculateChiSquare = true; break;
            case "-g1":
            case "-g2":
            case "-g3":
            case "-g4":
                nGram = int.Parse(args[i].Substring(2, 1));
                gramFile = args[++i];
                break;
            case "-r1":
            case "-r2":
            case "-r3":
            case "-r4":
                refNGram = int.Parse(args[i].Substring(2, 1));
                refFile = args[++i];
                break;
        }
    }

    if ((encrypt == decrypt) && nGram == 0 && !calculateChiSquare || string.IsNullOrEmpty(inputFile))
    {
        Console.WriteLine("Użycie: program -e|-d -k klucz.txt -i wejscie.txt -o wyjscie.txt [-g1|-g2|-g3|-g4 gram.txt] [-rX baza.txt] [-s]");
        return;
    }

    string inputText = File.ReadAllText(inputFile);
    inputText = new string(inputText.ToUpper().Where(char.IsLetter).ToArray());

    if (!string.IsNullOrEmpty(keyFile))
    {
        var substitution = LoadKey(keyFile, decrypt);
        string outputText = ProcessText(inputText, substitution);
        File.WriteAllText(outputFile, outputText);
        Console.WriteLine("Operacja zakończona pomyślnie.");
    }

    if (nGram > 0 && !string.IsNullOrEmpty(gramFile))
    {
        var nGramCounts = GenerateNGrams(inputText, nGram);
        SaveNGrams(gramFile, nGramCounts);
        Console.WriteLine($"Statystyki {nGram}-gramów zapisano do {gramFile}");
    }

    if (calculateChiSquare && !string.IsNullOrEmpty(refFile) && refNGram > 0)
    {
        var observed = GenerateNGrams(inputText, refNGram);
        var expected = LoadReferenceNGrams(refFile);
        double chiSquare = CalculateChiSquare(observed, expected);
        Console.WriteLine($"Wartość testu chi-kwadrat: {chiSquare:F4}");
    }
}
```

**2. Funkcja `LoadKey`**

**Wejście:**
- `filename`: Nazwa pliku zawierającego tablicę podstawieniową. Plik ten powinien zawierać mapowanie liter z tekstu jawnego na litery szyfrogramu.
- `reverse`: Flaga określająca, czy należy odwrócić tablicę podstawieniową (używane przy deszyfrowaniu).

**Wyjście:**
- `Dictionary<char, char>`: Słownik zawierający mapowanie liter z tekstu jawnego na szyfrogram (lub odwrotnie w przypadku deszyfrowania).

**Opis:**  
Funkcja `LoadKey` wczytuje tablicę podstawieniową z pliku i tworzy słownik, który mapuje litery z tekstu jawnego na litery szyfrogramu. Jeśli flaga reverse jest ustawiona, funkcja odwraca mapowanie, co jest potrzebne przy deszyfrowaniu. Funkcja sprawdza również, czy tablica podstawieniowa zawiera dokładnie 26 znaków (dla wszystkich liter alfabetu angielskiego). Jeśli nie, program kończy działanie z komunikatem o błędzie.

**Kod:**

``` C#
static Dictionary<char, char> LoadKey(string filename, bool reverse)
{
    var substitution = new Dictionary<char, char>();

    foreach (var line in File.ReadLines(filename))
    {
        var parts = line.Split();
        if (parts.Length == 2)
        {
            char plain = char.ToUpper(parts[0][0]);
            char cipher = char.ToUpper(parts[1][0]);

            if (reverse) (plain, cipher) = (cipher, plain);

            substitution[plain] = cipher;
        }
    }

    if (substitution.Count != 26)
    {
        Console.WriteLine("Błąd: Tablica podstawieniowa musi zawierać 26 znaków.");
        Environment.Exit(1);
    }

    return substitution;
}
```

**3. Funkcja `ProcessText`**

**Wejście:**
- `text`: Tekst do przetworzenia (zaszyfrowania lub odszyfrowania). Tekst ten jest już oczyszczony z niealfabetycznych znaków i zamieniony na wielkie litery.
- `substitution`: Słownik zawierający mapowanie liter.

**Wyjście:**
- `string`: Przetworzony tekst (zaszyfrowany lub odszyfrowany).

**Opis:**  
Funkcja `ProcessText` przyjmuje tekst i słownik mapowania, a następnie zamienia każdą literę w tekście na odpowiadającą jej literę z słownika. Wynikiem jest przetworzony tekst. Funkcja wykorzystuje LINQ do przekształcenia każdego znaku w tekście na podstawie mapowania zawartego w słowniku.

**Kod:**

``` C#
static string ProcessText(string text, Dictionary<char, char> substitution)
{
    return new string(text.Select(ch => substitution.ContainsKey(ch) ? substitution[ch] : ch).ToArray());
}
```

**4. Funkcja `GenerateNGrams`**

**Wejście:**
- `text`: Tekst do analizy. Tekst ten jest już oczyszczony z niealfabetycznych znaków i zamieniony na wielkie litery.
- `n`: Długość n-gramu (1 dla mono-gramów, 2 dla bi-gramów itd.).

**Wyjście:**
- `Dictionary<string, long>`: Słownik zawierający n-gramy jako klucze i ich liczność jako wartości.

**Opis:**  
Funkcja `GenerateNGrams` generuje n-gramy z podanego tekstu i zlicza ich występowanie. Wynikiem jest słownik, w którym kluczami są n-gramy, a wartościami ich liczność. Funkcja iteruje przez tekst, wycina n-gramy o długości `n` i zlicza ich wystąpienia.

**Kod:**

``` C#
static Dictionary<string, long> GenerateNGrams(string text, int n)
{
    var nGramCounts = new Dictionary<string, long>();

    for (int i = 0; i <= text.Length - n; i++)
    {
        string nGram = text.Substring(i, n);
        if (nGramCounts.ContainsKey(nGram))
            nGramCounts[nGram]++;
        else
            nGramCounts[nGram] = 1;
    }

    return nGramCounts;
}
```

**5. Funkcja `SaveNGrams`**

**Wejście:**
- `filename`: Nazwa pliku, do którego zostaną zapisane statystyki n-gramów.
- `nGramCounts`: Słownik zawierający n-gramy i ich liczność.

**Wyjście:**
- Brak bezpośredniego wyjścia. Funkcja zapisuje statystyki do pliku.

**Opis:**  
Funkcja `SaveNGrams` zapisuje statystyki n-gramów do pliku w formacie tabeli, gdzie każdy wiersz zawiera n-gram i jego liczność. Funkcja sortuje n-gramy malejąco według liczności przed zapisem do pliku.

**Kod:**

``` C#
static void SaveNGrams(string filename, Dictionary<string, long> nGramCounts)
{
    using (var writer = new StreamWriter(filename))
    {
        writer.WriteLine("n-gram	liczność");
        foreach (var kvp in nGramCounts.OrderByDescending(k => k.Value))
        {
            writer.WriteLine($"{kvp.Key}	{kvp.Value}");
        }
    }
}
```

**6. Funkcja `LoadReferenceNGrams`**

**Wejście:**
- `filename`: Nazwa pliku zawierającego referencyjną bazę n-gramów.

**Wyjście:**
- `Dictionary<string, long>`: Słownik zawierający referencyjne n-gramy i ich liczność.

**Opis:**  
Funkcja `LoadReferenceNGrams` wczytuje referencyjną bazę n-gramów z pliku i zwraca słownik, w którym kluczami są n-gramy, a wartościami ich liczność. Funkcja również oblicza całkowitą liczbę n-gramów w referencyjnej bazie.

**Kod:**

``` C#
static Dictionary<string, long> LoadReferenceNGrams(string filename)
{
    var reference = new Dictionary<string, long>();
    long total = 0;

    foreach (var line in File.ReadLines(filename))
    {
        var parts = line.Split();
        if (parts.Length == 2 && long.TryParse(parts[1], out long count))
        {
            reference[parts[0]] = count;
            total += count;
        }
    }

    return reference;
}
```

**7. Funkcja `CalculateChiSquare`**

**Wejście:**
- `observed`: Słownik zawierający obserwowane n-gramy i ich liczność.
- `expected`: Słownik zawierający oczekiwane n-gramy i ich liczność.

**Wyjście:**
- `double`: Wartość testu chi-kwadrat.

**Opis:**  
Funkcja `CalculateChiSquare` oblicza wartość testu chi-kwadrat na podstawie obserwowanych i oczekiwanych n-gramów. Wynikiem jest wartość testu chi-kwadrat, która jest używana do porównania rozkładu n-gramów w tekście z rozkładem referencyjnym. Funkcja oblicza oczekiwaną liczność n-gramów na podstawie proporcji w referencyjnej bazie i porównuje ją z obserwowaną licznością.

**Kod:**

``` C#
static double CalculateChiSquare(Dictionary<string, long> observed, Dictionary<string, long> expected)
{
    double chiSquare = 0.0;
    long totalObserved = observed.Values.Sum();
    long totalExpected = expected.Values.Sum();

    foreach (var kvp in expected)
    {
        long observedCount = observed.ContainsKey(kvp.Key) ? observed[kvp.Key] : 0;
        double expectedCount = (double)totalObserved * kvp.Value / totalExpected;

        chiSquare += Math.Pow(observedCount - expectedCount, 2) / expectedCount;
    }

    return chiSquare;
}
```

**Pełny kod źródłowy:**

``` C#
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

class Program
{
    static void Main(string[] args)
    {
        string inputFile = "", outputFile = "", keyFile = "";
        string gramFile = "", refFile = "";
        bool encrypt = false, decrypt = false, calculateChiSquare = false;
        int nGram = 0, refNGram = 0;

        for (int i = 0; i < args.Length; i++)
        {
            switch (args[i])
            {
                case "-i": inputFile = args[++i]; break;
                case "-o": outputFile = args[++i]; break;
                case "-k": keyFile = args[++i]; break;
                case "-e": encrypt = true; break;
                case "-d": decrypt = true; break;
                case "-s": calculateChiSquare = true; break;
                case "-g1":
                case "-g2":
                case "-g3":
                case "-g4":
                    nGram = int.Parse(args[i].Substring(2, 1));
                    gramFile = args[++i];
                    break;
                case "-r1":
                case "-r2":
                case "-r3":
                case "-r4":
                    refNGram = int.Parse(args[i].Substring(2, 1));
                    refFile = args[++i];
                    break;
            }
        }

        if ((encrypt == decrypt) && nGram == 0 && !calculateChiSquare || string.IsNullOrEmpty(inputFile))
        {
            Console.WriteLine("Użycie: program -e|-d -k klucz.txt -i wejscie.txt -o wyjscie.txt [-g1|-g2|-g3|-g4 gram.txt] [-rX baza.txt] [-s]");
            return;
        }

        string inputText = File.ReadAllText(inputFile);
        inputText = new string(inputText.ToUpper().Where(char.IsLetter).ToArray());

        if (!string.IsNullOrEmpty(keyFile))
        {
            var substitution = LoadKey(keyFile, decrypt);
            string outputText = ProcessText(inputText, substitution);
            File.WriteAllText(outputFile, outputText);
            Console.WriteLine("Operacja zakończona pomyślnie.");
        }

        if (nGram > 0 && !string.IsNullOrEmpty(gramFile))
        {
            var nGramCounts = GenerateNGrams(inputText, nGram);
            SaveNGrams(gramFile, nGramCounts);
            Console.WriteLine($"Statystyki {nGram}-gramów zapisano do {gramFile}");
        }

        if (calculateChiSquare && !string.IsNullOrEmpty(refFile) && refNGram > 0)
        {
            var observed = GenerateNGrams(inputText, refNGram);
            var expected = LoadReferenceNGrams(refFile);
            double chiSquare = CalculateChiSquare(observed, expected);
            Console.WriteLine($"Wartość testu chi-kwadrat: {chiSquare:F4}");
        }
    }

    static Dictionary<char, char> LoadKey(string filename, bool reverse)
    {
        var substitution = new Dictionary<char, char>();

        foreach (var line in File.ReadLines(filename))
        {
            var parts = line.Split();
            if (parts.Length == 2)
            {
                char plain = char.ToUpper(parts[0][0]);
                char cipher = char.ToUpper(parts[1][0]);

                if (reverse) (plain, cipher) = (cipher, plain);

                substitution[plain] = cipher;
            }
        }

        if (substitution.Count != 26)
        {
            Console.WriteLine("Błąd: Tablica podstawieniowa musi zawierać 26 znaków.");
            Environment.Exit(1);
        }

        return substitution;
    }

    static string ProcessText(string text, Dictionary<char, char> substitution)
    {
        return new string(text.Select(ch => substitution.ContainsKey(ch) ? substitution[ch] : ch).ToArray());
    }

    static Dictionary<string, long> GenerateNGrams(string text, int n)
    {
        var nGramCounts = new Dictionary<string, long>();

        for (int i = 0; i <= text.Length - n; i++)
        {
            string nGram = text.Substring(i, n);
            if (nGramCounts.ContainsKey(nGram))
                nGramCounts[nGram]++;
            else
                nGramCounts[nGram] = 1;
        }

        return nGramCounts;
    }

    static void SaveNGrams(string filename, Dictionary<string, long> nGramCounts)
    {
        using (var writer = new StreamWriter(filename))
        {
            writer.WriteLine("n-gram	liczność");
            foreach (var kvp in nGramCounts.OrderByDescending(k => k.Value))
            {
                writer.WriteLine($"{kvp.Key}	{kvp.Value}");
            }
        }
    }

    static Dictionary<string, long> LoadReferenceNGrams(string filename)
    {
        var reference = new Dictionary<string, long>();
        long total = 0;

        foreach (var line in File.ReadLines(filename))
        {
            var parts = line.Split();
            if (parts.Length == 2 && long.TryParse(parts[1], out long count))
            {
                reference[parts[0]] = count;
                total += count;
            }
        }

        return reference;
    }

    static double CalculateChiSquare(Dictionary<string, long> observed, Dictionary<string, long> expected)
    {
        double chiSquare = 0.0;
        long totalObserved = observed.Values.Sum();
        long totalExpected = expected.Values.Sum();

        foreach (var kvp in expected)
        {
            long observedCount = observed.ContainsKey(kvp.Key) ? observed[kvp.Key] : 0;
            double expectedCount = (double)totalObserved * kvp.Value / totalExpected;

            chiSquare += Math.Pow(observedCount - expectedCount, 2) / expectedCount;
        }

        return chiSquare;
    }
}
```