# Kryptografia i kryptoanaliza
## Laboratorium 5
### Grupa 22B
### Autorzy: Przemysław Kałużiński, Michał Kaczor

### Zadanie 1

Dokonać implementacji kryptosystemu strumieniowego, którego strumień klucza generowany jest przy pomocy LFSR.  
Należy przyjąć, iż:  

- Model rejestru zdefiniowany jest następującym wielomianem połączeń: $P(x) = 1 + x + x^3 + x^5 + x^{16} + x^{17}$  
- Sekwencja inicjująca jest następująca: `[0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1]`  

Implementowany kryptosystem powinien mieć funkcjonalność:  
- Szyfrowania fragmentu tekstu odczytanego z pliku tekstowego  
- Zapis szyfrogramu do nowego pliku

#### Implementacja

**1. Zmienne globalne**

W kodzie zdefiniowano stałe globalne: `TAPS` określające pozycje sprzężeń (tapów) rejestru LFSR zgodnie z wielomianem $P(x)=1+x+x^3+x^5+x^16+x^17$ oraz `INITIAL_STATE`, który zawiera 17-bitową sekwencję inicjującą rejestr. Obie te wartości są podstawą do generowania strumienia klucza w kryptosystemie strumieniowym.

``` C#
private static readonly int[] TAPS = { 0, 1, 3, 5, 16 };

private static readonly List<int> INITIAL_STATE = new List<int> { 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1 };
```

**2. Funkcja `GenerateKeystream`**

***Wejście:**  
- `length` (int) - długość generowanego strumienia klucza w bitach

**Wyjście:**  
- `List<int>` - lista bitów reprezentująca strumień klucza

**Opis:**  
Generuje pseudolosowy strumień klucza przy użyciu rejestru LFSR (Linear Feedback Shift Register). Inicjalizuje stan początkowy wartością `INITIAL_STATE`, następnie dla każdego bitu oblicza nową wartość na podstawie pozycji `TAPS` (operacja XOR). Każda iteracja dodaje ostatni bit stanu do strumienia klucza, wstawia nowy bit na początek rejestru i usuwa ostatni bit.

**Kod:**
``` C#
private static List<int> GenerateKeystream(int length)
{
    List<int> state = new List<int>(INITIAL_STATE); // Inicjalizacja stanu początkowego
    List<int> keystream = new List<int>(); // Inicjalizacja strumienia klucza

    for (int i = 0; i < length; i++)
    {
        // Dodanie ostatniego bitu stanu do strumienia klucza
        keystream.Add(state[state.Count - 1]);

        // Obliczenie nowego bitu na podstawie pozycji określonych w TAPS (operacja XOR)
        int newBit = 0;
        foreach (int t in TAPS)
        {
            newBit ^= state[t];
        }

        // Wstawienie nowego bitu na początek rejestru i usunięcie ostatniego bitu
        state.Insert(0, newBit);
        state.RemoveAt(state.Count - 1);
    }

    return keystream;
}
```

**3. Funkcja `BitsFromBytes`**

**Wejście:**  
- `dataBytes` (byte[]) - tablica bajtów do konwersji

**Wyjście:**  
- `List<int>` - lista bitów (0 i 1) reprezentująca przekonwertowane dane

**Opis:**  
Konwertuje tablicę bajtów na listę bitów. Dla każdego bajta w tablicy wyodrębnia poszczególne bity (od najbardziej znaczącego do najmniej znaczącego) i dodaje je do wynikowej listy. Każdy bajt jest rozbijany na 8 bitów.

**Kod:**
``` C#
private static List<int> BitsFromBytes(byte[] dataBytes)
{
    List<int> bits = new List<int>();

    foreach (byte b in dataBytes)
    {
        // Dla każdego bitu w bajcie (od najbardziej znaczącego do najmniej znaczącego)
        for (int i = 7; i >= 0; i--)
        {
            bits.Add((b >> i) & 1); // Wyodrębnienie i-tego bitu
        }
    }

    return bits;
}
```

