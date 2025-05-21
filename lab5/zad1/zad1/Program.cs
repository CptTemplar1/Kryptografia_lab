﻿using System;
using System.Collections.Generic;
using System.IO;

class Program
    {
        // Parametry LFSR (Linear Feedback Shift Register)
        // Wielomian: P(x)=1 + x + x^3 + x^5 + x^16 + x^17
        // Odpowiadające mu pozycje w rejestrze, które są używane do obliczenia nowego bitu (XOR)
        private static readonly int[] TAPS = { 0, 1, 3, 5, 16 };

        // Sekwencja inicjująca (initial state) rejestru LFSR
        // [0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1]
        private static readonly List<int> INITIAL_STATE = new List<int> { 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1 };

        // Generuje strumień klucza (keystream) o podanej długości za pomocą LFSR
        private static List<int> GenerateKeystream(int length)
        {
            List<int> state = new List<int>(INITIAL_STATE); // Inicjalizacja stanu początkowego
            List<int> keystream = new List<int>(); // Inicjalizacja strumienia klucza

            for (int i = 0; i < length; i++)
            {
                // Dodanie ostatniego bitu stanu do strumienia klucza
                keystream.Add(state[state.Count - 1]);

                // Obliczenie nowego bitu na podstawie pozycji określonych w TAPS (operacja XOR)
                int newBit = 0;
                foreach (int t in TAPS)
                {
                    newBit ^= state[t];
                }

                // Wstawienie nowego bitu na początek rejestru i usunięcie ostatniego bitu
                state.Insert(0, newBit);
                state.RemoveAt(state.Count - 1);
            }

            return keystream;
        }

        // Konwertuje tablicę bajtów na listę bitów
        private static List<int> BitsFromBytes(byte[] dataBytes)
        {
            List<int> bits = new List<int>();

            foreach (byte b in dataBytes)
            {
                // Dla każdego bitu w bajcie (od najbardziej znaczącego do najmniej znaczącego)
                for (int i = 7; i >= 0; i--)
                {
                    bits.Add((b >> i) & 1); // Wyodrębnienie i-tego bitu
                }
            }

            return bits;
        }

        // Konwertuje listę bitów na tablicę bajtów
        private static byte[] BytesFromBits(List<int> bits)
        {
            List<byte> outBytes = new List<byte>();

            for (int i = 0; i < bits.Count; i += 8)
            {
                byte byteValue = 0;
                // Łączenie 8 bitów w jeden bajt
                for (int j = 0; j < 8; j++)
                {
                    if (i + j < bits.Count)
                    {
                        byteValue = (byte)((byteValue << 1) | bits[i + j]); // Dodanie bitu do bajtu
                    }
                }
                outBytes.Add(byteValue); // Dodanie bajtu do listy wynikowej
            }

            return outBytes.ToArray();
        }

        // Szyfruje lub deszyfruje dane z pliku wejściowego i zapisuje do pliku wyjściowego
        private static void Encrypt(string inputPath, string outputPath)
        {
            // Odczytanie danych wejściowych
            byte[] plaintext = File.ReadAllBytes(inputPath);
            // Konwersja bajtów na bity
            List<int> ptBits = BitsFromBytes(plaintext);
            // Generowanie strumienia klucza o długości równej liczbie bitów danych wejściowych
            List<int> ks = GenerateKeystream(ptBits.Count);

            // Szyfrowanie/deszyfrowanie poprzez operację XOR na bitach danych i strumienia klucza
            List<int> ctBits = new List<int>();
            for (int i = 0; i < ptBits.Count; i++)
            {
                ctBits.Add(ptBits[i] ^ ks[i]);
            }

            // Konwersja bitów wynikowych na bajty i zapis do pliku wyjściowego
            byte[] ciphertext = BytesFromBits(ctBits);
            File.WriteAllBytes(outputPath, ciphertext);
        }

        static void Main(string[] args)
        {
            // Sprawdzenie liczby argumentów
            if (args.Length != 3)
            {
                Console.WriteLine("Użycie: LFSRCrypto <encrypt|decrypt> <wejście> <wyjście>");
                Environment.Exit(1);
            }

            string mode = args[0]; // Tryb pracy (encrypt/decrypt)
            string inputFile = args[1]; // Ścieżka do pliku wejściowego
            string outputFile = args[2]; // Ścieżka do pliku wyjściowego

            // Sprawdzenie poprawności trybu
            if (mode != "encrypt" && mode != "decrypt")
            {
                Console.WriteLine("Tryb nieznany. Wybierz 'encrypt' lub 'decrypt'.");
                Environment.Exit(1);
            }

            // Wywołanie funkcji Encrypt (deszyfrowanie jest tym samym co szyfrowanie w LFSR)
            Encrypt(inputFile, outputFile);
        }
    }  