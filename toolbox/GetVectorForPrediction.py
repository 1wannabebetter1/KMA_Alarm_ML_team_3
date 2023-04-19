import os
import datetime
import pandas as pd
from bs4 import BeautifulSoup
from toolbox import scrapper as scr
from toolbox import TextLematizer as tl
from toolbox import TextVectorizer as tv
import pickle

MODEL_FOLDER = "data/model"
tfidf_transformer_model = "tfidf_transformer"
count_vectorizer_model = "count_vectorizer"
tfidf_transformer_version = "v1"
count_vectorizer_version = "v1"
vector_folder = 'predictioninfo/vector/'
html_folder = 'predictioninfo/html/'

def GetVector(date):
    if(os.path.isfile(vector_folder+date+'.csv')):
        readyVector = pd.read_csv(vector_folder+date+'.csv', sep=";")
        return readyVector
    else:
        return TryGenerateVector(date);
def TryGenerateVector(date):
    scr.savePage(date, html_folder)
    previousDate = datetime.datetime.strptime(date, '%Y-%m-%d') - datetime.timedelta(days=1)
    fileName = html_folder + date + '.html'
    if(os.path.isfile(fileName)==False):
        return GetVector(previousDate.strftime('%Y-%m-%d'))
    df = generateBaseDF(date)
    df['lemm'] = df['main_html'].apply(lambda x: tl.prepareLemm(x))
    tfidf_df = transformToVector(df)
    tfidf_df.to_csv(vector_folder+date+'.csv', sep=";", index=False)
    return tfidf_df

def generateBaseDF(date):
    html_name = html_folder + date + '.html'
    text = ""
    all_isw = []
    d = {}
    file_name = html_name.split('\\')[-1]
    with open(html_name, "r", encoding="UTF-8") as cfile:
        parsed_html = BeautifulSoup(cfile.read(), "html.parser")
        text_main = parsed_html.find('div', attrs={
            'class': 'field field-name-body field-type-text-with-summary field-label-hidden'}).text
        text = text_main
        d = {
            "date": date,
            "main_html": text_main,
        }
        all_isw.append(d)
    return pd.DataFrame.from_dict(all_isw)
def transformToVector(df):
    tfidf = pickle.load(open(f"{MODEL_FOLDER}/{tfidf_transformer_model}_{tfidf_transformer_version}.pkl", "rb"))
    cv = pickle.load(open(f"{MODEL_FOLDER}/{count_vectorizer_model}_{count_vectorizer_version}.pkl", "rb"))
    df['keywords'] = df['lemm'].apply(lambda x: tv.conver_doc_to_vector(x, cv, tfidf))
    word_vector = cv.transform([df.iloc[0]["lemm"]])
    tfidf_vector = tfidf.transform(word_vector)
    tfidf_df = pd.DataFrame(tfidf_vector.todense())
    return tfidf_df


#print(GetVector('2023-04-20').shape)
