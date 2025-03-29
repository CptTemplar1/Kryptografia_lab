import argparse
import random
import string
import json

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

# Przetwarza plik wejściowy: czyści tekst, szyfruje lub deszyfruje i zapisuje wynik
def process_file(input_file, output_file, key_file, encrypt, decrypt):
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
        raise ValueError("Niepoprawny tryb. Użyj flag -e dla szyfrowania lub -d dla deszyfrowania.")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(transformed)

# Główna funkcja obsługująca argumenty wiersza poleceń
def main():
    parser = argparse.ArgumentParser(description='Szyfr podstawieniowy')
    parser.add_argument('-i', required=True, help='Plik wejściowy z tekstem')
    parser.add_argument('-o', required=True, help='Plik wyjściowy z wynikiem')
    parser.add_argument('-k', required=True, help='Plik do zapisania/odczytu klucza')
    parser.add_argument('-e', action='store_true', help='Tryb szyfrowania')
    parser.add_argument('-d', action='store_true', help='Tryb deszyfrowania')
    
    args = parser.parse_args()
    
    if args.e and args.d:
        raise ValueError("Nie można jednocześnie wybrać trybu szyfrowania i deszyfrowania.")
    
    process_file(args.i, args.o, args.k, args.e, args.d)

if __name__ == '__main__':
    main()
