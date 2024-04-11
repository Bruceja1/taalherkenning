# Dataset: https://www.kaggle.com/datasets/basilb2s/language-detection
# Engels, Malayalam, Hindi, Tamil, Kannada, Frans, Spaans, Portugees, Italiaans, Russisch, Zweeds, Nederlands,
# Arabisch, Turks, Duits, Deens, Grieks
import pandas as pd

df=pd.read_csv('languages.csv', sep=',')

# Dataset aanpassen zodat woorden als "hallo" en "hallo!" niet als twee verschillende woorden worden beschouwd.
df['Text'] = df['Text'].str.lower()
symbols = [",", ".", "?", "(", ")", '"', "'", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
for s in symbols:
    df['Text']=df['Text'].str.replace(s,'')
print(df.head(100))
#print(df.tail())
#print(list(df.columns))
#print(df.info)