**4. Funkcja `BytesFromBits`**

**Wejście:**  
- `bits` (List<int>) - lista bitów (0 i 1) do konwersji

**Wyjście:**  
- `byte[]` - tablica bajtów reprezentująca przekonwertowane dane

**Opis:**  
Konwertuje listę bitów na tablicę bajtów. Grupuje bity w bloki po 8 (od najbardziej znaczącego do najmniej znaczącego) i łączy je w pojedyncze bajty. Jeśli liczba bitów nie jest podzielna przez 8, ostatni bajt jest uzupełniany zerami.  

**Kod:**
``` C#
private static byte[] BytesFromBits(List<int> bits)
{
    List<byte> outBytes = new List<byte>();

    for (int i = 0; i < bits.Count; i += 8)
    {
        byte byteValue = 0;
        // Łączenie 8 bitów w jeden bajt
        for (int j = 0; j < 8; j++)
        {
            if (i + j < bits.Count)
            {
                byteValue = (byte)((byteValue << 1) | bits[i + j]); // Dodanie bitu do bajtu
            }
        }
        outBytes.Add(byteValue); // Dodanie bajtu do listy wynikowej
    }

    return outBytes.ToArray();
}
```

**Wejście:**  
- `inputPath` (string) - ścieżka do pliku wejściowego
- `outputPath` (string) - ścieżka do pliku wyjściowego

**Wyjście:**  
- Brak (wynik zapisywany jest do pliku)

**Opis:**  
Realizuje operację szyfrowania/deszyfrowania pliku przy użyciu algorytmu LFSR. Odczytuje dane wejściowe, konwertuje je na bity, generuje strumień klucza o odpowiedniej długości, wykonuje operację XOR na bitach danych i strumienia klucza, a następnie zapisuje wynik do pliku wyjściowego. W przypadku LFSR operacje szyfrowania i deszyfrowania są identyczne.

**Kod:**
``` C#
private static void Encrypt(string inputPath, string outputPath)
{
    // Odczytanie danych wejściowych
    byte[] plaintext = File.ReadAllBytes(inputPath);
    // Konwersja bajtów na bity
    List<int> ptBits = BitsFromBytes(plaintext);
    // Generowanie strumienia klucza o długości równej liczbie bitów danych wejściowych
    List<int> ks = GenerateKeystream(ptBits.Count);

    // Szyfrowanie/deszyfrowanie poprzez operację XOR na bitach danych i strumienia klucza
    List<int> ctBits = new List<int>();
    for (int i = 0; i < ptBits.Count; i++)
    {
        ctBits.Add(ptBits[i] ^ ks[i]);
    }

    // Konwersja bitów wynikowych na bajty i zapis do pliku wyjściowego
    byte[] ciphertext = BytesFromBits(ctBits);
    File.WriteAllBytes(outputPath, ciphertext);
}
```

**6. Funkcja `Main`**

**Wejście:**  
- `args` (string[]) - argumenty wiersza poleceń:
  - `args[0]` - tryb pracy ("encrypt" lub "decrypt")
  - `args[1]` - ścieżka do pliku wejściowego
  - `args[2]` - ścieżka do pliku wyjściowego

**Wyjście:**  
- Brak (wynik zapisywany jest do pliku)

**Opis:**  
Główna funkcja programu, która obsługuje argumenty wiersza poleceń. Sprawdza poprawność liczby i wartości argumentów, a następnie wywołuje funkcję `Encrypt` w odpowiednim trybie. W przypadku błędnych argumentów wyświetla komunikaty i kończy działanie programu.

