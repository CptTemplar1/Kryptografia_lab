using System;
using System.Collections.Generic;
using System.IO;

namespace LFSRCrypto
{
    class Program
    {
        // Hardcoded LFSR parameters
        // Polinom: P(x)=1 + x + x^3 + x^5 + x^16 + x^17
        private static readonly int[] TAPS = { 0, 1, 3, 5, 16 };

        // Sekwencja inicjująca: [0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1]
        private static readonly List<int> INITIAL_STATE = new List<int> { 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1 };

        /// <summary>
        /// Generuje keystream długości `length` bitów na bazie LFSR
        /// </summary>
        private static List<int> GenerateKeystream(int length)
        {
            List<int> state = new List<int>(INITIAL_STATE);
            List<int> keystream = new List<int>();

            for (int i = 0; i < length; i++)
            {
                // Wyjście: ostatni bit rejestru
                keystream.Add(state[state.Count - 1]);

                // Oblicz nowy bit jako XOR wybranych tapów
                int newBit = 0;
                foreach (int t in TAPS)
                {
                    newBit ^= state[t];
                }

                // Przesuń rejestr w prawo i wstaw nowy bit na początku
                state.Insert(0, newBit);
                state.RemoveAt(state.Count - 1);
            }

            return keystream;
        }

        /// <summary>
        /// Konwertuje bajty na listę bitów MSB-first
        /// </summary>
        private static List<int> BitsFromBytes(byte[] dataBytes)
        {
            List<int> bits = new List<int>();

            foreach (byte b in dataBytes)
            {
                for (int i = 7; i >= 0; i--)
                {
                    bits.Add((b >> i) & 1);
                }
            }

            return bits;
        }

        /// <summary>
        /// Konwertuje listę bitów MSB-first na bajty
        /// </summary>
        private static byte[] BytesFromBits(List<int> bits)
        {
            List<byte> outBytes = new List<byte>();

            for (int i = 0; i < bits.Count; i += 8)
            {
                byte byteValue = 0;
                for (int j = 0; j < 8; j++)
                {
                    if (i + j < bits.Count)
                    {
                        byteValue = (byte)((byteValue << 1) | bits[i + j]);
                    }
                }
                outBytes.Add(byteValue);
            }

            return outBytes.ToArray();
        }

        /// <summary>
        /// Szyfruje lub deszyfruje plik (dla szyfru strumieniowego operacja jest identyczna)
        /// </summary>
        private static void Encrypt(string inputPath, string outputPath)
        {
            byte[] plaintext = File.ReadAllBytes(inputPath);
            List<int> ptBits = BitsFromBytes(plaintext);
            List<int> ks = GenerateKeystream(ptBits.Count);

            List<int> ctBits = new List<int>();
            for (int i = 0; i < ptBits.Count; i++)
            {
                ctBits.Add(ptBits[i] ^ ks[i]);
            }

            byte[] ciphertext = BytesFromBits(ctBits);
            File.WriteAllBytes(outputPath, ciphertext);
        }

        static void Main(string[] args)
        {
            if (args.Length != 3)
            {
                Console.WriteLine("Użycie: LFSRCrypto <encrypt|decrypt> <wejście> <wyjście>");
                Environment.Exit(1);
            }

            string mode = args[0];
            string inputFile = args[1];
            string outputFile = args[2];

            if (mode != "encrypt" && mode != "decrypt")
            {
                Console.WriteLine("Tryb nieznany. Wybierz 'encrypt' lub 'decrypt'.");
                Environment.Exit(1);
            }

            // Dla strumieniowego szyfrowania i deszyfrowania operacja jest identyczna
            Encrypt(inputFile, outputFile);
        }
    }
}