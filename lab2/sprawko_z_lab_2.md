# Kryptografia i kryptoanaliza
## Laboratorium 2
### Grupa 22B
### Autorzy: Przemysław Kałużiński, Michał Kaczor

### Zadanie 1

Napisz program (w języku: C++, RUST, Python) implementujący algorytm szyfru przesuwnego (szyfr Cezara).
1. Tekst jawny powinien być importowany do programu z pliku tekstowego, którego nazwa określona powinna być
po zdefiniowanym argumencie / fladze: -i.
2. Wynik pracy programu powinien być eksportowany do pliku tekstowego, którego nazwa określona powinna być
po zdefiniowanym argumencie / fladze: -o.
3. Klucz powinien być określany za pomocą parametru / flagi -k.
4. Tryb pracy programu powinien być określony poprzez flagi: -e dla procesu szyfrowania, -d dla procesu deszyfrowania.

Przykład wywołania programu w celu zaszyfrowania tekstu:

./program -e -k klucz.txt -i tekst_jawny.txt -o szyfrogram.txt

Przykład wywołania programu w celu odszyfrowania tekstu:

./program -d -k klucz.txt -i szyfrogram.txt -o tekst_odszyfrowany.txt

**Uwagi:** 
- Kolejność argumentów powinna być dowolna.
- Odczytany tekst jawny, przed dalszym przetwarzaniem, powinien być zamieniony do postaci składającej się
tylko z dużych liter. Ponadto z tekstu powinny być usunięte wszystkie znaki, które nie są literami, np: odstępy,
przecinki, kropki itp.

#### Implementacja

Ze względu na fakt, że zadania 1-2 są ze sobą powiązane i polegają na rozbudowie jednego programu, zdecydowaliśmy się na umieszczenie kodu źródłowego w osobnej sekcji implementacja, znajdującej się pod zadaniem 2.

#### Wyniki

Przed uruchomieniem programu, musieliśmy utworzyć plik z kluczem, który będzie używany do szyfrowania i deszyfrowania tekstu oraz zadeklarować plik z tekstem jawnym, który będzie poddany szyfrowaniu. Można było również wykonać szyfrowanie i deszyfrowanie na zasadzie podania przesunięcia, w przypadku szyfru Cezara o 3, natomiast zdecydowaliśmy o wczytywaniu klucza z pliku. Poniżej znajduje się wykorzystany przez nas klucz oraz tekst jawny:

**Klucz (klucz.txt):**

