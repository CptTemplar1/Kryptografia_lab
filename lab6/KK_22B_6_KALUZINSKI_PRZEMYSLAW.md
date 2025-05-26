# Kryptografia i kryptoanaliza
## Laboratorium 6
### Grupa 22B
### Autorzy: Przemysław Kałuziński, Michał Kaczor

### Zadanie 1

Dokonać implementacji kryptosystemu strumieniowego, którego strumień klucza $k$ generowany jest przy pomocy rejestrów przesuwnych $X$, $Y$ oraz $Z$, gdzie:
- $x_{i+3} = x_i \oplus x_{i+1}$,
- $y_{i+4} = y_i \oplus y_{i+3}$,
- $z_{i+5} = z_i \oplus z_{i+2}$,

natomiast i-ty bit strumienia klucza określony jest funkcją łączącą:

$$k_i = f(x_i, y_i, z_i) = x_i y_i \oplus y_i z_i \oplus z_i.$$

Kryptosystem taki powinien mieć zdefiniowane metody:
- szyfrowania danych pobranych z pliku oraz zapisu szyfrogramu do wskazanego pliku,
- jak również odszyfrowania szyfrogramu i zapisania wyniku do określonego pliku.

**Uwagi:**  
1. Jeżeli:
   - $L_X$ jest długością cyklu generowanego przez rejestr przesuwny $X$, a $L_Y$ i $L_Z$ są długościami cykli rejestrów $Y$ oraz $Z$, to strumień klucza wygenerowany przez podany kryptosystem będzie miał długość: $\text{lcm}(L_X, L_Y, L_Z)$, gdzie $\text{lcm}$ to najmniejsza wspólna wielokrotność.
   - Dla zdefiniowanego w ramach zadania kryptosystemu, długość cyklu generatora klucza będzie wynosić: $L_X = 7$, $L_Y = 15$ i $L_Z = 31$ bitów. Zatem ostatecznie, długość cyklu będzie wynosić 3255 bitów, pod warunkiem, że początkowym wypełnieniem żadnego z rejestrów nie jest wektor zerowy.

2. Z konstrukcji generatora klucza, wynika iż do zainicjowania pracy kryptosystemu, konieczny jest 12 bitowy klucz, określający początkowe wypełnienia rejestrów. Jeżeli początkowe wypełnienia rejestrów wynoszą: 
   - $X$: 011, 
   - $Y$: 0101, 
   - $Z$: 11100,

   to pierwsze 31 bitów generatora powinno być następujące:

| Tabela 1: Bity rejestru i strumień klucza |  
| Bity                              |$i = 0, 1, 2, \dots, 29, 30$                                   |
|-----------------------------------|---------------------------------------------------------------|
| $x_i$                             | 0 1 1 1 0 0 1 1 1 0 1 1 0 0 1 1 0 1 1 0 1 0 1 1 1 1 0 0 1 1 1 |
| $y_i$                             | 0 1 0 1 1 1 0 0 1 1 1 0 0 1 1 1 0 0 1 1 0 0 1 1 0 1 0 0 1 1 0 |
| $z_i$                             | 1 1 1 0 0 0 1 1 1 1 0 1 0 1 1 0 1 1 1 1 0 1 1 1 0 1 0 1 0 0 1 |
| $k_i$                             | 1 1 1 0 0 1 0 0 1 1 1 0 1 1 0 1 1 0 0 0 1 1 1 1 0 1 1 0 1 0 0 |


#### Implementacja

**1. Podział na klasy**

Program został podzielony na dwie główne klasy: `KeyStreamGenerator` i `StreamCipher`. Klasa `KeyStreamGenerator` odpowiada za generowanie strumienia klucza na podstawie rejestrów X, Y i Z, natomiast klasa `StreamCipher` implementuje funkcje szyfrowania i odszyfrowania danych przy użyciu wygenerowanego strumienia klucza.

**2. Funkcja `KeyStreamGenerator: __init__`**

**Wejście:**
- `x_init` (list): Lista 3 bitów inicjalizujących rejestr X.
- `y_init` (list): Lista 4 bitów inicjalizujących rejestr Y.
- `z_init` (list): Lista 5 bitów inicjalizujących rejestr Z.

**Wyjście:**
- Brak bezpośredniego wyjścia. Inicjalizuje obiekt klasy `KeyStreamGenerator`.

**Opis:**
Funkcja inicjalizuje generator strumienia klucza, sprawdzając poprawność długości podanych rejestrów oraz czy żaden z nich nie jest całkowicie zerowy. Następnie kopiuje wartości inicjalizujące do odpowiednich rejestrów przesuwnych (X, Y, Z).


**Kod:**
```python
def __init__(self, x_init, y_init, z_init):
    # Sprawdzenie poprawności długości rejestrów
    if len(x_init) != 3 or len(y_init) != 4 or len(z_init) != 5:
        raise ValueError("Długości inicjalizacyjne muszą wynosić odpowiednio: X=3, Y=4, Z=5")
    # Sprawdzenie czy żaden rejestr nie jest całkowicie zerowy
    if x_init == [0, 0, 0] or y_init == [0, 0, 0, 0] or z_init == [0, 0, 0, 0, 0]:
        raise ValueError("Żaden rejestr nie może być całkowicie zerowy")

    # Inicjalizacja rejestrów przesuwnych
    self.X = x_init.copy()  # Rejestr X - 3 bitowy
    self.Y = y_init.copy()  # Rejestr Y - 4 bitowy
    self.Z = z_init.copy()  # Rejestr Z - 5 bitowy
```

**3. Funkcja `KeyStreamGenerator: _next_bit`**

**Wejście:**
- Brak parametrów wejściowych.

**Wyjście:**
- `ki` (int): Kolejny bit strumienia klucza wygenerowany na podstawie aktualnego stanu rejestrów.

**Opis:**
Funkcja generuje kolejny bit strumienia klucza, wykorzystując aktualne stany rejestrów X, Y i Z. Oblicza nowy bit na podstawie funkcji nieliniowej, aktualizuje rejestry przesuwne zgodnie z ich równaniami sprzężenia zwrotnego i zwraca wygenerowany bit.

**Kod:**
```python
def _next_bit(self):
    # Pobranie pierwszych bitów z każdego rejestru
    xi = self.X[0]  # Pierwszy bit rejestru X
    yi = self.Y[0]  # Pierwszy bit rejestru Y
    zi = self.Z[0]  # Pierwszy bit rejestru Z

    # Funkcja łącząca (nieliniowa): ki = xi*yi XOR yi*zi XOR zi
    ki = (xi & yi) ^ (yi & zi) ^ zi

    # Aktualizacja rejestrów (funkcje sprzężenia zwrotnego)
    x_new = self.X[0] ^ self.X[2]  # xi+3 = xi ⊕ xi+1
    y_new = self.Y[0] ^ self.Y[3]  # yi+4 = yi ⊕ yi+3
    z_new = self.Z[0] ^ self.Z[2]  # zi+5 = zi ⊕ zi+2

    # Przesunięcie rejestrów i dodanie nowych bitów
    self.X = self.X[1:] + [x_new]  # Przesuń X i dodaj nowy bit
    self.Y = self.Y[1:] + [y_new]  # Przesuń Y i dodaj nowy bit
    self.Z = self.Z[1:] + [z_new]  # Przesuń Z i dodaj nowy bit

    return ki  # Zwróć kolejny bit strumienia klucza
```

**4. Funkcja `KeyStreamGenerator: get_key_stream`**

**Wejście:**
- `length` (int): Długość strumienia klucza do wygenerowania.

**Wyjście:**
- `list`: Lista bitów strumienia klucza o zadanej długości.

**Opis:**
Funkcja generuje strumień klucza o określonej długości, wielokrotnie wywołując metodę `_next_bit` i zwracając wynik jako listę bitów.

**Kod:**
```python
def get_key_stream(self, length):
    # Generowanie strumienia klucza o zadanej długości
    return [self._next_bit() for _ in range(length)]
```

**5. Funkcja `StreamCipher: __init__`**

**Wejście:**
- `key_bits` (str): 12-bitowy ciąg znaków '0' i '1' reprezentujący klucz.

**Wyjście:**
- Brak bezpośredniego wyjścia. Inicjalizuje obiekt klasy `StreamCipher`.

