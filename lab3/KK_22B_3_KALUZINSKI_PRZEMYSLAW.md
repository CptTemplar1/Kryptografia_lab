# Kryptografia i kryptoanaliza
## Laboratorium 3
### Grupa 22B
### Autorzy: Przemysław Kałużiński, Michał Kaczor

### Zadanie 1

Zrealizować program implementujący podstawieniowy algorytm szyfrowania.
1.	Wybrać dłuższy fragment tekstu w języku angielskim (np. akapit składający się z kilkunastu zdań).
2.	Usunąć z niego wszystkie znaki niebędące literami (ograniczenie do 26 liter alfabetu łacińskiego).
3.	Zaszyfrować tekst używając wybranego w sposób losowy klucza (tablicy podstawień): permutacji.

#### Implementacja

**1. Funkcja `generate_key`**

**Wejście:**
- Brak parametrów wejściowych.

**Wyjście:**
- Słownik zawierający 26 par klucz-wartość, gdzie klucze to litery od 'A' do 'Z', a wartości to losowa permutacja tych liter. Każda litera jest mapowana na unikatową inną literę.

**Opis:**  
Funkcja generuje losowy klucz szyfrowania dla szyfru podstawieniowego poprzez przetasowanie liter alfabetu angielskiego. Klucz jest permutacją - nie ma powtórzeń, a każda litera ma unikalne mapowanie. Złożoność przestrzeni kluczy wynosi 26! (~4.03×10^26 możliwości). Funkcja wykorzystuje moduł random do losowego mieszania liter.

**Kod:**
``` python
def generate_key():
    letters = list(string.ascii_uppercase)
    shuffled = letters[:]
    random.shuffle(shuffled)
    return dict(zip(letters, shuffled))
```

**2. Funkcja `invert_key`**

**Wejście:**
- `key` (dict): Słownik reprezentujący klucz szyfrowania, gdzie klucze to oryginalne litery (A-Z), a wartości to ich zaszyfrowane odpowiedniki.

**Wyjście:**
- Nowy słownik, gdzie klucze to zaszyfrowane litery, a wartości to oryginalne litery (odwrócone mapowanie).

**Opis:**  
Funkcja tworzy klucz deszyfrowania poprzez odwrócenie par klucz-wartość w słowniku szyfrowania. Implementacja wykorzystuje składnię dictionary comprehension. Jest to operacja deterministyczna - dla tego samego klucza wejściowego zawsze zwróci ten sam klucz wyjściowy.

**Kod:**
``` python
def invert_key(key):
    return {v: k for k, v in key.items()}
```

**3. Funkcja `clean_text`**

**Wejście:**
- `text` (str): Dowolny ciąg znaków, który może zawierać litery, cyfry, znaki interpunkcyjne, białe znaki itd.

**Wyjście:**
- Ciąg znaków zawierający tylko wielkie litery alfabetu angielskiego (A-Z), pozbawiony wszystkich innych znaków.

**Opis:**  
Funkcja filtruje tekst wejściowy, usuwając wszystkie znaki, które nie są literami (w tym polskie znaki diakrytyczne), a następnie konwertuje pozostałe litery na wielkie. Implementacja używa filter() z funkcją str.isalpha oraz join(). Jest to ważny krok przygotowawczy przed szyfrowaniem/deszyfrowaniem. 

**Kod:**
``` python
def clean_text(text):
    return ''.join(filter(str.isalpha, text)).upper()
```

**4. Funkcja `substitute`**

**Wejście:**
- `text` (str): Tekst do transformacji (zaszyfrowania lub odszyfrowania).
- `key` (dict): Słownik mapujący litery na ich zaszyfrowane/odszyfrowane odpowiedniki.

**Wyjście:**
- Przekształcony tekst, gdzie każda litera została zamieniona zgodnie z mapowaniem w kluczu.

**Opis:**  
Funkcja wykonuje podstawienie znak po znaku zgodnie z podanym kluczem. Dla każdej litery w tekście sprawdza jej mapowanie w kluczu. Jeśli litera nie istnieje w kluczu (np. po wyczyszczeniu tekstu nie powinno się to zdarzyć), pozostawia ją bez zmian. Implementacja używa generator expression z join() dla efektywności.

**Kod:**
``` python
def substitute(text, key):
    return ''.join(key.get(char, char) for char in text)
```

**5. Funkcja `process_file`**

**Wejście:**
- `input_file` (str): Ścieżka do pliku z tekstem do przetworzenia.
- `output_file` (str): Ścieżka do pliku wyjściowego.
- `key_file` (str): Ścieżka do pliku JSON z kluczem.
- `encrypt` (bool): Flaga aktywująca tryb szyfrowania.
- `decrypt` (bool): Flaga aktywująca tryb deszyfrowania.
- `generate_new_key` (bool): Flaga wymuszająca generację nowego klucza.

**Wyjście:**
- Zapisuje wynik do pliku wyjściowego.
- W trybie szyfrowania zapisuje również klucz do pliku JSON.
- Komunikaty statusu wypisywane na stdout.

**Opis:**  
Główna funkcja zarządzająca procesem szyfrowania/deszyfrowania. Czyści tekst wejściowy, w zależności od flag albo szyfruje go (ewentualnie generując nowy klucz), albo deszyfruje przy użyciu podanego klucza. Obsługuje błędy związane z nieistniejącym plikiem klucza. Wykorzystuje funkcje pomocnicze clean_text, substitute i invert_key.

**Kod:**
``` python
def process_file(input_file, output_file, key_file, encrypt, decrypt, generate_new_key):
    # Otwarcie i odczyt pliku wejściowego
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Usunięcie znaków specjalnych i spacji, konwersja na wielkie litery
    clean = clean_text(text)
    
    if encrypt:
        # Generowanie nowego klucza szyfrowania
        if generate_new_key:
            key = generate_key()
            print("Wygenerowano nowy klucz szyfrowania.")
        # Próba wczytania istniejącego klucza
        else:
            try:
                with open(key_file, 'r', encoding='utf-8') as kf:
                    key = json.load(kf)
                print(f"Wczytano istniejący klucz z {key_file}.")
            # Jeśli plik klucza nie istnieje, generujemy nowy klucz
            except FileNotFoundError:
                print("Błąd: Plik klucza nie istnieje. Generuję nowy klucz.")
                key = generate_key()
        
        # Zaszyfrowanie tekstu
        transformed = substitute(clean, key)
        
        # Wyświetlenie komunikatu i zapisanie zaszyfrowanego tekstu oraz klucza do pliku
        with open(key_file, 'w', encoding='utf-8') as kf:
            json.dump(key, kf)
        print(f"Tekst został zaszyfrowany i zapisany do {output_file}. Klucz zapisano w {key_file}.")
    
    elif decrypt:
        # Wczytanie klucza szyfrowania z pliku
        with open(key_file, 'r', encoding='utf-8') as kf:
            key = json.load(kf)
        inv_key = invert_key(key)

        # Deszyfrowanie tekstu
        transformed = substitute(clean, inv_key)
        
        # Wyświetlenie komunikatu i zapisanie odszyfrowanego tekstu do pliku
        print(f"Tekst został odszyfrowany i zapisany do {output_file}.")
    else:
        raise ValueError("Niepoprawny tryb. Użyj flag -e dla szyfrowania lub -d dla deszyfrowania.")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(transformed)
```

**6. Funkcja `brute_force_attack`**

**Wejście:**
- `input_file` (str): Ścieżka do pliku z zaszyfrowanym tekstem.
- `output_file` (str): Ścieżka do pliku wyjściowego.
- `iterations` (int, opcjonalne): Maksymalna liczba prób (domyślnie 1 000 000).

**Wyjście:**
- Zapisuje najlepszy znaleziony tekst do pliku wyjściowego.
- Zapisuje odpowiadający mu klucz do pliku JSON.
- Wypisuje statystyki na stdout.

