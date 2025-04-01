import argparse
import random
import string
import json
import math
from collections import defaultdict
import numpy as np

###########################################################################################################################################################
#SZYFROWANIE I DESZYFROWANIE TEKSTU z GENEREOWANYM KLUCZEM

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

###########################################################################################################################################################
# ATAK BRUTE-FORCE NA SZYFR PODSTAWIENIOWY

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

###########################################################################################################################################################
# FUNKCJE POMOCNICZE DLA ZADAŃ 2, 3 i 4

# Funkcja do tworzenia macierzy bigramów z tekstu
def create_bigram_matrix(text):
    bigram_matrix = np.zeros((26, 26))
    for i in range(len(text)-1):
        current = ord(text[i]) - ord('A')
        next_char = ord(text[i+1]) - ord('A')
        bigram_matrix[current][next_char] += 1
    return bigram_matrix

# Funkcja do obliczania logarytmicznej funkcji wiarygodności
def log_likelihood(decrypted_bigrams, reference_bigrams):
    log_likelihood = 0.0
    for i in range(26):
        for j in range(26):
            if reference_bigrams[i][j] > 0 and decrypted_bigrams[i][j] > 0:
                log_likelihood += decrypted_bigrams[i][j] * math.log(reference_bigrams[i][j])
    return log_likelihood

# Funkcja do generowania nowej permutacji przez zamianę dwóch znaków
def generate_new_key(current_key):
    letters = list(string.ascii_uppercase)
    new_key = current_key.copy()
    i, j = random.sample(range(26), 2)
    new_key[letters[i]], new_key[letters[j]] = new_key[letters[j]], new_key[letters[i]]
    return new_key

###########################################################################################################################################################
# ZADANIE 2 (Metropolis-Hastings)

# Implementacja algorytmu Metropolis-Hastings dla kryptoanalizy
def metropolis_hastings_attack(cipher_text, reference_bigrams, iterations=10000):
    current_key = generate_key()
    current_inv_key = invert_key(current_key)
    current_decrypted = substitute(cipher_text, current_inv_key)
    current_bigrams = create_bigram_matrix(current_decrypted)
    current_log_likelihood = log_likelihood(current_bigrams, reference_bigrams)
    
    best_key = current_key
    best_log_likelihood = current_log_likelihood
    
    for t in range(iterations):
        new_key = generate_new_key(current_key)
        new_inv_key = invert_key(new_key)
        new_decrypted = substitute(cipher_text, new_inv_key)
        new_bigrams = create_bigram_matrix(new_decrypted)
        new_log_likelihood = log_likelihood(new_bigrams, reference_bigrams)
        
        acceptance_ratio = min(1.0, math.exp(new_log_likelihood - current_log_likelihood))
        
        if random.random() <= acceptance_ratio:
            current_key = new_key
            current_log_likelihood = new_log_likelihood
            
            if new_log_likelihood > best_log_likelihood:
                best_key = new_key
                best_log_likelihood = new_log_likelihood
        
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
    # Dodaj 1 aby uniknąć log(0) - smoothing
    reference_bigrams += 1
    
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

###########################################################################################################################################################
# ZADANIE 3 (Simulated Annealing)

