using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

class Program
{
    static void Main(string[] args)
    {
        string inputFile = "", outputFile = "", keyFile = "";
        string gramFile = "";
        bool encrypt = false, decrypt = false;
        int nGram = 0;

        for (int i = 0; i < args.Length; i++)
        {
            switch (args[i])
            {
                case "-i": inputFile = args[++i]; break;
                case "-o": outputFile = args[++i]; break;
                case "-k": keyFile = args[++i]; break;
                case "-e": encrypt = true; break;
                case "-d": decrypt = true; break;
                case "-g1":
                case "-g2":
                case "-g3":
                case "-g4":
                    nGram = int.Parse(args[i].Substring(2, 1));
                    gramFile = args[++i];
                    break;
            }
        }

        if ((encrypt == decrypt) && nGram == 0 || string.IsNullOrEmpty(inputFile))
        {
            Console.WriteLine("Użycie: program -e|-d -k klucz.txt -i wejscie.txt -o wyjscie.txt [-g1|-g2|-g3|-g4 gram.txt]");
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
}
