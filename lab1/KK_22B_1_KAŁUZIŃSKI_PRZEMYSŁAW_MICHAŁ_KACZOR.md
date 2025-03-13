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



### Zadanie 4

Wykonać eksperymenty:
- Dokonaj obserwacji wyniku testu χ2 dla tekstu jawnego i zaszyfrowanego o różnych długościach.
- Wiadomo, iż wynik testu może być znacząco zaburzony w przypadku gdy brane są pod uwagę symbole (n-gramy), które rzadko występują w tekście, np w przypadku mono-gramów języka angielskiego są to litery: J, K, Q, X oraz Z (patrz odczytana tablica częstości mono-gramów). Zbadaj wynik testu χ2 w przypadku gdy do wyznaczenia testu pominięte zostaną rzadko występujące n-gramy.

#### Implementacja

Ze względu na fakt, że zadania 1-4 są ze sobą powiązane i polegają na rozbudowie jednego programu, zdecydowaliśmy się na umieszczenie kodu źródłowego w osobnej sekcji implementacja, znajdującej się pod zadaniem 4.

#### Wyniki



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