**Opis:**
Funkcja waliduje klucz, dzieli go na części odpowiednie dla rejestrów X, Y i Z, a następnie inicjalizuje generator strumienia klucza (`KeyStreamGenerator`) z tymi wartościami.

**Kod:**
```python
def __init__(self, key_bits):  # key_bits to 12-bitowy ciąg znaków '0' i '1'
    # Walidacja klucza
    if len(key_bits) != 12 or any(c not in '01' for c in key_bits):
        raise ValueError("Klucz musi być łańcuchem 12-bitowym składającym się z 0 i 1")

    # Podział klucza na części dla poszczególnych rejestrów
    x_init = [int(b) for b in key_bits[0:3]]   # 3 bity dla X
    y_init = [int(b) for b in key_bits[3:7]]   # 4 bity dla Y
    z_init = [int(b) for b in key_bits[7:12]]  # 5 bitów dla Z

    # Inicjalizacja generatora strumienia klucza
    self.generator = KeyStreamGenerator(x_init, y_init, z_init)
```

**6. Funkcja `StreamCipher: _bytes_to_bits`**

**Wejście:**
- `byte_data` (bytes): Dane bajtowe do konwersji na bity.

**Wyjście:**
- `list`: Lista bitów reprezentujących przekazane dane bajtowe.

**Opis:**
Funkcja konwertuje dane bajtowe na listę bitów, rozbijając każdy bajt na 8 bitów i łącząc je w jedną listę.

**Kod:**
```python
def _bytes_to_bits(self, byte_data):
    # Konwersja danych bajtowych na listę bitów
    return list(itertools.chain.from_iterable(
        [(byte >> i) & 1 for i in reversed(range(8))] for byte in byte_data))
```

**7. Funkcja `StreamCipher: _bits_to_bytes`**

**Wejście:**
- `bits` (list): Lista bitów do konwersji na bajty.

**Wyjście:**
- `bytes`: Dane bajtowe powstałe z połączenia bitów.

**Opis:**
Funkcja konwertuje listę bitów z powrotem na bajty, grupując bity w bloki po 8 i zamieniając je na odpowiadające wartości bajtów.

**Kod:**
```python
def _bits_to_bytes(self, bits):
    # Konwersja listy bitów z powrotem na bajty
    return bytes([
        sum([bits[i * 8 + j] << (7 - j) for j in range(8)])
        for i in range(len(bits) // 8)
    ])
```

**8. Funkcja `StreamCipher: encrypt`**

**Wejście:**
- `input_file` (str): Ścieżka do pliku wejściowego zawierającego dane do zaszyfrowania.
- `output_file` (str): Ścieżka do pliku wyjściowego, gdzie zostanie zapisany szyfrogram.

**Wyjście:**
- Brak bezpośredniego wyjścia. Zapisuje zaszyfrowane dane do pliku.

**Opis:**
Funkcja odczytuje dane z pliku wejściowego, konwertuje je na bity, generuje strumień klucza o odpowiedniej długości, wykonuje operację XOR na bitach danych i klucza, a następnie zapisuje wynik do pliku wyjściowego w postaci bajtów.

**Kod:**
```python
def encrypt(self, input_file, output_file):
    # Odczyt pliku wejściowego w trybie binarnym
    with open(input_file, 'rb') as f:
        plaintext = f.read()

    # Konwersja tekstu jawnego na bity
    plain_bits = self._bytes_to_bits(plaintext)
    # Generowanie strumienia klucza o długości tekstu jawnego
    key_stream = self.generator.get_key_stream(len(plain_bits))
    # Szyfrowanie poprzez XOR każdego bitu tekstu z bitem klucza
    cipher_bits = [b ^ k for b, k in zip(plain_bits, key_stream)]

    # Konwersja zaszyfrowanych bitów na bajty i zapis do pliku
    ciphertext = self._bits_to_bytes(cipher_bits)
    with open(output_file, 'wb') as f:
        f.write(ciphertext)
```

**9. Funkcja `StreamCipher: decrypt`**

**Wejście:**
- `input_file` (str): Ścieżka do pliku wejściowego zawierającego szyfrogram.
- `output_file` (str): Ścieżka do pliku wyjściowego, gdzie zostanie zapisany odszyfrowany tekst.

**Wyjście:**
- Brak bezpośredniego wyjścia. Zapisuje odszyfrowane dane do pliku.

**Opis:**
Funkcja wykorzystuje metodę `encrypt` do odszyfrowania danych, ponieważ operacja XOR jest odwracalna. Wymaga ponownej inicjalizacji generatora strumienia klucza z tym samym kluczem.

**Kod:**
```python
def decrypt(self, input_file, output_file):
    # Deszyfrowanie to to samo co szyfrowanie (XOR jest odwracalny)
    self.encrypt(input_file, output_file) 
```

**10. Funkcja `Main`**

**Wejście:**
- Brak parametrów wejściowych.

**Wyjście:**
- Brak bezpośredniego wyjścia. Wykonuje przykładowe szyfrowanie i deszyfrowanie plików.

**Opis:**
Funkcja demonstruje użycie klasy `StreamCipher`, inicjalizując szyfr z przykładowym kluczem, szyfrując plik `plain.txt` do `cipher.txt`, a następnie deszyfrując go z powrotem do `decrypted.txt`.

**Kod:**
```python
if __name__ == "__main__":
    # Przykładowy 12-bitowy klucz
    klucz = "011010111100"  # X: 011, Y: 0101, Z: 11100

    # Inicjalizacja szyfru strumieniowego
    szyfr = StreamCipher(klucz)

    # Szyfrowanie pliku
    szyfr.encrypt("plain.txt", "cipher.txt")

    # Deszyfrowanie pliku (wymaga nowej instancji z tym samym kluczem)
    szyfr = StreamCipher(klucz)
    szyfr.decrypt("cipher.txt", "decrypted.txt")
```

#### Wyniki

W ramach zadania 1 zaimplementowano kryptosystem strumieniowy wykorzystujący trzy rejestry przesuwne (LFSR) X, Y i Z do generowania strumienia klucza. Rejestry zostały skonfigurowane zgodnie z podanymi równaniami sprzężenia zwrotnego:
- Rejestr X: $x_{i+3} = x_i \oplus x_{i+1}$ (długość cyklu: 7 bitów)
- Rejestr Y: $y_{i+4} = y_i \oplus y_{i+3}$ (długość cyklu: 15 bitów)
- Rejestr Z: $z_{i+5} = z_i \oplus z_{i+2}$ (długość cyklu: 31 bitów)

Strumień klucza generowany był za pomocą nieliniowej funkcji łączącej:  
$$k_i = x_i y_i \oplus y_i z_i \oplus z_i.$$

**Proces szyfrowania:**  
Program został uruchomiony z przykładowym 12-bitowym kluczem `011010111100`, który odpowiada następującym wypełnieniom rejestrów:
- X: `[0, 1, 1]`
- Y: `[0, 1, 0, 1]`
- Z: `[1, 1, 1, 0, 0]`

Do uruchomienia programu użyto polecenia `python zad1.py`, które w pierwszej kolejności spowodowało zaszyfrowanie pliku `plain.txt` i zapisanie wyniku do pliku `cipher.txt`. 

**Tekst jawny: plik `plain.txt`:**
```plaintext
CALL me Ishmael. Some years ago never mind how 
long precisely having little or no money in my purse, 
and nothing particular to interest me on shore, I thought 
I would sail about a little and see the watery part of the 
world. It is a way I have of driving off the spleen, and 
regulating the circulation. Whenever I find myself 
growing grim about the mouth ; whenever it is a damp, 
drizzly November in my soul ; whenever I find myself 
involuntarily pausing before coffin warehouses, and bring- 
ing up the rear of every funeral I meet ; and especially 
whenever my hypos get such an upper hand of me, that 
it requires a strong moral principle to prevent me from 
deliberately stepping into the street, and methodically 
knocking people's hats off then, I account it high time 
to get to sea as soon as I can. This is my substitute for 
pistol and ball. With a philosophical flourish Cato throws 
himself upon his sword ; I quietly take to the ship. 
There is nothing surprising in this. If they but knew 
it, almost all men in their degree, some time or other, 
cherish very nearly the same feelings toward the ocean 
with me. 
```