**Kod:**
``` C#
static void Main(string[] args)
{
    // Sprawdzenie liczby argumentów
    if (args.Length != 3)
    {
        Console.WriteLine("Użycie: LFSRCrypto <encrypt|decrypt> <wejście> <wyjście>");
        Environment.Exit(1);
    }

    string mode = args[0]; // Tryb pracy (encrypt/decrypt)
    string inputFile = args[1]; // Ścieżka do pliku wejściowego
    string outputFile = args[2]; // Ścieżka do pliku wyjściowego

    // Sprawdzenie poprawności trybu
    if (mode != "encrypt" && mode != "decrypt")
    {
        Console.WriteLine("Tryb nieznany. Wybierz 'encrypt' lub 'decrypt'.");
        Environment.Exit(1);
    }

    // Wywołanie funkcji Encrypt (deszyfrowanie jest tym samym co szyfrowanie w LFSR)
    Encrypt(inputFile, outputFile);
}
```

#### Wyniki



### Zadanie 2

# Zadanie 2

Dokonać ataku na zbudowany w ramach pierwszego zadania kryptosystem. Przyjąć następujące złożenia ataku:

- Znane są tylko: tekst jawny i szyfrogram.
- Celem ataku jest:
  - Odzyskanie klucza.
  - Określenie schematu połączeń rejestru LFSR.
  - Zbudowanie własnego kryptosystemu, będącego w stanie odczytać szyfrogramy generowane przez kryptosystem z 1 zadania (kryptosystem nadawcy).

Procedura postępowania:  
- Odzyskanie klucza: W tym celu wystarczy wykonać operację:  
  $s_i = x_i \oplus y_i \quad \text{dla} \quad i = 1, \ldots, n$  
  gdzie \( n \) jest ilością bitów wiadomości (szyfrogramu).
- Określenie schematu połączeń LFSR: Do tego celu należy użyć algorytmu z 3 zadania 4 instrukcji.

Następnie:
- Zbudować kryptosystem w oparciu o zidentyfikowany w ramach przedstawionej procedury rejestr LFSR.
- Dokonać implementacji funkcji porównującej odzyskany klucz z kluczem wygenerowanym w ramach nowego kryptosystemu.
  - Uwaga: zgodność kluczy będzie można porównać tylko wtedy, gdy zidentyfikowany (nowy) kryptosystem zostanie zainicjowany taką samą sekwencją inicjującą, jakiej użył nadawca wiadomości. Sekwencja ta będzie znana po wykonaniu procedury odzyskania klucza. Ilość bitów sekwencji inicjującej będzie znana po zidentyfikowaniu schematu połączeń LFSR.
- Jeżeli klucze będą się zgadzać, dokonać odszyfrowania szyfrogramu przy pomocy zidentyfikowanego kryptosystemu!

#### Implementacja

**1. Funkcja `BerlekampMassey`**

**Wejście:**  
- `s` (List<int>) - fragment strumienia klucza w postaci listy bitów

**Wyjście:**  
- krotka `(int L, List<int> C)`:
  - `L` - długość rejestru LFSR
  - `C` - wielomian charakterystyczny reprezentowany jako lista współczynników

**Opis:**  
Implementuje algorytm Berlekampa-Massey'a służący do identyfikacji parametrów LFSR na podstawie fragmentu jego strumienia wyjściowego. Algorytm iteracyjnie oblicza wielomian charakterystyczny i długość rejestru, minimalizując przy tym złożoność. Wykorzystuje operacje XOR i aktualizację wielomianów charakterystycznych.