**Opis:**  
Funkcja implementuje atak brute-force na szyfr podstawieniowy. Generuje losowe klucze i ocenia je za pomocą statystyki chi-kwadrat, porównując rozkład liter z typowym rozkładem dla języka angielskiego. Przechowuje najlepsze znalezione rozwiązanie. Może zakończyć się wcześniej, jeśli znajdzie idealne dopasowanie (chi-kwadrat bliskie 0).

**Kod:**
``` python
def brute_force_attack(input_file, output_file, iterations=1000000):
    # Wczytanie zaszyfrowanego tekstu i usunięcie niealfabetycznych znaków
    with open(input_file, 'r', encoding='utf-8') as f:
        cipher_text = clean_text(f.read())
    
    # Częstotliwości liter w języku angielskim (do porównania)
    english_frequencies = {
        'A': 0.08167, 'B': 0.01492, 'C': 0.02782, 'D': 0.04253,
        'E': 0.12702, 'F': 0.02228, 'G': 0.02015, 'H': 0.06094,
        'I': 0.06966, 'J': 0.00153, 'K': 0.00772, 'L': 0.04025,
        'M': 0.02406, 'N': 0.06749, 'O': 0.07507, 'P': 0.01929,
        'Q': 0.00095, 'R': 0.05987, 'S': 0.06327, 'T': 0.09056,
        'U': 0.02758, 'V': 0.00978, 'W': 0.02360, 'X': 0.00150,
        'Y': 0.01974, 'Z': 0.00074
    }
    
    # Inicjalizacja najlepszego wyniku (najmniejsze chi-kwadrat)
    best_score = float('inf')
    best_text = ""
    best_key = {}
    
    # Główna pętla ataku brute-force
    for attempt in range(iterations):
        key = generate_key()
        inv_key = invert_key(key)
        decrypted_text = substitute(cipher_text, inv_key)
        
        # Pominięcie pustego tekstu
        text_length = len(decrypted_text)
        if text_length == 0:
            continue

        # Obliczenie częstotliwości liter w odszyfrowanym tekście
        observed_frequencies = {}
        for letter in string.ascii_uppercase:
            observed_frequencies[letter] = decrypted_text.count(letter) / text_length
        
        # Obliczenie statystyki chi-kwadrat (im mniejsza, tym lepsze dopasowanie)
        chi_squared = 0.0
        for letter in english_frequencies:
            expected = english_frequencies[letter]
            observed = observed_frequencies.get(letter, 0.0)
            chi_squared += ((observed - expected) ** 2) / expected
        
        # Aktualizacja najlepszego wyniku
        if chi_squared < best_score:
            best_score = chi_squared
            best_text = decrypted_text
            best_key = key
            
            # Przerwanie, jeśli wynik jest wystarczająco dobry
            if math.isclose(best_score, 0.0, abs_tol=0.01):
                break
    
    # Wypisanie wyników i zapisanie najlepszego odszyfrowanego tekstu i klucza do pliku
    print(f"Znaleziono najlepsze dopasowanie z wynikiem chi-kwadrat: {best_score:.4f}")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(best_text)
    
    key_output_file = output_file + '.JSON'
    with open(key_output_file, 'w', encoding='utf-8') as kf:
        json.dump(best_key, kf)
    print(f"Zapisano odszyfrowany tekst do {output_file} i klucz do {key_output_file}")
```

#### Wyniki



**Wnioski:**



### Implementacja pomocniczych funkcji dla dalszych algorytmów

**1. Funkcja `create_bigram_matrix`**

**Wejście:**
- `text` (str): Tekst do analizy (już oczyszczony).

**Wyjście:**
- Macierz numpy 26x26 zawierająca zliczenia wystąpień wszystkich możliwych par liter (bigramów).

**Opis:**  
Funkcja tworzy macierz częstości występowania par kolejnych liter w tekście. Każda komórka matrix[i][j] reprezentuje liczbę wystąpień pary liter (i-tej i j-tej litery alfabetu). Wykorzystuje indeksowanie ASCII (ord(letter) - ord('A')) do mapowania liter na indeksy. Macierz jest inicjalizowana zerami, a następnie wypełniana podczas jednego przejścia przez tekst. 

**Kod:**
``` python
def create_bigram_matrix(text):
    bigram_matrix = np.zeros((26, 26))
    for i in range(len(text)-1):
        current = ord(text[i]) - ord('A')
        next_char = ord(text[i+1]) - ord('A')
        bigram_matrix[current][next_char] += 1
    return bigram_matrix
```

**2. Funkcja `log_likelihood`**

**Wejście:**
- `decrypted_bigrams` (numpy.ndarray): Macierz bigramów tekstu odszyfrowanego.
- `reference_bigrams` (numpy.ndarray): Macierz bigramów tekstu referencyjnego (znormalizowana).

**Wyjście:**
- Wartość logarytmicznej funkcji wiarygodności (float).

**Opis:**  
Funkcja oblicza miarę dopasowania tekstu odszyfrowanego do tekstu referencyjnego. Dla każdej pary liter oblicza iloczyn częstości w tekście odszyfrowanym i logarytmu częstości referencyjnej, a następnie sumuje te wartości. Im wyższa wartość, tym lepsze dopasowanie. Używa logarytmów, aby uniknąć underflow w obliczeniach na małych prawdopodobieństwach.

**Kod:**
``` python
def log_likelihood(decrypted_bigrams, reference_bigrams):
    log_likelihood = 0.0
    for i in range(26):
        for j in range(26):
            if reference_bigrams[i][j] > 0 and decrypted_bigrams[i][j] > 0:
                log_likelihood += decrypted_bigrams[i][j] * math.log(reference_bigrams[i][j])
    return log_likelihood
```

**3. Funkcja `generate_new_key`**

**Wejście:**
- `current_key` (dict): Aktualny klucz permutacyjny.

**Wyjście:**
- Nowy klucz, który różni się od wejściowego zamianą dwóch losowo wybranych liter.

**Opis:**  
Funkcja tworzy nowy klucz poprzez losową transpozycję (zamianę miejscami) dwóch liter w obecnym kluczu. Zachowuje właściwość permutacji - każda litera nadal ma unikalne mapowanie. Jest to tzw. "sąsiedztwo" w przestrzeni przeszukiwania, używane w algorytmach optymalizacji.

**Kod:**
``` python
def generate_new_key(current_key):
    letters = list(string.ascii_uppercase)
    new_key = current_key.copy()
    i, j = random.sample(range(26), 2)
    new_key[letters[i]], new_key[letters[j]] = new_key[letters[j]], new_key[letters[i]]
    return new_key
```

### Zadanie 2

Dokonać kryptoanalizy heurystycznej na zaimplementowany w ramach pierwszego zadania monoalfabetyczny kryptosystem podstawieniowy. Założenia ataku są następujące:

1. Znany jest szyfrogram.
2. Wiadomo jaki kryptosystem użyty został do zaszyfrowania wiadomości.
3. Należy odzyskać klucz i tekst jawny.

Do realizacji zadania kryptoanalizy heurystycznej, należy użyć algorytmu *Metropolis-Hastings*. Algorytm ten umożliwia realizację procedury poszukiwania klucza (czyli mapowania znaków), który najlepiej dopasowuje się do rozkładu prawdopodobieństwa tekstu jawnego. Przebieg tego procesu wygląda następująco:

1. Wybieramy reprezentację klucza jako permutację $\hat{\pi}$:
    - Zakładamy losowy klucz początkowy, czyli permutację znaków klucza.
2. Definiujemy funkcję oceny klucza (funkcja celu / funkcja wiarygodności) $\text{pl}(\hat{\pi})$:
    - Funkcja ta jest miarą tego jak bardzo odszyfrowany tekst przypomina tekst naturalny.
    - Na potrzeby zadania, funkcja ta zdefiniowana jest w następujący sposób:
