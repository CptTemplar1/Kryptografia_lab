import argparse

def berlekamp_massey(sequence):
    n = len(sequence)

    C = [1]  # Wielomian połączeń (connection polynomial)
    B = [1]  # Kopia pomocnicza wielomianu połączeń
    L = 0    # Złożoność liniowa
    m = -1   # Indeks ostatniej aktualizacji

    for N in range(n):
        # Krok 1: Obliczanie rozbieżności d
        d = sequence[N]
        for i in range(1, L + 1):
            if i < len(C):
                d ^= C[i] & sequence[N - i]

        if d == 0:
            continue  # Jeśli nie ma rozbieżności, przejdź do następnego elementu
        else:
            # Krok 2: Aktualizacja wielomianu połączeń
            T = C.copy()
            przesuniecie = N - m
            if len(C) < len(B) + przesuniecie:
                C += [0] * (len(B) + przesuniecie - len(C))

            for i in range(len(B)):
                C[i + przesuniecie] ^= B[i]

            # Krok 3: Aktualizacja złożoności liniowej
            if 2 * L <= N:
                L = N + 1 - L
                B = T
                m = N

    # Odwrócenie kolejności współczynników, aby pasowały do generatora LFSR z zadania 1
    return C[::-1], L

def format_polynomial(C):
    terms = []
    for i, coeff in enumerate(C):
        if coeff == 1:
            if i == 0:
                terms.append("1")
            elif i == 1:
                terms.append("x")
            else:
                terms.append(f"x^{i}")
    return " + ".join(terms)

def main():
    # Parsowanie argumentów wejściowych
    parser = argparse.ArgumentParser(description="Algorytm Berlekampa-Masseya nad GF(2)")
    parser.add_argument('--sequence', '-s', nargs='+', type=int, required=True,
                        help="Wprowadź sekwencję bitów (np. --sequence 1 0 1 0 1)")
    args = parser.parse_args()

    # Przypisanie sekwencji do zmiennej
    sequence = args.sequence

    # Sprawdzenie, czy sekwencja zawiera tylko 0 i 1
    if not all(bit in (0, 1) for bit in sequence):
        print("Błąd: Sekwencja może zawierać tylko bity 0 i 1.")
        return

    # Uruchomienie algorytmu Berlekampa-Masseya
    polynomial, complexity = berlekamp_massey(sequence)

    # Wyświetlanie wyników
    print(f"Złożoność liniowa (L): {complexity}")
    print(f"Współczynniki wielomianu połączeń (C(x)) (lista współczynników): {polynomial}")
    print(f"Wielomian połączeń C(x) w postaci czytelnej: {format_polynomial(polynomial)}")

if __name__ == "__main__":
    main()
