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

...

#### Wyniki

W ramach zadania 1 zaimplementowano kryptosystem strumieniowy wykorzystujący rejestr LFSR (Linear Feedback Shift Register) do generowania strumienia klucza. Rejestr został skonfigurowany zgodnie z podanym wielomianem połączeń $P(x) = 1 + x + x^3 + x^5 + x^{16} + x^{17}$ oraz sekwencją inicjującą `[0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1]`. Te zmienne zostały umieszczone w kodzie "na sztywno" za pomocą zmiennych globalnych. Implementacja umożliwia zarówno szyfrowanie, jak i deszyfrowanie tekstu poprzez operację XOR na bitach tekstu jawnego i strumienia klucza.

**Proces szyfrowania:**  
Wykorzystano fragment powieści "Moby Dick" jako tekst jawny (plik `tekst_jawny.txt`). Tekst został zaszyfrowany przy użyciu następującego polecenia:  
`dotnet run -- encrypt tekst_jawny.txt szyfrogram.txt`

**Tekst jawny (plik `tekst_jawny.txt`):**  
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

W rezultacie szyfrowania powstał plik `szyfrogram.txt`, który zawiera zaszyfrowany tekst. Plik ten jest binarny i nieczytelny w formie tekstowej. Poniżej przedstawiono zawartość pliku `szyfrogram.txt`:

**Uzyskany szyfrogram (plik `szyfrogram.txt`):**  
```plaintext
öô^a¶gťl4™Gf85!ń‹O»¦·elŰŞR‰­Ę©A¸<ŘÓáóP›ěp¤ŻŠV·^^v†×5 ||Čâüô­Ěě.Úé"µ2{ÖŮ8»‰t­Ç§.>Ź=©fIůKÄĆâ6 "˘ăĎ÷Ŕ|Ůž™Î—râ*­s’VLţ$,ˇżîZ˘»hÝ•o‡
 đőhpĂęđĹd3Ť_›D¸ďQűD˙x1«ÚU§ĎŞ,msămč†ŠŤm—ďń%6«or6 ň)TŹpqp;ď’>RÁqîŰ@sřfŇ8®˛Ô”6zúVo•6ĚCŽ°úŠÜPOFěř+xGXQŹ)8Tş×şÇ“ď6PaÁÇE‹ Ç‘ÝA!uß±ą,
˝9Ż †ĺŹ©§"ęS8KrOüçţŹđ­T˙njL;}óxBöĆ0śyZůşś¦DHĂólŃügôđ.*q" śF‰y ŽúëgK”ŃĎ¬˝ľZD&űTčý€´Ťdď.Ű°vŠÝY{éŻ|¦Ą‡÷ĺĐ’™ăY5Ţ›ŁYÎ~&Ň™ :BYŽ¤—MŇ<ÇV(6ď˙X€ngŁ(JP¨/‡ýÔ<„0÷…’,Ň'Ĺ˙Üw6źâmh ,ÚB˙‚x6Ł×ÚĂ ĂéKXÝ“ć‚} `ž»gK¶űSz­wŰŇ2XNűvŐ??.‘GqttMRűOé¦ňb„qžąTŠ­íěZ¸+Śžł˝UĆ—Łb÷ŇĺP¸UMîľ+;|~Ô´ńçűČűi’ü;®57Ôś#éÚoˇ[Š©.{m°m´Z…Ř°*.ď‹é¶Úp„Ö·őrřm˙f‚QQĺ"*íżĽ	˘¦'ÚśLgšđč9ÎŁôĎO'3´
ŠZ˛ôBł]şU]•OTß©Şir{čdş†€”`—ýĄ<+©mr> âf ž}J%k*˝€:RKi Ďl
¬oEĎ3Şţµça‚QeÔu1Ń
€ăŞŽ“]S|ěř)nGXË/9G˝ÁbőŔ–¬-[5’Ţ]Î
ŔÚ• ;x’Ů“Sb®#ă±›«śćó9ęY9tLňý·ţre¦P˙%<}!4ÉxMě9Ĺ4]ćóĺŮW_ŚâjÍAŃ
öđ0Z$
Ye8DČLŤ5ĎŻČfÇŃŮä¨¸V^,úô´Š¦ÁM"ç Ă˛Ć%ď÷~hôş&ľ´ŐÖýŐ×ů‹T.“¨ĹIF}=žGËTmYKŹł…›<ÇV?*čţn4˛%G…QÉú!8őÂŢXř>.ŐţŹ’yeÝévrbŢ
ę‘c(ńÉČŘĚ¦WÚ×Ż=C	šézM´ŻSŇj•Ţ|HIű·3kpÔGo9tXľ‡F÷˙żaź?’Ą’ĺÁĄEý*ťŮúřQ„ÓđhéÇ P´\^iĂŰ(;|bťâ™ź¸Íç;“ö#á0rÁ€w§Ě{°_Óč43“=łiń‚Óü,ińÎ±ůŮy‹”ÖÎ—~¬"îf’JšM.¤ŞôZ»±f”
```

**Proces deszyfrowania:**  
W celu sprawdzenia poprawności działania całego programu, zaszyfrowany plik (`szyfrogram.txt`) został następnie odszyfrowany z użyciem tego samego klucza (domyślne parametry LFSR w programie). W tym celu użyto następującego polecenia:    
`dotnet run -- decrypt szyfrogram.txt tekst_odszyfrowany.txt`

**Weryfikacja wyników:**  
Porównanie plików `tekst_jawny.txt` i `tekst_odszyfrowany.txt` wykazało ich identyczność, co potwierdza poprawność działania implementacji. Oryginalny tekst został w pełni odzyskany, co ilustruje odwracalność operacji XOR w szyfrach strumieniowych.

**Wnioski**  
Implementacja kryptosystemu strumieniowego opartego na LFSR działa zgodnie z założeniami. Zarówno szyfrowanie, jak i deszyfrowanie zostały wykonane poprawnie, a tekst odszyfrowany jest identyczny z oryginalnym tekstem jawnym. 

### Zadanie 2

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

...

#### Wyniki

W ramach zadania 2 przeprowadzono atak na kryptosystem strumieniowy zaimplementowany w zadaniu 1, wykorzystując znany fragment tekstu jawnego (`tekst_jawny.txt`) oraz odpowiadający mu szyfrogram (`szyfrogram.txt`). Celem ataku było odzyskanie klucza, określenie schematu połączeń rejestru LFSR oraz zbudowanie własnego kryptosystemu zdolnego do odszyfrowania wiadomości. 

Program został uruchomiony za pomocą następującego polecenia, w którym jako argumenty podano nazwy plików z tekstem jawnym, szyfrogramem oraz plikiem wyjściowym:
`dotnet run -- tekst_jawny.txt szyfrogram.txt tekst_odszyfrowany_po_ataku.txt`  

1. **Odzyskanie klucza:**  
   - Fragment strumienia klucza został odzyskany poprzez operację XOR na bitach tekstu jawnego i szyfrogramu.  
   - Algorytm Berlekampa-Massey'a zidentyfikował parametry rejestru LFSR:  
     - Długość rejestru: `L = 11`  
     - Wielomian charakterystyczny: $C(x) = 1 + x^5 + x^6 + x^8 + x^{10} + x^{11}$ (reprezentowany jako `[1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1]`).  
     - Pozycje sprzężeń zwrotnych (taps): `[4, 5, 7, 9, 10]`.  
   - Zrekonstruowany wektor inicjujący (IV): `[1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1]` (pierwsze 11 bitów strumienia klucza). 

2. **Odszyfrowanie:**  
   - Zidentyfikowany wielomian charakterystyczny **nie pokrywa się** z wielomianem użytym w kryptosystemie z zadania 1 $P(x) = 1 + x + x^3 + x^5 + x^{16} + x^{17}$.  
   - Na podstawie odzyskanych parametrów wygenerowano pełny strumień klucza i odszyfrowano cały szyfrogram.  
   - Mimo niezgodności wielomianów, odszyfrowanie zakończyło się sukcesem, a plik `tekst_odszyfrowany_po_ataku.txt` był identyczny z oryginalnym tekstem jawnym, co potwierdzono przez pomyślne dekodowanie UTF-8. 

Poniżej przedstawiono odszyfowany za pomocą algorytmu Berlekampa-Massey'a tekst:
**Odszyfrowany tekst (plik `tekst_odszyfrowany_po_ataku.txt`):**  
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

**Wnioski:**
Algorytm Berlekampa-Massey'a znajduje **najkrótszy możliwy rejestr** generujący dany fragment strumienia klucza. W tym przypadku 11-bitowy LFSR okazał się wystarczający do odtworzenia sekwencji klucza dla dostępnego fragmentu danych. Ponieważ znany fragment tekstu jawnego był długi (zawierał wystarczającą liczbę bitów), wygenerowany strumień klucza z mniejszego LFSR (L=11) **pokrywał się** z fragmentem użytym do szyfrowania. Operacja XOR jest odwracalna – nawet jeśli strumień klucza został wygenerowany przez inny LFSR, ale jego wartości binarne były identyczne dla danej pozycji, odszyfrowanie pozostaje poprawne.  

Atak udowodnił, że **krótszy LFSR może generować taki sam fragment strumienia klucza** jak oryginalny, co wystarcza do złamania szyfru przy znanym tekście jawnym. **Oryginalny LFSR (L=17) był nadmiarowy** dla tej konkretnej sekwencji – jego dodatkowe bity nie wpłynęły na unikalność strumienia klucza w analizowanym fragmencie. W praktyce oznacza to, że bezpieczeństwo LFSR zależy nie tylko od długości rejestru, ale także od **ilości dostępnych danych do analizy**.

### Zadanie 3

Dokonać ataku na zbudowany w ramach pierwszego zadania kryptosystem Przyjąć następujące złożenia ataku:
- Znane są tylko: szyfrogram i początkowy fragment tekstu jawnego.
- Celem ataku jest:
  - Odzyskanie klucza.
  - Określenie schematu połączeń rejestru LFSR.
  - Określenie minimalnej długości (ilości bitów) tekstu jawnego, umożliwiającego odzyskanie kompletnej wiadomości.
  - Określenie zależności pomiędzy złożonością liniową zidentyfikowanego kryptosystemu, maksymalną sekwencją klucza, która generowana jest przez ten kryptosystem a wymaganą minimalną długością znanego tekstu jawnego.

#### Implementacja

...

#### Wyniki

W ramach zadania 3 przeprowadzono atak na kryptosystem strumieniowy wykorzystujący LFSR, analizując wpływ długości znanego fragmentu tekstu jawnego na skuteczność ataku. Badanie obejmowało dwa scenariusze: z wystarczającym i niewystarczającym fragmentem tekstu jawnego.

W zadaniu wykorzystaliśmy zaszyfrowaną wiadomość (`szyfrogram.txt`) z zadania 1. Poniżej przedstawiono zawartość pliku z szyfrogramem:
```plaintext
öô^a¶gťl4™Gf85!ń‹O»¦·elŰŞR‰­Ę©A¸<ŘÓáóP›ěp¤ŻŠV·^^v†×5 ||Čâüô­Ěě.Úé"µ2{ÖŮ8»‰t­Ç§.>Ź=©fIůKÄĆâ6 "˘ăĎ÷Ŕ|Ůž™Î—râ*­s’VLţ$,ˇżîZ˘»hÝ•o‡
 đőhpĂęđĹd3Ť_›D¸ďQűD˙x1«ÚU§ĎŞ,msămč†ŠŤm—ďń%6«or6 ň)TŹpqp;ď’>RÁqîŰ@sřfŇ8®˛Ô”6zúVo•6ĚCŽ°úŠÜPOFěř+xGXQŹ)8Tş×şÇ“ď6PaÁÇE‹ Ç‘ÝA!uß±ą,
˝9Ż †ĺŹ©§"ęS8KrOüçţŹđ­T˙njL;}óxBöĆ0śyZůşś¦DHĂólŃügôđ.*q" śF‰y ŽúëgK”ŃĎ¬˝ľZD&űTčý€´Ťdď.Ű°vŠÝY{éŻ|¦Ą‡÷ĺĐ’™ăY5Ţ›ŁYÎ~&Ň™ :BYŽ¤—MŇ<ÇV(6ď˙X€ngŁ(JP¨/‡ýÔ<„0÷…’,Ň'Ĺ˙Üw6źâmh ,ÚB˙‚x6Ł×ÚĂ ĂéKXÝ“ć‚} `ž»gK¶űSz­wŰŇ2XNűvŐ??.‘GqttMRűOé¦ňb„qžąTŠ­íěZ¸+Śžł˝UĆ—Łb÷ŇĺP¸UMîľ+;|~Ô´ńçűČűi’ü;®57Ôś#éÚoˇ[Š©.{m°m´Z…Ř°*.ď‹é¶Úp„Ö·őrřm˙f‚QQĺ"*íżĽ	˘¦'ÚśLgšđč9ÎŁôĎO'3´
ŠZ˛ôBł]şU]•OTß©Şir{čdş†€”`—ýĄ<+©mr> âf ž}J%k*˝€:RKi Ďl
¬oEĎ3Şţµça‚QeÔu1Ń
€ăŞŽ“]S|ěř)nGXË/9G˝ÁbőŔ–¬-[5’Ţ]Î
ŔÚ• ;x’Ů“Sb®#ă±›«śćó9ęY9tLňý·ţre¦P˙%<}!4ÉxMě9Ĺ4]ćóĺŮW_ŚâjÍAŃ
öđ0Z$
Ye8DČLŤ5ĎŻČfÇŃŮä¨¸V^,úô´Š¦ÁM"ç Ă˛Ć%ď÷~hôş&ľ´ŐÖýŐ×ů‹T.“¨ĹIF}=žGËTmYKŹł…›<ÇV?*čţn4˛%G…QÉú!8őÂŢXř>.ŐţŹ’yeÝévrbŢ
ę‘c(ńÉČŘĚ¦WÚ×Ż=C	šézM´ŻSŇj•Ţ|HIű·3kpÔGo9tXľ‡F÷˙żaź?’Ą’ĺÁĄEý*ťŮúřQ„ÓđhéÇ P´\^iĂŰ(;|bťâ™ź¸Íç;“ö#á0rÁ€w§Ě{°_Óč43“=łiń‚Óü,ińÎ±ůŮy‹”ÖÎ—~¬"îf’JšM.¤ŞôZ»±f”
```

**Przeprowadzone ataki i wyniki**
1. **Atak z wystarczającym fragmentem tekstu jawnego (fragment_tekstu_jawnego_1.txt):**
   - **Dane wejściowe:** 178 bajtów tekstu jawnego (1424 bity).
   - **Wynik analizy:**
     - Zidentyfikowany LFSR: `L=11`, wielomian $C(x)=1 + x^5 + x^6 + x^8 + x^{10} + x^{11}$.
     - Wektor inicjujący (IV): `[1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1]`.
     - Pozycje sprzężeń zwrotnych (taps): `[4, 5, 7, 9, 10]`.
   - **Minimalna wymagana długość tekstu:** 22 bity (2.75 bajta) – znacznie mniej niż użyty fragment.
   - **Rezultat:** Poprawnie odszyfrowany tekst (plik `tekst_odszyfrowany_atakiem_1.txt`), identyczny z oryginałem. Dekodowanie UTF-8 powiodło się.
    - **Wykorzystany fragment tekstu jawnego (plik `fragment_tekstu_jawnego_1.txt`):**  
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
    ```
    - **Odszyfrowany tekst (plik `tekst_odszyfrowany_atakiem_1.txt`):**  
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

2. **Atak z niewystarczającym fragmentem tekstu jawnego (fragment_tekstu_jawnego_2.txt):**
   - **Dane wejściowe:** 2 bajty tekstu jawnego (16 bitów).
   - **Wynik analizy:**
     - Zidentyfikowany LFSR: `L=8`, wielomian $C(x)=1 + x^8$.
     - Wektor inicjujący (IV): `[1, 0, 1, 1, 0, 1, 0, 1]`.
     - Pozycje sprzężeń zwrotnych (taps): `[7]`.
   - **Minimalna wymagana długość tekstu:** 16 bitów (2 bajty) – teoretycznie wystarczająca, ale:
     - **Problem:** Algorytm znalazł **krótszy LFSR** (L=8), który generował zgodny strumień klucza tylko dla 16 bitów, ale nie dla całej wiadomości.
     - **Rezultat:** Błędne odszyfrowanie (plik `tekst_odszyfrowany_atakiem_2.txt` zawierał losowe znaki). Dekodowanie UTF-8 nie powiodło się.
   - **Wykorzystany fragment tekstu jawnego (plik `fragment_tekstu_jawnego_2.txt`):**  
    ```plaintext
    CA
    ```
    - **Odszyfrowany tekst (plik `tekst_odszyfrowany_atakiem_1.txt`):**  
    ```plaintext
    [Y ̳ 0   4 ˕   \& 
     . v  $ g  u~L^ %6A 	'    ۲+z    eOQY aA wD   {t $   j
    "   T ik O   NbZm t34c: O   ?  S  C  p8  *   ]X ݮnG ]h  ɞ  6 B V R՜w  
    b    N E+ '  :B\     ߛ _  "ݢ ݖB?  l  Cv ޶U ˬ y9  W  8  a #W'q    AU.      "   .z j>B    lj & j<p  r    
    +H"
    G       QJS" ]    R    ^  [k 1Ե  T 1
    n^ | Q Y]     ܏ 1 $Ԫ#WF  9|b  V  EP-   B v. 'p  D 
    *ZH}?4N  s6 c   5  4    #	:  j   BR -       * P y ) Z(?   hR.qڛ2O  ŭ w R/՛zwn nD  p>K/Ъ 3  V    v   V x   <      V= D
    _ ) 3 ' @A  !3 k: ZH      C    y\JVeV ?Q   y1 Dw  '  .    (u    B&Dw 5){X U R /  H  @ 
    w1  7   ]EҔ c Yb⦊  ' Y    =8  r    E + -9 :P     ߓ O˪3  Ƈ-  %  
    b      b  SJ̵/  y؜| -N #>     AU.      f   l= Xm;    ?s c mw8   ?t>   N 61K^ G       _P, S  
    R  Ќ d  A% h    K ^Ht  !O ` | []     ȕ e    be˲j|tI  W  Y'
    l  J nk BZ  Y x{PxzT&  >, h   5 3 f    "( 6 j   ES ,Ù  (  d W , 5 Xos U  xS"?  pD  ߡ s G<΅\deu a
    wz=  7D     8s   V    y    * ZR 2 ? ?Hl P 0tWU )~] Dj
      Ĳnv    0O42`J >[ L  l- 
    a  ~E  > ĩ\ /~ Q   \cTt &9{c:  C ? 7  	 Y  9
    ```

**Wnioski:**
1. **Minimalna długość tekstu jawnego:**  
   Algorytm Berlekampa-Massey'a wymaga **co najmniej 2L bitów** znanego tekstu (gdzie `L` to długość rejestru), aby poprawnie zidentyfikować LFSR. W tym przypadku:
   - Dla L=11: wymagane 22 bity (~3 bajty).
   - Dla L=17 (oryginalny LFSR): wymagane 34 bity (~4.25 bajta).

2. **Dlaczego krótki fragment zawiódł?**  
   - **Niedostateczna złożoność liniowa:** 16 bitów wystarczyło do identyfikacji LFSR o L=8, ale nie L=17.  
   - **Błędne przybliżenie:** Krótszy LFSR generował **tylko lokalnie zgodny** strumień klucza, co prowadziło do błędów w dalszej części szyfrogramu.

3. **Efektywność ataku:**  
   - **Kilka bajtów wystarczy:** W praktyce, znając nawet **kilkadziesiąt bajtów** tekstu jawnego (np. nagłówek pliku), można złamać szyfr.  
   - **Maksymalny okres sekwencji:** Dla L=11 wynosi 2047 bitów (~256 bajtów), co pokazuje, że LFSR szybko się powtarza, ułatwiając atak.

**Podsumowując**
- **Podatność LFSR:** Nawet minimalna znajomość tekstu jawnego (kilka bajtów) pozwala na odzyskanie klucza, jeśli LFSR jest krótki (L < 20).  
- **Bezpieczeństwo praktyczne:** W rzeczywistych systemach należy:
  - Unikać pojedynczych LFSR.
  - Stosować nieliniowe przekształcenia strumienia klucza.
  - Używać kombinacji wielu rejestrów (np. A5/1 w GSM).  
- **Znaczenie długości klucza:** Dla L=17 wymagane jest ~4.25 bajta tekstu jawnego, ale już L=32 podnosi wymóg do 8 bajtów, znacząco utrudniając atak.