**Szyfrogram: plik`cipher.txt`:**
```plaintext
±(×+ćő^Ä¤O"|M(A±áq[AśÖ0î’WîśÇ)xU‘ó˘'»WüÓĚtršÂéŚ1:¸Ä©Ń
T6đ'ýIŚ¬
ĂjŐ>D"†đ	–µb$ÝÓúľLkßGŠŞŁö€3Ćż 9wj†­HNí
&ťŰĹűë^3ĂŁĚ2ôä ĚĄby+˝ó‚ ˇI”–±dĂ¸ń×ťťÂę‚ éŚÝ%˝LŰ:Ódä_ŤK•<t.‹ˇ ül‰ź7.ăřŢvÉkĘZ5Ý(Ď’é­h«„¬čă.ČIÇĄČüsŢmËţÇ¶ŐYČŃ°#$‘ąě»‚(l«Śłăý˝N– ‡ŹAűt
ŞÂLŹ¶Üh“K­CëdiľZś-Ć/ô4¦˙9ÍŰ]š˛S'ŘN}–­‰n"—fşÓ±o?7‰ĄV	qŔË ű\ëÜŐýÂ[KŽ÷p¶ÄÔŚąä?= öţM…â–@îÎŹ´ń
®Z_ź÷ý7ż[­Ú.łZqŁ,Đ4í"Ŕňů ‹}†¶Dďä^bŽ=ńO<¨ĺG˛t]¦Ą–ĄrD
z‰Ş®W>š°Ëř˝§mĐ0i1_ź¸ż#5JÜŘŇÖđČ°ĘjňT8yă¨[ŘX!Ŕ>śVĽ€Ó}—ŰG'†ĺ7
’Ţż§sZÂqĂ>ŽDTś˙ô;ĽHôĆµE(kkúçÉ3K^f?ŽG4ÓŽĹ‡á˝cťÓăpŻT†˛‡6´;ŮŁäkË·_
¤Ťđ ˛¸›śQÓ—wň3´B¨ĄÔ[ďk]zO9ůDÎśź0¨4ŐÜůÖżť5|„ż¦Ľč+ŕéŔ<<^TôŁCt&<‘ďč›“đÉĄŐb
ěőS`?Ř›Ą¤0)‰ÍÓă<¶•ŢáůĂĺ6Śŕ¦¸ą[Ď[ˇ÷+ÇJÝ†…G×ŻIĄĘ)· [–â:±ľôŠuź&ÍNV’7ďŻF‘˙jWňTŔ¨!BJ.Ľß ` ÉłÖbç˛Ź—>µGŐűĚz P/„¶ÍzýŃ€MżĆOá8˙’N°4€–rö!ĎÄŽSÖ
ţÚQéŐđt@‰˝_Ď?ś›âQŮîÔĆ°sV»ŻEĽéu ú§Îo[T&ďäüeÉ!Śµ“űúÖG›0
*ń˘¤ĄÍ~x<ŇÚmáŻ•™Î#őŇ­ü’tžĘć8şČˇ™ILz9c"Ęî9ÓĘ|ŇÔUÁ:ŐęéMsŹcŻe¬VX§Î9hEÉŁ$Đp„Ó“dbž‹¶×ř•—=ý;Cu8’ťńĂ5©z5—ÔĄÜ¤
ŻÜkăÉtý·ś5WE^öý(‘Z¬:ŐÎî€?F·wz„Ż»-üvŮ†`Cj˙TÉbË°î3žâĎ˘t{VŁ¦T=čď`Ĺ#{$ŠÂ˘ÓČU¦%ŹoďźŃđÓ„&¬`ĄÚ»ůüĘL™ŔgďI¤ż/} ×Ť¶"üK=€}˝OR\©Q·$ÚČoý:ÉÜ´ąŇFÉ*ăŔľ
```

**Proces deszyfrowania:**  
Zaszyfrowany plik (`cipher.txt`) został następnie odszyfrowany z użyciem tego samego klucza, co potwierdziło poprawność implementacji. Odszyfrowany tekst (plik `decrypted.txt`) był identyczny z oryginalnym tekstem jawnym.

**Tekst odszyfrowany: plik `decrypted.txt`:**  
```plaintext
CALL me Ishmael. Some years ago never mind how 
long precisely having little or no money in my purse, 
and nothing particular to interest me on shore, I thought 
I would sail about a little and see the watery part of the 
world. It is a way I have of driving off the spleen, and 
regulating the circulation. Whenever I find myself 
growing grim about the mouth ; whenever it is a damp, 
drizzly November in my soul ; whenever I find myself 
involuntarily pausing before coffin warehouses, and bring- 
ing up the rear of every funeral I meet ; and especially 
whenever my hypos get such an upper hand of me, that 
it requires a strong moral principle to prevent me from 
deliberately stepping into the street, and methodically 
knocking people's hats off then, I account it high time 
to get to sea as soon as I can. This is my substitute for 
pistol and ball. With a philosophical flourish Cato throws 
himself upon his sword ; I quietly take to the ship. 
There is nothing surprising in this. If they but knew 
it, almost all men in their degree, some time or other, 
cherish very nearly the same feelings toward the ocean 
with me. 
```

Implementacja kryptosystemu działa zgodnie z założeniami. Operacja XOR na bitach tekstu jawnego i strumienia klucza jest w pełni odwracalna, co pozwoliło na poprawne odszyfrowanie wiadomości. Długość cyklu generatora klucza wynosząca 3255 bitów (LCM(7, 15, 31)) zapewnia wystarczającą losowość strumienia klucza dla krótkich wiadomości.

### Zadanie 2

Dokonać ataku korelacyjnego na zbudowany w ramach pierwszego zadania kryptosystem, przyjmując iż znany jest szyfrogram i odpowiadające mu dane jawne. Zadaniem jest odzyskanie klucza a następnie początkowych wypełnień rejestrów generatora strumienia klucza kryptosystemu.

**Uwagi:**
1. Zgodnie z zasadą Kreckhoff’a, do dalszej pracy należy przyjąć, iż atakujący zna:
- funkcje sprzężenia zwrotnego LFSR,
- oraz nieliniową funkcję bool’owską f .  
  Atakujący nie zna klucza (początkowych wypełnień LFSR), którą zaszyfrowano wiadomość.
2. Tabela prawdy funkcji logicznej f ujawnia, iż: f (x, y, z) = x oraz f (x, y, z) = z zachodzi z prawdopodobieństwem równym $\frac{3}{4}$.

| Tabela 2: Tabela prawdy dla zdefiniowanej funkcji f |  
| x | y | z | xy | yz | f |
|---|---|---|----|----|---|
| 0 | 0 | 0 | 0  | 0  | 0 |
| 0 | 0 | 1 | 0  | 0  | 1 |
| 0 | 1 | 0 | 0  | 0  | 0 |
| 0 | 1 | 1 | 0  | 1  | 0 |
| 1 | 0 | 0 | 0  | 0  | 0 |
| 1 | 0 | 1 | 0  | 0  | 1 |
| 1 | 1 | 0 | 1  | 0  | 1 |
| 1 | 1 | 1 | 1  | 1  | 1 |

Atakujący może wykorzystać ten fakt do odzyskania początkowych wypełnień rejestrów X oraz Z generatora strumienia klucza. Można tego dokonać w następujący sposób:

- Wygenerować zbiór wszystkich możliwych permutacji początkowego wypełnienia wybranego rejestru (np. rejestru X).
- Dla każdej permutacji wygenerować strumień klucza (np. strumień składający się z 31 bitów).
- Wybrać jedną z opcji:
  - Porównać bity odzyskanego strumienia klucza z bitami strumienia wygenerowanego przez analizowany rejestr dla danej permutacji. Jeżeli zachodzi zgodność pomiędzy tymi bitami z prawdopodobieństwem bliskim $\frac{3}{4}$, to można uznać, iż dane początkowe wypełnienie jest poszukiwanym wypełnieniem.
  - Alternatywnie można zbudować funkcję obliczającą współczynnik korelacji Pearsona (Algorytm 1) dla dwóch bitowych strumieni kluczy, odzyskanego strumienia klucza i wygenerowanego przez analizowany rejestr dla danej permutacji początkowej. Następnie wybrać taką permutację, dla której wartość bezwzględna różnicy pomiędzy jednością a obliczonym współczynnikiem korelacji będzie najmniejsza.

3. Przedstawionej techniki nie można zastosować do odzyskania początkowego wypełnienia rejestru Y. Wynika to z faktu, iż prawdopodobieństwo f(x, y, z) = y wynosi dokładnie $\frac{1}{2}$; jednakże znając początkowe wypełnienia rejestrów X oraz Z można odzyskać początkowe wypełnienie rejestru Y stosując technikę *wyczerpującego wyszukiwania*.

#### Implementacja

**1. Podział na klasy**

Program został podzielony na dwie główne klasy: `KeyStreamGenerator` i `CorrelationAttack`. Klasa `KeyStreamGenerator` jest taka sama jak w zadaniu 1 i odpowiada za generowanie strumienia klucza, natomiast klasa `CorrelationAttack` implementuje atak korelacyjny na rejestry X, Y i Z.

**2. Funkcja `CorrelationAttack: __init__`**

**Wejście:**
- `known_plaintext` (bytes): Tekst jawny w postaci bajtów, znany atakującemu.
- `known_ciphertext` (bytes): Szyfrogram w postaci bajtów, odpowiadający znanemu tekstowi jawnemu.

**Wyjście:**
- Brak bezpośredniego wyjścia. Inicjalizuje obiekt klasy `CorrelationAttack`.

**Opis:**
Funkcja inicjalizuje atak korelacyjny, konwertując znane dane (tekst jawny i szyfrogram) na bity, odtwarzając strumień klucza poprzez operację XOR oraz przygotowując licznik operacji do statystyk wydajności.

**Kod:**
```python
def __init__(self, known_plaintext, known_ciphertext):
    # Inicjalizacja ataku korelacyjnego z znanym tekstem jawnym i szyfrogramem
    self.known_plain_bits = self._bytes_to_bits(known_plaintext)
    self.known_cipher_bits = self._bytes_to_bits(known_ciphertext)
    # Odtworzenie strumienia klucza poprzez XOR tekstu jawnego i szyfrogramu
    self.recovered_key_bits = [p ^ c for p, c in zip(self.known_plain_bits, self.known_cipher_bits)]
    self.operations_count = 0  # Licznik operacji dla statystyk wydajności
```

**3. Funkcja `CorrelationAttack: _bytes_to_bits`**

**Wejście:**
- `byte_data` (bytes): Dane bajtowe do konwersji na bity.

**Wyjście:**
- `list`: Lista bitów reprezentujących przekazane dane bajtowe.

**Opis:**
Funkcja konwertuje dane bajtowe na listę bitów, rozbijając każdy bajt na 8 bitów i łącząc je w jedną listę.

**Kod:**
```python
def _bytes_to_bits(self, byte_data):
    # Konwersja danych bajtowych na listę bitów
    return list(itertools.chain.from_iterable(
        [(byte >> i) & 1 for i in reversed(range(8))] for byte in byte_data))
```

**4. Funkcja `CorrelationAttack: _pearson_correlation`**

**Wejście:**
- `stream1` (list): Pierwszy strumień bitów do porównania.
- `stream2` (list): Drugi strumień bitów do porównania.

**Wyjście:**
- `float`: Wartość współczynnika korelacji Pearsona między strumieniami.

**Opis:**
Funkcja oblicza współczynnik korelacji Pearsona między dwoma strumieniami bitów, mierząc stopień ich liniowej zależności. Aktualizuje również licznik operacji dla celów statystycznych.

**Kod:**
```python
def _pearson_correlation(self, stream1, stream2):
    # Obliczenie współczynnika korelacji Pearsona między dwoma strumieniami bitów
    n = min(len(stream1), len(stream2))
    if n == 0:
        return 0
        
    sum1 = sum(stream1[:n])
    sum2 = sum(stream2[:n])
    
    sum1_sq = sum(x*x for x in stream1[:n])
    sum2_sq = sum(x*x for x in stream2[:n])
    
    p_sum = sum(x*y for x, y in zip(stream1[:n], stream2[:n]))
    
    num = p_sum - (sum1 * sum2 / n)
    den = math.sqrt((sum1_sq - sum1**2 / n) * (sum2_sq - sum2**2 / n))
    
    self.operations_count += 10 + 6*n  # Aktualizacja licznika operacji
    
    if den == 0:
        return 0
        
    return num / den
```

**5. Funkcja `CorrelationAttack: _generate_x_stream`**

**Wejście:**
- `x_init` (list): Lista 3 bitów inicjalizujących rejestr X.
- `length` (int): Długość generowanego strumienia bitów.

**Wyjście:**
- `list`: Strumień bitów wygenerowany przez rejestr X.

**Opis:**
Funkcja generuje strumień bitów na podstawie początkowego wypełnienia rejestru X, stosując jego wielomian przesuwający. Aktualizuje licznik operacji.

**Kod:**
```python
def _generate_x_stream(self, x_init, length):
    # Generowanie strumienia bitów z rejestru X na podstawie początkowego wypełnienia
    x_reg = x_init.copy()
    stream = []
    for _ in range(length):
        stream.append(x_reg[0])
        x_new = x_reg[0] ^ x_reg[2]  # Wielomian przesuwający dla rejestru X
        x_reg = x_reg[1:] + [x_new]
        self.operations_count += 5  # Aktualizacja licznika operacji
    return stream
```

**6. Funkcja `CorrelationAttack: _generate_z_stream`**

**Wejście:**
- `z_init` (list): Lista 5 bitów inicjalizujących rejestr Z.
- `length` (int): Długość generowanego strumienia bitów.

**Wyjście:**
- `list`: Strumień bitów wygenerowany przez rejestr Z.

**Opis:**
Funkcja generuje strumień bitów na podstawie początkowego wypełnienia rejestru Z, stosując jego wielomian przesuwający. Aktualizuje licznik operacji.

**Kod:**
```python
def _generate_z_stream(self, z_init, length):
    # Generowanie strumienia bitów z rejestru Z na podstawie początkowego wypełnienia
    z_reg = z_init.copy()
    stream = []
    for _ in range(length):
        stream.append(z_reg[0])
        z_new = z_reg[0] ^ z_reg[2]  # Wielomian przesuwający dla rejestru Z
        z_reg = z_reg[1:] + [z_new]
        self.operations_count += 5
    return stream
```

**7. Funkcja `CorrelationAttack: _generate_y_stream`**

**Wejście:**
- `y_init` (list): Lista 4 bitów inicjalizujących rejestr Y.
- `length` (int): Długość generowanego strumienia bitów.

**Wyjście:**
- `list`: Strumień bitów wygenerowany przez rejestr Y.

**Opis:**
Funkcja generuje strumień bitów na podstawie początkowego wypełnienia rejestru Y, stosując jego wielomian przesuwający. Aktualizuje licznik operacji.

**Kod:**
```python
def _generate_y_stream(self, y_init, length):
    # Generowanie strumienia bitów z rejestru Y na podstawie początkowego wypełnienia
    y_reg = y_init.copy()
    stream = []
    for _ in range(length):
        stream.append(y_reg[0])
        y_new = y_reg[0] ^ y_reg[3]  # Wielomian przesuwający dla rejestru Y
        y_reg = y_reg[1:] + [y_new]
        self.operations_count += 5
    return stream
```

**8. Funkcja `CorrelationAttack: attack_x_register`**

**Wejście:**
- Brak parametrów wejściowych.

**Wyjście:**
- `list`: Najlepsze znalezione wypełnienie rejestru X.

**Opis:**
Funkcja przeprowadza atak korelacyjny na rejestr X, testując wszystkie możliwe inicjalizacje (z wyjątkiem wektora zerowego) i wybierając tę, której strumień najlepiej koreluje z odzyskanym strumieniem klucza. Wypisuje statystyki przetestowanych kandydatów.

**Kod:**
```python
def attack_x_register(self):
    # Atak korelacyjny na rejestr X (3-bitowy)
    best_corr = -1
    best_x_init = None
    total_candidates = 0
    
    # Przetestuj wszystkie możliwe inicjalizacje rejestru X (z wyjątkiem wektora zerowego)
    for x_init in itertools.product([0,1], repeat=3):
        if sum(x_init) == 0:
            continue
            
        total_candidates += 1
        x_stream = self._generate_x_stream(list(x_init), len(self.recovered_key_bits))
        corr = self._pearson_correlation(self.recovered_key_bits, x_stream)
        
        if abs(corr - 1/3) < abs(best_corr - 1/3) or best_corr == -1:
            best_corr = corr
            best_x_init = list(x_init)
            
    print(f"Przetestowano {total_candidates} kandydatów dla rejestru X")
    return best_x_init
```

**9. Funkcja `CorrelationAttack: attack_z_register`**

**Wejście:**
- Brak parametrów wejściowych.

**Wyjście:**
- `list`: Najlepsze znalezione wypełnienie rejestru Z.

**Opis:**
Funkcja przeprowadza atak korelacyjny na rejestr Z, testując wszystkie możliwe inicjalizacje (z wyjątkiem wektora zerowego) i wybierając tę, której strumień najlepiej koreluje z odzyskanym strumieniem klucza. Wypisuje statystyki przetestowanych kandydatów.

**Kod:**
```python
def attack_z_register(self):
    # Atak korelacyjny na rejestr Z (5-bitowy)
    best_corr = -1
    best_z_init = None
    total_candidates = 0
    
    # Przetestuj wszystkie możliwe inicjalizacje rejestru Z (z wyjątkiem wektora zerowego)
    for z_init in itertools.product([0,1], repeat=5):
        if sum(z_init) == 0:
            continue
            
        total_candidates += 1
        z_stream = self._generate_z_stream(list(z_init), len(self.recovered_key_bits))
        corr = self._pearson_correlation(self.recovered_key_bits, z_stream)
        
        if abs(corr - 1/3) < abs(best_corr - 1/3) or best_corr == -1:
            best_corr = corr
            best_z_init = list(z_init)
            
    print(f"Przetestowano {total_candidates} kandydatów dla rejestru Z")
    return best_z_init
```

**10. Funkcja `CorrelationAttack: attack_y_register`**

**Wejście:**
- `x_init` (list): Znalezione wypełnienie rejestru X.
- `z_init` (list): Znalezione wypełnienie rejestru Z.

**Wyjście:**
- `list`: Najlepsze znalezione wypełnienie rejestru Y.

**Opis:**
Funkcja odzyskuje wypełnienie rejestru Y poprzez wyczerpujące wyszukiwanie, wykorzystując znane już wypełnienia rejestrów X i Z. Wypisuje statystyki przetestowanych kandydatów.

**Kod:**
```python
def attack_y_register(self, x_init, z_init):
    # Atak korelacyjny na rejestr Y (4-bitowy) po znalezieniu X i Z
    best_corr = -1
    best_y_init = None
    total_candidates = 0
    
    # Przetestuj wszystkie możliwe inicjalizacje rejestru Y (z wyjątkiem wektora zerowego)
    for y_init in itertools.product([0,1], repeat=4):
        if sum(y_init) == 0:
            continue
            
        total_candidates += 1
        # Symulacja pełnego generatora klucza z aktualnymi kandydatami X i Z
        generator = KeyStreamGenerator(x_init, list(y_init), z_init)
        key_stream = generator.get_key_stream(len(self.recovered_key_bits))
        
        corr = self._pearson_correlation(self.recovered_key_bits, key_stream)
        
        if corr > best_corr:
            best_corr = corr
            best_y_init = list(y_init)
            
    print(f"Przetestowano {total_candidates} kandydatów dla rejestru Y")
    return best_y_init
```

**11. Funkcja `CorrelationAttack: full_attack`**

**Wejście:**
- Brak parametrów wejściowych.

**Wyjście:**
- `tuple`: Krotka zawierająca wypełnienia rejestrów X, Y i Z.

**Opis:**
Funkcja wykonuje pełny atak korelacyjny, kolejno odzyskując wypełnienia rejestrów X, Z i Y. Mierzy czas wykonania oraz liczbę operacji, wypisując szczegółowe statystyki wydajności.

**Kod:**
```python
def full_attack(self):
    # Pełny atak korelacyjny na wszystkie rejestry X, Y, Z
    start_time = time.time()
    self.operations_count = 0
    
    print("\nRozpoczęcie ataku korelacyjnego...")
    print(f"Długość analizowanego strumienia: {len(self.recovered_key_bits)} bitów")
    
    print("\nAtak na rejestr X...")
    x_init = self.attack_x_register()
    print(f"Znalezione początkowe wypełnienie X: {x_init}")
    
    print("\nAtak na rejestr Z...")
    z_init = self.attack_z_register()
    print(f"Znalezione początkowe wypełnienie Z: {z_init}")
    
    print("\nAtak na rejestr Y...")
    y_init = self.attack_y_register(x_init, z_init)
    print(f"Znalezione początkowe wypełnienie Y: {y_init}")
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print("\nStatystyki wydajności:")
    print(f"Czas wykonania: {elapsed_time:.4f} sekund")
    print(f"Łączna liczba operacji: {self.operations_count}")
    print(f"Operacje na sekundę: {self.operations_count/elapsed_time:.2f}")
    
    return x_init, y_init, z_init
```

**12. Funkcja `KeyStreamGenerator: __init__`**

**Wejście:**
- `x_init` (list): Lista 3 bitów inicjalizujących rejestr X.
- `y_init` (list): Lista 4 bitów inicjalizujących rejestr Y.
- `z_init` (list): Lista 5 bitów inicjalizujących rejestr Z.

**Wyjście:**
- Brak bezpośredniego wyjścia. Inicjalizuje obiekt klasy `KeyStreamGenerator`.

**Opis:**
Funkcja inicjalizuje generator strumienia klucza, sprawdzając poprawność długości podanych rejestrów oraz czy żaden z nich nie jest całkowicie zerowy.

**Kod:**
```python
def __init__(self, x_init, y_init, z_init):
    # Inicjalizacja generatora strumienia klucza z podanymi wypełnieniami rejestrów
    if len(x_init) != 3 or len(y_init) != 4 or len(z_init) != 5:
        raise ValueError("Długości inicjalizacyjne muszą wynosić odpowiednio: X=3, Y=4, Z=5")
    if x_init == [0, 0, 0] or y_init == [0, 0, 0, 0] or z_init == [0, 0, 0, 0, 0]:
        raise ValueError("Żaden rejestr nie może być całkowicie zerowy")

    self.X = x_init.copy()
    self.Y = y_init.copy()
    self.Z = z_init.copy()
```

**13. Funkcja `KeyStreamGenerator: _next_bit`**

**Wejście:**
- Brak parametrów wejściowych.

**Wyjście:**
- `int`: Kolejny bit strumienia klucza.

**Opis:**
Funkcja generuje kolejny bit strumienia klucza na podstawie aktualnego stanu rejestrów X, Y i Z, stosując nieliniową funkcję boolowską i aktualizując rejestry przesuwające.

**Kod:**
```python
def _next_bit(self):
    # Generowanie kolejnego bitu klucza na podstawie bieżącego stanu rejestrów
    xi = self.X[0]
    yi = self.Y[0]
    zi = self.Z[0]

    ki = (xi & yi) ^ (yi & zi) ^ zi  # Funkcja nieliniowa generująca bit klucza

    # Aktualizacja rejestrów przesuwających
    x_new = self.X[0] ^ self.X[2]
    y_new = self.Y[0] ^ self.Y[3]
    z_new = self.Z[0] ^ self.Z[2]

    self.X = self.X[1:] + [x_new]
    self.Y = self.Y[1:] + [y_new]
    self.Z = self.Z[1:] + [z_new]

    return ki
```

**14. Funkcja `KeyStreamGenerator: get_key_stream`**

**Wejście:**
- `length` (int): Długość strumienia klucza do wygenerowania.

**Wyjście:**
- `list`: Lista bitów strumienia klucza o zadanej długości.

**Opis:**
Funkcja generuje strumień klucza o określonej długości, wielokrotnie wywołując metodę `_next_bit`.

**Kod:**
```python
def get_key_stream(self, length):
    # Generowanie strumienia klucza o zadanej długości
    return [self._next_bit() for _ in range(length)]
```

**15. Funkcja `Main`**

**Wejście:**
- `sys.argv[1]` (str): Ścieżka do pliku z tekstem jawnym.
- `sys.argv[2]` (str): Ścieżka do pliku z szyfrogramem.

**Wyjście:**
- Brak bezpośredniego wyjścia. Wypisuje wyniki ataku na standardowe wyjście.

**Opis:**
Funkcja główna programu, która wczytuje dane wejściowe, inicjalizuje atak korelacyjny, wykonuje go i wypisuje odzyskany klucz oraz statystyki. Obsługuje również błędy związane z nieprawidłowymi danymi wejściowymi.

**Kod:**
```python
if __name__ == "__main__":
    # Główna funkcja wykonująca atak na podstawie plików wejściowych
    if len(sys.argv) != 3:
        print("Użycie: python zad2_atak.py plik_jawny.txt plik_szyfrogram.txt")
        sys.exit(1)
        
    plain_file = sys.argv[1]
    cipher_file = sys.argv[2]
    
    try:
        with open(plain_file, "rb") as f:
            known_plaintext = f.read()
        
        with open(cipher_file, "rb") as f:
            known_ciphertext = f.read()
            
        print(f"Wczytano {len(known_plaintext)} bajtów tekstu jawnego")
        print(f"Wczytano {len(known_ciphertext)} bajtów szyfrogramu")
        
        attacker = CorrelationAttack(known_plaintext, known_ciphertext)
        x_init, y_init, z_init = attacker.full_attack()
        
        key_bits = ''.join(map(str, x_init + y_init + z_init))
        print(f"\nOdzyskany klucz (12-bitowy): {key_bits}")
        
    except FileNotFoundError:
        print("Błąd: Nie można znaleźć pliku")
        sys.exit(1)
    except Exception as e:
        print(f"Błąd: {str(e)}")
        sys.exit(1)
```

#### Wyniki

W ramach zadania 2 przeprowadzono atak korelacyjny na kryptosystem strumieniowy zaimplementowany w zadaniu 1, wykorzystując znany tekst jawny (`plain.txt`) oraz odpowiadający mu szyfrogram (`cipher.txt`). Celem ataku było odzyskanie 12-bitowego klucza inicjalizującego rejestry X, Y i Z generatora strumienia klucza. Atak wykorzystywał algorytm Pearsona i polegał na analizie statystycznej zależności między odzyskanym strumieniem klucza a generowanymi sekwencjami z poszczególnych rejestrów LFSR.

---
**Współczynnik korelacji Pearsona**

**Algorithm 1** Wyznaczenie współczynnika korelacji Pearsona dla sekwencji bitowych  
**Require:** $x = (x_1, x_2, \ldots, x_n), \, y = (y_1, y_2, \ldots, y_n)$ - wektory bitów (0 lub 1)  

**Ensure:** \(\rho\) - współczynnik korelacji Pearsona  
1: **if** \(|x| \neq |y|\)  
2: **raise** ValueError("Strumienie bitów muszą być tej samej długości")  
3: **end if**  
4: $n \leftarrow |x|$  
5: $\bar{x} \leftarrow \frac{1}{n} \sum_{i=1}^{n} x_i$  
6: $\bar{y} \leftarrow \frac{1}{n} \sum_{i=1}^{n} y_i$  
7: $\texttt{cov}(X, Y) \leftarrow \sum_{i=1}^{n} \frac{(x_i - \bar{x})(y_i - \bar{y})}{n}$  
8: $\texttt{sx} \leftarrow \sqrt{\frac{\sum_{i=1}^{n} (x_i - \bar{x})^2}{n}}$  
9: $\texttt{sy} \leftarrow \sqrt{\frac{\sum_{i=1}^{n} (y_i - \bar{y})^2}{n}}$  
10: $\rho \leftarrow \frac{\texttt{cov}(X, Y)}{\texttt{sx} \cdot \texttt{sy}}$  
11: **return** $\rho$

---

Algorytm Pearsona mierzy liniową zależność między dwoma strumieniami bitów, obliczając wartość z przedziału [-1, 1], gdzie:
- 1 oznacza pełną korelację dodatnią
- -1 oznacza pełną korelację ujemną
- 0 oznacza brak korelacji

Dla rejestrów X i Z oczekiwano wartości bliskiej 0.33 (odpowiadającej teoretycznemu prawdopodobieństwu 3/4 zgodności bitów), natomiast dla rejestru Y - braku korelacji (wartość ~0).

**Przebieg ataku:**
1. **Przygotowanie danych:**
   - Wczytano pliki wejściowe: tekst jawny (1154 bajty) i szyfrogram (1154 bajty).
   - Odtworzono strumień klucza poprzez operację XOR na odpowiadających sobie bitach tekstu jawnego i szyfrogramu (łącznie 9232 bity).

2. **Faza korelacyjna (rejestry X i Z):**
   - Dla każdego możliwego wypełnienia rejestru:
     1) Generowano próbny strumień bitów
     2) Obliczano współczynnik Pearsona między strumieniem próbnym a odzyskanym
     3) Wybierano wypełnienie o współczynniku najbliższym oczekiwanej wartości
   - Dla rejestru X (3 bity) sprawdzono 7 kombinacji
   - Dla rejestru Z (5 bitów) sprawdzono 31 kombinacji

3. **Faza brute-force (rejestr Y):**
   - Po ustaleniu X i Z, przetestowano wszystkie 15 możliwych kombinacji Y
   - Wybrano wersję generującą strumień najbardziej zbliżony do oryginalnego

**Wynik działania programu:**
- **Odzyskany klucz:** `011010111100` (X: `011`, Y: `0101`, Z: `11100`)
- **Statystyki:** 
  - Czas wykonania: 0.2889 sekundy
  - Operacje: 4 690 386 (~16.2 mln operacji/sekundę)
  - Trafność: 100% (klucz zgodny z przykładem z zadania 1)

**Wnioski:**
1. Atak Pearsona okazał się skuteczny dla rejestrów X i Z dzięki silnej korelacji (3/4)
2. Brak korelacji dla rejestru Y wymusił zastosowanie metody brute-force
3. Wydajność algorytmu (~16 mln operacji/sek.) pokazuje praktyczną skuteczność ataku
4. Wynik potwierdza słabość systemów opartych na pojedynczych LFSR z prostymi funkcjami nieliniowymi

### Zadanie 3

Przeprowadzić atak korelacyjny na zbudowany w ramach pierwszego zadania kryptosystem, przyjmując iż znany jest szyfrogram i tylko fragment danych jawnych.

#### Implementacja

W tym zadaniu wykorzystano program z zadania 2 w niezmienionej formie, lecz z innymi argumentami wejściowymi. 

#### Wyniki

W ramach zadania 3 przeprowadzono atak korelacyjny przy użyciu fragmentu tekstu jawnego (449 bajtów) i pełnego szyfrogramu (1154 bajty). Pomimo ograniczonej ilości znanych danych, atak zakończył się pełnym sukcesem, odzyskując prawidłowy 12-bitowy klucz `011010111100` w czasie krótszym niż w zadaniu 2 (0.1143s vs 0.2889s).

**Fragment tekstu jawnego: plik `plain_fragment.txt`**
```plaintext
CALL me Ishmael. Some years ago never mind how 
long precisely having little or no money in my purse, 
and nothing particular to interest me on shore, I thought 
I would sail about a little and see the watery part of the 
world. It is a way I have of driving off the spleen, and 
regulating the circulation. Whenever I find myself 
growing grim about the mouth ; whenever it is a damp, 
drizzly November in my soul ; whenever I find myself 
```

**Statystyki wydajności:**
| Metryka               | Zadanie 3 (fragment tekstu jawnego) | Zadanie 2 (pełen tekst jawny) |
|-----------------------|-------------------------------------|-------------------------------|
| Czas wykonania        | 0.1143s                             | 0.2889s                       |
| Przetworzone operacje | 1 825 266                           | 4 690 386                     |
| Wydajność             | 15.97 Mops                          | 16.23 Mops                    |

**Wnioski:**
Osiągnięcie lepszego wyniku przy krótszym strumieniu danych wejściowych wynikało przede wszystkim z mniejszej liczby bitów do analizy (3592 zamiast 9232), co przełożyło się na mniejszą liczbę obliczeń korelacyjnych oraz lepsze wykorzystanie cache’u procesora dzięki mniejszemu zużyciu pamięci i większej lokalności danych. Dodatkowo krótszy strumień był wolny od szumu charakterystycznego dla dalszych fragmentów szyfrogramu, co pozwoliło algorytmowi Pearsona skuteczniej uwidocznić wyraźne korelacje pomiędzy fragmentami danych. Tym samym okazało się, że już 449 bajtów (3592 bitów) wystarcza do skutecznego przeprowadzenia ataku, co potwierdza, że bezpieczeństwo systemu nie zależy bezpośrednio od długości analizowanego szyfrogramu, lecz od obecności silnych korelacji. Skuteczność ataku przy częściowej znajomości tekstu jawnego wskazuje na realną podatność systemu szyfrowania, a zwiększona wydajność przy krótszym strumieniu podkreśla, że nie zawsze większa ilość danych przekłada się na lepszy wynik – kluczowe jest ich jakościowe znaczenie dla analizy.

### Zadanie 4

Przeprowadzić atak na zbudowany w ramach pierwszego zadania kryptosystem, przyjmując założenia z poprzedniego zadania, stosując jedynie technikę wyczerpującego wyszukiwania.
- Porównać wymagany do przeprowadzenia ataku nakład obliczeniowy z nakładem obliczeniowym wymaganym do prze- prowadzenia ataku korelacyjnego.

#### Implementacja

**1. Podział na klasy**

Program został podzielony na dwie główne klasy: `KeyStreamGenerator` i `BruteForceAttack`. Klasa `KeyStreamGenerator` jest taka sama jak w zadaniu 1 i odpowiada za generowanie strumienia klucza, natomiast klasa `BruteForceAttack` implementuje atak brute force na rejestry X, Y i Z.

**2. Funkcja `BruteForceAttack: __init__`**

**Wejście:**
- `known_plaintext` (bytes): Tekst jawny w postaci bajtów, znany atakującemu.
- `known_ciphertext` (bytes): Szyfrogram w postaci bajtów, odpowiadający znanemu tekstowi jawnemu.

**Wyjście:**
- Brak bezpośredniego wyjścia. Inicjalizuje obiekt klasy `BruteForceAttack`.

**Opis:**
Funkcja inicjalizuje atak brute force, konwertując znane dane (tekst jawny i szyfrogram) na bity, odtwarzając strumień klucza poprzez operację XOR oraz przygotowując licznik operacji do statystyk wydajności.

**Kod:**
```python
def __init__(self, known_plaintext, known_ciphertext):
    # Inicjalizacja ataku brute force z znanym tekstem jawnym i szyfrogramem
    self.known_plain_bits = self._bytes_to_bits(known_plaintext)
    self.known_cipher_bits = self._bytes_to_bits(known_ciphertext)
    # Odtworzenie strumienia klucza poprzez XOR tekstu jawnego i szyfrogramu
    self.recovered_key_bits = [p ^ c for p, c in zip(self.known_plain_bits, self.known_cipher_bits)]
    self.operations_count = 0  # Licznik operacji dla statystyk wydajności
```

**3. Funkcja `BruteForceAttack: _bytes_to_bits`**

**Wejście:**
- `byte_data` (bytes): Dane bajtowe do konwersji na bity.

**Wyjście:**
- `list`: Lista bitów reprezentujących przekazane dane bajtowe.

**Opis:**
Funkcja konwertuje dane bajtowe na listę bitów, rozbijając każdy bajt na 8 bitów i łącząc je w jedną listę.

**Kod:**
```python
def _bytes_to_bits(self, byte_data):
    # Konwersja danych bajtowych na listę bitów
    return list(itertools.chain.from_iterable(
        [(byte >> i) & 1 for i in reversed(range(8))] for byte in byte_data))
```

**4. Funkcja `BruteForceAttack: _hamming_distance`**

**Wejście:**
- `bits1` (list): Pierwszy strumień bitów do porównania.
- `bits2` (list): Drugi strumień bitów do porównania.

**Wyjście:**
- `int`: Odległość Hamminga między strumieniami bitów.

**Opis:**
Funkcja oblicza odległość Hamminga między dwoma strumieniami bitów, czyli liczbę pozycji, na których odpowiadające sobie bity są różne. Aktualizuje również licznik operacji dla celów statystycznych.

**Kod:**
```python
def _hamming_distance(self, bits1, bits2):
    # Obliczenie odległości Hamminga między dwoma strumieniami bitów
    distance = 0
    min_len = min(len(bits1), len(bits2))
    for i in range(min_len):
        if bits1[i] != bits2[i]:
            distance += 1
        self.operations_count += 3  # Aktualizacja licznika operacji (porównanie i inkrementacja)
    return distance
```

**5. Funkcja `BruteForceAttack: attack`**

**Wejście:**
- Brak parametrów wejściowych.

**Wyjście:**
- `dict` lub `None`: Słownik zawierający najlepsze dopasowanie klucza (wraz z wypełnieniami rejestrów i odległością Hamminga) lub `None`, jeśli nie znaleziono dopasowania.

**Opis:**
Funkcja wykonuje atak brute force, testując wszystkie możliwe 12-bitowe klucze (z wyłączeniem klucza zerowego). Dla każdego klucza generuje strumień klucza, oblicza odległość Hamminga od odzyskanego strumienia i wybiera klucz z najmniejszą odległością. Wypisuje szczegółowe statystyki wydajności, w tym liczbę przetestowanych kandydatów, czas wykonania i liczbę operacji.

**Kod:**
```python
def attack(self):
    # Główna metoda wykonująca atak brute force
    start_time = time.time()
    best_match = None
    best_distance = float('inf')  # Początkowa odległość ustawiona na nieskończoność
    total_candidates = 0
    
    # Generowanie wszystkich możliwych 12-bitowych kluczy (z wyłączeniem klucza zerowego)
    for key_bits in itertools.product([0,1], repeat=12):
        if sum(key_bits) == 0:
            continue  # Pominięcie klucza zerowego
            
        total_candidates += 1
        key_str = ''.join(map(str, key_bits))
        
        try:
            # Podział klucza na inicjalizacje rejestrów X, Y, Z
            x_init = list(key_bits[:3])
            y_init = list(key_bits[3:7])
            z_init = list(key_bits[7:12])
            
            # Inicjalizacja generatora strumienia klucza
            generator = KeyStreamGenerator(x_init, y_init, z_init)
            key_stream = generator.get_key_stream(len(self.recovered_key_bits))
            
            # Obliczenie odległości Hamminga między odzyskanym a wygenerowanym strumieniem
            distance = self._hamming_distance(self.recovered_key_bits, key_stream)
            self.operations_count += len(self.recovered_key_bits) * 5  # Szacunek operacji dla generacji strumienia
            
            # Aktualizacja najlepszego dopasowania
            if distance < best_distance:
                best_distance = distance
                best_match = {
                    'key': key_str,
                    'x_init': x_init,
                    'y_init': y_init,
                    'z_init': z_init,
                    'distance': distance
                }
                
            # Optymalizacja: przerwanie pętli przy idealnym dopasowaniu
            if distance == 0:
                break
                
        except ValueError:
            continue  # Pominięcie nieprawidłowych kombinacji (np. rejestry zerowe)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    # Wyświetlenie statystyk wydajności
    print("\nStatystyki wydajności:")
    print(f"Przetestowano kandydatów: {total_candidates}")
    print(f"Czas wykonania: {elapsed_time:.4f} sekund")
    print(f"Łączna liczba operacji: {self.operations_count}")
    print(f"Operacje na sekundę: {self.operations_count/elapsed_time:.2f}")
    
    if best_match:
        # Wyświetlenie najlepszego znalezionego klucza
        print("\nNajlepsze dopasowanie:")
        print(f"Klucz: {best_match['key']}")
        print(f"X: {best_match['x_init']}, Y: {best_match['y_init']}, Z: {best_match['z_init']}")
        print(f"Odległość Hamminga: {best_match['distance']}")
        return best_match
    else:
        print("Nie znaleziono pasującego klucza")
        return None
```

**6. Funkcja `KeyStreamGenerator: __init__`**

**Wejście:**
- `x_init` (list): Lista 3 bitów inicjalizujących rejestr X.
- `y_init` (list): Lista 4 bitów inicjalizujących rejestr Y.
- `z_init` (list): Lista 5 bitów inicjalizujących rejestr Z.

**Wyjście:**
- Brak bezpośredniego wyjścia. Inicjalizuje obiekt klasy `KeyStreamGenerator`.

**Opis:**
Funkcja inicjalizuje generator strumienia klucza, sprawdzając poprawność długości podanych rejestrów oraz czy żaden z nich nie jest całkowicie zerowy.

**Kod:**
```python
def __init__(self, x_init, y_init, z_init):
    # Inicjalizacja generatora strumienia klucza z podanymi wypełnieniami rejestrów
    if len(x_init) != 3 or len(y_init) != 4 or len(z_init) != 5:
        raise ValueError("Długości inicjalizacyjne muszą wynosić odpowiednio: X=3, Y=4, Z=5")
    if x_init == [0, 0, 0] or y_init == [0, 0, 0, 0] or z_init == [0, 0, 0, 0, 0]:
        raise ValueError("Żaden rejestr nie może być całkowicie zerowy")

    self.X = x_init.copy()
    self.Y = y_init.copy()
    self.Z = z_init.copy()
```

**7. Funkcja `KeyStreamGenerator: _next_bit`**

**Wejście:**
- Brak parametrów wejściowych.

**Wyjście:**
- `int`: Kolejny bit strumienia klucza.

**Opis:**
Funkcja generuje kolejny bit strumienia klucza na podstawie aktualnego stanu rejestrów X, Y i Z, stosując nieliniową funkcję boolowską i aktualizując rejestry przesuwające.

**Kod:**
```python
def _next_bit(self):
    # Generowanie kolejnego bitu klucza na podstawie bieżącego stanu rejestrów
    xi = self.X[0]
    yi = self.Y[0]
    zi = self.Z[0]

    ki = (xi & yi) ^ (yi & zi) ^ zi  # Funkcja nieliniowa generująca bit klucza

    # Aktualizacja rejestrów przesuwających
    x_new = self.X[0] ^ self.X[2]
    y_new = self.Y[0] ^ self.Y[3]
    z_new = self.Z[0] ^ self.Z[2]

    self.X = self.X[1:] + [x_new]
    self.Y = self.Y[1:] + [y_new]
    self.Z = self.Z[1:] + [z_new]

    return ki
```

**8. Funkcja `KeyStreamGenerator: get_key_stream`**

**Wejście:**
- `length` (int): Długość strumienia klucza do wygenerowania.

**Wyjście:**
- `list`: Lista bitów strumienia klucza o zadanej długości.

**Opis:**
Funkcja generuje strumień klucza o określonej długości, wielokrotnie wywołując metodę `_next_bit`.

**Kod:**
```python
def get_key_stream(self, length):
    # Generowanie strumienia klucza o zadanej długości
    return [self._next_bit() for _ in range(length)]
```

**9. Funkcja `Main`**

**Wejście:**
- `sys.argv[1]` (str): Ścieżka do pliku z tekstem jawnym.
- `sys.argv[2]` (str): Ścieżka do pliku z szyfrogramem.

**Wyjście:**
- Brak bezpośredniego wyjścia. Wypisuje wyniki ataku na standardowe wyjście.

**Opis:**
Funkcja główna programu, która wczytuje dane wejściowe, inicjalizuje atak brute force, wykonuje go i wypisuje odzyskany klucz oraz statystyki. Obsługuje również błędy związane z nieprawidłowymi danymi wejściowymi.

**Kod:**
```python
if __name__ == "__main__":
    # Główna funkcja wykonująca atak na podstawie plików wejściowych
    if len(sys.argv) != 3:
        print("Użycie: python zad4_bruteforce.py plik_jawny.txt plik_szyfrogram.txt")
        sys.exit(1)
        
    plain_file = sys.argv[1]
    cipher_file = sys.argv[2]
    
    try:
        # Wczytanie znanego tekstu jawnego i szyfrogramu
        with open(plain_file, "rb") as f:
            known_plaintext = f.read()
        
        with open(cipher_file, "rb") as f:
            known_ciphertext = f.read()
            
        print(f"Wczytano {len(known_plaintext)} bajtów tekstu jawnego")
        print(f"Wczytano {len(known_ciphertext)} bajtów szyfrogramu")
        print(f"Długość analizowanego strumienia: {len(known_plaintext)*8} bitów")
        
        print("\nRozpoczęcie ataku brute force...")
        attacker = BruteForceAttack(known_plaintext, known_ciphertext)
        result = attacker.attack()
        
    except FileNotFoundError:
        print("Błąd: Nie można znaleźć pliku")
        sys.exit(1)
    except Exception as e:
        print(f"Błąd: {str(e)}")
        sys.exit(1)
```

#### Wyniki

W ramach zadania 4 przeprowadzono atak brute force na kryptosystem strumieniowy, testując jego skuteczność dla pełnego tekstu jawnego (1154 bajty) oraz jego fragmentu (449 bajtów). W obu przypadkach atak zakończył się pełnym sukcesem, odzyskując prawidłowy 12-bitowy klucz `011010111100` z zerową odległością Hamminga.

**Statystyki wydajności:**
| Parametr               | Pełny tekst jawny | Fragment tekstu jawnego |
|------------------------|-------------------|-------------------------|
| Długość strumienia     | 9232 bity         | 3592 bity               |
| Przetestowane klucze   | 1724              | 1724                    |
| Czas wykonania         | 9.5249 s          | 3.5646 s (62% szybciej) |
| Łączne operacje        | 79 912 192        | 31 092 352              |
| Wydajność              | 8.39 Mops         | 8.72 Mops               |


**Efektywność ataku:**  
Przeprowadzenie ataku na skróconym fragmencie danych (3592 bity zamiast 9232) pozwoliło skrócić czas jego trwania o 62% przy zachowaniu pełnej, 100-procentowej skuteczności. Co istotne, liczba testowanych kandydatów pozostała taka sama (1724), ponieważ przestrzeń kluczy – zdefiniowana przez długość rejestru LFSR – nie uległa zmianie. Poprawa wydajności wynikała natomiast z ograniczenia liczby operacji korelacyjnych, które musiały zostać wykonane na krótszym strumieniu bitów. Mniejszy rozmiar danych nie tylko ograniczył czas obliczeń, ale również wpłynął korzystnie na wykorzystanie cache’u procesora oraz lokalność pamięci, co dodatkowo przyspieszyło analizę.

**Stabilność metody:**  
W obu przypadkach (dla pełnego i skróconego strumienia) uzyskano zerową odległość Hamminga między odszyfrowanym a rzeczywistym tekstem, co jednoznacznie potwierdza idealne dopasowanie i pełną skuteczność ataku. Pokazuje to, że brute force – choć metodą kosztowną obliczeniowo – cechuje się wysoką niezawodnością. Skrócenie długości analizowanego strumienia nie wpłynęło na jakość końcowego wyniku, a jedynie zwiększyło efektywność całego procesu, czyniąc go bardziej praktycznym w warunkach ograniczonych zasobów obliczeniowych.

**Wnioski:**  
Metoda brute force pozostaje najpewniejszym sposobem złamania szyfru, choć jednocześnie jest jedną z najbardziej czasochłonnych. Redukcja długości danych wejściowych znacząco poprawia wydajność, nie wpływając negatywnie na skuteczność ataku, o ile korelacje między tekstem jawnym a szyfrogramem są dostatecznie wyraźne. W przypadku 12-bitowego klucza, który daje 4096 możliwych konfiguracji, taka metoda okazuje się w pełni wykonalna w rozsądnym czasie. Jednak jej praktyczne zastosowanie dla dłuższych kluczy byłoby ograniczone przez wykładniczy wzrost złożoności obliczeniowej, co czyniłoby ją nieefektywną bez zastosowania optymalizacji lub bardziej zaawansowanych technik analizy kryptograficznej.

### Zadanie 5

Przedstawić wnioski dotyczące budowy nieliniowego generatora strumienia klucza dla kryptosystemu strumieniowego.

#### Wyniki


| Metryka               | Algorytm Pearsona (pełny tekst) | Algorytm Pearsona (fragment) | Brute Force (pełny tekst) | Brute Force (fragment) |
|-----------------------|--------------------------------|-----------------------------|--------------------------|------------------------|
| **Długość strumienia** | 9232 bity                     | 3592 bity                   | 9232 bity               | 3592 bity             |
| **Czas wykonania**    | 0.2889 s                      | 0.1143 s (60% szybciej)     | 9.5249 s                | 3.5646 s (62% szybciej) |
| **Operacje**          | 4 690 386                     | 1 825 266                   | 79 912 192              | 31 092 352            |
| **Wydajność**         | 16.23 Mops                    | 15.97 Mops                  | 8.39 Mops               | 8.72 Mops             |
| **Przetestowane klucze** | N/D (korelacja)              | N/D (korelacja)             | 1724                    | 1724                  |