**Kod:**
``` C#
static (int L, List<int> C) BerlekampMassey(List<int> s)
{
    int n = s.Count;
    List<int> C = new List<int>(new int[n + 1]); // Wielomian charakterystyczny (aktualny)
    C[0] = 1; // Inicjalizacja: C(x) = 1
    List<int> B = new List<int>(new int[n + 1]); // Poprzedni wielomian charakterystyczny
    B[0] = 1; // Inicjalizacja: B(x) = 1
    int L = 0; // Długość LFSR
    int m = 1; // Licznik przesunięć

    for (int i = 0; i < n; i++)
    {
        // Obliczenie różnicy (d) między przewidywanym a rzeczywistym bitem
        int d = s[i];
        for (int j = 1; j <= L; j++)
        {
            d ^= C[j] & s[i - j]; // XOR z poprzednimi bitami i współczynnikami C
        }

        if (d != 0) // Jeśli różnica niezerowa, aktualizacja wielomianu C
        {
            List<int> T = new List<int>(C); // Kopia aktualnego wielomianu
            for (int j = 0; j < B.Count; j++)
            {
                if (B[j] != 0) // Aktualizacja C przez XOR z przesuniętym B
                {
                    if (j + m < C.Count)
                        C[j + m] ^= 1;
                }
            }
            if (2 * L <= i) // Jeśli długość LFSR jest za mała, zwiększ ją
            {
                L = i + 1 - L;
                B = new List<int>(T); // Zapisz poprzedni wielomian
                m = 1; // Zresetuj licznik przesunięć
            }
            else
            {
                m++; // Inkrementuj licznik przesunięć
            }
        }
        else
        {
            m++; // Inkrementuj licznik przesunięć
        }
    }

    return (L, C.GetRange(0, L + 1)); // Zwróć długość LFSR i wielomian charakterystyczny
}
```

**2. Funkcja `BitsFromBytes`**

**Wejście:**  
- `data` (byte[]) - tablica bajtów do konwersji

**Wyjście:**  
- `List<int>` - lista bitów (wartości 0 i 1) reprezentująca przekonwertowane dane

**Opis:**  
Konwertuje dane bajtowe na reprezentację bitową. Każdy bajt jest rozbijany na 8 bitów (od najbardziej znaczącego do najmniej znaczącego) i zapisywany w postaci listy wartości binarnych. Funkcja jest kluczowa dla przygotowania danych do analizy kryptograficznej.

**Kod:**
``` C#
static List<int> BitsFromBytes(byte[] data)
{
    List<int> bits = new List<int>();
    foreach (byte b in data)
    {
        for (int i = 7; i >= 0; i--)
        {
            bits.Add((b >> i) & 1); // Wyodrębnienie i-tego bitu
        }
    }
    return bits;
}
```

**3. Funkcja `BytesFromBits`**

**Wejście:**  
- `bits` (List<int>) - lista bitów (wartości 0 i 1) do konwersji

**Wyjście:**  
- `byte[]` - tablica bajtów powstała z połączenia bitów

**Opis:**  
Odwrotność funkcji `BitsFromBytes`. Łączy grupy 8 bitów w pojedyncze bajty, umożliwiając zapis danych w postaci binarnej. Automatycznie obsługuje niepełne grupy bitów (uzupełniając je zerami).


**Kod:**
``` C#
static byte[] BytesFromBits(List<int> bits)
{
    List<byte> outBytes = new List<byte>();
    for (int i = 0; i < bits.Count; i += 8)
    {
        byte byteValue = 0;
        for (int j = 0; j < 8 && i + j < bits.Count; j++)
        {
            byteValue = (byte)((byteValue << 1) | bits[i + j]); // Składanie bajtu z bitów
        }
        outBytes.Add(byteValue);
    }
    return outBytes.ToArray();
}
```

**4. Funkcja `GenerateKeystream`**

**Wejście:**  
- `iv` (List<int>) - wektor inicjujący (initial vector)
- `taps` (List<int>) - pozycje bitów używane do sprzężenia zwrotnego
- `length` (int) - długość generowanego strumienia w bitach

**Wyjście:**  
- `List<int>` - wygenerowany strumień klucza

**Opis:**  
Generuje strumień pseudolosowy za pomocą rejestru LFSR. Wykorzystuje podany wektor inicjujący i pozycje sprzężeń zwrotnych (taps) do iteracyjnego obliczania kolejnych bitów strumienia. Każda iteracja przesuwa rejestr i oblicza nowy bit na podstawie operacji XOR na wskazanych pozycjach.

