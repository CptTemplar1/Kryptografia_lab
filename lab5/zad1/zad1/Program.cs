using System;
using System.Collections.Generic;
using System.IO;

namespace LFSRCrypto
{
    class Program
    {
        //Parametry LFSR
        //Wielomian: P(x)=1 + x + x^3 + x^5 + x^16 + x^17
        private static readonly int[] TAPS = { 0, 1, 3, 5, 16 };

        // Sekwencja inicjująca: [0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1]
        private static readonly List<int> INITIAL_STATE = new List<int> { 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1 };

        private static List<int> GenerateKeystream(int length)
        {
            List<int> state = new List<int>(INITIAL_STATE);
            List<int> keystream = new List<int>();

            for (int i = 0; i < length; i++)
            {
                keystream.Add(state[state.Count - 1]);

                int newBit = 0;
                foreach (int t in TAPS)
                {
                    newBit ^= state[t];
                }

                state.Insert(0, newBit);
                state.RemoveAt(state.Count - 1);
            }

            return keystream;
        }

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

            Encrypt(inputFile, outputFile);
        }
    }
}