import argparse
import random
import string
import json
from scipy.stats import chi2
import itertools


# Generuje losowy klucz szyfrowania (permutacja alfabetu)
def generate_key():
    letters = list(string.ascii_uppercase)
    shuffled = letters[:]
    random.shuffle(shuffled)
    return dict(zip(letters, shuffled))

# Odwraca klucz szyfrowania do deszyfrowania
def invert_key(key):
    return {v: k for k, v in key.items()}

# Usuwa wszystkie znaki niebędące literami i zamienia na wielkie litery
def clean_text(text):
    return ''.join(filter(str.isalpha, text)).upper()

# Zamienia litery zgodnie z kluczem szyfrowania
def substitute(text, key):
    return ''.join(key.get(char, char) for char in text)

# Oblicza statystykę chi-kwadrat dla tekstu
def chi_square_test(text):
    expected_freq = {
        'E': 12.7, 'T': 9.1, 'A': 8.2, 'O': 7.5, 'I': 7.0, 'N': 6.7, 'S': 6.3, 'H': 6.1, 'R': 6.0, 'D': 4.3,
        'L': 4.0, 'C': 2.8, 'U': 2.8, 'M': 2.4, 'W': 2.4, 'F': 2.2, 'G': 2.0, 'Y': 2.0, 'P': 1.9, 'B': 1.5,
        'V': 1.0, 'K': 0.8, 'X': 0.2, 'J': 0.2, 'Q': 0.1, 'Z': 0.1
    }
    total = len(text)
    if total == 0:
        return float('inf')
    observed_freq = {char: text.count(char) / total * 100 for char in string.ascii_uppercase}
    chi_sq = sum((observed_freq.get(char, 0) - expected_freq[char])**2 / expected_freq[char] for char in expected_freq)
    return chi_sq

# Atak brute-force
def brute_force_attack(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        cipher_text = clean_text(f.read())
    
    best_attempt = ""
    best_score = float('inf')
    df = 25  # 26 liter - 1
    critical_value = chi2.ppf(0.95, df)
    
    for perm in [dict(zip(string.ascii_uppercase, p)) for p in itertools.permutations(string.ascii_uppercase)]:
        decrypted = substitute(cipher_text, invert_key(perm))
        score = chi_square_test(decrypted)
        if score < best_score:
            best_score = score
            best_attempt = decrypted
            if best_score < critical_value:
                break
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(best_attempt)
    print(f"Najlepsza próba deszyfrowania zapisana w {output_file}. Wynik chi-kwadrat: {best_score}")

# Przetwarza plik wejściowy: czyści tekst, szyfruje lub deszyfruje i zapisuje wynik
def process_file(input_file, output_file, key_file, encrypt, decrypt, attack):
    if attack == 'bf':
        brute_force_attack(input_file, output_file)
        return
    
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    clean = clean_text(text)
    
    if encrypt:
        key = generate_key()
        transformed = substitute(clean, key)
        with open(key_file, 'w', encoding='utf-8') as kf:
            json.dump(key, kf)
        print(f"Tekst został zaszyfrowany i zapisany do {output_file}. Klucz zapisano w {key_file}.")
    elif decrypt:
        with open(key_file, 'r', encoding='utf-8') as kf:
            key = json.load(kf)
        inv_key = invert_key(key)
        transformed = substitute(clean, inv_key)
        print(f"Tekst został odszyfrowany i zapisany do {output_file}.")
    else:
        raise ValueError("Niepoprawny tryb. Użyj flag -e dla szyfrowania, -d dla deszyfrowania lub -a bf dla ataku brute-force.")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(transformed)

# Główna funkcja obsługująca argumenty wiersza poleceń
def main():
    parser = argparse.ArgumentParser(description='Szyfr podstawieniowy')
    parser.add_argument('-i', required=True, help='Plik wejściowy z tekstem')
    parser.add_argument('-o', required=True, help='Plik wyjściowy z wynikiem')
    parser.add_argument('-k', help='Plik do zapisania/odczytu klucza (wymagane dla -e i -d)')
    parser.add_argument('-e', action='store_true', help='Tryb szyfrowania')
    parser.add_argument('-d', action='store_true', help='Tryb deszyfrowania')
    parser.add_argument('-a', choices=['bf'], help='Atak: bf (brute-force)')
    
    args = parser.parse_args()
    
    if args.e and args.d:
        raise ValueError("Nie można jednocześnie wybrać trybu szyfrowania i deszyfrowania.")
    if args.a and (args.e or args.d):
        raise ValueError("Nie można jednocześnie wykonywać ataku brute-force i szyfrowania/deszyfrowania.")
    
    process_file(args.i, args.o, args.k, args.e, args.d, args.a)

if __name__ == '__main__':
    main()