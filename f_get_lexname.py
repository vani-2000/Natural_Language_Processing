from nltk.corpus import wordnet as wn
import matplotlib.pyplot as plt


def plot_histogram(book_file_name, freq_dist, name):
    """
    function:   Plot the histogram of frequency of each category for noun (and verb).

    Input:      A string:   "book_file_name" which is name of the book as stored on Hard disk.
                A dict:     "freq_dist"
                A string:   "name", which has value 'noun' or 'verbs'

    Returns:    Nothing, it plots the histogram and saves it on disk.
    """

    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    ax.bar(freq_dist.keys(), freq_dist.values(), width=1, edgecolor='black', color='cyan')

    plt.xticks(rotation=90)  # ratate X-axis text by 90 degree
    plt.savefig('f_lexname_Histogram_' + name + '_' + book_file_name + '.png', bbox_inches="tight")


def get_freq_dist(dict_of_noun_lexname, dict_of_verb_lexname, book_file_name):
    """
    function:   Get freq dist and Plot the histogram of frequency of each category for noun (and verb).

    Input:      dict_of_noun_lexname: a dictionary of nouns and their corresponding lexame
                dict_of_verb_lexname: a dictionary of verbs and their corresponding lexame
                A string:   "book_file_name" which is name of the book as stored on Hard disk.

    Returns:    Nothing, it gets freq dist and plots the histogram and saves it on disk.
    """

    # first making a freq dist of each dict
    freq_dist_nouns = {}
    freq_dist_verbs = {}

    for x in dict_of_noun_lexname:
        if dict_of_noun_lexname[x] not in freq_dist_nouns:
            freq_dist_nouns[dict_of_noun_lexname[x]] = 1
        else:
            freq_dist_nouns[dict_of_noun_lexname[x]] += 1

    for x in dict_of_verb_lexname:
        if dict_of_verb_lexname[x] not in freq_dist_verbs:
            freq_dist_verbs[dict_of_verb_lexname[x]] = 1
        else:
            freq_dist_verbs[dict_of_verb_lexname[x]] += 1

    # writing types of nouns (lexnames) and their frequency to file
    lexname_file_noun = open("f_freq_dist_of_lexname_noun_" + book_file_name + "_.txt", 'w+')

    lexname_file_noun.write("Here are the types of nouns (lexnames) and their frequency for " + book_file_name + "\n\n")
    lexname_file_noun.write("Lexname: \t Frequency\n\n")
    for x in freq_dist_nouns:
        lexname_file_noun.write(str(x) + " : \t\t" + str(freq_dist_nouns[x]) + '\n')

    # writing types of verbs (lexnames) and their frequency to file
    lexname_file_verb = open("f_freq_dist_of_lexname_verb_" + book_file_name + "_.txt", 'w+')
    lexname_file_verb.write("Here are the types of Verbs (lexnames) and their frequency for " + book_file_name + "\n\n")
    lexname_file_verb.write("Lexname: \t Frequency\n\n")
    for x in freq_dist_verbs:
        lexname_file_verb.write(str(x) + ": \t\t" + str(freq_dist_verbs[x]) + '\n')

    # plotting the histogram for nouns
    plot_histogram(book_file_name, freq_dist_nouns, 'nouns')

    # plotting the histogram for verbs
    plot_histogram(book_file_name, freq_dist_verbs, 'verbs')


def get_nouns_verbs_lexname(tags, book_file_name):
    """
    function:   get list of nouns and verbs, find their categories (lexnames) and plot histogram

    Input:      A list: "tags", which contains a tuple as its elements. Each tuple is a word along with its tag.
                A string:   "book_file_name" which is name of the book as stored on Hard disk.

    Returns:    set_of_nouns: a set of unique nouns in the book
                set_of_verbs: a set of unique verbs in the book
                dict_of_noun_lexname: a dictionary of nouns and their corresponding lexame
                dict_of_verb_lexname: a dictionary of verbs and their corresponding lexame
    """

    """
    The 25 categories of nouns are the 25 lexnames in nltk.
    Similarly for verbs, the 16 categories are the 16 lexnames in nltk.
    
    Since each word can have multiple meanings, the nltk will return all those meanings in a list
    and we will pass the Pos tag of that word and then chose the first meaning of that word in the list. Why?
    
    We choose the most frequent sense for each word from the senses in a labeled corpus.
    This corresponds to the take the first sense heuristic, 
    since senses in WordNet are generally ordered from most-frequent to least-frequent
    
    Note: We will be passing the pos tag for the word to nltk to help in finding lexname.
          This will be useful in case like when "book" is used both as verb and as a noun. 
    """

    # if the 2nd place in tuple has "NN" in it, then the first place of that tuple is a Noun, similarly for verb.
    # We will be making a set of these words instead of a list so no duplicate words are stored.
    set_of_nouns = {
        str(x[0]).lower()
        for x in tags
        if "NN" in x[1]
    }
    set_of_verbs = {
        str(x[0]).lower()
        for x in tags
        if "VB" in x[1]
    }

    # These are two dictionaries, one for verb and one for noun, that will store the lexname of each word
    # along with the word. The words will be taken from above lists for both noun and verbs respectively.
    dict_of_noun_lexname = {}
    dict_of_verb_lexname = {}

    for noun in set_of_nouns:
        try:
            syn = wn.synsets(noun, pos=wn.NOUN)[0]  # The "pos=wn.NOUN" flag makes sure to select the first noun lexname
            x, y = str(syn.lexname()).split('.')
            dict_of_noun_lexname[noun] = y  # add that lexname to the dict along with the word
        except IndexError:
            continue

    for verb in set_of_verbs:
        try:
            syn = wn.synsets(verb, pos=wn.VERB)[0]  # The "pos=wn.VERB" flag makes sure to select the first verb lexname
            x, y = str(syn.lexname()).split('.')
            dict_of_verb_lexname[verb] = y  # add that lexname to the dict along with the word
        except IndexError:
            continue

    # plot the histogram
    get_freq_dist(dict_of_noun_lexname, dict_of_verb_lexname, book_file_name)

    return set_of_nouns, set_of_verbs, dict_of_noun_lexname, dict_of_verb_lexname