``` plaintext
A D
B E
C F
D G
E H
F I
G J
H K
I L
J M
K N
L O
M P
N Q
O R
P S
Q T
R U
S V
T W
U X
V Y
W Z
X A
Y B
Z C
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

``` plaintext
YDOHQWLQHVGDBRUVDLQWYDOHQWLQHVGDBLVDKROLGDBWKDWLQWKHXQLWHGVWDWHVWDNHVSODFHRQIHEUXDUBDQGWHFKQLFDOOBVLJQLILHVWKHDFFRPSOLVKPHQWVRIVWYDOHQWLQHDWKLUGFHQWXUBURPDQVDLQWZLWKWKDWVDLGPRVWDPHULFDQVLQVWHDGRIKRQRULQJVWYDOHQWLQHWKURXJKUHOLJLRXVFHUHPRQBHQMRBWKHKROLGDBEBHQJDJLQJLQURPDQWLFEHKDYLRUZLWKWKHLUVLJQLILFDQWRWKHURUVRPHRQHZKRWKHBZLVKWREHWKHLUVLJQLILFDQWRWKHUJLIWVVSHFLDOGLQQHUVDQGRWKHUDFNQRZOHGJHPHQWVRIDIIHFWLRQFRPSULVHPRVWLQGLYLGXDOVYDOHQWLQHVGDBFHOHEUDWLRQVFKRFRODWHVDQGIORZHUVDUHFRPPRQOBJLYHQDVJLIWVGXULQJYDOHQWLQHVGDBDVDUHDFFRPSDQBLQJJUHHWLQJFDUGVJUHHWLQJFDUGFRPSDQLHVUHOHDVHQHZYDOHQWLQHVGDBGHVLJQVDQQXDOOBUHGDQGSLQNDUHJHQHUDOOBXQGHUVWRRGWREHWKHFRORUVRIYDOHQWLQHVGDBDQGPDQBLQGLYLGXDOVLQVWHDGRIFHOHEUDWLQJURPDQWLFDOOBVSHQGWKHKROLGDBZLWKWKHLUIULHQGVDQGRUIDPLOBPHPEHUVYDULDWLRQVRIYDOHQWLQHVGDBDUHFHOHEUDWHGDFURVVWKHJOREHWKURXJKRXWWKHBHDULQDPHULFDWKHKROLGDBDOWKRXJKDFNQRZOHGJHGEBWKHYDVWPDMRULWBRIWKHSRSXODWLRQLVQWIHGHUDOOBUHFRJQLCHGQRWLPHRIIZRUNLVJUDQWHGIRUYDOHQWLQHVGDB
```

Następnie uruchomiliśmy program ponownie w celu odszyfrowania tekstu. Polecenie, którego użyliśmy do wywołania programu w celu odszyfrowania tekstu:  
`dotnet run -d -k klucz.txt -i szyfrogram.txt -o tekst_odszyfrowany.txt`

Po uruchomieniu programu z przedstawionymi argumentami otrzymaliśmy odszyfrowany tekst, który został zapisany do pliku `tekst_odszyfrowany.txt`. Poniżej znajduje się wynik odszyfrowania:

**Tekst odszyfrowany (tekst_odszyfrowany.txt):**

``` plaintext
VALENTINESDAYORSAINTVALENTINESDAYISAHOLIDAYTHATINTHEUNITEDSTATESTAKESPLACEONFEBRUARYANDTECHNICALLYSIGNIFIESTHEACCOMPLISHMENTSOFSTVALENTINEATHIRDCENTURYROMANSAINTWITHTHATSAIDMOSTAMERICANSINSTEADOFHONORINGSTVALENTINETHROUGHRELIGIOUSCEREMONYENJOYTHEHOLIDAYBYENGAGINGINROMANTICBEHAVIORWITHTHEIRSIGNIFICANTOTHERORSOMEONEWHOTHEYWISHTOBETHEIRSIGNIFICANTOTHERGIFTSSPECIALDINNERSANDOTHERACKNOWLEDGEMENTSOFAFFECTIONCOMPRISEMOSTINDIVIDUALSVALENTINESDAYCELEBRATIONSCHOCOLATESANDFLOWERSARECOMMONLYGIVENASGIFTSDURINGVALENTINESDAYASAREACCOMPANYINGGREETINGCARDSGREETINGCARDCOMPANIESRELEASENEWVALENTINESDAYDESIGNSANNUALLYREDANDPINKAREGENERALLYUNDERSTOODTOBETHECOLORSOFVALENTINESDAYANDMANYINDIVIDUALSINSTEADOFCELEBRATINGROMANTICALLYSPENDTHEHOLIDAYWITHTHEIRFRIENDSANDORFAMILYMEMBERSVARIATIONSOFVALENTINESDAYARECELEBRATEDACROSSTHEGLOBETHROUGHOUTTHEYEARINAMERICATHEHOLIDAYALTHOUGHACKNOWLEDGEDBYTHEVASTMAJORITYOFTHEPOPULATIONISNTFEDERALLYRECOGNIZEDNOTIMEOFFWORKISGRANTEDFORVALENTINESDAY
```

**Wnioski:**

Przed szyfrowaniem tekst jawny został przekształcony w ciąg wielkich liter, z usunięciem wszystkich znaków niebędących literami (np. spacji, znaków interpunkcyjnych). Miało to na celu uproszczenie procesu szyfrowania i uniknięcie niejednoznaczności. Po uruchomieniu programu z flagą `-e` (szyfrowanie) oraz podaniu odpowiednich argumentów (`-k klucz.txt`, `-i tekst_jawny.txt`, `-o szyfrogram.txt`), program zaszyfrował tekst jawny przy użyciu podanego klucza. Wynikiem szyfrowania jest tekst zaszyfrowany szyfrem Cezara, który został zapisany do pliku `szyfrogram.txt`. Tekst ten jest ciągiem znaków, w którym każda litera z tekstu jawnego została zastąpiona odpowiadającą jej literą z klucza. Na przykład litera `A` została zamieniona na `D`. W efekcie otrzymaliśmy tekst, który jest trudny do odczytania bez znajomości klucza ale nie niemożliwy do odczytania chcąc złamać klucz.

Następnie, aby zweryfikować poprawność szyfrowania, uruchomiliśmy program z flagą `-d` (deszyfrowanie) oraz tymi samymi argumentami (`-k klucz.txt`, `-i szyfrogram.txt`, `-o tekst_odszyfrowany.txt`). Program odszyfrował tekst zaszyfrowany, używając odwrotnego mapowania z klucza. Wynikiem jest tekst odszyfrowany, który został zapisany do pliku `tekst_odszyfrowany.txt`. Tekst ten jest identyczny z oryginalnym tekstem jawnym, z wyjątkiem tego, że wszystkie litery zostały zamienione na wielkie, a znaki niebędące literami (np. spacje, znaki interpunkcyjne) zostały usunięte.

### Zadanie 2

Rozbuduj program z poprzedniego zadania poprzez implementację ataku typu brute-force na szyfrogram wygenerowany przy pomocy algorytmu przesuwnego.
1. Algorytm powinien być wyzwalany po użyciu flagi -a z parametrem bf.

Przykład wywołania programu:
./program -a bf -i szyfrogram -o tekst_odszyfrowany

**Uwagi:** 

- Program w celu klasyfikacji wyniku działania algorytmu, powinien wykorzystywać test χ2 na poziomie istotności 0.05 (patrz ostatnie zadanie z poprzedniej instrukcji).
- Do wyznaczenia wartości krytycznej, decydującej o odrzuceniu hipotezy zerowej (odszyfrowany tekst jest tekstem w języku angielskim), należy użyć funkcji gsl_cdf_chisq_Pinv(p, df) z biblioteki gsl (C++).
  - Funkcja ta oblicza dystrybuantę (CDF) rozkładu χ2 a następnie zwraca wartość zmiennej losowej χ2, dla której dystrybuanta ta przyjmuje podaną wartość prawdopodobieństwa (pierwszy argument funkcji).
    - Przykład, jeżeli podane prawdopodobieństwo p = 0.95, to funkcja zwróci wartość charakterystyki χ2, dla której 95% obszaru pod krzywą rozkładu znajduje się na lewo od tej wartości.
  - Drugim argumentem funkcji jest liczba stopni swobody. Jest to wartość, która odnosi się do liczby niezależnych zmiennych, które mogą swobodnie przyjmować wartości w określonym zbiorze danych (liczba wartości w próbie, które mogą się zmieniać bez narzucania ograniczeń przez inne zmienne).
    - W kontekście odszyfrowywania tekstu zaszyfrowanego szyfrem Cezara z wykorzystaniem metody b-f, liczba stopni swobody odnosi się do liczby możliwych przesunięć klucza. Ponieważ szyfr Cezara, polega na przesunięci każdej litery o stałą wartość, to liczba tych możliwych przesunięć zależy od ilości liter w alfabecie. Dla alfabetu o n znakach, liczba stopni swobody będzie wynosiła n − 1 ponieważ pomijane jest przesunięcie o 0 znaków.
    - W kontekście odszyfrowywania tekstu zaszyfrowanego szyfrem afinicznym z wykorzystaniem metody b-f, liczba stopni swobody, również określona jest przez liczbę możliwych wartości klucza. Jednakże tym razem liczba ta jest wynikiem iloczynu wartości dwóch komponentów klucza, to jest a × b = 12 × 26 = 312.
- Korzystając z języka RUST, do wyznaczenia wartości krytycznej, należy użyć obiektu utworzonego przy pomocy konstruktora rozkładu ChiSquared, wywołując metodę new(df), gdzie df to liczba stopni swobody. Następnie na tak utworzonym obiekcie, należy wywołać metodę inverse_cdf(p), gdzie p to wartość prawdopodobieństwa. Narzędzia te dostępne sa po dołączeniu do projektu biblioteki statrs i modułu distribution.
- Korzystając z język Python, wartość krytyczną można wyznaczyć używając obiektu chi2 z modułu stats biblioteki scipi. Na obiekcie tym należy wywołać metodę ppf(p, df).

#### Implementacja

Ze względu na fakt, że zadania 1-2 są ze sobą powiązane i polegają na rozbudowie jednego programu, zdecydowaliśmy się na umieszczenie kodu źródłowego w osobnej sekcji implementacja, znajdującej się pod zadaniem 2.

#### Wyniki

W ramach zadania 2 zaimplementowaliśmy atak brute-force na szyfrogram zaszyfrowany szyfrem Cezara i wykorzystaliśmy test χ2 do oceny jakości odszyfrowanego tekstu. 

Na początku zaszyfrowaliśmy tekst jawny znajdujący się w pliku `tekst_jawny.txt` szyfrem Cezara i zapisaliśmy go w pliku `szyfrogram.txt`. 

Następnie wykonaliśmy polecenie: 

`dotnet run -- -a bf -i szyfrogram.txt -o tekst_odszyfrwany.txt`.

**Tekst jawny:**

``` plaintext
Valentine's Day (or Saint Valentine's Day) is a holiday that, in the United States, takes place on February 14, and technically signifies the accomplishments of St. Valentine, a third-century Roman saint.

