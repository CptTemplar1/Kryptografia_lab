import argparse

# Funkcja realizująca LFSR — generator strumienia klucza
def lfsr(initial_state, taps, output_length):
    state = initial_state.copy()
    output = []

    # Generowanie kolejnych bitów strumienia
    for _ in range(output_length):
        output.append(state[0])  # bit wyjściowy to pierwszy bit rejestru
        new_bit = 0

        # XOR bitów wskazanych przez tap-y (sprzężenia zwrotne)
        for t in taps:
            new_bit ^= state[t]

        # Przesunięcie rejestru i dodanie nowego bitu na końcu
        state = state[1:] + [new_bit]

    return output

# Zamiana tekstu na listę bitów (ciąg 0 i 1 dla każdego znaku ASCII)
def text_to_bits(text):
    return [int(bit) for char in text for bit in format(ord(char), '08b')]

# Zamiana listy bitów z powrotem na tekst (co 8 bitów = 1 znak)
def bits_to_text(bits):
    chars = []
    for b in range(0, len(bits), 8):
        byte = bits[b:b + 8]
        if len(byte) < 8:
            break  # pomijamy niepełny bajt
        chars.append(chr(int("".join(map(str, byte)), 2)))
    return ''.join(chars)

# Funkcja XOR dwóch list bitów
def xor_bits(bits1, bits2):
    return [b1 ^ b2 for b1, b2 in zip(bits1, bits2)]

# Funkcja szyfrująca tekst z wykorzystaniem LFSR
def encrypt(message, initial_state, taps):
    message_bits = text_to_bits(message)  # tekst na bity
    keystream = lfsr(initial_state, taps, len(message_bits))  # generowanie klucza
    encrypted_bits = xor_bits(message_bits, keystream)  # XOR wiadomości z kluczem
    return encrypted_bits

# Funkcja deszyfrująca — identyczna operacja XOR z tym samym kluczem
def decrypt(bits, initial_state, taps):
    keystream = lfsr(initial_state, taps, len(bits))  # generowanie klucza
    decrypted_bits = xor_bits(bits, keystream)  # XOR szyfrogramu z kluczem
    return bits_to_text(decrypted_bits)  # bity na tekst

# Główna funkcja programu
def main():
    parser = argparse.ArgumentParser(description="Strumieniowy kryptosystem LFSR")
    
    # Wybór trybu działania — tylko jeden z dwóch naraz
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-e', '--encrypt', action='store_true', help="Tryb szyfrowania")
    group.add_argument('-d', '--decrypt', action='store_true', help="Tryb deszyfrowania")
    
    # Pliki wejściowy i wyjściowy oraz parametry LFSR
    parser.add_argument('--input_file', '-in', required=True, help="Plik wejściowy")
    parser.add_argument('--output_file', '-out', required=True, help="Plik wyjściowy")
    parser.add_argument('--initial_state', '-i', nargs='+', type=int, required=True, help="Stan początkowy LFSR, np. 1 0 1 1")
    parser.add_argument('--taps', '-t', nargs='+', type=int, required=True, help="Pozycje sprzężenia zwrotnego, np. 0 2")
    
    args = parser.parse_args()

    if args.encrypt:
        # Odczytaj tekst jawny z pliku
        with open(args.input_file, 'r', encoding='utf-8') as f:
            plaintext = f.read()

        # Zaszyfruj tekst i zapisz bity do pliku
        encrypted_bits = encrypt(plaintext, args.initial_state, args.taps)
        with open(args.output_file, 'w', encoding='utf-8') as f:
            f.write(' '.join(str(bit) for bit in encrypted_bits))

        print(f"✅ Wiadomość zaszyfrowana i zapisana do: {args.output_file}")

    elif args.decrypt:
        # Odczytaj szyfrogram (ciąg bitów) z pliku
        with open(args.input_file, 'r', encoding='utf-8') as f:
            bit_str = f.read().strip()

        # Zamień ciąg tekstowy na listę bitów
        bits = [int(b) for b in bit_str.split()]

        # Odszyfruj i zapisz tekst jawny
        decrypted_text = decrypt(bits, args.initial_state, args.taps)
        with open(args.output_file, 'w', encoding='utf-8') as f:
            f.write(decrypted_text)

        print(f"✅ Wiadomość odszyfrowana i zapisana do: {args.output_file}")

if __name__ == "__main__":
    main()