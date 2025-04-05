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

#### Wyniki

**Wnioski:**



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
COŚ
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
COŚ
```
---

- $π_k$: Losowa permutacja 26 liter alfabetu łacińskiego, wybrana z rozkładu jednostajnego $A_{26}$.
- $Ψ_k$: Rozwiązanie wygenerowane w k - tej iteracji, bazujące na permutacji $π_k$.
- $Λ_k$: Wartość funkcji celu dla rozwiązania $Ψ_k$.
- $A_{26}$: Zbiór wszystkich możliwych permutacji 26-literowego alfabetu.
- $U(A_{26})$: Rozkład jednostajny na zbiorze $A_{26}$, z którego losowana jest permutacja $π_k$.


#### Implementacja

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
COŚ
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
COŚ
```
---

- Dokonać operacji mutacji :
  - Z niewielkim prawdopodobieństwem zamienić dwa znaki w kluczu miejscami (geny w chro- mosomie).
    - Zapewnia to różnorodność genetyczną i zapobiega zbieżności do lokalnych minimów.  
    $π = [x_1, . . . , x_a, . . . , x_b, . . . , x_{26}] ⇒ π′ = [x_1, . . . , x_b, . . . , x_a, . . . , x_{26}$]


---
**Algorithm 6 Mutacja**

```
COŚ
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
COŚ
```
---

#### Implementacja

#### Wyniki

**Wnioski:**

### Zadanie 5

Dokonać analizy pracy zaimplementowanych algorytmów, porównując ich wydajność w ataku na analizowany kryptosystem.

#### Implementacja

#### Wyniki

**Wnioski:**