"""
zad3.py
Atak CKPA: znany fragment plaintext + ciphertext.
Procedura:
1) Odtworzenie fragmentu keystreamu (XOR fragmentu plaintextu i ciphertextu).
2) Algorytm Berlekamp–Massey do znalezienia L i wektora C.
3) Obliczenie minimalnej długości (2L) i maksymalnego okresu (2^L - 1).
4) Generacja pełnego keystreamu, odszyfrowanie całego szyfrogramu.
5) Dekodowanie UTF-8 i zapis wyniku do pliku tekstowego.
"""
import sys

def bytes_to_bits(data):
    bits = []
    for byte in data:
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)
    return bits

def bits_to_bytes(bits):
    out = bytearray()
    for i in range(0, len(bits), 8):
        byte = 0
        for bit in bits[i:i+8]:
            byte = (byte << 1) | bit
        out.append(byte)
    return bytes(out)

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
    print("Użycie: python3 zad3.py <ciphertext> <plaintext_fragment> <output_text>")
    sys.exit(1)

ct_file, frag_file, out_text = sys.argv[1:]
# 1) Wczytaj pliki
ct = open(ct_file, 'rb').read()
frag = open(frag_file, 'rb').read()
ct_bits = bytes_to_bits(ct)
frag_bits = bytes_to_bits(frag)

# 2) Odtwórz fragment keystreamu
n_frag = len(frag_bits)
ks_frag = [frag_bits[i] ^ ct_bits[i] for i in range(n_frag)]

# 3) BM -> L, C
L, C = berlekamp_massey(ks_frag)
print(f"Zidentyfikowane LFSR: L = {L}, wektor C = {C}")

# 4) Obliczenia długości
required = 2 * L
max_period = (1 << L) - 1
print(f"Minimalna długość znanego tekstu do pełnego odzyskania: {required} bitów")
print(f"Maksymalny okres sekwencji: {max_period} bitów")
if n_frag < required:
    print(f"Uwaga: użyto {n_frag} bitów; potrzeba co najmniej {required} bitów.")

# 5) Przygotuj IV i taps
iv = ks_frag[:L]
taps = [j-1 for j in range(1, len(C)) if C[j] == 1]
print(f"IV (pierwsze {L} bitów): {iv}")
print(f"Tapy: {taps}")

# 6) Generuj keystream i odszyfruj
full_ks = generate_keystream(iv, taps, len(ct_bits))
dec_bits = [ct_bits[i] ^ full_ks[i] for i in range(len(ct_bits))]
dec_bytes = bits_to_bytes(dec_bits)

# 7) Dekoduj i zapisz tekst
try:
    text = dec_bytes.decode('utf-8')
    with open(out_text, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"Zdekodowany tekst (UTF-8) zapisano do: {out_text}")
except UnicodeDecodeError:
    print("Dekodowanie UTF-8 nie powiodło się; upewnij się, że fragment plaintextu jest wystarczający.")