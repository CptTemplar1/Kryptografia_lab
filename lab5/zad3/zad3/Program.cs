using System;
using System.Collections.Generic;
using System.IO;
using System.Text;

namespace LFSRCKPA
{
    class Program
    {
        /// <summary>
        /// Konwertuje bajty na listę bitów (MSB-first)
        /// </summary>
        static List<int> BytesToBits(byte[] data)
        {
            List<int> bits = new List<int>();
            foreach (byte b in data)
            {
                for (int i = 7; i >= 0; i--)
                {
                    bits.Add((b >> i) & 1);
                }
            }
            return bits;
        }

        /// <summary>
        /// Konwertuje listę bitów na bajty (MSB-first)
        /// </summary>
        static byte[] BitsToBytes(List<int> bits)
        {
            List<byte> outBytes = new List<byte>();
            for (int i = 0; i < bits.Count; i += 8)
            {
                byte byteValue = 0;
                for (int j = 0; j < 8 && i + j < bits.Count; j++)
                {
                    byteValue = (byte)((byteValue << 1) | bits[i + j]);
                }
                outBytes.Add(byteValue);
            }
            return outBytes.ToArray();
        }

        /// <summary>
        /// Algorytm Berlekamp-Massey do znajdowania parametrów LFSR
        /// </summary>
        static (int L, List<int> C) BerlekampMassey(List<int> s)
        {
            int n = s.Count;
            List<int> C = new List<int>(new int[n + 1]);
            C[0] = 1;
            List<int> B = new List<int>(new int[n + 1]);
            B[0] = 1;
            int L = 0, m = 1;

            for (int i = 0; i < n; i++)
            {
                int d = s[i];
                for (int j = 1; j <= L; j++)
                {
                    d ^= C[j] & s[i - j];
                }

                if (d != 0)
                {
                    List<int> T = new List<int>(C);
                    for (int j = 0; j < B.Count; j++)
                    {
                        if (B[j] != 0)
                        {
                            if (j + m < C.Count)
                                C[j + m] ^= 1;
                        }
                    }
                    if (2 * L <= i)
                    {
                        L = i + 1 - L;
                        B = new List<int>(T);
                        m = 1;
                    }
                    else
                    {
                        m++;
                    }
                }
                else
                {
                    m++;
                }
            }

            return (L, C.GetRange(0, L + 1));
        }

        /// <summary>
        /// Generuje keystream na podstawie IV i tapów
        /// </summary>
        static List<int> GenerateKeystream(List<int> iv, List<int> taps, int length)
        {
            List<int> state = new List<int>(iv);
            List<int> ks = new List<int>();
            for (int i = 0; i < length; i++)
            {
                ks.Add(state[state.Count - 1]);
                int newBit = 0;
                foreach (int t in taps)
                {
                    newBit ^= state[t];
                }
                state.Insert(0, newBit);
                state.RemoveAt(state.Count - 1);
            }
            return ks;
        }

        static void Main(string[] args)
        {
            if (args.Length != 3)
            {
                Console.WriteLine("Użycie: LFSRCKPA <ciphertext> <plaintext_fragment> <output_text>");
                Environment.Exit(1);
            }

            string ctFile = args[0];
            string fragFile = args[1];
            string outText = args[2];

            // 1) Wczytaj pliki
            byte[] ct = File.ReadAllBytes(ctFile);
            byte[] frag = File.ReadAllBytes(fragFile);
            List<int> ctBits = BytesToBits(ct);
            List<int> fragBits = BytesToBits(frag);

            // 2) Odtwórz fragment keystreamu
            int nFrag = fragBits.Count;
            List<int> ksFrag = new List<int>();
            for (int i = 0; i < nFrag; i++)
            {
                ksFrag.Add(fragBits[i] ^ ctBits[i]);
            }

            // 3) Algorytm Berlekamp-Massey
            var (L, C) = BerlekampMassey(ksFrag);
            Console.WriteLine($"Zidentyfikowane LFSR: L = {L}, wektor C = [{string.Join(", ", C)}]");

            // 4) Obliczenia długości
            int required = 2 * L;
            int maxPeriod = (1 << L) - 1;
            Console.WriteLine($"Minimalna długość znanego tekstu do pełnego odzyskania: {required} bitów");
            Console.WriteLine($"Maksymalny okres sekwencji: {maxPeriod} bitów");
            if (nFrag < required)
            {
                Console.WriteLine($"Uwaga: użyto {nFrag} bitów; potrzeba co najmniej {required} bitów.");
            }

            // 5) Przygotuj IV i taps
            List<int> iv = ksFrag.GetRange(0, L);
            List<int> taps = new List<int>();
            for (int j = 1; j < C.Count; j++)
            {
                if (C[j] == 1)
                {
                    taps.Add(j - 1);
                }
            }
            Console.WriteLine($"IV (pierwsze {L} bitów): [{string.Join(", ", iv)}]");
            Console.WriteLine($"Tapy: [{string.Join(", ", taps)}]");

            // 6) Generuj keystream i odszyfruj
            List<int> fullKs = GenerateKeystream(iv, taps, ctBits.Count);
            List<int> decBits = new List<int>();
            for (int i = 0; i < ctBits.Count; i++)
            {
                decBits.Add(ctBits[i] ^ fullKs[i]);
            }
            byte[] decBytes = BitsToBytes(decBits);

            // 7) Dekoduj i zapisz tekst
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
}