from flask import Flask,render_template,url_for,request
import re
import string
import sys
import os
import json
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import model_from_json

sys.path.append(os.path.abspath('./model'))


app = Flask(__name__)

def remove_stopwords(message):
    '''
    This functions removes the stopwords
    '''
    new_string = []

    stop = [ "a", "about", "above", "after", "again", "against", "all",
            "am", "an", "and", "any", "are", "as", "at", "be", "because", "been",
            "before", "being", "below", "between", "both", "but", "by", "could", "did", "do",
            "does", "doing", "down", "during", "each", "few", "for", "from", "further", "had",
            "has", "have", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's",
            "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll",
            "i'm", "i've", "if", "in", "into", "is", "it", "it's", "its", "itself", "let's", 
            "me", "more", "most", "my", "myself", "nor", "of", "on", "once", "only", "or",
            "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "she", 
            "she'd", "she'll", "she's", "should", "so", "some", "such", "than", "that", "that's",
            "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these",
            "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", 
            "too", "under", "until", "up", "very", "was", "we", "we'd", "we'll", "we're", 
            "we've", "were", "what", "what's", "when", "when's", "where", "where's", "which", 
            "while", "who", "who's", "whom", "why", "why's", "with", "would", "you", 
            "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves" ]

    for mes in message.split():
        if mes not in stop:
            new_string.append(mes)
    mes = (" ").join(new_string)

    return mes

def clean_text(text):
    text = text.lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)
    return text
def remove_emoji(text):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

def token_loader():
    with open('./model/tokenizer.json') as f:
        data = json.load(f)
        token = tf.keras.preprocessing.text.tokenizer_from_json(data)
        return token

tokenizer = token_loader()

def tokener(tokenizer, message):
    seq_text = tokenizer.texts_to_sequences(message)
    pad_text = pad_sequences(seq_text, padding='post', maxlen=120)
    return pad_text

def init():
    json_file = open('./model/model_glove_LSTM_200.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights('./model/model_glove_LSTM_200.h5')
    print('loaded model from disk')
    loaded_model.compile(loss='binary_crossentropy',optimizer='adam', metrics=['accuracy'])
    return loaded_model

model = init()


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict',methods=['POST'])
def predict():
    if request.method == 'POST':
        message = request.form['message']
        message = clean_text(message)
        message = remove_emoji(message)
        message = remove_stopwords(message)
        pad_mes = tokener(tokenizer, [message])
        pred = model.predict(pad_mes) > 0.5
        return render_template('result.html', prediction = pred)

if __name__ == '__main__':
    app.run()