**Kod:**
``` C#
static List<int> GenerateKeystream(List<int> iv, List<int> taps, int length)
{
    List<int> state = new List<int>(iv); // Inicjalizacja stanu początkowego (IV)
    List<int> ks = new List<int>(); // Strumień klucza
    for (int i = 0; i < length; i++)
    {
        ks.Add(state[state.Count - 1]); // Dodanie ostatniego bitu stanu do strumienia
        int newBit = 0;
        foreach (int t in taps)
        {
            newBit ^= state[t]; // Obliczenie nowego bitu (XOR z TAPS)
        }
        state.Insert(0, newBit); // Wstawienie nowego bitu na początek
        state.RemoveAt(state.Count - 1); // Usunięcie ostatniego bitu
    }
    return ks;
}
```

**5. Funkcja `Main`**

**Wejście:**  
- `args` (string[]) - argumenty wiersza poleceń:
  - `args[0]` - ścieżka do pliku z znanym fragmentem plaintextu
  - `args[1]` - ścieżka do pliku z szyfrogramem
  - `args[2]` - ścieżka do pliku wyjściowego

**Wyjście:**  
- Brak (wyniki zapisywane są do pliku i wyświetlane w konsoli)

**Opis:**  
Główna funkcja programu realizująca atak kryptograficzny ze znanym fragmentem tekstu jawnego. Wykonuje następujące kroki:
1. Wczytuje i konwertuje dane wejściowe
2. Rekonstruuje fragment strumienia klucza
3. Identyfikuje parametry LFSR za pomocą algorytmu Berlekampa-Massey'a
4. Generuje pełny strumień klucza
5. Odszyfrowuje cały szyfrogram
6. Weryfikuje poprawność wyniku poprzez próbę dekodowania UTF-8
7. Zapisuje wyniki i wyświetla informacje diagnostyczne

**Kod:**
``` C#
static void Main(string[] args)
{
    // Sprawdzenie liczby argumentów
    if (args.Length != 3)
    {
        Console.WriteLine("Użycie: LFSRAttack <known_plaintext> <ciphertext> <output_plaintext>");
        Environment.Exit(1);
    }

    string ptFile = args[0]; // Ścieżka do znanego plaintextu
    string ctFile = args[1]; // Ścieżka do szyfrogramu
    string outFile = args[2]; // Ścieżka do pliku wyjściowego (odszyfrowany tekst)

    // Odczytanie plików i konwersja na bity
    byte[] pt = File.ReadAllBytes(ptFile);
    byte[] ct = File.ReadAllBytes(ctFile);
    List<int> ptBits = BitsFromBytes(pt);
    List<int> ctBits = BitsFromBytes(ct);
    int n = ctBits.Count; // Długość szyfrogramu w bitach

    // Wygenerowanie fragmentu strumienia klucza (XOR znanego plaintextu i szyfrogramu)
    int minLen = Math.Min(ptBits.Count, n);
    List<int> ksFrag = new List<int>();
    for (int i = 0; i < minLen; i++)
    {
        ksFrag.Add(ptBits[i] ^ ctBits[i]);
    }

    // Znalezienie parametrów LFSR za pomocą algorytmu Berlekampa-Massey'a
    var (L, C) = BerlekampMassey(ksFrag);
    Console.WriteLine($"Odnalezione LFSR: długość L={L}, wielomian C=[{string.Join(", ", C)}]");

    // Wyodrębnienie IV (pierwsze L bitów strumienia klucza)
    List<int> iv = ksFrag.GetRange(0, L);
    Console.WriteLine($"Zrekonstruowany IV (pierwsze {L} bitów): [{string.Join(", ", iv)}]");

    // Konwersja wielomianu charakterystycznego na pozycje TAPS (pomijając C[0])
    List<int> taps = new List<int>();
    for (int j = 1; j < C.Count; j++)
    {
        if (C[j] == 1)
        {
            taps.Add(j - 1); // Pozycje TAPS to indeksy współczynników 1 w wielomianie
        }
    }
    Console.WriteLine($"Pozycje taps: [{string.Join(", ", taps)}]");

    // Generowanie pełnego strumienia klucza i odszyfrowanie całego szyfrogramu
    List<int> fullKs = GenerateKeystream(iv, taps, n);
    List<int> decBits = new List<int>();
    for (int i = 0; i < n; i++)
    {
        decBits.Add(ctBits[i] ^ fullKs[i]); // XOR szyfrogramu ze strumieniem klucza
    }

    // Zapis odszyfrowanych danych do pliku
    byte[] plaintext = BytesFromBits(decBits);
    File.WriteAllBytes(outFile, plaintext);
    Console.WriteLine($"Odszyfrowano cały szyfrogram do pliku: {outFile}");

    // Próba dekodowania jako UTF-8 (dla tekstowych danych)
    try
    {
        string decodedText = Encoding.UTF8.GetString(plaintext);
        Console.WriteLine("Dekodowanie UTF-8 powiodło się.");
    }
    catch (ArgumentException)
    {
        Console.WriteLine("Uwaga: dekodowanie UTF-8 NIE powiodło się. Sprawdź poprawność plaintext.");
    }
}
```