def simulated_annealing_attack(cipher_text, reference_bigrams, initial_temp=1000.0, cooling_rate=0.99, iterations=10000):
    """
    Perform simulated annealing attack on substitution cipher.
    
    Args:
        cipher_text (str): Encrypted text to attack
        reference_bigrams (np.array): Reference bigram frequencies (26x26 matrix)
        initial_temp (float): Initial temperature
        cooling_rate (float): Cooling rate (0 < rate < 1)
        iterations (int): Number of iterations
        
    Returns:
        tuple: (best_key, best_score) where best_key is the found key and best_score is its score
    """
    # Initialize with random key
    current_key = generate_key()
    current_inv_key = invert_key(current_key)
    current_decrypted = substitute(cipher_text, current_inv_key)
    current_bigrams = create_bigram_matrix(current_decrypted)
    current_score = log_likelihood(current_bigrams, reference_bigrams)
    
    best_key = current_key
    best_score = current_score
    
    temp = initial_temp
    
    for i in range(iterations):
        # Generate new key by swapping two random letters
        new_key = generate_new_key(current_key)
        new_inv_key = invert_key(new_key)
        new_decrypted = substitute(cipher_text, new_inv_key)
        new_bigrams = create_bigram_matrix(new_decrypted)
        new_score = log_likelihood(new_bigrams, reference_bigrams)
        
        # Calculate score difference
        score_diff = new_score - current_score
        
        # Acceptance probability
        if score_diff > 0:
            # Always accept better solutions
            accept = True
        else:
            # Accept worse solutions with some probability
            accept_prob = math.exp(score_diff / temp)
            accept = random.random() < accept_prob
        
        if accept:
            current_key = new_key
            current_score = new_score
            
            if current_score > best_score:
                best_key = current_key
                best_score = current_score
        
        # Cool down
        temp *= cooling_rate
        
        if i % 1000 == 0:
            print(f"Iteration {i}: temp={temp:.2f}, current_score={current_score:.2f}, best_score={best_score:.2f}")
    
    return best_key, best_score

# Funkcja do ataku symulowanego wyżarzania
def sa_attack(input_file, output_file, reference_file, iterations=10000, initial_temp=1000.0, cooling_rate=0.99):
    """
    Perform simulated annealing attack on a ciphertext file.
    """
    # Read ciphertext
    with open(input_file, 'r', encoding='utf-8') as f:
        cipher_text = clean_text(f.read())
    
    # Read reference text and create bigram matrix
    with open(reference_file, 'r', encoding='utf-8') as f:
        reference_text = clean_text(f.read())
    reference_bigrams = create_bigram_matrix(reference_text)
    
    # Add smoothing to avoid zeros
    reference_bigrams += 1
    # Normalize bigram matrix
    row_sums = reference_bigrams.sum(axis=1)
    reference_bigrams = reference_bigrams / row_sums[:, np.newaxis]
    
    # Run simulated annealing
    best_key, best_score = simulated_annealing_attack(
        cipher_text, reference_bigrams, initial_temp, cooling_rate, iterations)
    
    # Decrypt with best key
    best_inv_key = invert_key(best_key)
    decrypted_text = substitute(cipher_text, best_inv_key)
    
    # Save results
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(decrypted_text)
    
    key_output_file = output_file + '.JSON'
    with open(key_output_file, 'w', encoding='utf-8') as kf:
        json.dump(best_key, kf)
    
    print(f"Simulated annealing attack completed. Best score: {best_score:.2f}")
    print(f"Decrypted text saved to {output_file}, key saved to {key_output_file}")


###########################################################################################################################################################
# ZADANIE 4 (Algorytm Genetyczny)

def fitness_function(decrypted_text, reference_bigrams):
    """
    Calculate fitness score using log-likelihood of bigram frequencies
    """
    decrypted_bigrams = create_bigram_matrix(decrypted_text)
    return log_likelihood(decrypted_bigrams, reference_bigrams)

def roulette_wheel_selection(population, fitness_scores):
    """
    Perform roulette wheel selection
    """
    total_fitness = sum(fitness_scores)
    if total_fitness == 0:
        return random.choice(population)
    probabilities = [score/total_fitness for score in fitness_scores]
    r = random.random()
    cumulative = 0
    for i, prob in enumerate(probabilities):
        cumulative += prob
        if r <= cumulative:
            return population[i]
    return population[-1]

