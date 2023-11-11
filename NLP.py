from bs4 import BeautifulSoup #pip install beautifulsoup4  pip install lxml

import re

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
        
import py3langid as langid #pip install py3langid

import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context


nltk.download('stopwords')
nltk.download('punkt')
        

# Überschrift erzeugen
def Überschift_erzeugen(Text):
    
    # Entfernen der HTML-Tags
    Text = Text.replace('<p>', '')
    Text = Text.replace('</p>', '\n')
    Text = Text.replace('<br>', '')
    Text = Text.replace('</br>', '\n')
    Text = Text.replace('<br />', '\n')
    Text = Text.replace('<div>', '')
    Text = Text.replace('</div>', '\n')
    Text = Text.replace('<div/>', '\n')
    Text = Text.replace('<h1/>', '\n')
    Text = Text.replace('<h2/>', '\n')
    Text = Text.replace('<h3/>', '\n')
    Text = Text.replace('<h4/>', '\n')
    Text = Text.replace('<h5/>', '\n')
    Text = Text.replace('<h6/>', '\n')
    Text = Text.replace('</h1>', '\n')
    
    Text = Text.replace('<h1>', '')
    Text = Text.replace('<h2>', '')
    Text = Text.replace('<h3>', '')
    Text = Text.replace('<h4>', '')
    Text = Text.replace('<h5>', '')
    Text = Text.replace('<h6>', '')
    Text = Text.replace('</h>', '')
    
    
    # Spliten beim Zeilenumruch
    Text = Text.split('\n')[0]    
    
    # Leerzeichen entfernen
    Text = Text.strip()
    
    Text = BeautifulSoup(Text, "lxml").text
    
    return Text



# Sprachcode übersetzen
def langid_to_nltk_name(langid_code):
    # Wörterbuch zur Übersetzung von ISO 639-1 Sprachcodes zu den entsprechenden NLTK-Namen
    langid_to_nltk = {
        'af': 'afrikaans', 'am': 'amharic', 'an': 'aragonese', 'ar': 'arabic', 'as': 'assamese',
        'az': 'azerbaijani', 'be': 'belarusian', 'bg': 'bulgarian', 'bn': 'bengali', 'br': 'breton',
        'bs': 'bosnian', 'ca': 'catalan', 'cs': 'czech', 'cy': 'welsh', 'da': 'danish', 'de': 'german',
        'dz': 'dzongkha', 'el': 'greek', 'en': 'english', 'eo': 'esperanto', 'es': 'spanish',
        'et': 'estonian', 'eu': 'basque', 'fa': 'persian', 'fi': 'finnish', 'fo': 'faroese',
        'fr': 'french', 'ga': 'irish', 'gl': 'galician', 'gu': 'gujarati', 'he': 'hebrew',
        'hi': 'hindi', 'hr': 'croatian', 'ht': 'haitian', 'hu': 'hungarian', 'hy': 'armenian',
        'id': 'indonesian', 'is': 'icelandic', 'it': 'italian', 'ja': 'japanese', 'jv': 'javanese',
        'ka': 'georgian', 'kk': 'kazakh', 'km': 'khmer', 'kn': 'kannada', 'ko': 'korean', 'ku': 'kurdish',
        'ky': 'kyrgyz', 'la': 'latin', 'lb': 'luxembourgish', 'lo': 'lao', 'lt': 'lithuanian',
        'lv': 'latvian', 'mg': 'malagasy', 'mk': 'macedonian', 'ml': 'malayalam', 'mn': 'mongolian',
        'mr': 'marathi', 'ms': 'malay', 'mt': 'maltese', 'nb': 'norwegian', 'ne': 'nepali',
        'nl': 'dutch', 'nn': 'norwegian_nynorsk', 'no': 'norwegian', 'oc': 'occitan', 'or': 'oriya',
        'pa': 'punjabi', 'pl': 'polish', 'ps': 'pashto', 'pt': 'portuguese', 'qu': 'quechua',
        'ro': 'romanian', 'ru': 'russian', 'rw': 'kinyarwanda', 'se': 'northern_sami', 'si': 'sinhalese',
        'sk': 'slovak', 'sl': 'slovenian', 'sq': 'albanian', 'sr': 'serbian', 'sv': 'swedish',
        'sw': 'swahili', 'ta': 'tamil', 'te': 'telugu', 'th': 'thai', 'tl': 'tagalog', 'tr': 'turkish',
        'ug': 'uyghur', 'uk': 'ukrainian', 'ur': 'urdu', 'vi': 'vietnamese', 'vo': 'volapuk',
        'wa': 'walloon', 'xh': 'xhosa', 'zh': 'chinese', 'zu': 'zulu'
    }

    return langid_to_nltk.get(langid_code, 'unknown')



# NLP Auswertung
def Umwandeln(Text):
    
    # Entfernen der HTML-Tags aus dem Text
    cleantext = BeautifulSoup(Text, "lxml").text
    
    # Text in Sätze aufteilen
    sentences = nltk.sent_tokenize(cleantext)
    
    Sätze_Ausgabe = ""
    for sentence in sentences:
        
        # Sprache erkennen
        lang, _ = langid.classify(sentence)
        
        # von kurzer Sprache in die lange bersion
        nltk_name = langid_to_nltk_name(lang)

        #Stopp Wörter entfernen
        try:
            stop_words = set(stopwords.words(nltk_name))
        except:
            print ("Sprache nicht erkannt")
            stop_words = set(stopwords.words('german'))
            nltk_name="german"
        
        # Tokenisiere den Text
        word_tokens = word_tokenize(sentence)
        
        # Erstelle eine Liste der Wörter, die keine Stoppwörter sind
        filtered_words = [word for word in word_tokens if word.lower() not in stop_words]

        # Erstelle einen neuen Text aus den gefilterten Wörtern
        filtered_text = " ".join(filtered_words)
        
        # Sonderzeichen usw. entfernen mit re
        filtered_text = re.sub(r'[^\w\s]', '', filtered_text)
        
        # doppelte Leerzeichen entfernen
        filtered_text = re.sub(' +', ' ', filtered_text)
        
        # Zahlen entfern
        filtered_text = re.sub(r'\d+', '', filtered_text)
        
        
        # Wörter auf die Grundform zurückführen
        stemmer = SnowballStemmer(nltk_name)
        for Wort in filtered_text.split(" "):
            filtered_text = filtered_text.replace(Wort,stemmer.stem(Wort))
        
        
        # Stop wörter entfernen
        for Wort in filtered_text.split(" "):
            if Wort in stop_words:
                filtered_text = filtered_text.replace(Wort,"")
                
                
        # Alles klein schreiben
        filtered_text = filtered_text.lower()
        
        Sätze_Ausgabe=Sätze_Ausgabe+filtered_text+" "
        
    
    return Sätze_Ausgabe.replace("  "," ").strip()


    
    
