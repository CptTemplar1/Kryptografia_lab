﻿using System;
using System.Collections.Generic;
using System.IO;
using System.Text;

class Program
    {
        // Konwertuje tablicę bajtów na listę bitów (każdy bajt na 8 bitów, od MSB do LSB)
        static List<int> BytesToBits(byte[] data)
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
        static byte[] BitsToBytes(List<int> bits)
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

        // Algorytm Berlekampa-Massey'a do znajdowania parametrów LFSR
        // na podstawie fragmentu strumienia klucza (s)
        // Zwraca długość rejestru (L) i wielomian charakterystyczny (C)
        static (int L, List<int> C) BerlekampMassey(List<int> s)
        {
            int n = s.Count;
            List<int> C = new List<int>(new int[n + 1]); // Wielomian charakterystyczny
            C[0] = 1; // Inicjalizacja C(x) = 1
            List<int> B = new List<int>(new int[n + 1]); // Poprzedni wielomian
            B[0] = 1; // Inicjalizacja B(x) = 1
            int L = 0; // Aktualna długość LFSR
            int m = 1; // Licznik przesunięć

            for (int i = 0; i < n; i++)
            {
                // Obliczenie różnicy (d) między przewidywanym a rzeczywistym bitem
                int d = s[i];
                for (int j = 1; j <= L; j++)
                {
                    d ^= C[j] & s[i - j]; // XOR z poprzednimi bitami
                }

                if (d != 0) // Jeśli różnica niezerowa, aktualizacja wielomianu
                {
                    List<int> T = new List<int>(C); // Kopia aktualnego wielomianu
                    for (int j = 0; j < B.Count; j++)
                    {
                        if (B[j] != 0)
                        {
                            if (j + m < C.Count)
                                C[j + m] ^= 1; // Aktualizacja C przez XOR z przesuniętym B
                        }
                    }
                    if (2 * L <= i) // Jeśli długość LFSR jest za mała
                    {
                        L = i + 1 - L; // Zwiększ długość LFSR
                        B = new List<int>(T); // Zapisz poprzedni wielomian
                        m = 1; // Reset licznika
                    }
                    else
                    {
                        m++; // Inkrementuj licznik
                    }
                }
                else
                {
                    m++; // Inkrementuj licznik
                }
            }

            return (L, C.GetRange(0, L + 1)); // Zwróć długość i wielomian
        }

        // Generuje strumień klucza dla LFSR o podanym IV, tapach i długości
        static List<int> GenerateKeystream(List<int> iv, List<int> taps, int length)
        {
            List<int> state = new List<int>(iv); // Stan początkowy (IV)
            List<int> ks = new List<int>(); // Strumień klucza

            for (int i = 0; i < length; i++)
            {
                ks.Add(state[state.Count - 1]); // Dodaj ostatni bit stanu
                int newBit = 0;
                foreach (int t in taps)
                {
                    newBit ^= state[t]; // Oblicz nowy bit (XOR z tapami)
                }
                state.Insert(0, newBit); // Wstaw nowy bit na początek
                state.RemoveAt(state.Count - 1); // Usuń ostatni bit
            }

            return ks;
        }

        static void Main(string[] args)
        {
            // Sprawdzenie argumentów
            if (args.Length != 3)
            {
                Console.WriteLine("Użycie: LFSRCKPA <ciphertext> <plaintext_fragment> <output_text>");
                Environment.Exit(1);
            }

            string ctFile = args[0]; // Plik szyfrogramu
            string fragFile = args[1]; // Plik fragmentu plaintextu
            string outText = args[2]; // Plik wyjściowy

            // Odczyt i konwersja na bity
            byte[] ct = File.ReadAllBytes(ctFile);
            byte[] frag = File.ReadAllBytes(fragFile);
            List<int> ctBits = BytesToBits(ct);
            List<int> fragBits = BytesToBits(frag);

            // Generowanie fragmentu strumienia klucza (XOR fragmentu plaintextu i szyfrogramu)
            int nFrag = fragBits.Count;
            List<int> ksFrag = new List<int>();
            for (int i = 0; i < nFrag; i++)
            {
                ksFrag.Add(fragBits[i] ^ ctBits[i]);
            }

            // Znajdowanie parametrów LFSR
            var (L, C) = BerlekampMassey(ksFrag);
            Console.WriteLine($"Zidentyfikowane LFSR: L = {L}, wektor C = [{string.Join(", ", C)}]");

            // Obliczenie minimalnej wymaganej długości i maksymalnego okresu
            int required = 2 * L;
            int maxPeriod = (1 << L) - 1;
            Console.WriteLine($"Minimalna długość znanego tekstu do pełnego odzyskania: {required} bitów");
            Console.WriteLine($"Maksymalny okres sekwencji: {maxPeriod} bitów");
            if (nFrag < required)
            {
                Console.WriteLine($"Uwaga: użyto {nFrag} bitów; potrzeba co najmniej {required} bitów.");
            }

            // Wyodrębnienie IV i tapów z wielomianu charakterystycznego
            List<int> iv = ksFrag.GetRange(0, L);
            List<int> taps = new List<int>();
            for (int j = 1; j < C.Count; j++)
            {
                if (C[j] == 1)
                {
                    taps.Add(j - 1); // Pozycje tapów odpowiadają współczynnikom 1 w wielomianie
                }
            }
            Console.WriteLine($"IV (pierwsze {L} bitów): [{string.Join(", ", iv)}]");
            Console.WriteLine($"Tapy: [{string.Join(", ", taps)}]");

            // Generowanie pełnego strumienia klucza i deszyfrowanie
            List<int> fullKs = GenerateKeystream(iv, taps, ctBits.Count);
            List<int> decBits = new List<int>();
            for (int i = 0; i < ctBits.Count; i++)
            {
                decBits.Add(ctBits[i] ^ fullKs[i]); // XOR szyfrogramu ze strumieniem klucza
            }

            // Konwersja i zapis wyniku
            byte[] decBytes = BitsToBytes(decBits);

            // Próba dekodowania jako UTF-8
            try
            {
                string text = Encoding.UTF8.GetString(decBytes);
                File.WriteAllText(outText, text, Encoding.UTF8);
                Console.WriteLine($"Zdekodowany tekst (UTF-8) zapisano do: {outText}");
            }
            catch (ArgumentException)
            {
                Console.WriteLine("Dekodowanie UTF-8 nie powiodło się; upewnij się, że fragment plaintextu jest wystarczający.");
            }
        }
    }