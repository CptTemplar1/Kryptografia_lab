# Kryptografia i kryptoanaliza
## Laboratorium 6
### Grupa 22B
### Autorzy: Przemysław Kałużiński, Michał Kaczor

### Zadanie 1

## Zadanie 1

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



**2. Funkcja `KeyStreamGenerator: __init__`**

***Wejście:**  
- 

**Wyjście:**  
- 

**Opis:**  


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

***Wejście:**  
- 

**Wyjście:**  
- 

**Opis:**  


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

***Wejście:**  
- 

**Wyjście:**  
- 

**Opis:**  


**Kod:**
```python
def get_key_stream(self, length):
    # Generowanie strumienia klucza o zadanej długości
    return [self._next_bit() for _ in range(length)]
```

**5. Funkcja `StreamCipher: __init__`**

***Wejście:**  
- 

**Wyjście:**  
- 

**Opis:**  


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

***Wejście:**  
- 

**Wyjście:**  
- 

**Opis:**  


**Kod:**
```python
def _bytes_to_bits(self, byte_data):
    # Konwersja danych bajtowych na listę bitów
    return list(itertools.chain.from_iterable(
        [(byte >> i) & 1 for i in reversed(range(8))] for byte in byte_data))
```

**7. Funkcja `StreamCipher: _bits_to_bytes`**

***Wejście:**  
- 

**Wyjście:**  
- 

**Opis:**  


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

***Wejście:**  
- 

**Wyjście:**  
- 

**Opis:**  


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

***Wejście:**  
- 

**Wyjście:**  
- 

**Opis:**  


**Kod:**
```python
def decrypt(self, input_file, output_file):
    # Deszyfrowanie to to samo co szyfrowanie (XOR jest odwracalny)
    self.encrypt(input_file, output_file) 
```

**10. Funkcja `Main`**

***Wejście:**  
- 

**Wyjście:**  
- 

**Opis:**  


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

**2. Funkcja `CorrelationAttack: __init__`**

***Wejście:**  
- 

**Wyjście:**  
- 

**Opis:**  


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

***Wejście:**  
- 

**Wyjście:**  
- 

**Opis:**  


**Kod:**
```python
def _bytes_to_bits(self, byte_data):
    # Konwersja danych bajtowych na listę bitów
    return list(itertools.chain.from_iterable(
        [(byte >> i) & 1 for i in reversed(range(8))] for byte in byte_data))
```

**4. Funkcja `CorrelationAttack: _pearson_correlation`**

***Wejście:**  
- 

**Wyjście:**  
- 

**Opis:**  


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

***Wejście:**  
- 

**Wyjście:**  
- 

**Opis:**  


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

***Wejście:**  
- 

**Wyjście:**  
- 

**Opis:**  


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

***Wejście:**  
- 

**Wyjście:**  
- 

**Opis:**  


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

***Wejście:**  
- 

**Wyjście:**  
- 

**Opis:**  


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

***Wejście:**  
- 

**Wyjście:**  
- 

**Opis:**  


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

***Wejście:**  
- 

**Wyjście:**  
- 

**Opis:**  


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

***Wejście:**  
- 

**Wyjście:**  
- 

**Opis:**  


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

***Wejście:**  
- 

**Wyjście:**  
- 

**Opis:**  


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

***Wejście:**  
- 

**Wyjście:**  
- 

**Opis:**  


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

***Wejście:**  
- 

**Wyjście:**  
- 

**Opis:**  


**Kod:**
```python
def get_key_stream(self, length):
    # Generowanie strumienia klucza o zadanej długości
    return [self._next_bit() for _ in range(length)]
```

**15. Funkcja `Main`**

***Wejście:**  
- 

**Wyjście:**  
- 

**Opis:**  


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

### Zadanie 3

Przeprowadzić atak korelacyjny na zbudowany w ramach pierwszego zadania kryptosystem, przyjmując iż znany jest szyfrogram i tylko fragment danych jawnych.

#### Implementacja

W tym zadaniu wykorzystano program z zadania 2 w niezmienionej formie, lecz z innymi argumentami wejściowymi. 

#### Wyniki



### Zadanie 4

Przeprowadzić atak na zbudowany w ramach pierwszego zadania kryptosystem, przyjmując założenia z poprzedniego zadania, stosując jedynie technikę wyczerpującego wyszukiwania.
- Porównać wymagany do przeprowadzenia ataku nakład obliczeniowy z nakładem obliczeniowym wymaganym do prze- prowadzenia ataku korelacyjnego.


#### Implementacja

**1. Podział na klasy**

**2. Funkcja `BruteForceAttack: __init__`**

***Wejście:**  
- 

**Wyjście:**  
- 

**Opis:**  


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

***Wejście:**  
- 

**Wyjście:**  
- 

**Opis:**  


**Kod:**
```python
def _bytes_to_bits(self, byte_data):
    # Konwersja danych bajtowych na listę bitów
    return list(itertools.chain.from_iterable(
        [(byte >> i) & 1 for i in reversed(range(8))] for byte in byte_data))
```

**4. Funkcja `BruteForceAttack: _hamming_distance`**

***Wejście:**  
- 

**Wyjście:**  
- 

**Opis:**  


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

***Wejście:**  
- 

**Wyjście:**  
- 

**Opis:**  


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

***Wejście:**  
- 

**Wyjście:**  
- 

**Opis:**  


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

***Wejście:**  
- 

**Wyjście:**  
- 

**Opis:**  


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

***Wejście:**  
- 

**Wyjście:**  
- 

**Opis:**  


**Kod:**
```python
def get_key_stream(self, length):
    # Generowanie strumienia klucza o zadanej długości
    return [self._next_bit() for _ in range(length)]
```

**9. Funkcja `Main`**

***Wejście:**  
- 

**Wyjście:**  
- 

**Opis:**  


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



### Zadanie 5

Przedstawić wnioski dotyczące budowy nieliniowego generatora strumienia klucza dla kryptosystemu strumieniowego.

#### Wyniki