With that said, most Americans, instead of honoring St. Valentine through religious ceremony, enjoy the holiday by engaging in "romantic" behavior with their significant other or someone who they wish to be their significant other; gifts, special dinners, and other acknowledgements of affection comprise most individuals' Valentine's Day celebrations.

Chocolates and flowers are commonly given as gifts during Valentine's Day, as are accompanying greeting cards (greeting card companies release new Valentine's Day designs annually). Red and pink are generally understood to be "the colors" of Valentine's Day, and many individuals, instead of celebrating romantically, spend the holiday with their friends and/or family members.

Variations of Valentine's Day are celebrated across the globe throughout the year. In America, the holiday, although acknowledged by the vast majority of the population, isn't federally recognized; no time off work is granted for Valentine's Day.
```

**Szyfrogram:**

``` plaintext
YDOHQWLQHVGDBRUVDLQWYDOHQWLQHVGDBLVDKROLGDBWKDWLQWKHXQLWHGVWDWHVWDNHVSODFHRQIHEUXDUBDQGWHFKQLFDOOBVLJQLILHVWKHDFFRPSOLVKPHQWVRIVWYDOHQWLQHDWKLUGFHQWXUBURPDQVDLQWZLWKWKDWVDLGPRVWDPHULFDQVLQVWHDGRIKRQRULQJVWYDOHQWLQHWKURXJKUHOLJLRXVFHUHPRQBHQMRBWKHKROLGDBEBHQJDJLQJLQURPDQWLFEHKDYLRUZLWKWKHLUVLJQLILFDQWRWKHURUVRPHRQHZKRWKHBZLVKWREHWKHLUVLJQLILFDQWRWKHUJLIWVVSHFLDOGLQQHUVDQGRWKHUDFNQRZOHGJHPHQWVRIDIIHFWLRQFRPSULVHPRVWLQGLYLGXDOVYDOHQWLQHVGDBFHOHEUDWLRQVFKRFRODWHVDQGIORZHUVDUHFRPPRQOBJLYHQDVJLIWVGXULQJYDOHQWLQHVGDBDVDUHDFFRPSDQBLQJJUHHWLQJFDUGVJUHHWLQJFDUGFRPSDQLHVUHOHDVHQHZYDOHQWLQHVGDBGHVLJQVDQQXDOOBUHGDQGSLQNDUHJHQHUDOOBXQGHUVWRRGWREHWKHFRORUVRIYDOHQWLQHVGDBDQGPDQBLQGLYLGXDOVLQVWHDGRIFHOHEUDWLQJURPDQWLFDOOBVSHQGWKHKROLGDBZLWKWKHLUIULHQGVDQGRUIDPLOBPHPEHUVYDULDWLRQVRIYDOHQWLQHVGDBDUHFHOHEUDWHGDFURVVWKHJOREHWKURXJKRXWWKHBHDULQDPHULFDWKHKROLGDBDOWKRXJKDFNQRZOHGJHGEBWKHYDVWPDMRULWBRIWKHSRSXODWLRQLVQWIHGHUDOOBUHFRJQLCHGQRWLPHRIIZRUNLVJUDQWHGIRUYDOHQWLQHVGDB
```

**Otrzymany wynik:**

``` plaintext
Najlepsze przesunięcie: 3, wynik chi-kwadrat: 0,06397110381789516
```

**Otrzymany odszyfrowany tekst:**

``` plaintext
VALENTINESDAYORSAINTVALENTINESDAYISAHOLIDAYTHATINTHEUNITEDSTATESTAKESPLACEONFEBRUARYANDTECHNICALLYSIGNIFIESTHEACCOMPLISHMENTSOFSTVALENTINEATHIRDCENTURYROMANSAINTWITHTHATSAIDMOSTAMERICANSINSTEADOFHONORINGSTVALENTINETHROUGHRELIGIOUSCEREMONYENJOYTHEHOLIDAYBYENGAGINGINROMANTICBEHAVIORWITHTHEIRSIGNIFICANTOTHERORSOMEONEWHOTHEYWISHTOBETHEIRSIGNIFICANTOTHERGIFTSSPECIALDINNERSANDOTHERACKNOWLEDGEMENTSOFAFFECTIONCOMPRISEMOSTINDIVIDUALSVALENTINESDAYCELEBRATIONSCHOCOLATESANDFLOWERSARECOMMONLYGIVENASGIFTSDURINGVALENTINESDAYASAREACCOMPANYINGGREETINGCARDSGREETINGCARDCOMPANIESRELEASENEWVALENTINESDAYDESIGNSANNUALLYREDANDPINKAREGENERALLYUNDERSTOODTOBETHECOLORSOFVALENTINESDAYANDMANYINDIVIDUALSINSTEADOFCELEBRATINGROMANTICALLYSPENDTHEHOLIDAYWITHTHEIRFRIENDSANDORFAMILYMEMBERSVARIATIONSOFVALENTINESDAYARECELEBRATEDACROSSTHEGLOBETHROUGHOUTTHEYEARINAMERICATHEHOLIDAYALTHOUGHACKNOWLEDGEDBYTHEVASTMAJORITYOFTHEPOPULATIONISNTFEDERALLYRECOGNIZEDNOTIMEOFFWORKISGRANTEDFORVALENTINESDAY
```

**Wnioski:**

Atak brute-force okazał się skuteczną metodą łamania szyfru Cezara. Dzięki przetestowaniu wszystkich możliwych przesunięć (od 0 do 25), program był w stanie znaleźć poprawne odszyfrowanie szyfrogramu. Szyfr Cezara jest bardzo podatny na ataki brute-force ze względu na małą liczbę możliwych kluczy (tylko 26). To pokazuje jak istotne jest korzystanie z lepszego szyfrowania, ponieważ nawet w przypadku tekstu z ilością **1185 znaków** atak brute-force poradził sobie bardzo szybko. Test χ² okazał się bardzo przydatnym narzędziem do oceny, które przesunięcie daje tekst najbardziej zbliżony do języka angielskiego. Dzięki porównaniu częstotliwości występowania liter w odszyfrowanym tekście z oczekiwanymi częstotliwościami w języku angielskim, program mógł automatycznie wybrać najlepsze przesunięcie.

### Implementacja

**1. Funkcja `Main`**

**Wejście:**
- `args`: Argumenty przekazane do programu z linii poleceń. Argumenty te określają operacje do wykonania, takie jak szyfrowanie, deszyfrowanie lub atak brute-force.

**Wyjście:**
- Brak bezpośredniego wyjścia. Program wykonuje operacje na plikach i wyświetla komunikaty w konsoli, informujące o postępie i wynikach operacji.

**Opis:**  
Funkcja `Main` jest punktem wejścia programu. Odczytuje argumenty z linii poleceń, przetwarza je i wywołuje odpowiednie funkcje w zależności od podanych flag. Program obsługuje szyfrowanie, deszyfrowanie oraz atak brute-force na szyfrogram. Funkcja sprawdza poprawność przekazanych argumentów i wyświetla komunikat o błędzie, jeśli argumenty są nieprawidłowe.

**Kod:**
```csharp
static void Main(string[] args)
{
    string inputFile = "", outputFile = "", keyFile = "";
    bool encrypt = false, decrypt = false, bruteForce = false;

    for (int i = 0; i < args.Length; i++)
    {
        switch (args[i])
        {
            case "-i": inputFile = args[++i]; break;
            case "-o": outputFile = args[++i]; break;
            case "-k": keyFile = args[++i]; break;
            case "-e": encrypt = true; break;
            case "-d": decrypt = true; break;
            case "-a":
                if (args[++i] == "bf") bruteForce = true;
                break;
        }
    }

    if (bruteForce)
    {
        if (string.IsNullOrEmpty(inputFile) || string.IsNullOrEmpty(outputFile))
        {
            Console.WriteLine("Użycie: program -a bf -i szyfrogram.txt -o tekst_odszyfrowany.txt");
            return;
        }

        BruteForceAttack(inputFile, outputFile);
    }
    else if ((encrypt == decrypt) || string.IsNullOrEmpty(inputFile) || string.IsNullOrEmpty(outputFile) || string.IsNullOrEmpty(keyFile))
    {
        Console.WriteLine("Użycie: program -e|-d -k klucz.txt -i wejscie.txt -o wyjscie.txt");
        return;
    }
    else
    {
        var substitution = LoadKey(keyFile, decrypt);
        string inputText = File.ReadAllText(inputFile);
        inputText = new string(inputText.ToUpper().Where(char.IsLetter).ToArray());

        string outputText = ProcessText(inputText, substitution);
        File.WriteAllText(outputFile, outputText);
        Console.WriteLine("Operacja zakończona pomyślnie.");
    }
}
```

---

#### **2. Funkcja `LoadKey`**

**Wejście:**
- `filename`: Nazwa pliku zawierającego tablicę podstawieniową. Plik ten powinien zawierać mapowanie liter z tekstu jawnego na litery szyfrogramu.
- `reverse`: Flaga określająca, czy należy odwrócić tablicę podstawieniową (używane przy deszyfrowaniu).

**Wyjście:**
- `Dictionary<char, char>`: Słownik zawierający mapowanie liter z tekstu jawnego na szyfrogram (lub odwrotnie w przypadku deszyfrowania).

**Opis:**  
Funkcja `LoadKey` wczytuje tablicę podstawieniową z pliku i tworzy słownik, który mapuje litery z tekstu jawnego na litery szyfrogramu. Jeśli flaga `reverse` jest ustawiona, funkcja odwraca mapowanie, co jest potrzebne przy deszyfrowaniu. Funkcja sprawdza również, czy tablica podstawieniowa zawiera dokładnie 26 znaków (dla wszystkich liter alfabetu angielskiego). Jeśli nie, program kończy działanie z komunikatem o błędzie.

**Kod:**
```csharp
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