$
\text{pl}(\hat{\pi}) = \prod_{i,j} (M_{i,j})^{\hat{M}_{i,j}}
$

      - $M$ to macierz bigramów utworzona na bazie tekstu referencyjnego, natomiast $M_{i,j}$ to liczba wystąpień pary $(i, j)$ w tekście referencyjnym.
      - $\hat{M}$ to macierz bigramów utworzona na bazie szyfrogramu, natomiast $\hat{M}_{i,j}$ to liczba wystąpień pary $(i, j)$ w szyfrogramie.
    - Uwaga: zdefiniowaną funkcję należy rozpatrywać w kategorii prawdopodobieństwa.

3. Losujemy nową permutację klucza $\hat{\pi}'$:
    - Zadanie to realizowane jest poprzez losową zamianę dwóch znaków w permutacji (klucza) $\hat{\pi}$.

4. Definiujemy kryterium akceptacji $\rho(\hat{\pi}, \hat{\pi}')$:
    - Algorytm *Metropolis-Hastings* akceptuje nowy klucz z pewnym prawdopodobieństwem, które zależy od stosunku funkcji oceny dla nowego i starego klucza. Jeśli nowy klucz $\hat{\pi}'$ prowadzi do lepszego dopasowania, to akceptujemy go jako $X_{t+1}$, jeśli nie, to zostajemy przy starym $\hat{\pi}$.
    - Dla rozważanego przypadku, kryterium akceptacji można zdefiniować w następujący sposób:
$
\rho(\hat{\pi}, \hat{\pi}') = \frac{\text{pl}(\hat{\pi}')}{\text{pl}(\hat{\pi})}
$

    - Dla rozważanego algorytmu, należy wylosować liczbę $u$ należącą do rozkładu jednostajnego na przedziale [0, 1] i następnie dokonać porównania: $u \leq \rho(\hat{\pi}, \hat{\pi}')$. Jeśli warunek ten jest spełniony, to akceptujemy nowy klucz (permutację), jeżeli nie to zostajemy przy starym kluczu.

5. Iteracja procesu:

- Proces ten jest powtarzany, tworząc łańcuch kluczy $\{X_t : t = 0, \ldots, T \}$, które przybliżają optymalne rozwiązanie.
- W miarę postępu procesu iteracyjnego, algorytm koncentruje się na obszarach rozwiązań, które lepiej odtwarzają tekst jawny.

Algorytm *Metropolis-Hastings* dla rozważanego problemu, przyjmuje następującą postać:

---

**Algorithm 1 MH**

```
1:  t ← 0  
2:  X₀ ← π̂₀  
3:  for t = 1, ..., T do  
4:      dla Xₜ ← π̂  
5:          wygeneruj i, j ~ U({1, 2, ..., 26})       ▷ ~ znaczy ma rozkład  
6:          wygeneruj π̂′                              ▷ zamieniając znaki na pozycjach i oraz j w kluczu π̂  
7:          ρ(π̂, π̂′) ← p(π̂′) / p(π̂)                  ▷ ρ - prawdopodobieństwo akceptacji  
8:          wylosuj u ~ U([0,1])  
9:          if u ≤ ρ(π̂, π̂′) then  
10:             Xₜ₊₁ ← π̂′  
11:         else  
12:             Xₜ₊₁ ← π̂  
13:         end if  
14: end for
```
---

**Uwagi:**

- Wyznaczenie funkcji pl, może prowadzić do przekroczenia zakresu numerycznego. Aby uniknąć problemów związanych z precyzją numeryczną, można zastosować logarytmowanie funkcji pl.

$$
\log \text{pl}(\hat{\pi}) = \sum_{i,j} \hat{M}_{i,j} \cdot \log M_{i,j}
$$

- Uwaga, przekształcenie to w konsekwencji prowadzi do innego sposobu wyznaczenia współczynnika akceptacji poprzez obliczenie wartości funkcji wykładniczej, której argumentem jest różnica pomiędzy $\text{pl}(\hat{\pi}')$ a $\text{pl}(\hat{\pi})$.

Zamiast obliczać:
$
\rho(\hat{\pi}, \hat{\pi}') = \frac{\text{pl}(\hat{\pi}')}{\text{pl}(\hat{\pi})}
$
    należy obliczyć:
$$
\rho(\hat{\pi}, \hat{\pi}') = \exp \left[ \log \text{pl}(\hat{\pi}') - \log \text{pl}(\hat{\pi}) \right]
$$
Należy również zauważyć, iż współczynnik akceptacji nie powinien być większy do jedności.
- Jest to powszechny sposób stabilizacji obliczeń w algorytmach probabilistycznych.

---

#### Implementacja

**1. Funkcja `metropolis_hastings_attack`**

**Wejście:**
- `cipher_text` (str): Tekst zaszyfrowany.
- `reference_bigrams` (numpy.ndarray): Znormalizowana macierz bigramów referencyjnych.
- `iterations` (int): Liczba iteracji algorytmu.

**Wyjście:**
- Najlepszy znaleziony klucz (dict).
- Najlepsza wartość funkcji wiarygodności (float).

**Opis:**  
Implementacja algorytmu Metropolis-Hastings do łamania szyfru podstawieniowego. W każdej iteracji generuje nowy klucz poprzez małą modyfikację obecnego, a następnie decyduje o jego akceptacji na podstawie poprawy wiarygodności i losowego prawdopodobieństwa. Pozwala na czasowe akceptowanie gorszych rozwiązań, co pomaga uniknąć minima lokalnego. Śledzi najlepsze znalezione rozwiązanie niezależnie od ścieżki przeszukiwania. 

**Kod:**
``` python
def metropolis_hastings_attack(cipher_text, reference_bigrams, iterations=10000):
    # Inicjalizacja początkowego klucza
    current_key = generate_key()
    current_inv_key = invert_key(current_key)
    current_decrypted = substitute(cipher_text, current_inv_key)
    current_bigrams = create_bigram_matrix(current_decrypted)
    current_log_likelihood = log_likelihood(current_bigrams, reference_bigrams)
    
    best_key = current_key
    best_log_likelihood = current_log_likelihood
    
    for t in range(iterations):
        # Generowanie nowego klucza przez zamianę dwóch liter
        new_key = generate_new_key(current_key)
        new_inv_key = invert_key(new_key)
        new_decrypted = substitute(cipher_text, new_inv_key)
        new_bigrams = create_bigram_matrix(new_decrypted)
        new_log_likelihood = log_likelihood(new_bigrams, reference_bigrams)
        
        # Obliczenie prawdopodobieństwa akceptacji nowego klucza
        acceptance_ratio = min(1.0, math.exp(new_log_likelihood - current_log_likelihood))
        
        # Akceptacja nowego klucza z pewnym prawdopodobieństwem
        if random.random() <= acceptance_ratio:
            current_key = new_key
            current_log_likelihood = new_log_likelihood
            
            # Aktualizacja najlepszego klucza, jeśli nowy jest lepszy
            if new_log_likelihood > best_log_likelihood:
                best_key = new_key
                best_log_likelihood = new_log_likelihood
        
        # Wyświetlanie postępu co 1000 iteracji
        if t % 1000 == 0:
            print(f"Iteracja {t}: aktualne log-wiarygodność = {current_log_likelihood:.2f}, najlepsze = {best_log_likelihood:.2f}")
    
    return best_key, best_log_likelihood
```

**2. Funkcja `mh_attack`**

**Wejście:**
- `input_file` (str): Plik z tekstem zaszyfrowanym.
- `output_file` (str): Plik wyjściowy.
- `reference_file` (str): Plik z tekstem referencyjnym.
- `iterations` (int): Liczba iteracji.

**Wyjście:**
- Zapisuje odszyfrowany tekst i klucz do plików.
- Wypisuje statystyki na stdout.

**Opis:**  
Funkcja przygotowująca dane i uruchamiająca atak Metropolis-Hastings. Wczytuje i czyści teksty, normalizuje macierz bigramów referencyjnych (dodaje 1 i normalizuje do rozkładu prawdopodobieństwa), a następnie wywołuje główny algorytm. Na koniec zapisuje wyniki i wypisuje podsumowanie. 

