import itertools
import sys
import time

class BruteForceAttack:
    def __init__(self, known_plaintext, known_ciphertext):
        # Inicjalizacja ataku brute force z znanym tekstem jawnym i szyfrogramem
        self.known_plain_bits = self._bytes_to_bits(known_plaintext)
        self.known_cipher_bits = self._bytes_to_bits(known_ciphertext)
        # Odtworzenie strumienia klucza poprzez XOR tekstu jawnego i szyfrogramu
        self.recovered_key_bits = [p ^ c for p, c in zip(self.known_plain_bits, self.known_cipher_bits)]
        self.operations_count = 0  # Licznik operacji dla statystyk wydajności
        
    def _bytes_to_bits(self, byte_data):
        # Konwersja danych bajtowych na listę bitów
        return list(itertools.chain.from_iterable(
            [(byte >> i) & 1 for i in reversed(range(8))] for byte in byte_data))
    
    def _hamming_distance(self, bits1, bits2):
        # Obliczenie odległości Hamminga między dwoma strumieniami bitów
        distance = 0
        min_len = min(len(bits1), len(bits2))
        for i in range(min_len):
            if bits1[i] != bits2[i]:
                distance += 1
            self.operations_count += 3  # Aktualizacja licznika operacji (porównanie i inkrementacja)
        return distance
    
    def attack(self):
        # Główna metoda wykonująca atak brute force
        start_time = time.time()
        best_match = None
        best_distance = float('inf')  # Początkowa odległość ustawiona na nieskończoność
        total_candidates = 0
        
        # Generowanie wszystkich możliwych 12-bitowych kluczy (z wyłączeniem klucza zerowego)
        for key_bits in itertools.product([0,1], repeat=12):
            if sum(key_bits) == 0:
                continue  # Pominięcie klucza zerowego
                
            total_candidates += 1
            key_str = ''.join(map(str, key_bits))
            
            try:
                # Podział klucza na inicjalizacje rejestrów X, Y, Z
                x_init = list(key_bits[:3])
                y_init = list(key_bits[3:7])
                z_init = list(key_bits[7:12])
                
                # Inicjalizacja generatora strumienia klucza
                generator = KeyStreamGenerator(x_init, y_init, z_init)
                key_stream = generator.get_key_stream(len(self.recovered_key_bits))
                
                # Obliczenie odległości Hamminga między odzyskanym a wygenerowanym strumieniem
                distance = self._hamming_distance(self.recovered_key_bits, key_stream)
                self.operations_count += len(self.recovered_key_bits) * 5  # Szacunek operacji dla generacji strumienia
                
                # Aktualizacja najlepszego dopasowania
                if distance < best_distance:
                    best_distance = distance
                    best_match = {
                        'key': key_str,
                        'x_init': x_init,
                        'y_init': y_init,
                        'z_init': z_init,
                        'distance': distance
                    }
                    
                # Optymalizacja: przerwanie pętli przy idealnym dopasowaniu
                if distance == 0:
                    break
                    
            except ValueError:
                continue  # Pominięcie nieprawidłowych kombinacji (np. rejestry zerowe)
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        # Wyświetlenie statystyk wydajności
        print("\nStatystyki wydajności:")
        print(f"Przetestowano kandydatów: {total_candidates}")
        print(f"Czas wykonania: {elapsed_time:.4f} sekund")
        print(f"Łączna liczba operacji: {self.operations_count}")
        print(f"Operacje na sekundę: {self.operations_count/elapsed_time:.2f}")
        
        if best_match:
            # Wyświetlenie najlepszego znalezionego klucza
            print("\nNajlepsze dopasowanie:")
            print(f"Klucz: {best_match['key']}")
            print(f"X: {best_match['x_init']}, Y: {best_match['y_init']}, Z: {best_match['z_init']}")
            print(f"Odległość Hamminga: {best_match['distance']}")
            return best_match
        else:
            print("Nie znaleziono pasującego klucza")
            return None

# Klasa generatora strumienia klucza z Zadania 1
class KeyStreamGenerator:
    def __init__(self, x_init, y_init, z_init):
        # Inicjalizacja generatora strumienia klucza z podanymi wypełnieniami rejestrów
        if len(x_init) != 3 or len(y_init) != 4 or len(z_init) != 5:
            raise ValueError("Długości inicjalizacyjne muszą wynosić odpowiednio: X=3, Y=4, Z=5")
        if x_init == [0, 0, 0] or y_init == [0, 0, 0, 0] or z_init == [0, 0, 0, 0, 0]:
            raise ValueError("Żaden rejestr nie może być całkowicie zerowy")

        self.X = x_init.copy()
        self.Y = y_init.copy()
        self.Z = z_init.copy()

    def _next_bit(self):
        # Generowanie kolejnego bitu klucza na podstawie bieżącego stanu rejestrów
        xi = self.X[0]
        yi = self.Y[0]
        zi = self.Z[0]

        ki = (xi & yi) ^ (yi & zi) ^ zi  # Funkcja nieliniowa generująca bit klucza

        # Aktualizacja rejestrów przesuwających
        x_new = self.X[0] ^ self.X[2]
        y_new = self.Y[0] ^ self.Y[3]
        z_new = self.Z[0] ^ self.Z[2]

        self.X = self.X[1:] + [x_new]
        self.Y = self.Y[1:] + [y_new]
        self.Z = self.Z[1:] + [z_new]

        return ki

    def get_key_stream(self, length):
        # Generowanie strumienia klucza o zadanej długości
        return [self._next_bit() for _ in range(length)]

if __name__ == "__main__":
    # Główna funkcja wykonująca atak na podstawie plików wejściowych
    if len(sys.argv) != 3:
        print("Użycie: python zad4_bruteforce.py plik_jawny.txt plik_szyfrogram.txt")
        sys.exit(1)
        
    plain_file = sys.argv[1]
    cipher_file = sys.argv[2]
    
    try:
        # Wczytanie znanego tekstu jawnego i szyfrogramu
        with open(plain_file, "rb") as f:
            known_plaintext = f.read()
        
        with open(cipher_file, "rb") as f:
            known_ciphertext = f.read()
            
        print(f"Wczytano {len(known_plaintext)} bajtów tekstu jawnego")
        print(f"Wczytano {len(known_ciphertext)} bajtów szyfrogramu")
        print(f"Długość analizowanego strumienia: {len(known_plaintext)*8} bitów")
        
        print("\nRozpoczęcie ataku brute force...")
        attacker = BruteForceAttack(known_plaintext, known_ciphertext)
        result = attacker.attack()
        
    except FileNotFoundError:
        print("Błąd: Nie można znaleźć pliku")
        sys.exit(1)
    except Exception as e:
        print(f"Błąd: {str(e)}")
        sys.exit(1)