---

#### **3. Funkcja `ProcessText`**

**Wejście:**
- `text`: Tekst do przetworzenia (zaszyfrowania lub odszyfrowania). Tekst ten jest już oczyszczony z niealfabetycznych znaków i zamieniony na wielkie litery.
- `substitution`: Słownik zawierający mapowanie liter.

**Wyjście:**
- `string`: Przetworzony tekst (zaszyfrowany lub odszyfrowany).

**Opis:**  
Funkcja `ProcessText` przyjmuje tekst i słownik mapowania, a następnie zamienia każdą literę w tekście na odpowiadającą jej literę z słownika. Wynikiem jest przetworzony tekst. Funkcja wykorzystuje LINQ do przekształcenia każdego znaku w tekście na podstawie mapowania zawartego w słowniku.

**Kod:**
```csharp
static string ProcessText(string text, Dictionary<char, char> substitution)
{
    return new string(text.Select(ch => substitution.ContainsKey(ch) ? substitution[ch] : ch).ToArray());
}
```

---

#### **4. Funkcja `BruteForceAttack`**

**Wejście:**
- `inputFile`: Nazwa pliku zawierającego szyfrogram.
- `outputFile`: Nazwa pliku, do którego zostanie zapisany odszyfrowany tekst.

**Wyjście:**
- Brak bezpośredniego wyjścia. Funkcja zapisuje odszyfrowany tekst do pliku i wyświetla informacje w konsoli.

**Opis:**  
Funkcja `BruteForceAttack` wykonuje atak brute-force na szyfrogram, testując wszystkie możliwe przesunięcia (od 0 do 25). Dla każdego przesunięcia odszyfrowuje tekst i oblicza wartość testu chi-kwadrat, aby ocenić, czy odszyfrowany tekst jest podobny do języka angielskiego. Najlepsze przesunięcie (z najmniejszą wartością chi-kwadrat) jest wybierane, a odpowiadający mu tekst zapisywany do pliku.

**Kod:**
```csharp
static void BruteForceAttack(string inputFile, string outputFile)
{
    string cipherText = File.ReadAllText(inputFile);
    cipherText = new string(cipherText.ToUpper().Where(char.IsLetter).ToArray());

    double bestChiSquared = double.MaxValue;
    string bestText = "";
    int bestShift = 0;

    for (int shift = 0; shift < 26; shift++)
    {
        string decryptedText = DecryptCaesar(cipherText, shift);
        double chiSquared = ChiSquaredTest(decryptedText);

        if (chiSquared < bestChiSquared)
        {
            bestChiSquared = chiSquared;
            bestText = decryptedText;
            bestShift = shift;
        }
    }

    File.WriteAllText(outputFile, bestText);
    Console.WriteLine($"Najlepsze przesunięcie: {bestShift}, wynik chi-kwadrat: {bestChiSquared}");
    Console.WriteLine("Operacja zakończona pomyślnie.");
}
```

---

#### **5. Funkcja `DecryptCaesar`**

**Wejście:**
- `cipherText`: Tekst zaszyfrowany.
- `shift`: Przesunięcie, które ma zostać zastosowane do odszyfrowania tekstu.

**Wyjście:**
- `string`: Odszyfrowany tekst.

**Opis:**  
Funkcja `DecryptCaesar` odszyfrowuje tekst zaszyfrowany szyfrem Cezara, stosując podane przesunięcie. Każda litera w tekście jest przesuwana o `shift` pozycji wstecz w alfabecie.

