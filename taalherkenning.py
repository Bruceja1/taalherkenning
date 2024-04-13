# Dataset: https://www.kaggle.com/datasets/basilb2s/language-detection
# Engels, Malayalam, Hindi, Tamil, Kannada, Frans, Spaans, Portugees, Italiaans, Russisch, Zweeds, Nederlands,
# Arabisch, Turks, Duits, Deens, Grieks
import numpy as np
import pandas as pd
import re
from collections import defaultdict

df = pd.read_csv('languages.csv', sep = ',')

df['Text'] = df['Text'].str.lower()
df['Text'] = df['Text'].str.strip()

symbols = ["!",",", ".", "?", "(", ")", '"', "'", "[", "]", ":", ";", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
for s in symbols:
    df['Text'] = df['Text'].str.replace(s,'')
print(df.head(100))
#print(df.tail())
#print(list(df.columns))
#print(df.info)

def get_trigram_frequencies(df):
    trigram_frequencies = defaultdict(lambda: defaultdict(int))

    trigram_counts = defaultdict(lambda: defaultdict(int))

    for index, row in df.iterrows():
        text = row['Text']
        language = row['Language']

        for i in range(len(text) - 2):
            trigram = text[i:i + 3]
            trigram_counts[language][trigram] += 1
    
    for language, counts in trigram_counts.items():
        total_trigrams = sum(counts.values())
        for trigram, count in counts.items():
            trigram_frequencies[language][trigram] = count / total_trigrams

    return trigram_frequencies

def get_bigram_frequencies(df):
    bigram_frequencies = defaultdict(lambda: defaultdict(int))

    bigram_counts = defaultdict(lambda: defaultdict(int))

    for index, row in df.iterrows():
        text = row['Text']
        language = row['Language']

        for i in range(len(text) - 1):
            bigram = text[i:i + 2]
            bigram_counts[language][bigram] += 1
    
    for language, counts in bigram_counts.items():
        total_bigrams = sum(counts.values())
        for bigram, count in counts.items():
            bigram_frequencies[language][bigram] = count / total_bigrams

    return bigram_frequencies

def get_language_probabilities(userInput):
    inputTrigrams = []
    for i in range(len(userInput) - 2):
        trigram = userInput[i:i + 3]
        inputTrigrams.append(trigram)
    print(f"De trigrammen van de input zijn: {inputTrigrams}")

    inputBigrams = [] 
    for i in range(1, len(userInput) - 2): # Alleen de 'tussen' bigrammen worden opgeslagen
        bigram = userInput[i:i + 2]
        inputBigrams.append(bigram)
    print(f"De 'tussen' bigrammen van de input zijn: {inputBigrams}")

    
    for language in trigram_frequencies.keys():
        matching_trigram_frequencies = []
        for trigram in inputTrigrams:
            if trigram in trigram_frequencies[language].keys():
                matching_trigram_frequencies.append(trigram_frequencies[language][trigram])
            else:
                matching_trigram_frequencies.append(0) # Smoothing wordt later toegepast
        matching_bigram_frequencies = []
        for bigram in inputBigrams:
            if bigram in bigram_frequencies[language].keys():
                matching_bigram_frequencies.append(bigram_frequencies[language][trigram])
            else:
                matching_bigram_frequencies.append(0) # Ook hier wordt later smoothing toegepast
        print(f"De taal is {language} met de volgende matching trigram frequencies: {matching_trigram_frequencies}")

        # Smoothing: als het trigram (of bigram) niet voorkomt, deze toch een kleine kans toekennen. 
        # De kansen van de trigrammen (en bigrammen) die wél voorkomen worden dan verlaagd met hetzelfde aantal. 
        for frequency in range(len(matching_trigram_frequencies)):
            if matching_trigram_frequencies[frequency] == 0:
                matching_trigram_frequencies[frequency] += 0.00001
            else:
                matching_trigram_frequencies[frequency] -= 0.00001
        print(f"De taal is {language} met de volgende matching trigram frequencies: {matching_trigram_frequencies}")
        for frequency in range(len(matching_bigram_frequencies)):
            if matching_bigram_frequencies[frequency] == 0:
                matching_bigram_frequencies[frequency] += 0.000001
            else:
                matching_bigram_frequencies[frequency] -= 0.000001

        # De formule van het trigram pdf document toepassen
        """ product_trigram_frequencies = np.prod(matching_trigram_frequencies)
        product_bigram_frequencies = np.prod(matching_bigram_frequencies)

        if product_trigram_frequencies == 0:
            product_trigram_frequencies = 0.0000000001
        if product_bigram_frequencies == 0:
            product_bigram_frequencies = 9999999999

        probability = (product_trigram_frequencies) / (product_bigram_frequencies)  """
        
        probability = (np.prod(matching_trigram_frequencies)) / (np.prod(matching_bigram_frequencies)) 
        language_probabilities[language] = probability
    
    return language_probabilities

trigram_frequencies = get_trigram_frequencies(df)
bigram_frequencies = get_bigram_frequencies(df)

""" for language in bigram_frequencies.keys():
    print(f"Taal: {language} heeft als som: {sum(bigram_frequencies[language].values())}") """
languages = []
for language in trigram_frequencies.keys():
    languages.append(language)
while True:
    print(f"De volgende talen zijn toegestaan: {languages}")
    userInput = input("Geef een voorbeeldzin in een van de bovenstaande talen... \n")
    m = re.compile(r'[a-zA-Z0-9().?! ]')
    if (m.match(userInput)):
        break
    else:
        print("De invoer mag alleen de volgende tekens bevatten: 'a-zA-Z0-9().?!'")

for s in symbols:
    userInput = userInput.replace(s, '')
userInput = userInput.lower()
userInput = userInput.strip()
print(f"De nieuwe input is: {userInput}")

language_probabilities = defaultdict(int)
get_language_probabilities(userInput)

for language in language_probabilities:
    print(f"De 'kans' op {language} is {language_probabilities[language]}")

print(f"De taal van de invoerzin is: {max(language_probabilities, key=language_probabilities.get)}")