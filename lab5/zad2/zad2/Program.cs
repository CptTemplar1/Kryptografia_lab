using System;
using System.Collections.Generic;
using System.IO;
using System.Text;

namespace LFSRAttack
{
    class Program
    {
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

        static List<int> BitsFromBytes(byte[] data)
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

        static byte[] BytesFromBits(List<int> bits)
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
                Console.WriteLine("Użycie: LFSRAttack <known_plaintext> <ciphertext> <output_plaintext>");
                Environment.Exit(1);
            }

            string ptFile = args[0];
            string ctFile = args[1];
            string outFile = args[2];

            byte[] pt = File.ReadAllBytes(ptFile);
            byte[] ct = File.ReadAllBytes(ctFile);
            List<int> ptBits = BitsFromBytes(pt);
            List<int> ctBits = BitsFromBytes(ct);
            int n = ctBits.Count;

            int minLen = Math.Min(ptBits.Count, n);
            List<int> ksFrag = new List<int>();
            for (int i = 0; i < minLen; i++)
            {
                ksFrag.Add(ptBits[i] ^ ctBits[i]);
            }

            var (L, C) = BerlekampMassey(ksFrag);
            Console.WriteLine($"Odnalezione LFSR: długość L={L}, wielomian C=[{string.Join(", ", C)}]");

            List<int> iv = ksFrag.GetRange(0, L);
            Console.WriteLine($"Zrekonstruowany IV (pierwsze {L} bitów): [{string.Join(", ", iv)}]");

            List<int> taps = new List<int>();
            for (int j = 1; j < C.Count; j++)
            {
                if (C[j] == 1)
                {
                    taps.Add(j - 1);
                }
            }
            Console.WriteLine($"Pozycje taps: [{string.Join(", ", taps)}]");

            List<int> fullKs = GenerateKeystream(iv, taps, n);
            List<int> decBits = new List<int>();
            for (int i = 0; i < n; i++)
            {
                decBits.Add(ctBits[i] ^ fullKs[i]);
            }
            byte[] plaintext = BytesFromBits(decBits);
            File.WriteAllBytes(outFile, plaintext);
            Console.WriteLine($"Odszyfrowano cały szyfrogram do pliku: {outFile}");

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