**Kod:**
```csharp
static string DecryptCaesar(string cipherText, int shift)
{
    return new string(cipherText.Select(ch => (char)('A' + (ch - 'A' - shift + 26) % 26)).ToArray());
}
```

---

#### **6. Funkcja `ChiSquaredTest`**

**Wejście:**
- `text`: Tekst do analizy.

**Wyjście:**
- `double`: Wartość testu chi-kwadrat.

**Opis:**  
Funkcja `ChiSquaredTest` oblicza wartość testu chi-kwadrat dla podanego tekstu, porównując częstotliwość występowania liter z oczekiwanymi częstotliwościami w języku angielskim. Wynik jest używany do oceny, czy tekst jest podobny do języka angielskiego.

**Kod:**
```csharp
static double ChiSquaredTest(string text)
{
    var englishFrequencies = new Dictionary<char, double>
    {
        {'A', 0.08167}, {'B', 0.01492}, {'C', 0.02782}, {'D', 0.04253},
        {'E', 0.12702}, {'F', 0.02228}, {'G', 0.02015}, {'H', 0.06094},
        {'I', 0.06966}, {'J', 0.00153}, {'K', 0.00772}, {'L', 0.04025},
        {'M', 0.02406}, {'N', 0.06749}, {'O', 0.07507}, {'P', 0.01929},
        {'Q', 0.00095}, {'R', 0.05987}, {'S', 0.06327}, {'T', 0.09056},
        {'U', 0.02758}, {'V', 0.00978}, {'W', 0.0236}, {'X', 0.0015},
        {'Y', 0.01974}, {'Z', 0.00074}
    };

    var observedFrequencies = text.GroupBy(ch => ch)
                                  .ToDictionary(g => g.Key, g => (double)g.Count() / text.Length);

    double chiSquared = 0.0;
    foreach (var kvp in englishFrequencies)
    {
        char letter = kvp.Key;
        double expected = kvp.Value;
        double observed = observedFrequencies.ContainsKey(letter) ? observedFrequencies[letter] : 0.0;
        chiSquared += Math.Pow(observed - expected, 2) / expected;
    }

    return chiSquared;
}
```

### Zadanie 3

Napisz program analogiczny do programu z zadania 1, który tym razem implementuje szyfr afiniczny.

#### Implementacja

Ze względu na fakt, że zadania 3-4 są ze sobą powiązane i polegają na rozbudowie jednego programu, zdecydowaliśmy się na umieszczenie kodu źródłowego w osobnej sekcji implementacja, znajdującej się pod zadaniem 4.

#### Wyniki

Przed uruchomieniem programu, musieliśmy utworzyć plik z kluczem, który będzie używany do szyfrowania i deszyfrowania tekstu oraz zadeklarować plik z tekstem jawnym, który będzie poddany szyfrowaniu. Można było również wykonać szyfrowanie i deszyfrowanie na zasadzie podania wartości przy wpisywanej fladze, natomiast zdecydowaliśmy o wczytywaniu klucza z pliku. Poniżej znajduje się wykorzystany przez nas klucz oraz tekst jawny:

**Klucz (klucz.txt):**

``` plaintext
5
8
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

``` plaintext
JILCVZWVCUXIYAPUIWVZJILCVZWVCUXIYWUIRALWXIYZRIZWVZRCEVWZCXUZIZCUZIGCUFLISCAVHCNPEIPYIVXZCSRVWSILLYUWMVWHWCUZRCISSAQFLWURQCVZUAHUZJILCVZWVCIZRWPXSCVZEPYPAQIVUIWVZOWZRZRIZUIWXQAUZIQCPWSIVUWVUZCIXAHRAVAPWVMUZJILCVZWVCZRPAEMRPCLWMWAEUSCPCQAVYCVBAYZRCRALWXIYNYCVMIMWVMWVPAQIVZWSNCRIJWAPOWZRZRCWPUWMVWHWSIVZAZRCPAPUAQCAVCORAZRCYOWURZANCZRCWPUWMVWHWSIVZAZRCPMWHZUUFCSWILXWVVCPUIVXAZRCPISGVAOLCXMCQCVZUAHIHHCSZWAVSAQFPWUCQAUZWVXWJWXEILUJILCVZWVCUXIYSCLCNPIZWAVUSRASALIZCUIVXHLAOCPUIPCSAQQAVLYMWJCVIUMWHZUXEPWVMJILCVZWVCUXIYIUIPCISSAQFIVYWVMMPCCZWVMSIPXUMPCCZWVMSIPXSAQFIVWCUPCLCIUCVCOJILCVZWVCUXIYXCUWMVUIVVEILLYPCXIVXFWVGIPCMCVCPILLYEVXCPUZAAXZANCZRCSALAPUAHJILCVZWVCUXIYIVXQIVYWVXWJWXEILUWVUZCIXAHSCLCNPIZWVMPAQIVZWSILLYUFCVXZRCRALWXIYOWZRZRCWPHPWCVXUIVXAPHIQWLYQCQNCPUJIPWIZWAVUAHJILCVZWVCUXIYIPCSCLCNPIZCXISPAUUZRCMLANCZRPAEMRAEZZRCYCIPWVIQCPWSIZRCRALWXIYILZRAEMRISGVAOLCXMCXNYZRCJIUZQIBAPWZYAHZRCFAFELIZWAVWUVZHCXCPILLYPCSAMVWDCXVAZWQCAHHOAPGWUMPIVZCXHAPJILCVZWVCUXIY
```

Następnie uruchomiliśmy program ponownie w celu odszyfrowania tekstu. Polecenie, którego użyliśmy do wywołania programu w celu odszyfrowania tekstu:  
`dotnet run -d -k klucz.txt -i szyfrogram.txt -o tekst_odszyfrowany.txt`

Po uruchomieniu programu z przedstawionymi argumentami otrzymaliśmy odszyfrowany tekst, który został zapisany do pliku `tekst_odszyfrowany.txt`. Poniżej znajduje się wynik odszyfrowania:

**Tekst odszyfrowany (tekst_odszyfrowany.txt):**

``` plaintext
VALENTINESDAYORSAINTVALENTINESDAYISAHOLIDAYTHATINTHEUNITEDSTATESTAKESPLACEONFEBRUARYANDTECHNICALLYSIGNIFIESTHEACCOMPLISHMENTSOFSTVALENTINEATHIRDCENTURYROMANSAINTWITHTHATSAIDMOSTAMERICANSINSTEADOFHONORINGSTVALENTINETHROUGHRELIGIOUSCEREMONYENJOYTHEHOLIDAYBYENGAGINGINROMANTICBEHAVIORWITHTHEIRSIGNIFICANTOTHERORSOMEONEWHOTHEYWISHTOBETHEIRSIGNIFICANTOTHERGIFTSSPECIALDINNERSANDOTHERACKNOWLEDGEMENTSOFAFFECTIONCOMPRISEMOSTINDIVIDUALSVALENTINESDAYCELEBRATIONSCHOCOLATESANDFLOWERSARECOMMONLYGIVENASGIFTSDURINGVALENTINESDAYASAREACCOMPANYINGGREETINGCARDSGREETINGCARDCOMPANIESRELEASENEWVALENTINESDAYDESIGNSANNUALLYREDANDPINKAREGENERALLYUNDERSTOODTOBETHECOLORSOFVALENTINESDAYANDMANYINDIVIDUALSINSTEADOFCELEBRATINGROMANTICALLYSPENDTHEHOLIDAYWITHTHEIRFRIENDSANDORFAMILYMEMBERSVARIATIONSOFVALENTINESDAYARECELEBRATEDACROSSTHEGLOBETHROUGHOUTTHEYEARINAMERICATHEHOLIDAYALTHOUGHACKNOWLEDGEDBYTHEVASTMAJORITYOFTHEPOPULATIONISNTFEDERALLYRECOGNIZEDNOTIMEOFFWORKISGRANTEDFORVALENTINESDAY
```

**Wnioski:**

Szyfr afiniczny jest bardziej złożony niż szyfr Cezara, ale nadal jest podatny na ataki kryptoanalityczne. Wprowadzenie dodatkowego klucza 𝑎 wymagało sprawdzenia jego zgodności z warunkiem gcd(𝑎, 26) = 1, a także obliczenia odwrotności modulo 26 w przypadku deszyfrowania. Choć szyfr afiniczny jest równie prosty do zaimplementowania, jak szyfr Cezara, to zapewnia on większe bezpieczeństwo.

Szyfr afiniczny zapewnia większą liczbę możliwych kluczy niż szyfr Cezara, co zwiększa jego odporność na proste ataki.

### Zadanie 4

Rozbuduj program z poprzedniego zadania poprzez implementację ataku typu brute-force na szyfrogram zaimplementowany przy pomocy szyfru afinicznego. Sposób pracy z programem powinien być analogiczny do pracy z
programem z zadania 2.

#### Implementacja

Ze względu na fakt, że zadania 3-4 są ze sobą powiązane i polegają na rozbudowie jednego programu, zdecydowaliśmy się na umieszczenie kodu źródłowego w osobnej sekcji implementacja, znajdującej się pod zadaniem 4.

#### Wyniki

W ramach zadania 4 zaimplementowaliśmy atak brute-force na szyfrogram zaszyfrowany szyfrem afinicznym i wykorzystaliśmy test χ2 do oceny jakości odszyfrowanego tekstu. 

Na początku zaszyfrowaliśmy tekst jawny znajdujący się w pliku `tekst_jawny.txt` szyfrem Cezara i zapisaliśmy go w pliku `szyfrogram.txt`. 

Następnie wykonaliśmy polecenie: 

`dotnet run -- -a bf -i szyfrogram.txt -o tekst_odszyfrwany.txt`.

**Tekst jawny:**

``` plaintext
Valentine's Day (or Saint Valentine's Day) is a holiday that, in the United States, takes place on February 14, and technically signifies the accomplishments of St. Valentine, a third-century Roman saint.

