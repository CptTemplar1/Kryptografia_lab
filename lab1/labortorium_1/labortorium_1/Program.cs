using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

class Program
{
    static void Main(string[] args)
    {
        string inputFile = "", outputFile = "", keyFile = "";
        bool encrypt = false, decrypt = false;

        for (int i = 0; i < args.Length; i++)
        {
            switch (args[i])
            {
                case "-i": inputFile = args[++i]; break;
                case "-o": outputFile = args[++i]; break;
                case "-k": keyFile = args[++i]; break;
                case "-e": encrypt = true; break;
                case "-d": decrypt = true; break;
            }
        }

        if ((encrypt == decrypt) || string.IsNullOrEmpty(inputFile) || string.IsNullOrEmpty(outputFile) || string.IsNullOrEmpty(keyFile))
        {
            Console.WriteLine("Użycie: program -e|-d -k klucz.txt -i wejscie.txt -o wyjscie.txt");
            return;
        }

        var substitution = LoadKey(keyFile, decrypt);

        string inputText = File.ReadAllText(inputFile);
        string outputText = ProcessText(inputText, substitution);

        File.WriteAllText(outputFile, outputText);

        Console.WriteLine("Operacja zakończona pomyślnie.");
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
        return new string(text.ToUpper().Where(char.IsLetter)
            .Select(ch => substitution.ContainsKey(ch) ? substitution[ch] : ch)
            .ToArray());
    }
}