#### Wyniki



### Zadanie 3

Dokonać ataku na zbudowany w ramach pierwszego zadania kryptosystem Przyjąć następujące złożenia ataku:
- Znane są tylko: szyfrogram i początkowy fragment tekstu jawnego.
- Celem ataku jest:
  - Odzyskanie klucza.
  - Określenie schematu połączeń rejestru LFSR.
  - Określenie minimalnej długości (ilości bitów) tekstu jawnego, umożliwiającego odzyskanie kompletnej wiadomości.
  - Określenie zależności pomiędzy złożonością liniową zidentyfikowanego kryptosystemu, maksymalną sekwencją klucza, która generowana jest przez ten kryptosystem a wymaganą minimalną długością znanego tekstu jawnego.

#### Implementacja

**1. Funkcja `BytesToBits`**

**Wejście:**  
- `data` (byte[]) - tablica bajtów do konwersji

**Wyjście:**  
- `List<int>` - lista bitów (wartości 0 i 1) w kolejności od MSB do LSB

**Opis:**  
Konwertuje dane bajtowe na reprezentację bitową. Dla każdego bajta w tablicy wyodrębnia kolejne bity (od najbardziej znaczącego - bit 7, do najmniej znaczącego - bit 0) i dodaje je do wynikowej listy. Każdy bajt generuje dokładnie 8 bitów w outputcie.

**Kod:**
``` C#
static List<int> BytesToBits(byte[] data)
{
    List<int> bits = new List<int>();
    foreach (byte b in data)
    {
        for (int i = 7; i >= 0; i--)
        {
            bits.Add((b >> i) & 1); // Wyodrębnienie i-tego bitu
        }
    }
    return bits;
}
```

**2. Funkcja `BitsToBytes`**

**Wejście:**  
- `bits` (List<int>) - lista bitów do konwersji (wartości 0 i 1)

**Wyjście:**  
- `byte[]` - tablica bajtów powstała z połączenia bitów

**Opis:**  
Odwrotna operacja do `BytesToBits`. Łączy grupy po 8 bitów w pojedyncze bajty. Jeśli liczba bitów nie jest podzielna przez 8, ostatni bajt jest uzupełniany zerami z prawej strony (najmniej znaczące bity). Bity są składane w bajty w kolejności od najbardziej znaczącego.

**Kod:**
``` C#
static byte[] BitsToBytes(List<int> bits)
{
    List<byte> outBytes = new List<byte>();
    for (int i = 0; i < bits.Count; i += 8)
    {
        byte byteValue = 0;
        for (int j = 0; j < 8 && i + j < bits.Count; j++)
        {
            byteValue = (byte)((byteValue << 1) | bits[i + j]); // Składanie bajtu z bitów
        }
        outBytes.Add(byteValue);
    }
    return outBytes.ToArray();
}
```

**3. Funkcja `BerlekampMassey`**

**Wejście:**  
- `s` (List<int>) - fragment strumienia bitów (sekwencka znanych bitów)

**Wyjście:**  
- krotka `(int L, List<int> C)`:
  - `L` - minimalna długość rejestru LFSR
  - `C` - wielomian charakterystyczny (współczynniki od x^0 do x^L)

