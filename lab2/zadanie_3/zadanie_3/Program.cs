using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

class AffineCipher
{
    static void Main(string[] args)
    {
        string inputFile = "", outputFile = "", keyFile = "";
        bool encrypt = false, decrypt = false, bruteForce = false;

        for (int i = 0; i < args.Length; i++)
        {
            switch (args[i])
            {
                case "-i": inputFile = args[++i]; break;
                case "-o": outputFile = args[++i]; break;
                case "-k": keyFile = args[++i]; break;
                case "-e": encrypt = true; break;
                case "-d": decrypt = true; break;
                case "-a":
                    if (args[++i] == "bf") bruteForce = true;
                    break;
            }
        }

        if (bruteForce)
        {
            if (string.IsNullOrEmpty(inputFile) || string.IsNullOrEmpty(outputFile))
            {
                Console.WriteLine("Użycie: program -a bf -i szyfrogram.txt -o tekst_odszyfrowany.txt");
                return;
            }

            BruteForceAttack(inputFile, outputFile);
        }
        else if ((encrypt == decrypt) || string.IsNullOrEmpty(inputFile) || string.IsNullOrEmpty(outputFile) || string.IsNullOrEmpty(keyFile))
        {
            Console.WriteLine("Użycie: program -e|-d -k klucz.txt -i wejscie.txt -o wyjscie.txt");
            return;
        }
        else
        {
            var (a, b) = LoadKey(keyFile);
            string inputText = File.ReadAllText(inputFile);
            inputText = new string(inputText.ToUpper().Where(char.IsLetter).ToArray());

            string outputText = ProcessText(inputText, a, b, encrypt);
            File.WriteAllText(outputFile, outputText);
            Console.WriteLine("Operacja zakończona pomyślnie.");
        }
    }

    static (int a, int b) LoadKey(string filename)
    {
        var lines = File.ReadAllLines(filename);
        if (lines.Length < 2)
        {
            Console.WriteLine("Błąd: Plik klucza musi zawierać dwie liczby (a i b).");
            Environment.Exit(1);
        }

        int a = int.Parse(lines[0]);
        int b = int.Parse(lines[1]);

        if (GCD(a, 26) != 1)
        {
            Console.WriteLine("Błąd: Liczba a musi być względnie pierwsza z 26.");
            Environment.Exit(1);
        }

        return (a, b);
    }

    static int GCD(int a, int b)
    {
        while (b != 0)
        {
            int temp = b;
            b = a % b;
            a = temp;
        }
        return a;
    }

    static string ProcessText(string text, int a, int b, bool encrypt)
    {
        return new string(text.Select(ch => AffineTransform(ch, a, b, encrypt)).ToArray());
    }

    static char AffineTransform(char ch, int a, int b, bool encrypt)
    {
        int x = ch - 'A';
        int y;

        if (encrypt)
        {
            y = (a * x + b) % 26;
        }
        else
        {
            int aInverse = ModInverse(a, 26);
            y = aInverse * (x - b + 26) % 26;
        }

        return (char)(y + 'A');
    }

    static int ModInverse(int a, int m)
    {
        a = a % m;
        for (int x = 1; x < m; x++)
        {
            if ((a * x) % m == 1)
                return x;
        }
        return 1;
    }

    static void BruteForceAttack(string inputFile, string outputFile)
    {
        string cipherText = File.ReadAllText(inputFile);
        cipherText = new string(cipherText.ToUpper().Where(char.IsLetter).ToArray());

        double bestChiSquared = double.MaxValue;
        string bestText = "";
        int bestA = 0, bestB = 0;

        for (int a = 1; a < 26; a++)
        {
            if (GCD(a, 26) != 1) continue;

            for (int b = 0; b < 26; b++)
            {
                string decryptedText = ProcessText(cipherText, a, b, false);
                double chiSquared = ChiSquaredTest(decryptedText);

                if (chiSquared < bestChiSquared)
                {
                    bestChiSquared = chiSquared;
                    bestText = decryptedText;
                    bestA = a;
                    bestB = b;
                }
            }
        }

        File.WriteAllText(outputFile, bestText);
        Console.WriteLine($"Najlepsze klucze: a = {bestA}, b = {bestB}, wynik chi-kwadrat: {bestChiSquared}");
        Console.WriteLine("Operacja zakończona pomyślnie.");
    }

    static double ChiSquaredTest(string text)
    {
        var englishFrequencies = new Dictionary<char, double>
        {
            {'A', 0.08167}, {'B', 0.01492}, {'C', 0.02782}, {'D', 0.04253},
            {'E', 0.12702}, {'F', 0.02228}, {'G', 0.02015}, {'H', 0.06094},
            {'I', 0.06966}, {'J', 0.00153}, {'K', 0.00772}, {'L', 0.04025},
            {'M', 0.02406}, {'N', 0.06749}, {'O', 0.07507}, {'P', 0.01929},
            {'Q', 0.00095}, {'R', 0.05987}, {'S', 0.06327}, {'T', 0.09056},
            {'U', 0.02758}, {'V', 0.00978}, {'W', 0.0236}, {'X', 0.0015},
            {'Y', 0.01974}, {'Z', 0.00074}
        };

        var observedFrequencies = text.GroupBy(ch => ch)
                                      .ToDictionary(g => g.Key, g => (double)g.Count() / text.Length);

        double chiSquared = 0.0;
        foreach (var kvp in englishFrequencies)
        {
            char letter = kvp.Key;
            double expected = kvp.Value;
            double observed = observedFrequencies.ContainsKey(letter) ? observedFrequencies[letter] : 0.0;
            chiSquared += Math.Pow(observed - expected, 2) / expected;
        }

        return chiSquared;
    }
}