using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

class Program
{
    static void Main(string[] args)
    {
        string inputFile = "", outputFile = "", keyFile = "";
        string gramFile = "", refFile = "";
        bool encrypt = false, decrypt = false, calculateChiSquare = false;
        int nGram = 0, refNGram = 0;

        for (int i = 0; i < args.Length; i++)
        {
            switch (args[i])
            {
                case "-i": inputFile = args[++i]; break;
                case "-o": outputFile = args[++i]; break;
                case "-k": keyFile = args[++i]; break;
                case "-e": encrypt = true; break;
                case "-d": decrypt = true; break;
                case "-s": calculateChiSquare = true; break;
                case "-g1":
                case "-g2":
                case "-g3":
                case "-g4":
                    nGram = int.Parse(args[i].Substring(2, 1));
                    gramFile = args[++i];
                    break;
                case "-r1":
                case "-r2":
                case "-r3":
                case "-r4":
                    refNGram = int.Parse(args[i].Substring(2, 1));
                    refFile = args[++i];
                    break;
            }
        }

        if ((encrypt == decrypt) && nGram == 0 && !calculateChiSquare || string.IsNullOrEmpty(inputFile))
        {
            Console.WriteLine("Użycie: program -e|-d -k klucz.txt -i wejscie.txt -o wyjscie.txt [-g1|-g2|-g3|-g4 gram.txt] [-rX baza.txt] [-s]");
            return;
        }

        string inputText = File.ReadAllText(inputFile);
        inputText = new string(inputText.ToUpper().Where(char.IsLetter).ToArray());

        if (!string.IsNullOrEmpty(keyFile))
        {
            var substitution = LoadKey(keyFile, decrypt);
            string outputText = ProcessText(inputText, substitution);
            File.WriteAllText(outputFile, outputText);
            Console.WriteLine("Operacja zakończona pomyślnie.");
        }

        if (nGram > 0 && !string.IsNullOrEmpty(gramFile))
        {
            var nGramCounts = GenerateNGrams(inputText, nGram);
            SaveNGrams(gramFile, nGramCounts);
            Console.WriteLine($"Statystyki {nGram}-gramów zapisano do {gramFile}");
        }

        if (calculateChiSquare && !string.IsNullOrEmpty(refFile) && refNGram > 0)
        {
            var observed = GenerateNGrams(inputText, refNGram);
            var expected = LoadReferenceNGrams(refFile);
            double chiSquare = CalculateChiSquare(observed, expected);
            Console.WriteLine($"Wartość testu chi-kwadrat: {chiSquare:F4}");
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

    static Dictionary<string, int> GenerateNGrams(string text, int n)
    {
        var nGramCounts = new Dictionary<string, int>();

        for (int i = 0; i <= text.Length - n; i++)
        {
            string nGram = text.Substring(i, n);
            if (nGramCounts.ContainsKey(nGram))
                nGramCounts[nGram]++;
            else
                nGramCounts[nGram] = 1;
        }

        return nGramCounts;
    }

    static void SaveNGrams(string filename, Dictionary<string, int> nGramCounts)
    {
        using (var writer = new StreamWriter(filename))
        {
            writer.WriteLine("n-gram	liczność");
            foreach (var kvp in nGramCounts.OrderByDescending(k => k.Value))
            {
                writer.WriteLine($"{kvp.Key}	{kvp.Value}");
            }
        }
    }

    static Dictionary<string, double> LoadReferenceNGrams(string filename)
    {
        var reference = new Dictionary<string, double>();
        double total = 0;

        foreach (var line in File.ReadLines(filename))
        {
            var parts = line.Split();
            if (parts.Length == 2 && double.TryParse(parts[1], out double probability))
            {
                reference[parts[0]] = probability;
                total += probability;
            }
        }

        return reference;
    }

    static double CalculateChiSquare(Dictionary<string, int> observed, Dictionary<string, double> expected)
    {
        double chiSquare = 0.0;
        int totalObserved = observed.Values.Sum();

        foreach (var kvp in expected)
        {
            int observedCount = observed.ContainsKey(kvp.Key) ? observed[kvp.Key] : 0;
            double expectedCount = totalObserved * kvp.Value;

            chiSquare += Math.Pow(observedCount - expectedCount, 2) / expectedCount;
        }

        return chiSquare;
    }
}