**Opis:**  
Implementuje algorytm Berlekampa-Massey'a służący do identyfikacji parametrów LFSR na podstawie fragmentu jego outputu. Algorytm iteracyjnie znajduje najkrótszy rejestr przesuwny, który mógł wygenerować daną sekwencję. Wykorzystuje aktualizację wielomianu charakterystycznego i długości rejestru w każdej iteracji.

**Kod:**
``` C#
static (int L, List<int> C) BerlekampMassey(List<int> s)
{
    int n = s.Count;
    List<int> C = new List<int>(new int[n + 1]); // Wielomian charakterystyczny
    C[0] = 1; // Inicjalizacja C(x) = 1
    List<int> B = new List<int>(new int[n + 1]); // Poprzedni wielomian
    B[0] = 1; // Inicjalizacja B(x) = 1
    int L = 0; // Aktualna długość LFSR
    int m = 1; // Licznik przesunięć

    for (int i = 0; i < n; i++)
    {
        // Obliczenie różnicy (d) między przewidywanym a rzeczywistym bitem
        int d = s[i];
        for (int j = 1; j <= L; j++)
        {
            d ^= C[j] & s[i - j]; // XOR z poprzednimi bitami
        }

        if (d != 0) // Jeśli różnica niezerowa, aktualizacja wielomianu
        {
            List<int> T = new List<int>(C); // Kopia aktualnego wielomianu
            for (int j = 0; j < B.Count; j++)
            {
                if (B[j] != 0)
                {
                    if (j + m < C.Count)
                        C[j + m] ^= 1; // Aktualizacja C przez XOR z przesuniętym B
                }
            }
            if (2 * L <= i) // Jeśli długość LFSR jest za mała
            {
                L = i + 1 - L; // Zwiększ długość LFSR
                B = new List<int>(T); // Zapisz poprzedni wielomian
                m = 1; // Reset licznika
            }
            else
            {
                m++; // Inkrementuj licznik
            }
        }
        else
        {
            m++; // Inkrementuj licznik
        }
    }

    return (L, C.GetRange(0, L + 1)); // Zwróć długość i wielomian
}
```

**4. Funkcja `GenerateKeystream`**

**Wejście:**  
- `iv` (List<int>) - wektor inicjujący (początkowy stan rejestru)
- `taps` (List<int>) - lista pozycji sprzężeń zwrotnych
- `length` (int) - żądana długość strumienia wyjściowego

**Wyjście:**  
- `List<int>` - wygenerowany strumień pseudolosowy

**Opis:**  
Generuje strumień klucza przy użyciu rejestru LFSR o podanych parametrach. W każdej iteracji oblicza nowy bit jako XOR bitów na pozycjach określonych przez `taps`, przesuwa rejestr i dodaje ostatni bit do strumienia wyjściowego. Gwarantuje generację dokładnie `length` bitów.

**Kod:**
``` C#
static List<int> GenerateKeystream(List<int> iv, List<int> taps, int length)
{
    List<int> state = new List<int>(iv); // Stan początkowy (IV)
    List<int> ks = new List<int>(); // Strumień klucza

    for (int i = 0; i < length; i++)
    {
        ks.Add(state[state.Count - 1]); // Dodaj ostatni bit stanu
        int newBit = 0;
        foreach (int t in taps)
        {
            newBit ^= state[t]; // Oblicz nowy bit (XOR z tapami)
        }
        state.Insert(0, newBit); // Wstaw nowy bit na początek
        state.RemoveAt(state.Count - 1); // Usuń ostatni bit
    }

    return ks;
}
```

**5. Funkcja `Main`**

**Wejście:**  
- `args` (string[]) - argumenty wiersza poleceń:
  - `args[0]` - ścieżka do zaszyfrowanego pliku
  - `args[1]` - ścieżka do pliku z fragmentem plaintextu
  - `args[2]` - ścieżka do pliku wynikowego

**Wyjście:**  
- Brak (efekty zapisywane do pliku i konsoli)

