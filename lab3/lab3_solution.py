import argparse
import random
import string
import json
import math
from collections import defaultdict
import numpy as np

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

# Przetwarza plik wejściowy: czyści tekst, szyfruje lub deszyfruje i zapisuje wynik. Pozwala zdecydować, czy klucz ma być generowany na nowo czy wczytany z pliku.
def process_file(input_file, output_file, key_file, encrypt, decrypt, generate_new_key):
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    clean = clean_text(text)
    
    if encrypt:
        if generate_new_key:
            key = generate_key()
            print("Wygenerowano nowy klucz szyfrowania.")
        else:
            try:
                with open(key_file, 'r', encoding='utf-8') as kf:
                    key = json.load(kf)
                print(f"Wczytano istniejący klucz z {key_file}.")
            except FileNotFoundError:
                print("Błąd: Plik klucza nie istnieje. Generuję nowy klucz.")
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
        raise ValueError("Niepoprawny tryb. Użyj flag -e dla szyfrowania lub -d dla deszyfrowania.")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(transformed)

# Funkcja do ataku brute-force na szyfr podstawieniowy
def brute_force_attack(input_file, output_file, max_attempts=1000000):
    with open(input_file, 'r', encoding='utf-8') as f:
        cipher_text = clean_text(f.read())
    
    english_frequencies = {
        'A': 0.08167, 'B': 0.01492, 'C': 0.02782, 'D': 0.04253,
        'E': 0.12702, 'F': 0.02228, 'G': 0.02015, 'H': 0.06094,
        'I': 0.06966, 'J': 0.00153, 'K': 0.00772, 'L': 0.04025,
        'M': 0.02406, 'N': 0.06749, 'O': 0.07507, 'P': 0.01929,
        'Q': 0.00095, 'R': 0.05987, 'S': 0.06327, 'T': 0.09056,
        'U': 0.02758, 'V': 0.00978, 'W': 0.02360, 'X': 0.00150,
        'Y': 0.01974, 'Z': 0.00074
    }
    
    best_score = float('inf')
    best_text = ""
    best_key = {}
    
    for attempt in range(max_attempts):
        key = generate_key()
        inv_key = invert_key(key)
        decrypted_text = substitute(cipher_text, inv_key)
        
        text_length = len(decrypted_text)
        if text_length == 0:
            continue
            
        observed_frequencies = {}
        for letter in string.ascii_uppercase:
            observed_frequencies[letter] = decrypted_text.count(letter) / text_length
        
        chi_squared = 0.0
        for letter in english_frequencies:
            expected = english_frequencies[letter]
            observed = observed_frequencies.get(letter, 0.0)
            chi_squared += ((observed - expected) ** 2) / expected
        
        if chi_squared < best_score:
            best_score = chi_squared
            best_text = decrypted_text
            best_key = key
            
            if math.isclose(best_score, 0.0, abs_tol=0.01):
                break
    
    print(f"Znaleziono najlepsze dopasowanie z wynikiem chi-kwadrat: {best_score:.4f}")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(best_text)
    
    key_output_file = output_file + '.JSON'
    with open(key_output_file, 'w', encoding='utf-8') as kf:
        json.dump(best_key, kf)
    print(f"Zapisano odszyfrowany tekst do {output_file} i klucz do {key_output_file}")

# Funkcja do tworzenia macierzy bigramów z tekstu
def create_bigram_matrix(text):
    bigram_matrix = np.zeros((26, 26))
    for i in range(len(text)-1):
        current = ord(text[i]) - ord('A')
        next_char = ord(text[i+1]) - ord('A')
        bigram_matrix[current][next_char] += 1
    return bigram_matrix

# Funkcja do obliczania logarytmicznej funkcji wiarygodności
def log_likelihood(bigram_matrix, reference_matrix):
    log_likelihood = 0.0
    for i in range(26):
        for j in range(26):
            if reference_matrix[i][j] > 0 and bigram_matrix[i][j] > 0:
                log_likelihood += bigram_matrix[i][j] * math.log(reference_matrix[i][j])
    return log_likelihood

# Funkcja do generowania nowej permutacji przez zamianę dwóch znaków
def generate_new_key(current_key):
    letters = list(string.ascii_uppercase)
    new_key = current_key.copy()
    i, j = random.sample(range(26), 2)
    new_key[letters[i]], new_key[letters[j]] = new_key[letters[j]], new_key[letters[i]]
    return new_key

