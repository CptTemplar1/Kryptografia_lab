using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

class CaesarCipher
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
            var substitution = LoadKey(keyFile, decrypt);
            string inputText = File.ReadAllText(inputFile);
            inputText = new string(inputText.ToUpper().Where(char.IsLetter).ToArray());

            string outputText = ProcessText(inputText, substitution);
            File.WriteAllText(outputFile, outputText);
            Console.WriteLine("Operacja zakończona pomyślnie.");
        }
    }

    static Dictionary<char, char> LoadKey(string filename, bool reverse)
    {
        var substitution = new Dictionary<char, char>();

        foreach (var line in File.ReadLines(filename))
        {
            var parts = line.Split();
            if (parts.Length == 2)
            {
                char plain = char.ToUpper(parts[0][0]);
                char cipher = char.ToUpper(parts[1][0]);

                if (reverse) (plain, cipher) = (cipher, plain);

                substitution[plain] = cipher;
            }
        }

        if (substitution.Count != 26)
        {
            Console.WriteLine("Błąd: Tablica podstawieniowa musi zawierać 26 znaków.");
            Environment.Exit(1);
        }

        return substitution;
    }

    static string ProcessText(string text, Dictionary<char, char> substitution)
    {
        return new string(text.Select(ch => substitution.ContainsKey(ch) ? substitution[ch] : ch).ToArray());
    }

    static void BruteForceAttack(string inputFile, string outputFile)
    {
        string cipherText = File.ReadAllText(inputFile);
        cipherText = new string(cipherText.ToUpper().Where(char.IsLetter).ToArray());

        double bestChiSquared = double.MaxValue;
        string bestText = "";
        int bestShift = 0;

        for (int shift = 0; shift < 26; shift++)
        {
            string decryptedText = DecryptCaesar(cipherText, shift);
            double chiSquared = ChiSquaredTest(decryptedText);

            if (chiSquared < bestChiSquared)
            {
                bestChiSquared = chiSquared;
                bestText = decryptedText;
                bestShift = shift;
            }
        }

        File.WriteAllText(outputFile, bestText);
        Console.WriteLine($"Najlepsze przesunięcie: {bestShift}, wynik chi-kwadrat: {bestChiSquared}");
        Console.WriteLine("Operacja zakończona pomyślnie.");
    }

    static string DecryptCaesar(string cipherText, int shift)
    {
        return new string(cipherText.Select(ch => (char)('A' + (ch - 'A' - shift + 26) % 26)).ToArray());
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