**Kod:**
``` python
def mh_attack(input_file, output_file, reference_file, iterations=10000):
    # Wczytanie zaszyfrowanego tekstu i jego oczyszczenie
    with open(input_file, 'r', encoding='utf-8') as f:
        cipher_text = clean_text(f.read())
    
    # Wczytanie tekstu referencyjnego i jego oczyszczenie
    with open(reference_file, 'r', encoding='utf-8') as f:
        reference_text = clean_text(f.read())
    reference_bigrams = create_bigram_matrix(reference_text)
    reference_bigrams += 1   # Dodaj 1 aby uniknąć log(0) - smoothing
    
    reference_bigrams += 1  # Dodanie 1 aby uniknąć zer
    row_sums = reference_bigrams.sum(axis=1)
    reference_bigrams = reference_bigrams / row_sums[:, np.newaxis]
    
    # Uruchomienie ataku Metropolis-Hastings
    best_key, best_log_likelihood = metropolis_hastings_attack(
        cipher_text, reference_bigrams, iterations)
    
    # Odszyfrowanie tekstu przy użyciu najlepszego znalezionego klucza
    best_inv_key = invert_key(best_key)
    decrypted_text = substitute(cipher_text, best_inv_key)
    
    # Zapisanie odszyfrowanego tekstu i klucza do pliku
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(decrypted_text)
    
    key_output_file = output_file + '.JSON'
    with open(key_output_file, 'w', encoding='utf-8') as kf:
        json.dump(best_key, kf)
    
    # Wypisanie wyników 
    print(f"Zakończono atak Metropolis-Hastings. Znaleziono klucz z log-wiarygodnością: {best_log_likelihood:.2f}")
    print(f"Zapisano odszyfrowany tekst do {output_file} i klucz do {key_output_file}")
```

#### Wyniki

**Wnioski:**



### Zadanie 3

Dokonać kryptoanalizy heurystycznej na zaimplementowany w ramach pierwszego zadania monoalfabetyczny kryptosystem podstawieniowy. Założenia ataku są takie jak w zadaniu 2. Do ataku wykorzystać algorytm optymalizacji Symulowanego Wyżarzania (ang. *Simulated Annealing*).

**Algorytm symulowanego wyżarzania**
Symulowane wyżarzanie to metoda optymalizacji inspirowana procesem fizycznym zwanym wyżarzaniem, który jest stosowany w metalurgii i krystalografii. Proces ten polega na podgrzewaniu materiału do wysokiej temperatury, a następnie stopniowym chłodzeniu w celu osiągnięcia stanu minimalnej energii. Algorytm
 
symulowanego wyżarzania wykorzystuje tę koncepcję, aby znaleźć rozwiązanie problemu optymalizacyjnego, które minimalizuje (lub maksymalizuje) pewną funkcję celu.

**Ogólny opis algorytmu**
1. **Inicjalizacja:**
   - Algorytm zaczyna od pewnego początkowego rozwiązania (np. losowego lub opartego na pewnej heurystyce).
   - Ustalana jest początkowa temperatura, która kontroluje prawdopodobieństwo akceptacji gorszych rozwiązań.

2. **Główna pętla:**
   - W każdej iteracji algorytm generuje nowe rozwiązanie poprzez niewielką modyfikację bieżącego rozwiązania (np. zamiana dwóch elementów w mapowaniu liter).
   - Obliczana jest różnica wyników między nowym a aktualnym rozwiązaniem.
     - Jeśli nowe rozwiązanie jest lepsze (ma wyższy wynik), to zostaje zaakceptowane.
     - Jeśli nowe rozwiązanie jest gorsze, to może ono zostać zaakceptowane z pewnym prawdopodo- bieństwem, które zależy od różnicy wyników i aktualnej temperatury. To prawdopodobieństwo jest obliczane jako:
$$
P = exp\left(\frac{score\_diff}{temperature}\right)
$$

3. **Schładzanie:**
   - Temperatura jest stopniowo zmniejszana zgodnie z określoną regułą chłodzenia (np. mnożenie przez współczynnik chłodzenia, który jest mniejszy od 1). W miarę spadku temperatury algorytm staje się mniej skłonny do akceptowania gorszych rozwiązań.

4. **Zakończenie:**
   - Algorytm kończy się po osiągnięciu określonej liczby iteracji lub po osiągnięciu bardzo niskiej temperatury, kiedy przestaje akceptować gorsze rozwiązania.
   - Ostateczne rozwiązanie jest uważane za przybliżone optimum globalne.

**Opis algorytmu w kontekście ataku na analizowany kryptosystem**

Dane wejściowe:
- c - szyfrogram,
- $\pi_0$ - początkowe mapowanie,
- g - n-gramy referencyjne (bigramy),
- N - maks. iteracje,
- $T_0$ -początkowa temperatura,
- α współczynnik chłodzenia 

Opis Symboli:
- c: Szyfrogram, który chcemy odszyfrować.
- $\pi$: Permutacja, mapowanie liter (klucz szyfrujący).
- g: Referencyjne n-gramy (bigramy).
- $S_{curr}$: Aktualna wartość funkcji celu.

---
**Algorithm 2 SA**

```
1:  π ← π₀
2:  S_curr ← f_{c,g}(π)
3:  π_best ← π
4:  S_best ← S_curr
5:  T ← T₀
6:  for k = 1 to N do
7:      a ~ U(A), b ~ U(A \ {a})                     ▷ A = {A, B, ..., Z}
8:      π' ← a↔b(π)
9:      S_new ← f_{c,g}(π')
10:     ΔS ← S_new - S_curr
11:     if ΔS > 0 or exp(ΔS / T) > u dla u ~ U(0,1) then
12:         π ← π'
13:         S_curr ← S_new
14:         if S_curr > S_best then
15:             π_best ← π
16:             S_best ← S_curr
17:         end if
18:     end if
19:     T ← α × T
20: end for
21: Return: π_best
```
---

- $S_{new}$: Nowa wartość funkcji celu po zamianie liter.
- T : Temperatura, która kontroluje prawdopodobieństwo akceptacji gorszych rozwiązań.
- u ∼ U(0, 1): Liczba losowa z rozkładu jednostajnego na przedziale [0, 1].
- $σ_{a,b}(π)$: funkcja losowej zamiany miejscami liter w permutacji π.
- $f_{c,g}(π)$: Funkcja celu, może one być zdefiniowana w następujący sposób:

$$
f_{c,g}(π) = \sum_{i,j}^n v_i \cdot \frac{ϕ_i}{max Φ}
$$

gdzie:
- $ν_i$: oznacza częstość i-tego bigramu w analizowanym szyfrogramie c, który odszyfrowany został przy pomocy klucza: π.
- $ϕ_i$: oznacza częstość i-tego bigramu w rozkładzie referencyjnym (bigramy: g).
- max Φ: to maksymalna wartość w rozkładzie referencyjnym bigramów Φ = {ϕ1, ϕ2, . . . , ϕn}. 
 
Należy zwrócić uwagę na to, iż funkcja $f_{c,g}(π)$ implementuje algorytm normalizacji (dzielenie przez
max Φ), dzięki temu eliminuje się potencjalny problem z dokładnością numeryczną.

**Uwaga.** W celu poprawy stabilności uzyskiwanych wyników oraz unikania lokalnych maksimów, algorytm symulowanego wyżarzania należy uruchamiać wielokrotnie. Za każdym razem inicjując algorytm inną permu- tacją klucza. Następnie porównywać uzyskany wynik z poprzednio uzyskanym wynikiem i zachowując lepszy. Symbolicznie, podejście to można opisać w następujący sposób:

gdzie:
- $Λ_{max}$: Najlepszy dotychczasowy wynik funkcji celu, reprezentujący maksymalną wartość oceny spośród wszystkich iteracji.
- $Θ_{opt}$: Najlepsze znalezione rozwiązanie (mapowanie liter - klucz), które maksymalizuje funkcję celu.
- k: Indeks iteracji, liczba całkowita biegnąca od 1 do N, gdzie N to liczba restartów algorytmu.

