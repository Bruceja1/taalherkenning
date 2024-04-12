# Dataset: https://www.kaggle.com/datasets/basilb2s/language-detection
# Engels, Malayalam, Hindi, Tamil, Kannada, Frans, Spaans, Portugees, Italiaans, Russisch, Zweeds, Nederlands,
# Arabisch, Turks, Duits, Deens, Grieks
import pandas as pd
from collections import defaultdict

df = pd.read_csv('languages.csv', sep = ',')

df['Text'] = df['Text'].str.lower()
df['Text'] = df['Text'].str.strip()

symbols = [",", ".", "?", "(", ")", '"', "'", "[", "]", ":", ";", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
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
    

trigram_frequencies = get_trigram_frequencies(df)
bigram_frequencies = get_bigram_frequencies(df)

print(bigram_frequencies['Dutch'])