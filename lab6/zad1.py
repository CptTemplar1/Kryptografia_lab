import itertools

class KeyStreamGenerator:
    def __init__(self, x_init, y_init, z_init):
        # Sprawdzenie poprawności długości rejestrów
        if len(x_init) != 3 or len(y_init) != 4 or len(z_init) != 5:
            raise ValueError("Długości inicjalizacyjne muszą wynosić odpowiednio: X=3, Y=4, Z=5")
        # Sprawdzenie czy żaden rejestr nie jest całkowicie zerowy
        if x_init == [0, 0, 0] or y_init == [0, 0, 0, 0] or z_init == [0, 0, 0, 0, 0]:
            raise ValueError("Żaden rejestr nie może być całkowicie zerowy")

        # Inicjalizacja rejestrów przesuwnych
        self.X = x_init.copy()  # Rejestr X - 3 bitowy
        self.Y = y_init.copy()  # Rejestr Y - 4 bitowy
        self.Z = z_init.copy()  # Rejestr Z - 5 bitowy

    def _next_bit(self):
        # Pobranie pierwszych bitów z każdego rejestru
        xi = self.X[0]  # Pierwszy bit rejestru X
        yi = self.Y[0]  # Pierwszy bit rejestru Y
        zi = self.Z[0]  # Pierwszy bit rejestru Z

        # Funkcja łącząca (nieliniowa): ki = xi*yi XOR yi*zi XOR zi
        ki = (xi & yi) ^ (yi & zi) ^ zi

        # Aktualizacja rejestrów (funkcje sprzężenia zwrotnego)
        x_new = self.X[0] ^ self.X[2]  # xi+3 = xi ⊕ xi+1
        y_new = self.Y[0] ^ self.Y[3]  # yi+4 = yi ⊕ yi+3
        z_new = self.Z[0] ^ self.Z[2]  # zi+5 = zi ⊕ zi+2

        # Przesunięcie rejestrów i dodanie nowych bitów
        self.X = self.X[1:] + [x_new]  # Przesuń X i dodaj nowy bit
        self.Y = self.Y[1:] + [y_new]  # Przesuń Y i dodaj nowy bit
        self.Z = self.Z[1:] + [z_new]  # Przesuń Z i dodaj nowy bit

        return ki  # Zwróć kolejny bit strumienia klucza

    def get_key_stream(self, length):
        # Generowanie strumienia klucza o zadanej długości
        return [self._next_bit() for _ in range(length)]


class StreamCipher:
    def __init__(self, key_bits):  # key_bits to 12-bitowy ciąg znaków '0' i '1'
        # Walidacja klucza
        if len(key_bits) != 12 or any(c not in '01' for c in key_bits):
            raise ValueError("Klucz musi być łańcuchem 12-bitowym składającym się z 0 i 1")

        # Podział klucza na części dla poszczególnych rejestrów
        x_init = [int(b) for b in key_bits[0:3]]   # 3 bity dla X
        y_init = [int(b) for b in key_bits[3:7]]   # 4 bity dla Y
        z_init = [int(b) for b in key_bits[7:12]]  # 5 bitów dla Z

        # Inicjalizacja generatora strumienia klucza
        self.generator = KeyStreamGenerator(x_init, y_init, z_init)

    def _bytes_to_bits(self, byte_data):
        # Konwersja danych bajtowych na listę bitów
        return list(itertools.chain.from_iterable(
            [(byte >> i) & 1 for i in reversed(range(8))] for byte in byte_data))

    def _bits_to_bytes(self, bits):
        # Konwersja listy bitów z powrotem na bajty
        return bytes([
            sum([bits[i * 8 + j] << (7 - j) for j in range(8)])
            for i in range(len(bits) // 8)
        ])

    def encrypt(self, input_file, output_file):
        # Odczyt pliku wejściowego w trybie binarnym
        with open(input_file, 'rb') as f:
            plaintext = f.read()

        # Konwersja tekstu jawnego na bity
        plain_bits = self._bytes_to_bits(plaintext)
        # Generowanie strumienia klucza o długości tekstu jawnego
        key_stream = self.generator.get_key_stream(len(plain_bits))
        # Szyfrowanie poprzez XOR każdego bitu tekstu z bitem klucza
        cipher_bits = [b ^ k for b, k in zip(plain_bits, key_stream)]

        # Konwersja zaszyfrowanych bitów na bajty i zapis do pliku
        ciphertext = self._bits_to_bytes(cipher_bits)
        with open(output_file, 'wb') as f:
            f.write(ciphertext)

    def decrypt(self, input_file, output_file):
        # Deszyfrowanie to to samo co szyfrowanie (XOR jest odwracalny)
        self.encrypt(input_file, output_file) 


if __name__ == "__main__":
    # Przykładowy 12-bitowy klucz
    klucz = "011010111100"  # X: 011, Y: 0101, Z: 11100

    # Inicjalizacja szyfru strumieniowego
    szyfr = StreamCipher(klucz)

    # Szyfrowanie pliku
    szyfr.encrypt("plain.txt", "cipher.txt")

    # Deszyfrowanie pliku (wymaga nowej instancji z tym samym kluczem)
    szyfr = StreamCipher(klucz)
    szyfr.decrypt("cipher.txt", "decrypted.txt")