---
**Algorithm 3 Optymalizacja z wieloma restartami**

```
1:  Λ_max ← -∞
2:  Θ_opt ← ∅
3:  for k = 1 to N do
4:      π_k ~ U(A₂₆)                              ▷ Losowa permutacja z A₂₆, zbioru 26 liter
5:      Ψ_k, Λ_k ← Optimize(π_k)
6:      if Λ_k > Λ_max then
7:          Λ_max ← Λ_k
8:          Θ_opt ← Ψ_k
9:      end if
10: end for
11: return Θ_opt, Λ_max
```
---

- $π_k$: Losowa permutacja 26 liter alfabetu łacińskiego, wybrana z rozkładu jednostajnego $A_{26}$.
- $Ψ_k$: Rozwiązanie wygenerowane w k - tej iteracji, bazujące na permutacji $π_k$.
- $Λ_k$: Wartość funkcji celu dla rozwiązania $Ψ_k$.
- $A_{26}$: Zbiór wszystkich możliwych permutacji 26-literowego alfabetu.
- $U(A_{26})$: Rozkład jednostajny na zbiorze $A_{26}$, z którego losowana jest permutacja $π_k$.


#### Implementacja

**1. Funkcja `simulated_annealing_attack`**

**12. Funkcja simulated_annealing_attack**

**Wejście:**
- `cipher_text` (str): Tekst zaszyfrowany.
- `reference_bigrams` (numpy.ndarray): Macierz bigramów referencyjnych.
- `initial_temp` (float): Początkowa temperatura.
- `cooling_rate` (float): Szybkość schładzania.
- `iterations` (int): Liczba iteracji.

**Wyjście:**
- Najlepszy klucz i wartość funkcji celu.

**Opis:**  
Implementacja symulowanego wyżarzania dla problemu łamania szyfru. Podobna do Metropolis-Hastings, ale z dynamicznie malejącą "temperaturą", która systematycznie zmniejsza prawdopodobieństwo akceptacji gorszych rozwiązań. W wysokich temperaturach eksploruje przestrzeń rozwiązań, w niskich skupia się na eksploatacji najlepszych obszarów. Parametry temperatury mają kluczowe znaczenie dla skuteczności.

**Kod:**
``` python
def simulated_annealing_attack(cipher_text, reference_bigrams, initial_temp=1000.0, cooling_rate=0.99, iterations=10000):
    # Inicjalizacja klucza i temperatury
    current_key = generate_key()
    current_inv_key = invert_key(current_key)
    current_decrypted = substitute(cipher_text, current_inv_key)
    current_bigrams = create_bigram_matrix(current_decrypted)
    current_score = log_likelihood(current_bigrams, reference_bigrams)
    
    best_key = current_key
    best_score = current_score
    
    temp = initial_temp
    
    for i in range(iterations):
        # Generowanie nowego klucza
        new_key = generate_new_key(current_key)
        new_inv_key = invert_key(new_key)
        new_decrypted = substitute(cipher_text, new_inv_key)
        new_bigrams = create_bigram_matrix(new_decrypted)
        new_score = log_likelihood(new_bigrams, reference_bigrams)
        
        # Obliczenie różnicy w ocenie
        score_diff = new_score - current_score
        
        # Decyzja o akceptacji nowego klucza
        if score_diff > 0:
            accept = True # Akceptuj, jeśli nowy klucz jest lepszy
        else:
            # Akceptuj z prawdopodobieństwem zależnym od temperatury
            accept_prob = math.exp(score_diff / temp)
            accept = random.random() < accept_prob
        
        if accept:
            current_key = new_key
            current_score = new_score
            
            # Aktualizacja najlepszego klucza
            if current_score > best_score:
                best_key = current_key
                best_score = current_score
        
        # Zmniejszenie temperatury (schładzanie)
        temp *= cooling_rate
        
        # Wyświetlanie postępu co 1000 iteracji
        if i % 1000 == 0:
            print(f"Iteration {i}: temp={temp:.2f}, current_score={current_score:.2f}, best_score={best_score:.2f}")
    
    return best_key, best_score
```

**2. Funkcja `sa_attack`**

**Wejście:**
- `input_file`, `output_file`, `reference_file`: Ścieżki plików.
- `iterations`, `initial_temp`, `cooling_rate`: Parametry algorytmu.

**Wyjście:**
- Zapisuje wyniki do plików.

**Opis:**  
Funkcja przygotowująca i uruchamiająca symulowane wyżarzanie. Podobna w działaniu do mh_attack, ale z dodatkowymi parametrami kontrolującymi proces schładzania. Normalizuje macierz referencyjną i zarządza zapisem wyników.

**Kod:**
``` python
def sa_attack(input_file, output_file, reference_file, iterations=10000, initial_temp=1000.0, cooling_rate=0.99):
    # Wczytanie zaszyfrowanego tekstu i jego oczyszczenie
    with open(input_file, 'r', encoding='utf-8') as f:
        cipher_text = clean_text(f.read())
    
    # Wczytanie tekstu referencyjnego i jego oczyszczenie
    with open(reference_file, 'r', encoding='utf-8') as f:
        reference_text = clean_text(f.read())
    reference_bigrams = create_bigram_matrix(reference_text)
    
    reference_bigrams += 1 # Dodanie 1 aby uniknąć zer (smoothing)
    row_sums = reference_bigrams.sum(axis=1)
    reference_bigrams = reference_bigrams / row_sums[:, np.newaxis]
    
    # Uruchomienie ataku Symulowanego Wyżarzania
    best_key, best_score = simulated_annealing_attack(
        cipher_text, reference_bigrams, initial_temp, cooling_rate, iterations)
    
    # Odszyfrowanie tekstu przy użyciu najlepszego znalezionego klucza
    best_inv_key = invert_key(best_key)
    decrypted_text = substitute(cipher_text, best_inv_key)
    
    # Zapisanie odszyfrowanego tekstu i klucza do pliku
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(decrypted_text)
    
    key_output_file = output_file + '.JSON'
    with open(key_output_file, 'w', encoding='utf-8') as kf:
        json.dump(best_key, kf)
    
    # Wypisanie wyników
    print(f"Atak symulowanego wyżarzania zakończony. Znaleziono klucz z log-wiarygodnością: {best_score:.2f}")
    print(f"Zapisano odszyfrowany tekst do {output_file} i klucz do {key_output_file}")
```

#### Wyniki

**Wnioski:**



### Zadanie 4

Dokonać kryptoanalizy heurystycznej na zaimplementowany w ramach pierwszego zadania monoalfabetyczny kryptosystem podstawieniowy. Założenia ataku są takie jak w zadaniach 2 i 3. Do ataku wykorzystać gene- tyczny algorytm optymalizacji.

**Algorytm genetyczny**

Algorytm genetyczny (AG) to metoda optymalizacji inspirowana zasadami ewolucji biologicznej. Wykorzy- stuje pojęcia takie jak selekcja naturalna, krzyżowanie (rekombinacja) oraz mutacja. Jego celem jest znale- zienie rozwiązania problemu, które będzie jak najlepsze według określonej funkcji celu (fitness). Algorytmy genetyczne są często stosowane do rozwiązywania problemów trudnych obliczeniowo, takich jak optymalizacja w przestrzeni wielowymiarowej, planowanie, projektowanie, identyfikacja parametryczna modeli matematycz- nych czy też kryptoanaliza.

**Ogólny opis algorytmu**

Podstawowe komponenty algorytmu genetycznego:
- Populacja: Zbiór możliwych rozwiązań, zwanych osobnikami lub chromosomami. Populacja ewoluuje z pokolenia na pokolenie.
- Chromosom: Reprezentacja kandydata na rozwiązanie. Zwykle jest przedstawiany jako ciąg znaków lub cyfr binarnych, na które zamieniane są inne struktury danych, zależnie od charakteru problemu.
- Funkcja dopasowania (fitness function): Funkcja, która ocenia jakość każdego osobnika. Określa, jak dobrze dany chromosom rozwiązuje problem.