With that said, most Americans, instead of honoring St. Valentine through religious ceremony, enjoy the holiday by engaging in "romantic" behavior with their significant other or someone who they wish to be their significant other; gifts, special dinners, and other acknowledgements of affection comprise most individuals' Valentine's Day celebrations.

Chocolates and flowers are commonly given as gifts during Valentine's Day, as are accompanying greeting cards (greeting card companies release new Valentine's Day designs annually). Red and pink are generally understood to be "the colors" of Valentine's Day, and many individuals, instead of celebrating romantically, spend the holiday with their friends and/or family members.

Variations of Valentine's Day are celebrated across the globe throughout the year. In America, the holiday, although acknowledged by the vast majority of the population, isn't federally recognized; no time off work is granted for Valentine's Day.
```

**Szyfrogram:**

``` plaintext
JILCVZWVCUXIYAPUIWVZJILCVZWVCUXIYWUIRALWXIYZRIZWVZRCEVWZCXUZIZCUZIGCUFLISCAVHCNPEIPYIVXZCSRVWSILLYUWMVWHWCUZRCISSAQFLWURQCVZUAHUZJILCVZWVCIZRWPXSCVZEPYPAQIVUIWVZOWZRZRIZUIWXQAUZIQCPWSIVUWVUZCIXAHRAVAPWVMUZJILCVZWVCZRPAEMRPCLWMWAEUSCPCQAVYCVBAYZRCRALWXIYNYCVMIMWVMWVPAQIVZWSNCRIJWAPOWZRZRCWPUWMVWHWSIVZAZRCPAPUAQCAVCORAZRCYOWURZANCZRCWPUWMVWHWSIVZAZRCPMWHZUUFCSWILXWVVCPUIVXAZRCPISGVAOLCXMCQCVZUAHIHHCSZWAVSAQFPWUCQAUZWVXWJWXEILUJILCVZWVCUXIYSCLCNPIZWAVUSRASALIZCUIVXHLAOCPUIPCSAQQAVLYMWJCVIUMWHZUXEPWVMJILCVZWVCUXIYIUIPCISSAQFIVYWVMMPCCZWVMSIPXUMPCCZWVMSIPXSAQFIVWCUPCLCIUCVCOJILCVZWVCUXIYXCUWMVUIVVEILLYPCXIVXFWVGIPCMCVCPILLYEVXCPUZAAXZANCZRCSALAPUAHJILCVZWVCUXIYIVXQIVYWVXWJWXEILUWVUZCIXAHSCLCNPIZWVMPAQIVZWSILLYUFCVXZRCRALWXIYOWZRZRCWPHPWCVXUIVXAPHIQWLYQCQNCPUJIPWIZWAVUAHJILCVZWVCUXIYIPCSCLCNPIZCXISPAUUZRCMLANCZRPAEMRAEZZRCYCIPWVIQCPWSIZRCRALWXIYILZRAEMRISGVAOLCXMCXNYZRCJIUZQIBAPWZYAHZRCFAFELIZWAVWUVZHCXCPILLYPCSAMVWDCXVAZWQCAHHOAPGWUMPIVZCXHAPJILCVZWVCUXIY
```

**Otrzymany wynik:**

``` plaintext
Najlepsze klucze: a = 5, b = 8, wynik chi-kwadrat: 0,06397110381789516
```

**Otrzymany odszyfrowany tekst:**

``` plaintext
VALENTINESDAYORSAINTVALENTINESDAYISAHOLIDAYTHATINTHEUNITEDSTATESTAKESPLACEONFEBRUARYANDTECHNICALLYSIGNIFIESTHEACCOMPLISHMENTSOFSTVALENTINEATHIRDCENTURYROMANSAINTWITHTHATSAIDMOSTAMERICANSINSTEADOFHONORINGSTVALENTINETHROUGHRELIGIOUSCEREMONYENJOYTHEHOLIDAYBYENGAGINGINROMANTICBEHAVIORWITHTHEIRSIGNIFICANTOTHERORSOMEONEWHOTHEYWISHTOBETHEIRSIGNIFICANTOTHERGIFTSSPECIALDINNERSANDOTHERACKNOWLEDGEMENTSOFAFFECTIONCOMPRISEMOSTINDIVIDUALSVALENTINESDAYCELEBRATIONSCHOCOLATESANDFLOWERSARECOMMONLYGIVENASGIFTSDURINGVALENTINESDAYASAREACCOMPANYINGGREETINGCARDSGREETINGCARDCOMPANIESRELEASENEWVALENTINESDAYDESIGNSANNUALLYREDANDPINKAREGENERALLYUNDERSTOODTOBETHECOLORSOFVALENTINESDAYANDMANYINDIVIDUALSINSTEADOFCELEBRATINGROMANTICALLYSPENDTHEHOLIDAYWITHTHEIRFRIENDSANDORFAMILYMEMBERSVARIATIONSOFVALENTINESDAYARECELEBRATEDACROSSTHEGLOBETHROUGHOUTTHEYEARINAMERICATHEHOLIDAYALTHOUGHACKNOWLEDGEDBYTHEVASTMAJORITYOFTHEPOPULATIONISNTFEDERALLYRECOGNIZEDNOTIMEOFFWORKISGRANTEDFORVALENTINESDAY
```

**Wnioski:**

Atak brute-force na szyfr afiniczny jest wykonalny ze względu na stosunkowo małą przestrzeń kluczy, jednak jest bardziej czasochłonny niż w przypadku szyfru Cezara.
W rzeczywistych systemach kryptograficznych takie podejście nie jest skuteczne, ponieważ współczesne algorytmy używają znacznie większych przestrzeni kluczy. Można go również złamać poprzez znajomość dwóch par znaków (tekst jawny – szyfrogram), co pozwala algebraicznie wyznaczyć klucz. Implementacja ataku brute-force pokazuje, że szyfr afiniczny nie jest odporny na nowoczesne metody kryptoanalizy.

### Implementacja

**1. Funkcja `Main`**

**Wejście:**
- `args`: Argumenty przekazane do programu z linii poleceń. Argumenty te określają operacje do wykonania, takie jak szyfrowanie, deszyfrowanie lub atak brute-force.

**Wyjście:**
- Brak bezpośredniego wyjścia. Program wykonuje operacje na plikach i wyświetla komunikaty w konsoli, informujące o postępie i wynikach operacji.

**Opis:**  
Funkcja `Main` jest punktem wejścia programu. Odczytuje argumenty z linii poleceń, przetwarza je i wywołuje odpowiednie funkcje w zależności od podanych flag. Program obsługuje szyfrowanie, deszyfrowanie oraz atak brute-force na szyfrogram. Funkcja sprawdza poprawność przekazanych argumentów i wyświetla komunikat o błędzie, jeśli argumenty są nieprawidłowe.

**Kod:**
```csharp
static void Main(string[] args)
{
    string inputFile = "", outputFile = "", keyFile = "";
    bool encrypt = false, decrypt = false, bruteForce = false;

    for (int i = 0; i < args.Length; i++)
    {
        switch (args[i])
        {
            case "-i": inputFile = args[++i]; break;
            case "-o": outputFile = args[++i]; break;
            case "-k": keyFile = args[++i]; break;
            case "-e": encrypt = true; break;
            case "-d": decrypt = true; break;
            case "-a":
                if (args[++i] == "bf") bruteForce = true;
                break;
        }
    }

    if (bruteForce)
    {
        if (string.IsNullOrEmpty(inputFile) || string.IsNullOrEmpty(outputFile))
        {
            Console.WriteLine("Użycie: program -a bf -i szyfrogram.txt -o tekst_odszyfrowany.txt");
            return;
        }

        BruteForceAttack(inputFile, outputFile);
    }
    else if ((encrypt == decrypt) || string.IsNullOrEmpty(inputFile) || string.IsNullOrEmpty(outputFile) || string.IsNullOrEmpty(keyFile))
    {
        Console.WriteLine("Użycie: program -e|-d -k klucz.txt -i wejscie.txt -o wyjscie.txt");
        return;
    }
    else
    {
        var (a, b) = LoadKey(keyFile);
        string inputText = File.ReadAllText(inputFile);
        inputText = new string(inputText.ToUpper().Where(char.IsLetter).ToArray());

        string outputText = ProcessText(inputText, a, b, encrypt);
        File.WriteAllText(outputFile, outputText);
        Console.WriteLine("Operacja zakończona pomyślnie.");
    }
}
```

---

#### **2. Funkcja `LoadKey`**

**Wejście:**
- `filename`: Nazwa pliku zawierającego klucze `a` i `b`. Plik ten powinien zawierać dwie liczby całkowite, każda w osobnej linii.

**Wyjście:**
- `(int a, int b)`: Krotka zawierająca wartości kluczy `a` i `b`.

**Opis:**  
Funkcja `LoadKey` wczytuje klucze `a` i `b` z pliku. Sprawdza, czy klucz `a` jest względnie pierwszy z 26 (warunek konieczny dla szyfru afinicznego). Jeśli warunek nie jest spełniony, program kończy działanie z komunikatem o błędzie.

**Kod:**
```csharp
static (int a, int b) LoadKey(string filename)
{
    var lines = File.ReadAllLines(filename);
    if (lines.Length < 2)
    {
        Console.WriteLine("Błąd: Plik klucza musi zawierać dwie liczby (a i b).");
        Environment.Exit(1);
    }

    int a = int.Parse(lines[0]);
    int b = int.Parse(lines[1]);

    if (GCD(a, 26) != 1)
    {
        Console.WriteLine("Błąd: Liczba a musi być względnie pierwsza z 26.");
        Environment.Exit(1);
    }

    return (a, b);
}
```

---

#### **3. Funkcja `GCD`**

**Wejście:**
- `a`: Pierwsza liczba całkowita.
- `b`: Druga liczba całkowita.

**Wyjście:**
- `int`: Największy wspólny dzielnik (NWD) liczb `a` i `b`.

**Opis:**  
Funkcja `GCD` oblicza największy wspólny dzielnik dwóch liczb całkowitych za pomocą algorytmu Euklidesa.

**Kod:**
```csharp
static int GCD(int a, int b)
{
    while (b != 0)
    {
        int temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}
```

---

#### **4. Funkcja `ProcessText`**

**Wejście:**
- `text`: Tekst do przetworzenia (zaszyfrowania lub odszyfrowania). Tekst ten jest już oczyszczony z niealfabetycznych znaków i zamieniony na wielkie litery.
- `a`: Klucz `a` szyfru afinicznego.
- `b`: Klucz `b` szyfru afinicznego.
- `encrypt`: Flaga określająca, czy tekst ma być zaszyfrowany (`true`) czy odszyfrowany (`false`).

**Wyjście:**
- `string`: Przetworzony tekst (zaszyfrowany lub odszyfrowany).

**Opis:**  
Funkcja `ProcessText` przyjmuje tekst i klucze `a` oraz `b`, a następnie przekształca każdą literę w tekście za pomocą funkcji afinicznej. Wynikiem jest przetworzony tekst.

**Kod:**
```csharp
static string ProcessText(string text, int a, int b, bool encrypt)
{
    return new string(text.Select(ch => AffineTransform(ch, a, b, encrypt)).ToArray());
}
```

---

#### **5. Funkcja `AffineTransform`**

**Wejście:**
- `ch`: Znak do przekształcenia.
- `a`: Klucz `a` szyfru afinicznego.
- `b`: Klucz `b` szyfru afinicznego.
- `encrypt`: Flaga określająca, czy znak ma być zaszyfrowany (`true`) czy odszyfrowany (`false`).

**Wyjście:**
- `char`: Przekształcony znak.

**Opis:**  
Funkcja `AffineTransform` przekształca pojedynczy znak za pomocą funkcji afinicznej. W przypadku szyfrowania stosuje wzór `y = (a * x + b) % 26`, a w przypadku deszyfrowania `y = aInverse * (x - b + 26) % 26`, gdzie `aInverse` to odwrotność klucza `a` modulo 26.

**Kod:**
```csharp
static char AffineTransform(char ch, int a, int b, bool encrypt)
{
    int x = ch - 'A';
    int y;

    if (encrypt)
    {
        y = (a * x + b) % 26;
    }
    else
    {
        int aInverse = ModInverse(a, 26);
        y = aInverse * (x - b + 26) % 26;
    }

    return (char)(y + 'A');
}
```

---

#### **6. Funkcja `ModInverse`**

**Wejście:**
- `a`: Liczba całkowita, dla której obliczana jest odwrotność.
- `m`: Modulo (w tym przypadku 26).

**Wyjście:**
- `int`: Odwrotność liczby `a` modulo `m`.

**Opis:**  
Funkcja `ModInverse` oblicza odwrotność liczby `a` modulo `m` za pomocą przeszukiwania liniowego.

**Kod:**
```csharp
static int ModInverse(int a, int m)
{
    a = a % m;
    for (int x = 1; x < m; x++)
    {
        if ((a * x) % m == 1)
            return x;
    }
    return 1;
}
```

---

#### **7. Funkcja `BruteForceAttack`**

**Wejście:**
- `inputFile`: Nazwa pliku zawierającego szyfrogram.
- `outputFile`: Nazwa pliku, do którego zostanie zapisany odszyfrowany tekst.

**Wyjście:**
- Brak bezpośredniego wyjścia. Funkcja zapisuje odszyfrowany tekst do pliku i wyświetla informacje w konsoli.

**Opis:**  
Funkcja `BruteForceAttack` wykonuje atak brute-force na szyfrogram, testując wszystkie możliwe kombinacje kluczy `a` i `b`. Dla każdej kombinacji odszyfrowuje tekst i oblicza wartość testu chi-kwadrat, aby ocenić, czy odszyfrowany tekst jest podobny do języka angielskiego. Najlepsza kombinacja kluczy (z najmniejszą wartością chi-kwadrat) jest wybierana, a odpowiadający jej tekst zapisywany do pliku.

**Kod:**
```csharp
static void BruteForceAttack(string inputFile, string outputFile)
{
    string cipherText = File.ReadAllText(inputFile);
    cipherText = new string(cipherText.ToUpper().Where(char.IsLetter).ToArray());

    double bestChiSquared = double.MaxValue;
    string bestText = "";
    int bestA = 0, bestB = 0;

    for (int a = 1; a < 26; a++)
    {
        if (GCD(a, 26) != 1) continue;

        for (int b = 0; b < 26; b++)
        {
            string decryptedText = ProcessText(cipherText, a, b, false);
            double chiSquared = ChiSquaredTest(decryptedText);

            if (chiSquared < bestChiSquared)
            {
                bestChiSquared = chiSquared;
                bestText = decryptedText;
                bestA = a;
                bestB = b;
            }
        }
    }

    File.WriteAllText(outputFile, bestText);
    Console.WriteLine($"Najlepsze klucze: a = {bestA}, b = {bestB}, wynik chi-kwadrat: {bestChiSquared}");
    Console.WriteLine("Operacja zakończona pomyślnie.");
}
```

---

#### **8. Funkcja `ChiSquaredTest`**

**Wejście:**
- `text`: Tekst do analizy.

**Wyjście:**
- `double`: Wartość testu chi-kwadrat.

**Opis:**  
Funkcja `ChiSquaredTest` oblicza wartość testu chi-kwadrat dla podanego tekstu, porównując częstotliwość występowania liter z oczekiwanymi częstotliwościami w języku angielskim. Wynik jest używany do oceny, czy tekst jest podobny do języka angielskiego.

**Kod:**
```csharp
static double ChiSquaredTest(string text)
{
    var englishFrequencies = new Dictionary<char, double>
    {
        {'A', 0.08167}, {'B', 0.01492}, {'C', 0.02782}, {'D', 0.04253},
        {'E', 0.12702}, {'F', 0.02228}, {'G', 0.02015}, {'H', 0.06094},
        {'I', 0.06966}, {'J', 0.00153}, {'K', 0.00772}, {'L', 0.04025},
        {'M', 0.02406}, {'N', 0.06749}, {'O', 0.07507}, {'P', 0.01929},
        {'Q', 0.00095}, {'R', 0.05987}, {'S', 0.06327}, {'T', 0.09056},
        {'U', 0.02758}, {'V', 0.00978}, {'W', 0.0236}, {'X', 0.0015},
        {'Y', 0.01974}, {'Z', 0.00074}
    };

    var observedFrequencies = text.GroupBy(ch => ch)
                                  .ToDictionary(g => g.Key, g => (double)g.Count() / text.Length);

    double chiSquared = 0.0;
    foreach (var kvp in englishFrequencies)
    {
        char letter = kvp.Key;
        double expected = kvp.Value;
        double observed = observedFrequencies.ContainsKey(letter) ? observedFrequencies[letter] : 0.0;
        chiSquared += Math.Pow(observed - expected, 2) / expected;
    }

    return chiSquared;
}
```