def single_point_crossover(parent1, parent2):
    """
    Perform single-point crossover between two keys
    """
    letters = string.ascii_uppercase
    child1 = parent1.copy()
    child2 = parent2.copy()
    
    # Choose random crossover point (1-25)
    crossover_point = random.randint(1, 24)
    
    # Get the letters after crossover point from each parent
    parent1_letters = {k: v for k, v in parent1.items() if ord(k) - ord('A') >= crossover_point}
    parent2_letters = {k: v for k, v in parent2.items() if ord(k) - ord('A') >= crossover_point}
    
    # Create mapping for conflicting letters
    conflict_map1 = {}
    conflict_map2 = {}
    
    # Handle conflicts in child1 (parent1 + parent2's tail)
    for letter in parent2_letters:
        new_val = parent2_letters[letter]
        original_val = parent1[letter]
        
        # Find if new_val is already mapped to something else
        for k, v in child1.items():
            if v == new_val and k != letter:
                conflict_map1[k] = original_val
                break
        
        child1[letter] = new_val
    
    # Resolve conflicts in child1
    for k, v in conflict_map1.items():
        child1[k] = v
    
    # Handle conflicts in child2 (parent2 + parent1's tail)
    for letter in parent1_letters:
        new_val = parent1_letters[letter]
        original_val = parent2[letter]
        
        # Find if new_val is already mapped to something else
        for k, v in child2.items():
            if v == new_val and k != letter:
                conflict_map2[k] = original_val
                break
        
        child2[letter] = new_val
    
    # Resolve conflicts in child2
    for k, v in conflict_map2.items():
        child2[k] = v
    
    return child1, child2

def genetic_algorithm_attack(cipher_text, reference_bigrams, population_size=100, 
                           crossover_prob=0.8, mutation_prob=0.2, 
                           max_generations=1000, max_std_dev=0.1):
    """
    Perform genetic algorithm attack on substitution cipher
    """
    # Initialize population
    population = [generate_key() for _ in range(population_size)]
    
    # Evaluate initial population
    fitness_scores = []
    for key in population:
        inv_key = invert_key(key)
        decrypted = substitute(cipher_text, inv_key)
        score = fitness_function(decrypted, reference_bigrams)
        fitness_scores.append(score)
    
    best_key = population[np.argmax(fitness_scores)]
    best_score = max(fitness_scores)
    
    for generation in range(max_generations):
        new_population = []
        
        # Calculate population statistics
        mean_fitness = np.mean(fitness_scores)
        std_dev = np.std(fitness_scores)
        
        # Check convergence
        if std_dev < max_std_dev:
            print(f"Converged at generation {generation} with std dev {std_dev:.4f}")
            break
        
        # Create next generation
        while len(new_population) < population_size:
            # Selection
            parent1 = roulette_wheel_selection(population, fitness_scores)
            parent2 = roulette_wheel_selection(population, fitness_scores)
            
            # Crossover
            if random.random() < crossover_prob:
                child1, child2 = single_point_crossover(parent1, parent2)
            else:
                child1, child2 = parent1.copy(), parent2.copy()
            
            # Mutation
            if random.random() < mutation_prob:
                child1 = generate_new_key(child1)
            if random.random() < mutation_prob:
                child2 = generate_new_key(child2)
            
            new_population.extend([child1, child2])
        
        # Ensure population size stays constant
        population = new_population[:population_size]
        
        # Evaluate new population
        fitness_scores = []
        for key in population:
            inv_key = invert_key(key)
            decrypted = substitute(cipher_text, inv_key)
            score = fitness_function(decrypted, reference_bigrams)
            fitness_scores.append(score)
        
        # Update best key
        current_best_idx = np.argmax(fitness_scores)
        if fitness_scores[current_best_idx] > best_score:
            best_key = population[current_best_idx]
            best_score = fitness_scores[current_best_idx]
        
        if generation % 100 == 0:
            print(f"Generation {generation}: Best score = {best_score:.2f}, Mean score = {mean_fitness:.2f}, Std dev = {std_dev:.4f}")
    
    return best_key, best_score

def ga_attack(input_file, output_file, reference_file, population_size=100, 
             crossover_prob=0.8, mutation_prob=0.2, max_generations=1000, 
             max_std_dev=0.1):
    """
    Perform genetic algorithm attack on a ciphertext file
    """
    # Read ciphertext
    with open(input_file, 'r', encoding='utf-8') as f:
        cipher_text = clean_text(f.read())
    
    # Read reference text and create bigram matrix
    with open(reference_file, 'r', encoding='utf-8') as f:
        reference_text = clean_text(f.read())
    reference_bigrams = create_bigram_matrix(reference_text)
    
    # Add smoothing and normalize
    reference_bigrams += 1
    row_sums = reference_bigrams.sum(axis=1)
    reference_bigrams = reference_bigrams / row_sums[:, np.newaxis]
    
    # Run genetic algorithm
    best_key, best_score = genetic_algorithm_attack(
        cipher_text, reference_bigrams, population_size, crossover_prob,
        mutation_prob, max_generations, max_std_dev)
    
    # Decrypt with best key
    best_inv_key = invert_key(best_key)
    decrypted_text = substitute(cipher_text, best_inv_key)
    
    # Save results
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(decrypted_text)
    
    key_output_file = output_file + '.JSON'
    with open(key_output_file, 'w', encoding='utf-8') as kf:
        json.dump(best_key, kf)
    
    print(f"Genetic algorithm attack completed. Best score: {best_score:.2f}")
    print(f"Decrypted text saved to {output_file}, key saved to {key_output_file}")


