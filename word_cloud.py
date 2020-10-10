# Python program to generate WordCloud
import re

import multidict
from wordcloud import WordCloud, STOPWORDS


def print_image(wordcloud: WordCloud, book_file_name, stopwords_flag=0):
    # just for naming
    if stopwords_flag:
        name = "word_cloud_with_stopwords_removed_" + book_file_name
    else:
        name = "word_cloud_without_stopwords_removed_" + book_file_name

    # actual code to output
    wordcloud.to_file(name + '.png')


def getFrequencyDictForText(sentence, stopwords_flag):
    fullTermsDict = multidict.MultiDict()
    tmpDict = {}

    # making dict for counting frequencies
    for text in sentence.split(" "):
        if stopwords_flag and re.match("a|the|an|the|to|in|for|of|or|by|with|is|on|that|be", text):
            continue
        val = tmpDict.get(text, 0)
        tmpDict[text.lower()] = val + 1
    for key in tmpDict:
        fullTermsDict.add(key, tmpDict[key])

    return fullTermsDict


def start(words, book_file_name, stopwords_flag=0):
    # if we want to generate with stopwords removed, then stopwords_flag=1 and this is executed
    if stopwords_flag:
        my_stopwords = set(STOPWORDS)
        # my_stopwords = set(stopwords.words('english'))

        wordcloud = WordCloud(width=1920, height=1080,
                              background_color='white',
                              stopwords=my_stopwords).generate_from_frequencies(
            getFrequencyDictForText(words, stopwords_flag))

    # else for stopwords_flag=0 this is executed
    else:
        wordcloud = WordCloud(width=1920, height=1080,
                              background_color='white').generate_from_frequencies(
            getFrequencyDictForText(words, stopwords_flag))

    # print output to image
    print_image(wordcloud, book_file_name, stopwords_flag=stopwords_flag)
