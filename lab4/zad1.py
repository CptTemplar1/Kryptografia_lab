import argparse

#Funkcja realizująca działanie LFSR.
def lfsr(initial_state, taps, output_length):
    state = initial_state.copy()
    output = []

    for _ in range(output_length):
        # Zapisz obecny bit wyjściowy
        output.append(state[0])

        # Oblicz nowy bit jako XOR wskazanych pozycji (taps)
        new_bit = 0
        for t in taps:
            new_bit ^= state[t]

        # Przesunięcie rejestru w prawo i wstawienie nowego bitu
        state = state[1:] + [new_bit]

    return output

#Główna funkcja programu
def main():
    parser = argparse.ArgumentParser(description="LFSR Generator")

    # Definicja flag
    parser.add_argument('--initial_state', '-i', nargs='+', type=int, required=True,
                        help="Stan początkowy rejestru jako lista bitów, np. 0 0 1")
    parser.add_argument('--taps', '-t', nargs='+', type=int, required=True,
                        help="Indeksy sprzężenia zwrotnego, licząc od 0 (od lewej do prawej), np. 0 1")
    parser.add_argument('--output_length', '-o', type=int, required=True,
                        help="Żądana długość strumienia wyjściowego")

    args = parser.parse_args()

    # Wywołanie funkcji LFSR
    output = lfsr(args.initial_state, args.taps, args.output_length)

    # Wyświetlenie wyniku
    print("Wygenerowana sekwencja:", output)

if __name__ == "__main__":
    main()
