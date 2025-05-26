import itertools
import math
import sys
import time

class CorrelationAttack:
    def __init__(self, known_plaintext, known_ciphertext):
        # Inicjalizacja ataku korelacyjnego z znanym tekstem jawnym i szyfrogramem
        self.known_plain_bits = self._bytes_to_bits(known_plaintext)
        self.known_cipher_bits = self._bytes_to_bits(known_ciphertext)
        # Odtworzenie strumienia klucza poprzez XOR tekstu jawnego i szyfrogramu
        self.recovered_key_bits = [p ^ c for p, c in zip(self.known_plain_bits, self.known_cipher_bits)]
        self.operations_count = 0  # Licznik operacji dla statystyk wydajności
        
    def _bytes_to_bits(self, byte_data):
        # Konwersja danych bajtowych na listę bitów
        return list(itertools.chain.from_iterable(
            [(byte >> i) & 1 for i in reversed(range(8))] for byte in byte_data))
    
    def _pearson_correlation(self, stream1, stream2):
        # Obliczenie współczynnika korelacji Pearsona między dwoma strumieniami bitów
        n = min(len(stream1), len(stream2))
        if n == 0:
            return 0
            
        sum1 = sum(stream1[:n])
        sum2 = sum(stream2[:n])
        
        sum1_sq = sum(x*x for x in stream1[:n])
        sum2_sq = sum(x*x for x in stream2[:n])
        
        p_sum = sum(x*y for x, y in zip(stream1[:n], stream2[:n]))
        
        num = p_sum - (sum1 * sum2 / n)
        den = math.sqrt((sum1_sq - sum1**2 / n) * (sum2_sq - sum2**2 / n))
        
        self.operations_count += 10 + 6*n  # Aktualizacja licznika operacji
        
        if den == 0:
            return 0
            
        return num / den
    
    def _generate_x_stream(self, x_init, length):
        # Generowanie strumienia bitów z rejestru X na podstawie początkowego wypełnienia
        x_reg = x_init.copy()
        stream = []
        for _ in range(length):
            stream.append(x_reg[0])
            x_new = x_reg[0] ^ x_reg[2]  # Wielomian przesuwający dla rejestru X
            x_reg = x_reg[1:] + [x_new]
            self.operations_count += 5  # Aktualizacja licznika operacji
        return stream
    
    def _generate_z_stream(self, z_init, length):
        # Generowanie strumienia bitów z rejestru Z na podstawie początkowego wypełnienia
        z_reg = z_init.copy()
        stream = []
        for _ in range(length):
            stream.append(z_reg[0])
            z_new = z_reg[0] ^ z_reg[2]  # Wielomian przesuwający dla rejestru Z
            z_reg = z_reg[1:] + [z_new]
            self.operations_count += 5
        return stream
    
    def _generate_y_stream(self, y_init, length):
        # Generowanie strumienia bitów z rejestru Y na podstawie początkowego wypełnienia
        y_reg = y_init.copy()
        stream = []
        for _ in range(length):
            stream.append(y_reg[0])
            y_new = y_reg[0] ^ y_reg[3]  # Wielomian przesuwający dla rejestru Y
            y_reg = y_reg[1:] + [y_new]
            self.operations_count += 5
        return stream
    
    def attack_x_register(self):
        # Atak korelacyjny na rejestr X (3-bitowy)
        best_corr = -1
        best_x_init = None
        total_candidates = 0
        
        # Przetestuj wszystkie możliwe inicjalizacje rejestru X (z wyjątkiem wektora zerowego)
        for x_init in itertools.product([0,1], repeat=3):
            if sum(x_init) == 0:
                continue
                
            total_candidates += 1
            x_stream = self._generate_x_stream(list(x_init), len(self.recovered_key_bits))
            corr = self._pearson_correlation(self.recovered_key_bits, x_stream)
            
            if abs(corr - 1/3) < abs(best_corr - 1/3) or best_corr == -1:
                best_corr = corr
                best_x_init = list(x_init)
                
        print(f"Przetestowano {total_candidates} kandydatów dla rejestru X")
        return best_x_init
    
    def attack_z_register(self):
        # Atak korelacyjny na rejestr Z (5-bitowy)
        best_corr = -1
        best_z_init = None
        total_candidates = 0
        
        # Przetestuj wszystkie możliwe inicjalizacje rejestru Z (z wyjątkiem wektora zerowego)
        for z_init in itertools.product([0,1], repeat=5):
            if sum(z_init) == 0:
                continue
                
            total_candidates += 1
            z_stream = self._generate_z_stream(list(z_init), len(self.recovered_key_bits))
            corr = self._pearson_correlation(self.recovered_key_bits, z_stream)
            
            if abs(corr - 1/3) < abs(best_corr - 1/3) or best_corr == -1:
                best_corr = corr
                best_z_init = list(z_init)
                
        print(f"Przetestowano {total_candidates} kandydatów dla rejestru Z")
        return best_z_init
    
    def attack_y_register(self, x_init, z_init):
        # Atak korelacyjny na rejestr Y (4-bitowy) po znalezieniu X i Z
        best_corr = -1
        best_y_init = None
        total_candidates = 0
        
        # Przetestuj wszystkie możliwe inicjalizacje rejestru Y (z wyjątkiem wektora zerowego)
        for y_init in itertools.product([0,1], repeat=4):
            if sum(y_init) == 0:
                continue
                
            total_candidates += 1
            # Symulacja pełnego generatora klucza z aktualnymi kandydatami X i Z
            generator = KeyStreamGenerator(x_init, list(y_init), z_init)
            key_stream = generator.get_key_stream(len(self.recovered_key_bits))
            
            corr = self._pearson_correlation(self.recovered_key_bits, key_stream)
            
            if corr > best_corr:
                best_corr = corr
                best_y_init = list(y_init)
                
        print(f"Przetestowano {total_candidates} kandydatów dla rejestru Y")
        return best_y_init
    
    def full_attack(self):
        # Pełny atak korelacyjny na wszystkie rejestry X, Y, Z
        start_time = time.time()
        self.operations_count = 0
        
        print("\nRozpoczęcie ataku korelacyjnego...")
        print(f"Długość analizowanego strumienia: {len(self.recovered_key_bits)} bitów")
        
        print("\nAtak na rejestr X...")
        x_init = self.attack_x_register()
        print(f"Znalezione początkowe wypełnienie X: {x_init}")
        
        print("\nAtak na rejestr Z...")
        z_init = self.attack_z_register()
        print(f"Znalezione początkowe wypełnienie Z: {z_init}")
        
        print("\nAtak na rejestr Y...")
        y_init = self.attack_y_register(x_init, z_init)
        print(f"Znalezione początkowe wypełnienie Y: {y_init}")
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        print("\nStatystyki wydajności:")
        print(f"Czas wykonania: {elapsed_time:.4f} sekund")
        print(f"Łączna liczba operacji: {self.operations_count}")
        print(f"Operacje na sekundę: {self.operations_count/elapsed_time:.2f}")
        
        return x_init, y_init, z_init

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
        print("Użycie: python zad2_atak.py plik_jawny.txt plik_szyfrogram.txt")
        sys.exit(1)
        
    plain_file = sys.argv[1]
    cipher_file = sys.argv[2]
    
    try:
        with open(plain_file, "rb") as f:
            known_plaintext = f.read()
        
        with open(cipher_file, "rb") as f:
            known_ciphertext = f.read()
            
        print(f"Wczytano {len(known_plaintext)} bajtów tekstu jawnego")
        print(f"Wczytano {len(known_ciphertext)} bajtów szyfrogramu")
        
        attacker = CorrelationAttack(known_plaintext, known_ciphertext)
        x_init, y_init, z_init = attacker.full_attack()
        
        key_bits = ''.join(map(str, x_init + y_init + z_init))
        print(f"\nOdzyskany klucz (12-bitowy): {key_bits}")
        
    except FileNotFoundError:
        print("Błąd: Nie można znaleźć pliku")
        sys.exit(1)
    except Exception as e:
        print(f"Błąd: {str(e)}")
        sys.exit(1)