Operatory genetyczne:
- **Selekcja** lub inaczej **Reprodukcja**: Proces wybierania najlepszych osobników, które będą rodzicami przyszłych generacji.
  - Popularne metody selekcji obejmują selekcję ruletkową, turniejową lub rankingową.
- **Krzyżowanie** (crossover): Proces łączenia dwóch osobników (rodziców) w celu wygenerowania nowych osobników (potomków).
  - Celem jest wymiana genów między rodzicami, co może prowadzić do tworzenia lepszych rozwiązań.
- **Mutacja**: Proces wprowadzania niewielkich zmian w genotypie osobnika, aby zapewnić różnorodność genetyczną w populacji i uniknąć zbieżności do lokalnych minimów.

Parametry algorytmu:
- **Rozmiar populacji**: m - liczba osobników w każdej generacji (w rozpatrywanym przypadku jest to liczba kluczy).
- **Prawdopodobieństwo krzyżowania**: $p_c$ - procent rodziców który ulega krzyżowaniu.
- **Prawdopodobieństwo mutacji**: $p_m$ - prawdopodobieństwo modyfikacji genów (w rozpatrywanym przypadku jest prawdopodobieństwo zmian liter w kluczu).
- **Maksymalne odchylenie standardowe** funkcji dopasowania: max $s_f$ - kryterium zbieżności.
- **Maksymalna liczba generacji**: $i_max$. 

Ogólny schemat działania algorytmu genetycznego:
1.	**Inicjalizacja**:
  - Algorytm zaczyna od stworzenia początkowej populacji m losowych kluczy szyfrujących.
    - Klucz to permutacja alfabetu, która reprezentuje potencjalne rozwiązanie.
2.	**Ewaluacja funkcji dopasowania**:
  - Obliczyć wartość funkcji dopasowania korzystając funkcji logarytmicznej wiarygodności dla każ- dego klucza.
    - Porównując częstości bigramów w tekście zaszyfrowanym po zdekodowaniu przy użyciu klucza z częstościami referencyjnymi.
3.	**Selekcja**:
  - Wykorzystać algorytm ruletkowej selekcji, w której osobniki są wybierane z populacji z prawdo- podobieństwem proporcjonalnym do ich wartości funkcji dopasowania.
    - To oznacza, że lepiej dopasowane osobniki mają większą szansę na wybór.
  - Dla każdego osobnika (klucza) πi w populacji, prawdopodobieństwo wyboru wynosi:  
$$
p_i = \frac{S(π_i)}{\sum_{j=1}^{m} S(π_j)}
$$  
gdzie $S(π_i)$ jest funkcją wartości dopasowania dla osobnika $π_i$.

---
**Algorithm 4 Selekcja ruletkowa**

```
Require: 𝒫 = {π₁, π₂, ..., π_m}, S(π_i) ∀π_i ∈ 𝒫
Ensure: π_selected

1:  F ← ∑_{i=1}^{m} S(π_i)                         ▷ Sumaryczna wartość funkcji dopasowania
2:  p_i ← S(π_i) / F    ∀ i ∈ {1, 2, ..., m}        ▷ Prawdopodobieństwa wyboru
3:  r ~ U(0,1)                                      ▷ Losowa liczba z rozkładu jednostajnego
4:  C ← 0                                           ▷ Suma skumulowana
5:  for i ← 1 to m do
6:      C ← C + p_i
7:      if r ≤ C then
8:          return π_i                              ▷ Zwróć wybrany osobnik
9:      end if
10: end for
```
---

4. **Operatory genetyczne:**
- Dokonać operacji krzyżowania (crossover):
     - Dwaj rodzice są łączeni w celu stworzenia dwóch potomków.
     - Wykorzystać algorytm krzyżowania jednopunktowego, co oznacza, że losowo wybierany jest punkt cięcia, po którym geny (litery) są wymieniane między rodzicami.  
    Rodzice: $π_1$ = [$x_1$, . . . , $x_k$, . . . , $x_{26}$], $π_2$ = [$y_1$, . . . , $y_k$, . . . , $y_{26}$]  
    Dzieci: $π_1$ = [$x_1$, . . . , $x_k$, $y_{k+1}$, . . . , $y_{26}$], $π_2$ = [$y_1$, . . . , $y_k$, $x_{k+1}$, . . . , $x_{26}$]

---
**Algorithm 5 Krzyżowanie**

```
Require: π₁, π₂                                     ▷ Rodzice
Ensure: π_child1, π_child2                         ▷ Potomkowie

1:  k ~ U({1, ..., 25})                            ▷ Losowy punkt cięcia
2:  π_child1 ← [π₁[1:k] ∪ π₂[k+1:26]]
3:  π_child2 ← [π₂[1:k] ∪ π₁[k+1:26]]
4:  return π_child1, π_child2
```
---

- Dokonać operacji mutacji :
  - Z niewielkim prawdopodobieństwem zamienić dwa znaki w kluczu miejscami (geny w chro- mosomie).
    - Zapewnia to różnorodność genetyczną i zapobiega zbieżności do lokalnych minimów.  
    $π = [x_1, . . . , x_a, . . . , x_b, . . . , x_{26}] ⇒ π′ = [x_1, . . . , x_b, . . . , x_a, . . . , x_{26}$]


---
**Algorithm 6 Mutacja**

```
Require: π                                          ▷ Chromosom
Ensure: π'                                         ▷ Zmutowany chromosom

1:  a, b ~ U({1, ..., 26}),  a ≠ b                  ▷ Losowe indeksy
2:  π' ← a↔b(π)                                     ▷ Zamiana miejsc elementów π[a] i π[b]
3:  return π'
```
---

5. **Warunki zakończenia:**
   - Algorytm powinien sprawdzać, czy populacja osiągnęła zbieżność, to znaczy czy odchylenie stan- dardowe wartości dopasowania jest mniejsze niż przyjęte maksymalne odchylenie standardowe.
   - Jeśli nie osiągnięto zbieżności, to należy kontynuować proces iteracyjny aż osiągnięcia maksymalnej liczby generacji
6. **Zwrócenie najlepszego rozwiązania:**
   - Po zakończeniu algorytmu wybierany powinien być klucz, który miał najwyższą wartość funkcji dopasowania.
     - Jest to klucz, który najlepiej odtwarza oryginalny tekst.

**Opis algorytmu w kontekście ataku na analizowany kryptosystem**

Dane wejściowe:
- c - szyfrogram.
- g - n-gramy referencyjne (bigramy).
- m - rozmiar populacji.
- $p_c$ - prawdopodbieństwo krzyżowania.
- $p_m$ - prawdopodobieństwo mutacji.
 
- $i_{max}$ - maksymalna liczba generacji.
- $s_f$ - odchylenie standardowe funkcji dopasowania do wszystkich osobników z populacji P. Opis użytych symboli:
- π - Pojedynczy chromosom (klucz), permutacja liter alfabetu łacińskiego.
- $π_{best}$ - Najlepsza permutacja (klucz szyfrujący) znaleziona podczas ewolucji.
- S(π) - Wartość funkcji dopasowania dla permutacji π.
- P - Populacja permutacji kluczy szyfrujących.
- arg max - Oznacza wybór klucza z największą wartością funkcji dopasowania.
- $s_f ^{max}$ - Maksymalna dopuszczalna wartość odchylenia standardowego.
- $S_{RW}(P, S)$ - Selekcja ruletkowa, która wybiera osobnika π z populacji P proporcjonalnie do wartości funkcji dopasowania S(π).
- C - Operator krzyżowania.
- M - Operator mutacji.

---
**Algorithm 7 GA**

