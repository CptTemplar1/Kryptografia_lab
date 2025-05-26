import itertools

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


class StreamCipher:
    def __init__(self, key_bits):  # key_bits to łańcuch 12-bitowy np. "011010111100"
        if len(key_bits) != 12 or any(c not in '01' for c in key_bits):
            raise ValueError("Klucz musi być łańcuchem 12-bitowym składającym się z 0 i 1")

        x_init = [int(b) for b in key_bits[0:3]]
        y_init = [int(b) for b in key_bits[3:7]]
        z_init = [int(b) for b in key_bits[7:12]]

        self.generator = KeyStreamGenerator(x_init, y_init, z_init)

    def _bytes_to_bits(self, byte_data):
        return list(itertools.chain.from_iterable(
            [(byte >> i) & 1 for i in reversed(range(8))] for byte in byte_data))

    def _bits_to_bytes(self, bits):
        return bytes([
            sum([bits[i * 8 + j] << (7 - j) for j in range(8)])
            for i in range(len(bits) // 8)
        ])

    def encrypt(self, input_file, output_file):
        with open(input_file, 'rb') as f:
            plaintext = f.read()

        plain_bits = self._bytes_to_bits(plaintext)
        key_stream = self.generator.get_key_stream(len(plain_bits))
        cipher_bits = [b ^ k for b, k in zip(plain_bits, key_stream)]

        ciphertext = self._bits_to_bytes(cipher_bits)
        with open(output_file, 'wb') as f:
            f.write(ciphertext)

    def decrypt(self, input_file, output_file):
        # Deszyfrowanie = ponowne xorowanie z tym samym strumieniem klucza
        self.encrypt(input_file, output_file) 


if __name__ == "__main__":
    klucz = "011010111100"  # X: 011, Y: 0101, Z: 11100

    szyfr = StreamCipher(klucz)

    # Zaszyfruj
    szyfr.encrypt("plain.txt", "cipher.txt")

    # Odszyfruj
    szyfr = StreamCipher(klucz)  # nowa instancja dla tego samego klucza
    szyfr.decrypt("cipher.txt", "decrypted.txt")