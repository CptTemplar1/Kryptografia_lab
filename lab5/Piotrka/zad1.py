"""
zad1.py
Implementacja kryptosystemu strumieniowego z LFSR z wbudowanymi tapami i stanem początkowym.
Polinom: P(x)=1 + x + x^3 + x^5 + x^16 + x^17.
Sekwencja inicjująca: [0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1]
"""
import sys

# Hardcoded LFSR parameters
TAPS = [0, 1, 3, 5, 16]
INITIAL_STATE = [0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1]

def generate_keystream(length):
    """Generuje keystream długości `length` bitów na bazie LFSR."""
    state = INITIAL_STATE.copy()
    keystream = []
    for _ in range(length):
        # Wyjście: ostatni bit rejestru
        keystream.append(state[-1])
        # Oblicz nowy bit jako XOR wybranych tapów
        new_bit = 0
        for t in TAPS:
            new_bit ^= state[t]
        # Przesuń rejestr w prawo i wstaw nowy bit na początku
        state = [new_bit] + state[:-1]
    return keystream

def bits_from_bytes(data_bytes):
    """Konwertuje bajty na listę bitów MSB-first."""
    bits = []
    for b in data_bytes:
        for i in range(7, -1, -1):
            bits.append((b >> i) & 1)
    return bits

def bytes_from_bits(bits):
    """Konwertuje listę bitów MSB-first na bajty."""
    out = bytearray()
    for i in range(0, len(bits), 8):
        byte = 0
        for j in range(8):
            byte = (byte << 1) | bits[i + j]
        out.append(byte)
    return bytes(out)

def encrypt(input_path, output_path):
    with open(input_path, 'rb') as f:
        plaintext = f.read()
    pt_bits = bits_from_bytes(plaintext)
    ks = generate_keystream(len(pt_bits))
    ct_bits = [pt_bits[i] ^ ks[i] for i in range(len(pt_bits))]
    ciphertext = bytes_from_bits(ct_bits)
    with open(output_path, 'wb') as f:
        f.write(ciphertext)

if len(sys.argv) != 4:
    print("Użycie: python zad1.py <encrypt|decrypt> <wejście> <wyjście>")
    sys.exit(1)
mode, inp, outp = sys.argv[1:]
if mode not in ('encrypt', 'decrypt'):
    print("Tryb nieznany. Wybierz 'encrypt' lub 'decrypt'.")
    sys.exit(1)
# Dla strumieniowego szyfrowania i deszyfrowania operacja jest identyczna
encrypt(inp, outp)