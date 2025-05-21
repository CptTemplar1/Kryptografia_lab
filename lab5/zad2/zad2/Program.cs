﻿using System;
using System.Collections.Generic;
using System.IO;
using System.Text;

namespace LFSRAttack
{
    class Program
    {
        // Algorytm Berlekampa-Massey'a do znajdowania minimalnego wielomianu charakterystycznego LFSR
        // na podstawie fragmentu strumienia klucza (s).
        // Zwraca długość LFSR (L) oraz współczynniki wielomianu charakterystycznego (C).
        static (int L, List<int> C) BerlekampMassey(List<int> s)
        {
            int n = s.Count;
            List<int> C = new List<int>(new int[n + 1]); // Wielomian charakterystyczny (aktualny)
            C[0] = 1; // Inicjalizacja: C(x) = 1
            List<int> B = new List<int>(new int[n + 1]); // Poprzedni wielomian charakterystyczny
            B[0] = 1; // Inicjalizacja: B(x) = 1
            int L = 0; // Długość LFSR
            int m = 1; // Licznik przesunięć

            for (int i = 0; i < n; i++)
            {
                // Obliczenie różnicy (d) między przewidywanym a rzeczywistym bitem
                int d = s[i];
                for (int j = 1; j <= L; j++)
                {
                    d ^= C[j] & s[i - j]; // XOR z poprzednimi bitami i współczynnikami C
                }

                if (d != 0) // Jeśli różnica niezerowa, aktualizacja wielomianu C
                {
                    List<int> T = new List<int>(C); // Kopia aktualnego wielomianu
                    for (int j = 0; j < B.Count; j++)
                    {
                        if (B[j] != 0) // Aktualizacja C przez XOR z przesuniętym B
                        {
                            if (j + m < C.Count)
                                C[j + m] ^= 1;
                        }
                    }
                    if (2 * L <= i) // Jeśli długość LFSR jest za mała, zwiększ ją
                    {
                        L = i + 1 - L;
                        B = new List<int>(T); // Zapisz poprzedni wielomian
                        m = 1; // Zresetuj licznik przesunięć
                    }
                    else
                    {
                        m++; // Inkrementuj licznik przesunięć
                    }
                }
                else
                {
                    m++; // Inkrementuj licznik przesunięć
                }
            }

            return (L, C.GetRange(0, L + 1)); // Zwróć długość LFSR i wielomian charakterystyczny
        }

        // Konwertuje tablicę bajtów na listę bitów (każdy bajt na 8 bitów, od MSB do LSB)
        static List<int> BitsFromBytes(byte[] data)
        {
            List<int> bits = new List<int>();
            foreach (byte b in data)
            {
                for (int i = 7; i >= 0; i--)
                {
                    bits.Add((b >> i) & 1); // Wyodrębnienie i-tego bitu
                }
            }
            return bits;
        }

        // Konwertuje listę bitów na tablicę bajtów (co 8 bitów na bajt)
        static byte[] BytesFromBits(List<int> bits)
        {
            List<byte> outBytes = new List<byte>();
            for (int i = 0; i < bits.Count; i += 8)
            {
                byte byteValue = 0;
                for (int j = 0; j < 8 && i + j < bits.Count; j++)
                {
                    byteValue = (byte)((byteValue << 1) | bits[i + j]); // Składanie bajtu z bitów
                }
                outBytes.Add(byteValue);
            }
            return outBytes.ToArray();
        }

        // Generuje strumień klucza (keystream) dla LFSR o podanym IV, pozycjach TAPS i długości
        static List<int> GenerateKeystream(List<int> iv, List<int> taps, int length)
        {
            List<int> state = new List<int>(iv); // Inicjalizacja stanu początkowego (IV)
            List<int> ks = new List<int>(); // Strumień klucza
            for (int i = 0; i < length; i++)
            {
                ks.Add(state[state.Count - 1]); // Dodanie ostatniego bitu stanu do strumienia
                int newBit = 0;
                foreach (int t in taps)
                {
                    newBit ^= state[t]; // Obliczenie nowego bitu (XOR z TAPS)
                }
                state.Insert(0, newBit); // Wstawienie nowego bitu na początek
                state.RemoveAt(state.Count - 1); // Usunięcie ostatniego bitu
            }
            return ks;
        }

        static void Main(string[] args)
        {
            // Sprawdzenie liczby argumentów
            if (args.Length != 3)
            {
                Console.WriteLine("Użycie: LFSRAttack <known_plaintext> <ciphertext> <output_plaintext>");
                Environment.Exit(1);
            }

            string ptFile = args[0]; // Ścieżka do znanego plaintextu
            string ctFile = args[1]; // Ścieżka do szyfrogramu
            string outFile = args[2]; // Ścieżka do pliku wyjściowego (odszyfrowany tekst)

            // Odczytanie plików i konwersja na bity
            byte[] pt = File.ReadAllBytes(ptFile);
            byte[] ct = File.ReadAllBytes(ctFile);
            List<int> ptBits = BitsFromBytes(pt);
            List<int> ctBits = BitsFromBytes(ct);
            int n = ctBits.Count; // Długość szyfrogramu w bitach

            // Wygenerowanie fragmentu strumienia klucza (XOR znanego plaintextu i szyfrogramu)
            int minLen = Math.Min(ptBits.Count, n);
            List<int> ksFrag = new List<int>();
            for (int i = 0; i < minLen; i++)
            {
                ksFrag.Add(ptBits[i] ^ ctBits[i]);
            }

            // Znalezienie parametrów LFSR za pomocą algorytmu Berlekampa-Massey'a
            var (L, C) = BerlekampMassey(ksFrag);
            Console.WriteLine($"Odnalezione LFSR: długość L={L}, wielomian C=[{string.Join(", ", C)}]");

            // Wyodrębnienie IV (pierwsze L bitów strumienia klucza)
            List<int> iv = ksFrag.GetRange(0, L);
            Console.WriteLine($"Zrekonstruowany IV (pierwsze {L} bitów): [{string.Join(", ", iv)}]");

            // Konwersja wielomianu charakterystycznego na pozycje TAPS (pomijając C[0])
            List<int> taps = new List<int>();
            for (int j = 1; j < C.Count; j++)
            {
                if (C[j] == 1)
                {
                    taps.Add(j - 1); // Pozycje TAPS to indeksy współczynników 1 w wielomianie
                }
            }
            Console.WriteLine($"Pozycje taps: [{string.Join(", ", taps)}]");

            // Generowanie pełnego strumienia klucza i odszyfrowanie całego szyfrogramu
            List<int> fullKs = GenerateKeystream(iv, taps, n);
            List<int> decBits = new List<int>();
            for (int i = 0; i < n; i++)
            {
                decBits.Add(ctBits[i] ^ fullKs[i]); // XOR szyfrogramu ze strumieniem klucza
            }

            // Zapis odszyfrowanych danych do pliku
            byte[] plaintext = BytesFromBits(decBits);
            File.WriteAllBytes(outFile, plaintext);
            Console.WriteLine($"Odszyfrowano cały szyfrogram do pliku: {outFile}");

            // Próba dekodowania jako UTF-8 (dla tekstowych danych)
            try
            {
                string decodedText = Encoding.UTF8.GetString(plaintext);
                Console.WriteLine("Dekodowanie UTF-8 powiodło się.");
            }
            catch (ArgumentException)
            {
                Console.WriteLine("Uwaga: dekodowanie UTF-8 NIE powiodło się. Sprawdź poprawność plaintext.");
            }
        }
    }
}