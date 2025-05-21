"""
zad2.py
Atak KPA: znany plaintext + ciphertext.
1) Odtwarza fragment keystreamu jako XOR znanego plaintextu i ciphertextu.
2) Używa algorytmu Berlekamp-Massey, by określić LFSR (L i wielomian C).
3) Jako IV bierze pierwsze L bitów keystreamu, a taps to [j-1 for j where C[j]==1].
4) Generuje pełny keystream i odszyfrowuje cały szyfrogram.
5) Zapisuje wynik do pliku i sprawdza poprawność UTF-8.
"""
import sys

def berlekamp_massey(s):
    n = len(s)
    C = [1] + [0]*n
    B = [1] + [0]*n
    L, m = 0, 1
    for i in range(n):
        d = s[i]
        for j in range(1, L+1):
            d ^= C[j] & s[i-j]
        if d:
            T = C.copy()
            for j in range(len(B)):
                if B[j]:
                    C[j+m] ^= 1
            if 2 * L <= i:
                L, B = i+1-L, T
                m = 1
            else:
                m += 1
        else:
            m += 1
    return L, C[:L+1]

def bits_from_bytes(data):
    bits = []
    for byte in data:
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)
    return bits

def bytes_from_bits(bits):
    out = bytearray()
    for i in range(0, len(bits), 8):
        byte = 0
        for bit in bits[i:i+8]:
            byte = (byte << 1) | bit
        out.append(byte)
    return bytes(out)

def generate_keystream(iv, taps, length):
    state = iv.copy()
    ks = []
    for _ in range(length):
        ks.append(state[-1])
        new = 0
        for t in taps:
            new ^= state[t]
        state = [new] + state[:-1]
    return ks

if len(sys.argv) != 4:
    print("Użycie: python3 zad2.py <known_plaintext> <ciphertext> <output_plaintext>")
    sys.exit(1)

pt_file, ct_file, out_file = sys.argv[1:]
pt = open(pt_file, 'rb').read()
ct = open(ct_file, 'rb').read()
pt_bits = bits_from_bytes(pt)
ct_bits = bits_from_bytes(ct)
n = len(ct_bits)

# 1) odzyskanie fragmentu keystreamu
ks_frag = [pt_bits[i] ^ ct_bits[i] for i in range(min(len(pt_bits), n))]

# 2) algorytm BM
L, C = berlekamp_massey(ks_frag)
print(f"Odnalezione LFSR: długość L={L}, wielomian C={C}")

# 3) wyznaczenie IV i tapów
iv = ks_frag[:L]
print(f"Zrekonstruowany IV (pierwsze {L} bitów):", iv)
taps = [j-1 for j in range(1, len(C)) if C[j] == 1]
print("Pozycje taps:", taps)

# 4) generacja full keystreamu i odszyfrowanie
full_ks = generate_keystream(iv, taps, n)
dec_bits = [ct_bits[i] ^ full_ks[i] for i in range(n)]
plaintext = bytes_from_bits(dec_bits)
with open(out_file, 'wb') as f:
    f.write(plaintext)
print(f"Odszyfrowano cały szyfrogram do pliku: {out_file}")

# 5) walidacja UTF-8
try:
    _ = plaintext.decode('utf-8')
    print("Dekodowanie UTF-8 powiodło się.")
except UnicodeDecodeError:
    print("Uwaga: dekodowanie UTF-8 NIE powiodło się. Sprawdź poprawność plaintext.")
