import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
import pandas as pd

def summarizer(rawdocs, summary_len):
    stopwords = list(STOP_WORDS)
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(rawdocs)
    tokens = [token.text for token in doc]
    word_freq = {}
    for word in doc:
        if word.text.lower() not in  stopwords and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text] = 1
            else:
                word_freq[word.text] += 1
    max_freq = max(word_freq.values())
    for word in word_freq.keys():
        word_freq[word] = word_freq[word] / max_freq  # Normalizing the word frequency
        sent_scores = {}
    sent_tokens = [sent for sent in doc.sents]
    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent] = word_freq[word.text]
                else:
                    sent_scores[sent] += word_freq[word.text]

    scores_df = dictToDf(sent_scores) # create a dataframe for scores
    
    
    summary = nlargest(len(sent_tokens), sent_scores, key = sent_scores.get)
    
    final_summary = [word.text for word in summary]
    summary = ' '.join(final_summary)

    summary = spliceSummary(summary, summary_len)

    #print("length of words " , len(summary.split(' ')))
    return summary, doc, scores_df, len(rawdocs.split(' ')), len(summary.split(' '))

def dictToDf(dictionary):
    my_series = pd.Series(dictionary, name='Scores')

    # Reset the index to get a DataFrame
    df_from_series = my_series.reset_index()
    df_from_series.columns = ['Sentence', 'Scores']

    sentences = df_from_series.iloc[:, 0]
    # Here i have fixed the sentences as type str
    # because when the sentences was converted to dictionary
    # it was type series here i converted them back to format type string
    sentences = sentences.astype(str)
    scores = df_from_series.iloc[:, 1]
    df_combined = pd.concat([sentences, scores], axis=1)



    # Return Dataframe
    return df_combined
            
def spliceSummary(article, custom_len):

    #print(custom_len, "      ", len(article.split(' ')))
    len_article = int(len(article.split(' ')))
    #print(type(article))
    if custom_len > len_article:
        return "The Word count of the original article is " + str(len(article.split(' '))) + " please select lower word count"
    else:
        # Split the summary into words
        words = article.split(' ')
        # Take the first `custom_len` words
        spliced_summary = " ".join(words[:custom_len])
        #print("Length of spliced summary ", len(words))
        i = custom_len + 1
        while i < len(words):
            if words[i].endswith('.'):
                spliced_summary += ' ' + words[i]
                break
            else:
                spliced_summary += ' ' + words[i]
            i += 1
        #print("spliced summary: ", len(spliced_summary.split(' ')))
        return spliced_summary