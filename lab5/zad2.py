import argparse
from itertools import combinations

# Poprawiona implementacja algorytmu Berlekampa-Massey'ego z ograniczeniem długości
def berlekamp_massey(sequence, max_length=64):
    n = len(sequence)
    if n == 0:
        return []

    # Inicjalizacja
    C = [1] + [0] * (max_length - 1)
    B = [1] + [0] * (max_length - 1)
    L = 0
    m = 1
    b = 1

    for n_iter in range(n):
        if n_iter >= max_length * 2:
            break  # Ograniczamy analizę do rozsądnej długości

        # Oblicz różnicę d
        d = 0
        for i in range(min(L + 1, max_length)):
            d ^= C[i] & sequence[n_iter - i]
        d %= 2

        if d == 1:
            if 2 * L > n_iter:
                # Aktualizacja wielomianu
                for i in range(max_length - m):
                    if B[i] == 1:
                        C[i + m] ^= 1
                m += 1
            else:
                T = C.copy()
                for i in range(max_length - (n_iter + 1 - L)):
                    C[i + (n_iter + 1 - L)] ^= B[i]
                L = n_iter + 1 - L
                B = T
                m = 1
                b = 1
        else:
            m += 1

    # Zwróć pozycje sprzężeń (pomijając pierwszy element)
    taps = [i for i in range(1, min(L + 1, max_length)) if C[i] == 1]
    return taps

# Funkcja do testowania poprawności LFSR
def test_lfsr(sequence, length, taps):
    if not taps or max(taps) >= length:
        return False
    
    # Weź początkowy stan z sekwencji
    state = sequence[:length]
    
    # Sprawdź czy generuje resztę sekwencji
    for i in range(length, len(sequence)):
        new_bit = 0
        for t in taps:
            new_bit ^= state[t]
        new_bit %= 2
        
        if new_bit != sequence[i]:
            return False
            
        state = state[1:] + [new_bit]
    
    return True

# Funkcja znajdowania LFSR przez brute force dla małych długości
def find_lfsr(sequence, max_length=16):
    for length in range(2, max_length + 1):
        # Wygeneruj wszystkie możliwe kombinacje tapów
        for tap_count in range(1, length):
            for taps in combinations(range(1, length), tap_count):
                if test_lfsr(sequence, length, taps):
                    return length, taps
    return None, None

# Funkcje pomocnicze (jak poprzednio)
def text_to_bits(text):
    return [int(bit) for byte in text.encode('utf-8') for bit in format(byte, '08b')]

def bits_to_text(bits):
    bytes_list = []
    for b in range(0, len(bits), 8):
        byte = bits[b:b + 8]
        if len(byte) < 8:
            break
        bytes_list.append(int("".join(map(str, byte)), 2))
    return bytes(bytes_list).decode('utf-8', errors='ignore')

def xor_bits(bits1, bits2):
    return [b1 ^ b2 for b1, b2 in zip(bits1, bits2)]

def lfsr(initial_state, taps, output_length):
    state = initial_state.copy()
    output = []
    for _ in range(output_length):
        output.append(state[0])
        new_bit = 0
        for t in taps:
            new_bit ^= state[t]
        state = state[1:] + [new_bit]
    return output

def main():
    parser = argparse.ArgumentParser(description="Atak na kryptosystem LFSR z zadania 1")
    parser.add_argument('--plaintext_file', '-p', required=True, help="Plik z tekstem jawnym")
    parser.add_argument('--ciphertext_file', '-c', required=True, help="Plik z szyfrogramem (ciąg bitów)")
    parser.add_argument('--output_file', '-o', required=True, help="Plik wyjściowy z odszyfrowanym tekstem")
    args = parser.parse_args()

    # Wczytaj dane
    with open(args.plaintext_file, 'r', encoding='utf-8') as f:
        plaintext = f.read()
    plaintext_bits = text_to_bits(plaintext)

    with open(args.ciphertext_file, 'r', encoding='utf-8') as f:
        bit_str = f.read().strip()
    ciphertext_bits = [int(b) for b in bit_str.split()]

    # 1. Odzyskanie klucza
    recovered_key = xor_bits(plaintext_bits, ciphertext_bits)
    print(f"✅ Odzyskano klucz: {recovered_key[:20]}... (pierwsze 20 bitów)")

    # 2. Znajdź LFSR - najpierw spróbuj brute force dla krótkich długości
    #print("🔍 Próba znalezienia LFSR metodą brute force dla krótkich długości...")
    #lfsr_length, taps = find_lfsr(recovered_key, max_length=16)
    
    #if lfsr_length is None:
    #    print("🔍 Brute force nie znalazł rozwiązania, próba algorytmu Berlekampa-Massey'ego...")
    #    taps = berlekamp_massey(recovered_key)
    #    if taps:
    #        lfsr_length = max(taps) + 1
    #    else:
    #        lfsr_length = 0

    taps = berlekamp_massey(recovered_key)
    if taps:
        lfsr_length = max(taps) + 1
    else:
        lfsr_length = 0

    if not taps:
        print("❌ Nie udało się znaleźć sprzężeń LFSR")
        print("⏭ Przechodzę do odszyfrowania bezpośrednio odzyskanym kluczem...")
        decrypted_bits = xor_bits(ciphertext_bits, recovered_key)
        decrypted_text = bits_to_text(decrypted_bits)
        
        with open(args.output_file, 'w', encoding='utf-8') as f:
            f.write(decrypted_text)
        
        print(f"✅ Tekst odszyfrowany bezpośrednio odzyskanym kluczem zapisano do: {args.output_file}")
        return

    print(f"✅ Znaleziono sprzężenia LFSR na pozycjach: {taps}")
    print(f"✅ Długość rejestru LFSR: {lfsr_length}")

    # 3. Pobierz początkowy stan rejestru
    initial_state = recovered_key[:lfsr_length]
    print(f"✅ Początkowy stan rejestru: {initial_state}")

    # 4. Sprawdź czy generowany klucz pasuje
    generated_key = lfsr(initial_state, taps, len(recovered_key))
    
    if generated_key == recovered_key:
        print("✅ Klucze się zgadzają! Odtworzono poprawny LFSR.")
        decrypted_bits = xor_bits(ciphertext_bits, generated_key)
    else:
        print("❌ Klucze się nie zgadzają. Używam odzyskanego klucza...")
        decrypted_bits = xor_bits(ciphertext_bits, recovered_key)

    decrypted_text = bits_to_text(decrypted_bits)
    
    with open(args.output_file, 'w', encoding='utf-8') as f:
        f.write(decrypted_text)
    
    print(f"✅ Odszyfrowany tekst zapisano do: {args.output_file}")

if __name__ == "__main__":
    main()