###########################################################################################################################################################
# GŁÓWNA FUNKCJA MAIN Z OBSŁUGĄ ARGUMENTÓW WEJŚCIOWYCH

def main():
    parser = argparse.ArgumentParser(description='Szyfr podstawieniowy')
    parser.add_argument('-i', '--input', required=True, help='Plik wejściowy z tekstem')
    parser.add_argument('-o', '--output', required=True, help='Plik wyjściowy z wynikiem')
    parser.add_argument('-k', '--key', help='Plik do zapisania/odczytu klucza')
    parser.add_argument('-e', '--encrypt', action='store_true', help='Tryb szyfrowania')
    parser.add_argument('-d', '--decrypt', action='store_true', help='Tryb deszyfrowania')
    parser.add_argument('-a', '--attack', choices=['bf', 'mh', 'sa', 'ga'], 
                       help='Tryb ataku (bf - brute force, mh - Metropolis-Hastings, sa - Simulated Annealing, ga - Genetic Algorithm)')
    parser.add_argument('-r', '--reference', help='Plik z tekstem referencyjnym (wymagany dla ataków MH, SA i GA)')
    parser.add_argument('--iterations', type=int, default=10000, help='Liczba iteracji dla ataków MH i SA')
    parser.add_argument('--initial-temp', type=float, default=1000.0, help='Początkowa temperatura dla ataku SA')
    parser.add_argument('--cooling-rate', type=float, default=0.99, help='Współczynnik chłodzenia dla ataku SA')
    parser.add_argument('--population-size', type=int, default=100, help='Rozmiar populacji dla ataku GA')
    parser.add_argument('--crossover-prob', type=float, default=0.8, help='Prawdopodobieństwo krzyżowania dla ataku GA')
    parser.add_argument('--mutation-prob', type=float, default=0.2, help='Prawdopodobieństwo mutacji dla ataku GA')
    parser.add_argument('--max-std-dev', type=float, default=0.1, help='Maksymalne odchylenie standardowe dla zbieżności w ataku GA')
    parser.add_argument('-g', '--generate-key', action='store_true', 
                       help='Wymuś generację nowego klucza (tylko dla szyfrowania)')
    
    args = parser.parse_args()
    
    if args.attack == 'bf':
        brute_force_attack(args.input, args.output)
    elif args.attack == 'mh':
        if not args.reference:
            raise ValueError("Plik referencyjny jest wymagany dla ataku Metropolis-Hastings.")
        mh_attack(args.input, args.output, args.reference, args.iterations)
    elif args.attack == 'sa':
        if not args.reference:
            raise ValueError("Plik referencyjny jest wymagany dla ataku Symulowanego Wyżarzania.")
        sa_attack(args.input, args.output, args.reference, args.iterations, 
                 args.initial_temp, args.cooling_rate)
    elif args.attack == 'ga':
        if not args.reference:
            raise ValueError("Plik referencyjny jest wymagany dla ataku Algorytmem Genetycznym.")
        ga_attack(args.input, args.output, args.reference, args.population_size,
                 args.crossover_prob, args.mutation_prob, args.iterations,
                 args.max_std_dev)
    else:
        if args.encrypt and args.decrypt:
            raise ValueError("Nie można jednocześnie wybrać trybu szyfrowania i deszyfrowania.")
        if not args.key:
            raise ValueError("Plik klucza jest wymagany dla trybów szyfrowania i deszyfrowania.")
        
        process_file(args.input, args.output, args.key, 
                    args.encrypt, args.decrypt, args.generate_key)

if __name__ == '__main__':
    main()