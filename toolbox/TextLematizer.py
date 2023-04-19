from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from num2words import num2words
import numpy as np
import re
def remove_names_and_date(page_html_text):
    if(page_html_text.find("This map is updated daily alongside the static maps present in this report")!=-1):
        return page_html_text[page_html_text.find('This map is updated daily alongside the static maps present in this report')+len("This map is updated daily alongside the static maps present in this report"):]
    if(page_html_text.find("EST\n")!=-1):
        return page_html_text[page_html_text.find('EST\n')+len("EST\n"):]
    elif(page_html_text.find("EST\xa0")!=-1):
        return page_html_text[page_html_text.find('EST\xa0')+len("EST\xa0"):]
    elif(page_html_text.find("ET\n")!=-1):
        return page_html_text[page_html_text.find('ET\n')+len("ET\n"):]
    else:
        return page_html_text[page_html_text.find('ET\xa0')+len("ET\xa0"):]

def removeGarbage(text):
    pattern = "\[\d+\]"
    res = re.sub(pattern, "", text)
    res = re.sub(r'http(\S+.*\s)', "", res)
    res = re.sub(r' (©2022|©2023|2022|2023)', "", res)
    res = re.sub('\n', "", res)
    res = re.sub('\xa0', "", res)
    return res
def remove_one_letter_word(data):
    words = word_tokenize(str(data))
    new_text = ""
    for w in words:
        if len(w) > 1:
            new_text = new_text + " " + w
    return new_text
def convert_lower_case(data):
    return np.char.lower(data)
def remove_stop_words(data):
    stop_words = set(stopwords.words('english'))
    stop_stop_words = {"no", "not"}
    stop_words = stop_words - stop_stop_words

    words = word_tokenize(str(data))

    new_text = ""
    for w in words:
        if w not in stop_words and len(w) > 1:
            new_text = new_text + " " + w
    return new_text
def remove_punctuation(data):
    symbols = "!\"#$%&()*+—./:;<=>?@[\]^_`{|}~\n"
    for i in range(len(symbols)):
        data = np.char.replace(data, symbols[i], ' ')
        data = np.char.replace(data, "  ", " ")
        data = np.char.replace(data, ', ', ' ')
    return data
def remove_apostrophe(data):
    return np.char.replace(data, "'", "")
def stemming(data):
    stemmer= PorterStemmer()

    tokens = word_tokenize(str(data))
    new_text = ""
    for w in tokens:
        new_text = new_text + " " + stemmer.stem(w)
    return new_text
def lemmatizing(data):
    lemmatizer = WordNetLemmatizer()

    tokens = word_tokenize(str(data))
    new_text = ""
    for w in tokens:
        new_text = new_text + " " + lemmatizer.lemmatize(w)
    return new_text
def convert_numbers(data):
    tokens = word_tokenize(str(data))
    new_text = ""
    for w in tokens:
        if w.isdigit():
            if int(w)<100000000000:
                w = num2words(w)
            else:
                w = ' '
        new_text = new_text + " " + w
    new_text = np.char.replace(new_text, "−", " ")

    return new_text
def remove_url_string(data):
    words = word_tokenize(str(data))

    new_text = ""
    for w in words:
        w = re.sub(r'^https?:\/\/.*[\r\n]*', '', str(w), flags=re.MULTILINE)
        w = re.sub(r'^http?:\/\/.*[\r\n]*', '', str(w), flags=re.MULTILINE)

        new_text = new_text + " " + w

    return new_text
def preprocess(data, word_root_algo="lemm"):
    data = remove_one_letter_word(data)
    data = remove_url_string(data)
    data = convert_lower_case(data) # remove comma seperately
    data = remove_apostrophe(data)
    data = remove_stop_words(data)
    data = convert_numbers(data)
    data = stemming(data)
    data = remove_punctuation(data)
    data = convert_numbers(data)
    if word_root_algo == "lemm":
        data = lemmatizing(data)
    else:
        data = stemming(data)
    data = remove_punctuation(data)
    data = remove_stop_words(data)
    return data

def prepareLemm(text):
    res = remove_names_and_date(text)
    res = removeGarbage(res)
    res = preprocess(res, "lemm")
    return res