# Implementacja algorytmu Metropolis-Hastings dla kryptoanalizy
def metropolis_hastings_attack(cipher_text, reference_bigrams, iterations=10000):
    # Inicjalizacja losowego klucza
    current_key = generate_key()
    current_inv_key = invert_key(current_key)
    current_decrypted = substitute(cipher_text, current_inv_key)
    current_bigrams = create_bigram_matrix(current_decrypted)
    current_log_likelihood = log_likelihood(current_bigrams, reference_bigrams)
    
    best_key = current_key
    best_log_likelihood = current_log_likelihood
    
    for t in range(iterations):
        # Generowanie nowego klucza
        new_key = generate_new_key(current_key)
        new_inv_key = invert_key(new_key)
        new_decrypted = substitute(cipher_text, new_inv_key)
        new_bigrams = create_bigram_matrix(new_decrypted)
        new_log_likelihood = log_likelihood(new_bigrams, reference_bigrams)
        
        # Obliczanie współczynnika akceptacji
        if current_log_likelihood == 0:
            acceptance_ratio = 1.0
        else:
            acceptance_ratio = math.exp(new_log_likelihood - current_log_likelihood)
        
        # Akceptacja lub odrzucenie nowego klucza
        if random.random() <= acceptance_ratio:
            current_key = new_key
            current_log_likelihood = new_log_likelihood
            
            # Aktualizacja najlepszego klucza
            if new_log_likelihood > best_log_likelihood:
                best_key = new_key
                best_log_likelihood = new_log_likelihood
        
        # Wypisywanie postępu co 1000 iteracji
        if t % 1000 == 0:
            print(f"Iteracja {t}: aktualne log-wiarygodność = {current_log_likelihood:.2f}, najlepsze = {best_log_likelihood:.2f}")
    
    return best_key, best_log_likelihood

# Funkcja do ataku Metropolis-Hastings
def mh_attack(input_file, output_file, reference_file, iterations=10000):
    # Wczytanie szyfrogramu
    with open(input_file, 'r', encoding='utf-8') as f:
        cipher_text = clean_text(f.read())
    
    # Wczytanie tekstu referencyjnego i tworzenie macierzy bigramów
    with open(reference_file, 'r', encoding='utf-8') as f:
        reference_text = clean_text(f.read())
    reference_bigrams = create_bigram_matrix(reference_text)
    
    # Normalizacja macierzy bigramów
    reference_bigrams += 1  # Dodanie 1 aby uniknąć zer
    row_sums = reference_bigrams.sum(axis=1)
    reference_bigrams = reference_bigrams / row_sums[:, np.newaxis]
    
    # Uruchomienie algorytmu Metropolis-Hastings
    best_key, best_log_likelihood = metropolis_hastings_attack(
        cipher_text, reference_bigrams, iterations)
    
    # Odszyfrowanie tekstu najlepszym kluczem
    best_inv_key = invert_key(best_key)
    decrypted_text = substitute(cipher_text, best_inv_key)
    
    # Zapis wyników
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(decrypted_text)
    
    key_output_file = output_file + '.JSON'
    with open(key_output_file, 'w', encoding='utf-8') as kf:
        json.dump(best_key, kf)
    
    print(f"Zakończono atak Metropolis-Hastings. Znaleziono klucz z log-wiarygodnością: {best_log_likelihood:.2f}")
    print(f"Zapisano odszyfrowany tekst do {output_file} i klucz do {key_output_file}")

# Główna funkcja obsługująca argumenty wiersza poleceń
def main():
    parser = argparse.ArgumentParser(description='Szyfr podstawieniowy')
    parser.add_argument('-i', '--input', required=True, help='Plik wejściowy z tekstem')
    parser.add_argument('-o', '--output', required=True, help='Plik wyjściowy z wynikiem')
    parser.add_argument('-k', '--key', help='Plik do zapisania/odczytu klucza')
    parser.add_argument('-e', '--encrypt', action='store_true', help='Tryb szyfrowania')
    parser.add_argument('-d', '--decrypt', action='store_true', help='Tryb deszyfrowania')
    parser.add_argument('-a', '--attack', choices=['bf', 'mh'], help='Tryb ataku (bf - brute force, mh - Metropolis-Hastings)')
    parser.add_argument('-r', '--reference', help='Plik z tekstem referencyjnym (wymagany dla ataku MH)')
    parser.add_argument('--iterations', type=int, default=10000, help='Liczba iteracji dla ataku MH')
    parser.add_argument('-g', '--generate-key', action='store_true', 
                       help='Wymuś generację nowego klucza (tylko dla szyfrowania)')
    
    args = parser.parse_args()
    
    if args.attack == 'bf':
        brute_force_attack(args.input, args.output)
    elif args.attack == 'mh':
        if not args.reference:
            raise ValueError("Plik referencyjny jest wymagany dla ataku Metropolis-Hastings.")
        mh_attack(args.input, args.output, args.reference, args.iterations)
    else:
        if args.encrypt and args.decrypt:
            raise ValueError("Nie można jednocześnie wybrać trybu szyfrowania i deszyfrowania.")
        if not args.key:
            raise ValueError("Plik klucza jest wymagany dla trybów szyfrowania i deszyfrowania.")
        
        process_file(args.input, args.output, args.key, 
                    args.encrypt, args.decrypt, args.generate_key)

if __name__ == '__main__':
    main()