**Opis:**  
Główna funkcja realizująca atak ze znanym fragmentem tekstu. Wykonuje:
1. Wczytanie i konwersję danych wejściowych
2. Rekonstrukcję fragmentu strumienia klucza
3. Identyfikację parametrów LFSR
4. Generację pełnego strumienia klucza
5. Odszyfrowanie danych
6. Weryfikację poprawności przez dekodowanie UTF-8
7. Zapis wyników i diagnostykę

Dodatkowo oblicza i wyświetla minimalną wymaganą długość znanego tekstu oraz maksymalny okres sekwencji LFSR.

**Kod:**
``` C#
static void Main(string[] args)
{
    // Sprawdzenie argumentów
    if (args.Length != 3)
    {
        Console.WriteLine("Użycie: LFSRCKPA <ciphertext> <plaintext_fragment> <output_text>");
        Environment.Exit(1);
    }

    string ctFile = args[0]; // Plik szyfrogramu
    string fragFile = args[1]; // Plik fragmentu plaintextu
    string outText = args[2]; // Plik wyjściowy

    // Odczyt i konwersja na bity
    byte[] ct = File.ReadAllBytes(ctFile);
    byte[] frag = File.ReadAllBytes(fragFile);
    List<int> ctBits = BytesToBits(ct);
    List<int> fragBits = BytesToBits(frag);

    // Generowanie fragmentu strumienia klucza (XOR fragmentu plaintextu i szyfrogramu)
    int nFrag = fragBits.Count;
    List<int> ksFrag = new List<int>();
    for (int i = 0; i < nFrag; i++)
    {
        ksFrag.Add(fragBits[i] ^ ctBits[i]);
    }

    // Znajdowanie parametrów LFSR
    var (L, C) = BerlekampMassey(ksFrag);
    Console.WriteLine($"Zidentyfikowane LFSR: L = {L}, wektor C = [{string.Join(", ", C)}]");

    // Obliczenie minimalnej wymaganej długości i maksymalnego okresu
    int required = 2 * L;
    int maxPeriod = (1 << L) - 1;
    Console.WriteLine($"Minimalna długość znanego tekstu do pełnego odzyskania: {required} bitów");
    Console.WriteLine($"Maksymalny okres sekwencji: {maxPeriod} bitów");
    if (nFrag < required)
    {
        Console.WriteLine($"Uwaga: użyto {nFrag} bitów; potrzeba co najmniej {required} bitów.");
    }

    // Wyodrębnienie IV i tapów z wielomianu charakterystycznego
    List<int> iv = ksFrag.GetRange(0, L);
    List<int> taps = new List<int>();
    for (int j = 1; j < C.Count; j++)
    {
        if (C[j] == 1)
        {
            taps.Add(j - 1); // Pozycje tapów odpowiadają współczynnikom 1 w wielomianie
        }
    }
    Console.WriteLine($"IV (pierwsze {L} bitów): [{string.Join(", ", iv)}]");
    Console.WriteLine($"Tapy: [{string.Join(", ", taps)}]");

    // Generowanie pełnego strumienia klucza i deszyfrowanie
    List<int> fullKs = GenerateKeystream(iv, taps, ctBits.Count);
    List<int> decBits = new List<int>();
    for (int i = 0; i < ctBits.Count; i++)
    {
        decBits.Add(ctBits[i] ^ fullKs[i]); // XOR szyfrogramu ze strumieniem klucza
    }

    // Konwersja i zapis wyniku
    byte[] decBytes = BitsToBytes(decBits);

    // Próba dekodowania jako UTF-8
    try
    {
        string text = Encoding.UTF8.GetString(decBytes);
        File.WriteAllText(outText, text, Encoding.UTF8);
        Console.WriteLine($"Zdekodowany tekst (UTF-8) zapisano do: {outText}");
    }
    catch (ArgumentException)
    {
        Console.WriteLine("Dekodowanie UTF-8 nie powiodło się; upewnij się, że fragment plaintextu jest wystarczający.");
    }
}
```

#### Wyniki



