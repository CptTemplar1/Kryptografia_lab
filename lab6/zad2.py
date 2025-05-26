import itertools
import math

class CorrelationAttack:
    def __init__(self, known_plaintext, known_ciphertext):
        self.known_plain_bits = self._bytes_to_bits(known_plaintext)
        self.known_cipher_bits = self._bytes_to_bits(known_ciphertext)
        self.recovered_key_bits = [p ^ c for p, c in zip(self.known_plain_bits, self.known_cipher_bits)]
        
    def _bytes_to_bits(self, byte_data):
        return list(itertools.chain.from_iterable(
            [(byte >> i) & 1 for i in reversed(range(8))] for byte in byte_data))
    
    def _pearson_correlation(self, stream1, stream2):
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
        
        if den == 0:
            return 0
            
        return num / den
    
    def _generate_x_stream(self, x_init, length):
        x_reg = x_init.copy()
        stream = []
        for _ in range(length):
            stream.append(x_reg[0])
            x_new = x_reg[0] ^ x_reg[2]
            x_reg = x_reg[1:] + [x_new]
        return stream
    
    def _generate_z_stream(self, z_init, length):
        z_reg = z_init.copy()
        stream = []
        for _ in range(length):
            stream.append(z_reg[0])
            z_new = z_reg[0] ^ z_reg[2]
            z_reg = z_reg[1:] + [z_new]
        return stream
    
    def _generate_y_stream(self, y_init, length):
        y_reg = y_init.copy()
        stream = []
        for _ in range(length):
            stream.append(y_reg[0])
            y_new = y_reg[0] ^ y_reg[3]
            y_reg = y_reg[1:] + [y_new]
        return stream
    
    def attack_x_register(self):
        best_corr = -1
        best_x_init = None
        
        # Generuj wszystkie możliwe 3-bitowe inicjalizacje X (z wyjątkiem [0,0,0])
        for x_init in itertools.product([0,1], repeat=3):
            if sum(x_init) == 0:
                continue  # pomiń wektor zerowy
                
            x_stream = self._generate_x_stream(list(x_init), len(self.recovered_key_bits))
            corr = self._pearson_correlation(self.recovered_key_bits, x_stream)
            
            # Szukamy wysokiej korelacji (bliskiej 1/3)
            if abs(corr - 1/3) < abs(best_corr - 1/3) or best_corr == -1:
                best_corr = corr
                best_x_init = list(x_init)
                
        return best_x_init
    
    def attack_z_register(self):
        best_corr = -1
        best_z_init = None
        
        # Generuj wszystkie możliwe 5-bitowe inicjalizacje Z (z wyjątkiem [0,0,0,0,0])
        for z_init in itertools.product([0,1], repeat=5):
            if sum(z_init) == 0:
                continue  # pomiń wektor zerowy
                
            z_stream = self._generate_z_stream(list(z_init), len(self.recovered_key_bits))
            corr = self._pearson_correlation(self.recovered_key_bits, z_stream)
            
            # Szukamy wysokiej korelacji (bliskiej 1/3)
            if abs(corr - 1/3) < abs(best_corr - 1/3) or best_corr == -1:
                best_corr = corr
                best_z_init = list(z_init)
                
        return best_z_init
    
    def attack_y_register(self, x_init, z_init):
        best_corr = -1
        best_y_init = None
        
        # Generuj wszystkie możliwe 4-bitowe inicjalizacje Y (z wyjątkiem [0,0,0,0])
        for y_init in itertools.product([0,1], repeat=4):
            if sum(y_init) == 0:
                continue  # pomiń wektor zerowy
                
            # Symuluj pełny generator klucza
            generator = KeyStreamGenerator(x_init, list(y_init), z_init)
            key_stream = generator.get_key_stream(len(self.recovered_key_bits))
            
            corr = self._pearson_correlation(self.recovered_key_bits, key_stream)
            
            if corr > best_corr:
                best_corr = corr
                best_y_init = list(y_init)
                
        return best_y_init
    
    def full_attack(self):
        print("Atak na rejestr X...")
        x_init = self.attack_x_register()
        print(f"Znalezione początkowe wypełnienie X: {x_init}")
        
        print("\nAtak na rejestr Z...")
        z_init = self.attack_z_register()
        print(f"Znalezione początkowe wypełnienie Z: {z_init}")
        
        print("\nAtak na rejestr Y...")
        y_init = self.attack_y_register(x_init, z_init)
        print(f"Znalezione początkowe wypełnienie Y: {y_init}")
        
        return x_init, y_init, z_init

# Klasa KeyStreamGenerator z Zadania 1 (potrzebna do ataku na rejestr Y)
class KeyStreamGenerator:
    def __init__(self, x_init, y_init, z_init):
        if len(x_init) != 3 or len(y_init) != 4 or len(z_init) != 5:
            raise ValueError("Długości inicjalizacyjne muszą wynosić odpowiednio: X=3, Y=4, Z=5")
        if x_init == [0, 0, 0] or y_init == [0, 0, 0, 0] or z_init == [0, 0, 0, 0, 0]:
            raise ValueError("Żaden rejestr nie może być całkowicie zerowy")

        self.X = x_init.copy()
        self.Y = y_init.copy()
        self.Z = z_init.copy()

    def _next_bit(self):
        xi = self.X[0]
        yi = self.Y[0]
        zi = self.Z[0]

        # Funkcja łącząca: ki = xi * yi ⊕ yi * zi ⊕ zi
        ki = (xi & yi) ^ (yi & zi) ^ zi

        # Aktualizacja rejestrów
        x_new = self.X[0] ^ self.X[2]
        y_new = self.Y[0] ^ self.Y[3]
        z_new = self.Z[0] ^ self.Z[2]

        self.X = self.X[1:] + [x_new]
        self.Y = self.Y[1:] + [y_new]
        self.Z = self.Z[1:] + [z_new]

        return ki

    def get_key_stream(self, length):
        return [self._next_bit() for _ in range(length)]

if __name__ == "__main__":
    # Przykład użycia:
    # Załóżmy, że mamy parę tekst jawnego i szyfrogramu
    with open("plain.txt", "rb") as f:
        known_plaintext = f.read()
    
    with open("cipher.txt", "rb") as f:
        known_ciphertext = f.read()
    
    # Przeprowadź atak
    attacker = CorrelationAttack(known_plaintext, known_ciphertext)
    x_init, y_init, z_init = attacker.full_attack()
    
    # Wyświetl znaleziony klucz
    key_bits = ''.join(map(str, x_init + y_init + z_init))
    print(f"\nOdzyskany klucz (12-bitowy): {key_bits}")