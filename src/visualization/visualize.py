import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from os import path
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

def proportion(tweet_data):
    '''
    Plots the proportion of the data
    '''
    plt.figure(figsize=(8,4))
    plt.title('real vs not real')
    sns.countplot(x="target", data=tweet_data)
    plt.savefig('../reports/figures/real_vs_not_real.png')

def word_count(tweet_data):
    '''
    Shows the distributions of the word count
    '''
    fig, (ax1, ax2) = plt.subplots(1,2, figsize=(10,5))
    tweet_len = tweet_data[tweet_data['target'] == 1]['text'].str.split().map(lambda x: len(x))
    ax1.hist(tweet_len, color='blue')
    ax1.set_title('Disaster Tweets')
    tweet_len = tweet_data[tweet_data['target'] == 0]['text'].str.split().map(lambda x: len(x))
    ax2.hist(tweet_len, color='red')
    ax2.set_title('Not Disaster Tweets')
    fig.suptitle('Words in a tweet')
    plt.savefig('../reports/figures/word_count.png') 

def avg_word_length(tweet_data):
    '''
    Plots the distribution of avg word lenght
    '''
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10,5))
    word=tweet_data[tweet_data['target']==1]['text'].str.split().apply(lambda x : [len(i) for i in x])
    sns.distplot(word.map(lambda x: np.mean(x)),ax=ax1,color='blue')
    ax1.set_title('Disaster')
    word=tweet_data[tweet_data['target']==0]['text'].str.split().apply(lambda x : [len(i) for i in x])
    sns.distplot(word.map(lambda x: np.mean(x)),ax=ax2,color='red')
    ax2.set_title('Not disaster')
    fig.suptitle('Average word length in each tweet')
    plt.savefig('../reports/figures/avg_word_length.png')

def word_cloud(tweet_data):
    '''
    Create the word cloud
    '''
    stopwords = set(STOPWORDS)
    stopwords.update(["CO", "co", "https", "NAN"])
    
    plt.title('Disaster')
    text_disaster = " ".join(text for text in tweet_data[tweet_data['target'] == 1]['text'])
    wordcloud = WordCloud(stopwords=stopwords, background_color="black").generate(text_disaster)
    plt.imshow(wordcloud, interpolation='bilinear',)
    plt.show()
    plt.savefig('../reports/figures/disaster.png')
    
    plt.title('Non Disaster')
    text_normal = " ".join(text for text in tweet_data[tweet_data['target'] == 0]['text'])
    wordcloud = WordCloud(stopwords=stopwords, background_color="white").generate(text_normal)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.savefig('../reports/figures/non_disaster.png')
    plt.show()
    
    plt.title("Keyword disaster")
    keyword_disaster = " ".join(text for text in tweet_data[tweet_data['target'] == 1]['keyword'])
    wordcloud = WordCloud(stopwords=stopwords, background_color="black").generate(keyword_disaster)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.savefig('../reports/figures/keyword_disaster.png')
    plt.show()
    
    plt.title("Keyword nondisaster")
    keyword_nondisaster = " ".join(text for text in tweet_data[tweet_data['target'] == 0]['keyword'])
    wordcloud = WordCloud(stopwords=stopwords, background_color="white").generate(keyword_nondisaster)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.savefig('../reports/figures/keyword_nondisaster.png')
    plt.show()