```
Require: c, g, m, p_c, p_m, i_max, S_max^σ
Ensure: π_best

1:  𝒫 ← {π_i ~ Perm(𝒜) | i = 1, ..., m}             ▷ Losowe permutacje alfabetu
2:  S(π) ← f_{c,g}(π)    ∀π ∈ 𝒫
3:  π_best ← arg max_{π ∈ 𝒫} S(π)
4:  for i ← 1 to i_max do
5:      σ_f ← √[1/m ∑_{π ∈ 𝒫} (S(π) - 1/m ∑_{π ∈ 𝒫} S(π))²]  ▷ Oblicz odchylenie standardowe
6:      if σ_f ≤ S_max^σ then
7:          break                                        ▷ Zakończ, jeśli populacja jest zbieżna
8:      end if
9:      𝒫' ← ∅
10:     for j ← 1 to m/2 do
11:         π₁ ← SRW(𝒫, S)                          ▷ Selekcja ruletkowa
12:         π₂ ← SRW(𝒫 \ {π₁}, S)                  ▷ Selekcja ruletkowa bez π₁
13:         if u₁ ~ U(0,1) < p_c then
14:             (π_child1, π_child2) ← C(π₁, π₂)   ▷ Krzyżowanie
15:         else
16:             (π_child1, π_child2) ← (π₁, π₂)
17:         end if
18:         𝒫' ← 𝒫' ∪ {π_child1, π_child2}
19:     end for
20:     for all π ∈ 𝒫' do
21:         if u₂ ~ U(0,1) < p_m then
22:             π ← 𝓜(π)                          ▷ Mutacja
23:         end if
24:     end for
25:     S(π) ← f_{c,g}(π)    ∀π ∈ 𝒫'
26:     π_best ← arg max (S(π_best), max_{π ∈ 𝒫'} S(π))
27:     𝒫 ← 𝒫'
28: end for
29: return π_best
```
---

#### Implementacja

**1. Funkcja `fitness_function`**

**Wejście:**
- `decrypted_text` (str): Tekst do oceny.
- `reference_bigrams` (numpy.ndarray): Macierz referencyjna.

**Wyjście:**
- Wartość fitness (float).

**Opis:**  
Funkcja oceny jakości rozwiązania w algorytmie genetycznym. Wykorzystuje logarytmiczną funkcję wiarygodności bigramów. Im wyższa wartość, tym lepiej tekst pasuje do wzorca języka.

**Kod:**
``` python
def fitness_function(decrypted_text, reference_bigrams):
    decrypted_bigrams = create_bigram_matrix(decrypted_text)
    return log_likelihood(decrypted_bigrams, reference_bigrams)
```

**2. Funkcja `roulette_wheel_selection`**

**Wejście:**
- `population` (list): Populacja kluczy.
- `fitness_scores` (list): Oceny fitness.

**Wyjście:**
- Wybrany klucz (dict).

**Opis:**  
Implementacja selekcji ruletkowej w algorytmie genetycznym. Wybiera klucz z prawdopodobieństwem proporcjonalnym do jego fitness. Obsługuje przypadki skrajne (zerowy sumaryczny fitness).

**Kod:**
``` python
def roulette_wheel_selection(population, fitness_scores):
    total_fitness = sum(fitness_scores)
    if total_fitness == 0:
        return random.choice(population)
    probabilities = [score/total_fitness for score in fitness_scores]
    r = random.random()
    cumulative = 0
    for i, prob in enumerate(probabilities):
        cumulative += prob
        if r <= cumulative:
            return population[i]
    return population[-1]
```

**3. Funkcja `single_point_crossover`**

**Wejście:**
- `parent1`, `parent2` (dict): Klucze-rodzice.

**Wyjście:**
- Dwa nowe klucze (dict).

**Opis:**  
Operator krzyżowania jednopunktowego. Dzieli alfabet na dwie części i łączy odpowiednie fragmenty kluczy rodzicielskich. Zapewnia, że potomkowie są poprawnymi permutacjami poprzez specjalną obsługę konfliktów w mapowaniach. 

**Kod:**
``` python
def single_point_crossover(parent1, parent2):
    letters = string.ascii_uppercase
    child1 = parent1.copy()
    child2 = parent2.copy()
    
    # Wybierz punkt krzyżowania losowo w zakresie 1-24
    crossover_point = random.randint(1, 24)
    
    # Zamień litery w kluczach rodzicielskich na podstawie punktu krzyżowania
    parent1_letters = {k: v for k, v in parent1.items() if ord(k) - ord('A') >= crossover_point}
    parent2_letters = {k: v for k, v in parent2.items() if ord(k) - ord('A') >= crossover_point}
    
    # Stwórz mapowanie dla konfliktowych liter
    conflict_map1 = {}
    conflict_map2 = {}
    
    # Obsługuje konflikty w child1 (parent1 + ogon parent2)
    for letter in parent2_letters:
        new_val = parent2_letters[letter]
        original_val = parent1[letter]
        
        # Sprawdź, czy new_val jest już przypisany do czegoś innego
        for k, v in child1.items():
            if v == new_val and k != letter:
                conflict_map1[k] = original_val
                break
        
        child1[letter] = new_val
    
    # Rozwiązuje konflikty w child1
    for k, v in conflict_map1.items():
        child1[k] = v
    
    # To samo co powyżej, ale dla child2
    # Obsługuje konflikty w child2 (parent2 + ogon parent1)
    for letter in parent1_letters:
        new_val = parent1_letters[letter]
        original_val = parent2[letter]
        
        # Sprawdź, czy new_val jest już przypisany do czegoś innego
        for k, v in child2.items():
            if v == new_val and k != letter:
                conflict_map2[k] = original_val
                break
        
        child2[letter] = new_val
    
    # Rozwiązuje konflikty w child2
    for k, v in conflict_map2.items():
        child2[k] = v
    
    return child1, child2
```

**4. Funkcja `genetic_algorithm_attack`**

**Wejście:**
- `cipher_text` (str): Tekst zaszyfrowany.
- `reference_bigrams` (numpy.ndarray): Macierz referencyjna.
- `population_size` (int): Rozmiar populacji.
- `crossover_prob` (float): Prawd. krzyżowania.
- `mutation_prob` (float): Prawd. mutacji.
- `max_generations` (int): Maks. liczba pokoleń.
- `max_std_dev` (float): Kryterium zbieżności.

**Wyjście:**
- Najlepszy klucz i wartość fitness.

**Opis:**  
Pełna implementacja algorytmu genetycznego. Inicjalizuje populację, ewaluuje fitness, przeprowadza selekcję, krzyżowanie i mutację przez wiele pokoleń. Monitoruje zbieżność poprzez odchylenie standardowe fitness i może zakończyć się wcześniej, jeśli populacja się ustabilizuje.

