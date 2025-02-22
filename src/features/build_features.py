import pandas as pd
import numpy as np
import io
import json
import re
import string

def remove_stopwords(tweet_data_text):
    '''
    This functions removes the stopwords
    '''
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
    tweet_data_text = tweet_data_text.apply(lambda text: [item for item in text.split() if item not in stop])
    tweet_data_text = tweet_data_text.apply(lambda text: (" ").join(text))
    return tweet_data_text

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

def save_tokenizer(text_tokenizer):
    '''
    This function saves the tokenizer for 
    later purposes
    '''
    tokenizer_json = text_tokenizer.to_json()
    with io.open('../src/models/tokenizer.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(tokenizer_json, ensure_ascii=False))

def train_val_split(tweet_data, labels, split_size=0.8):
    '''
    Splits the data into train and val
    '''
    split = int(len(tweet_data) * split_size)
    train_text = tweet_data[:split]
    train_labels = labels[:split]
    
    val_text = tweet_data[split:]
    val_labels = labels[split:]
    return (train_text, train_labels), (val_text, val_labels)