**Kod:**
``` python
def genetic_algorithm_attack(cipher_text, reference_bigrams, population_size=100, crossover_prob=0.8, mutation_prob=0.2, max_generations=1000, max_std_dev=0.1):
    # Inicjalizacja populacji losowymi kluczami
    population = [generate_key() for _ in range(population_size)]
    
    # Obliczenie fitness dla każdego klucza w populacji
    fitness_scores = []
    for key in population:
        inv_key = invert_key(key)
        decrypted = substitute(cipher_text, inv_key)
        score = fitness_function(decrypted, reference_bigrams)
        fitness_scores.append(score)
    
    # Znalezienie najlepszego klucza w początkowej populacji
    best_key = population[np.argmax(fitness_scores)]
    best_score = max(fitness_scores)
    
    for generation in range(max_generations):
        new_population = []
        
        # Obliczenie statystyk populacji
        mean_fitness = np.mean(fitness_scores)
        std_dev = np.std(fitness_scores)
        
        # Sprawdzenie zbieżności (jeśli odchylenie standardowe jest małe)
        if std_dev < max_std_dev:
            print(f"Converged at generation {generation} with std dev {std_dev:.4f}")
            break
        
        # Tworzenie nowej populacji
        while len(new_population) < population_size:
            # Selekcja rodziców metodą ruletki
            parent1 = roulette_wheel_selection(population, fitness_scores)
            parent2 = roulette_wheel_selection(population, fitness_scores)
            
            # Krzyżowanie z prawdopodobieństwem crossover_prob
            if random.random() < crossover_prob:
                child1, child2 = single_point_crossover(parent1, parent2)
            else:
                child1, child2 = parent1.copy(), parent2.copy()
            
            # Mutacja z prawdopodobieństwem mutation_prob
            if random.random() < mutation_prob:
                child1 = generate_new_key(child1)
            if random.random() < mutation_prob:
                child2 = generate_new_key(child2)
            
            new_population.extend([child1, child2])
        
        # Przycięcie populacji do oryginalnego rozmiaru
        population = new_population[:population_size]
        
        # Obliczenie fitness dla nowej populacji
        fitness_scores = []
        for key in population:
            inv_key = invert_key(key)
            decrypted = substitute(cipher_text, inv_key)
            score = fitness_function(decrypted, reference_bigrams)
            fitness_scores.append(score)
        
        # Aktualizacja najlepszego klucza
        current_best_idx = np.argmax(fitness_scores)
        if fitness_scores[current_best_idx] > best_score:
            best_key = population[current_best_idx]
            best_score = fitness_scores[current_best_idx]
        
        # Wyświetlanie postępu co 100 generacji
        if generation % 100 == 0:
            print(f"Generation {generation}: Best score = {best_score:.2f}, Mean score = {mean_fitness:.2f}, Std dev = {std_dev:.4f}")
    
    return best_key, best_score
```

**5. Funkcja `ga_attack`**

**Wejście:**
- Parametry plików i parametry algorytmu.

**Wyjście:**
- Zapisuje wyniki do plików.

**Opis:**  
Funkcja przygotowująca dane i uruchamiająca algorytm genetyczny. Wczytuje i czyści teksty, przygotowuje macierz referencyjną, uruchamia główny algorytm i zarządza wynikami. 

**Kod:**
``` python
def ga_attack(input_file, output_file, reference_file, population_size=100, crossover_prob=0.8, mutation_prob=0.2, max_generations=1000, max_std_dev=0.1):
    
    # Wczytanie zaszyfrowanego tekstu i usunięcie niealfabetycznych znaków
    with open(input_file, 'r', encoding='utf-8') as f:
        cipher_text = clean_text(f.read())
    
    # Wczytanie tekstu referencyjnego i stworzenie macierzy bigramów
    with open(reference_file, 'r', encoding='utf-8') as f:
        reference_text = clean_text(f.read())
    reference_bigrams = create_bigram_matrix(reference_text)
    
    # Dodanie 1 do macierzy bigramów, aby uniknąć zer (smoothing)
    reference_bigrams += 1
    row_sums = reference_bigrams.sum(axis=1)
    reference_bigrams = reference_bigrams / row_sums[:, np.newaxis]
    
    # Uruchomienie algorytmu genetycznego
    best_key, best_score = genetic_algorithm_attack(
        cipher_text, reference_bigrams, population_size, crossover_prob,
        mutation_prob, max_generations, max_std_dev)
    
    # Odszyfrowanie tekstu za pomocą najlepszego klucza
    best_inv_key = invert_key(best_key)
    decrypted_text = substitute(cipher_text, best_inv_key)
    
    # Zapisanie odszyfrowanego tekstu i klucza do pliku
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(decrypted_text)
    
    key_output_file = output_file + '.JSON'
    with open(key_output_file, 'w', encoding='utf-8') as kf:
        json.dump(best_key, kf)
    
    # Wypisanie wyników i zapisanie najlepszego odszyfrowanego tekstu i klucza do pliku
    print(f"Genetic algorithm attack completed. Best score: {best_score:.2f}")
    print(f"Decrypted text saved to {output_file}, key saved to {key_output_file}")
```

#### Wyniki

**Wnioski:**



### Implementacja głównej funkcji programu

**Funkcja `Main`**

**Wejście:**
- Argumenty wiersza poleceń (argparse).

**Wyjście:**
- Wynik odpowiedniej operacji.

**Opis:**  
Główna funkcja programu. Parsuje argumenty, weryfikuje ich poprawność i wywołuje odpowiednią funkcję (szyfrowanie, deszyfrowanie lub wybrany atak) z podanymi parametrami. Obsługuje błędy wejściowe i zapewnia odpowiednie komunikaty dla użytkownika.

**Kod:**
```python
def main():
    parser = argparse.ArgumentParser(description='Szyfr podstawieniowy')
    parser.add_argument('-i', '--input', required=True, help='Plik wejściowy z tekstem')
    parser.add_argument('-o', '--output', required=True, help='Plik wyjściowy z wynikiem')
    parser.add_argument('-k', '--key', help='Plik do zapisania/odczytu klucza')
    parser.add_argument('-e', '--encrypt', action='store_true', help='Tryb szyfrowania')
    parser.add_argument('-d', '--decrypt', action='store_true', help='Tryb deszyfrowania')
    parser.add_argument('-a', '--attack', choices=['bf', 'mh', 'sa', 'ga'], 
                       help='Tryb ataku (bf - brute force, mh - Metropolis-Hastings, sa - Simulated Annealing, ga - Genetic Algorithm)')
    parser.add_argument('-r', '--reference', help='Plik z tekstem referencyjnym (wymagany dla ataków MH, SA i GA)')
    parser.add_argument('--iterations', type=int, default=10000, help='Liczba iteracji dla ataków BF, MH i SA')
    parser.add_argument('--initial-temp', type=float, default=1000.0, help='Początkowa temperatura dla ataku SA')
    parser.add_argument('--cooling-rate', type=float, default=0.99, help='Współczynnik chłodzenia dla ataku SA')
    parser.add_argument('--population-size', type=int, default=100, help='Rozmiar populacji dla ataku GA')
    parser.add_argument('--crossover-prob', type=float, default=0.8, help='Prawdopodobieństwo krzyżowania dla ataku GA')
    parser.add_argument('--mutation-prob', type=float, default=0.2, help='Prawdopodobieństwo mutacji dla ataku GA')
    parser.add_argument('--max-std-dev', type=float, default=0.1, help='Maksymalne odchylenie standardowe dla zbieżności w ataku GA')
    parser.add_argument('-g', '--generate-key', action='store_true', 
                       help='Wymuś generację nowego klucza (tylko dla szyfrowania)')
    
    args = parser.parse_args()
    
    # Sprawdzenie poprawności argumentów
    if args.attack == 'bf':
        brute_force_attack(args.input, args.output)
    elif args.attack == 'mh':
        if not args.reference:
            raise ValueError("Plik referencyjny jest wymagany dla ataku Metropolis-Hastings.")
        mh_attack(args.input, args.output, args.reference, args.iterations)
    elif args.attack == 'sa':
        if not args.reference:
            raise ValueError("Plik referencyjny jest wymagany dla ataku Symulowanego Wyżarzania.")
        sa_attack(args.input, args.output, args.reference, args.iterations, 
                 args.initial_temp, args.cooling_rate)
    elif args.attack == 'ga':
        if not args.reference:
            raise ValueError("Plik referencyjny jest wymagany dla ataku Algorytmem Genetycznym.")
        ga_attack(args.input, args.output, args.reference, args.population_size,
                 args.crossover_prob, args.mutation_prob, args.iterations,
                 args.max_std_dev)
    else:
        if args.encrypt and args.decrypt:
            raise ValueError("Nie można jednocześnie wybrać trybu szyfrowania i deszyfrowania.")
        if not args.key:
            raise ValueError("Plik klucza jest wymagany dla trybów szyfrowania i deszyfrowania.")
        
        process_file(args.input, args.output, args.key, 
                    args.encrypt, args.decrypt, args.generate_key)
```

### Zadanie 5

Dokonać analizy pracy zaimplementowanych algorytmów, porównując ich wydajność w ataku na analizowany kryptosystem.

#### Implementacja

#### Wyniki

**Wnioski:**