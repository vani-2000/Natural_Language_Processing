""""
This is The NLP Python project for team: The Spartans
Team Memebers:  Hritwik
                Vani
                Sameer
"""
import os

from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

from Base_Modules import d_relation_word_len_freq, f_get_lexname, e_pos_tag, b_freq_dist_tokens, g_get_entity_labels, \
    h_get_entity_relations, a_pre_process, c_word_cloud

lemmatizer = WordNetLemmatizer()


def import_book(book_file_name: str):
    """
    function:   to import book file and return the lines as list.

    Input:      A string: which contains the path to the book.

    Returns:    A List: which contain the lines of book as its elements.
    """

    """
    "sig" in "utf-8-sig" is the abbreviation of "signature" (i.e. signature utf-8 file).
    Using utf-8-sig to read a file will treat BOM as file info. instead of a string
    from https://stackoverflow.com/questions/57152985/what-is-the-difference-between-utf-8-and-utf-8-sig
    """
    with open(book_file_name, 'r+', encoding='utf-8-sig') as temp:
        book = [line.strip() for line in temp.readlines() if line.strip()]

    return book


def tokenize_and_lemmatization(book):
    """
    function:   tokenize the book, then lemmetize those tokens,
                then join those lemmas to a string which is stored as "new_book".

    Input:      A String which contain book.

    Returns:    A string called "new_book".
                A List called "lemmas".
    """

    # tokenize the book after lower-casing the sentences
    final_list = []
    word_tokens = word_tokenize(book.lower())
    final_list.extend(word_tokens)

    # Lemmatizing the tokens in final_list and storing them in "lemmas"
    lemmas = [lemmatizer.lemmatize(word)
              for word in final_list]

    # join the lemmas to form a book
    new_book = ' '.join(lemmas)

    # and return both the new book and lemmas
    return new_book, lemmas


def pre_processing_book(book: list):
    """
    function:   Process, generate tokens and do lemmatization.

    Input:      A List which contain the lines of book as its elements.

    Returns:    A string called "new_book".
                A List: "tokens" which contains lemmatized words.
    """

    # applying all pre-processing and storing result in a string
    new_book = a_pre_process.start(book)

    # lemmatizing and tokenize the book
    new_book, tokens = tokenize_and_lemmatization(new_book)

    return new_book, tokens


def analyze_freq_distribution_of_tokens(tokens, book_file_name):
    """
    function:   wrapper function for Analyzing the frequency distribution of tokens

    Input:      A List: "tokens" which contains lemmatized words.
                A string: "book_file_name" which is name of the book as stored on Hard disk.

    Returns:    Nothing
    """

    b_freq_dist_tokens.start(tokens, book_file_name)


def generate_word_cloud(words, book_file_name):
    """
    function:   Wrapper Function to generate word Clouds

    Input:      A string called "words" which contains the words of book.
                A string: "book_file_name" which is name of the book as stored on Hard disk.

    Returns:    Nothing
    """

    # without stopwords removal
    c_word_cloud.start(words, book_file_name, stopwords_flag=0)

    # with stopwords removal
    c_word_cloud.start(words, book_file_name, stopwords_flag=1)


def count_freq_of_each_token(tokens: list):
    """
    function:   Count freq of each token and store it in a Dict.

    Input:      A List: "tokens" which contains lemmatized words.

    Returns:    A dictionary: which contains the word as key and freq of each token as value.
    """

    freq = {}
    for word in tokens:
        freq[word] = freq.get(word, 0) + 1

    # return sorted dict by value
    return {k: v for k, v in sorted(freq.items(), key=lambda item: item[1], reverse=True)}


def get_relationship_between_the_word_length_and_frequency(tokens: list, book_file_name):
    """
    function:   To get relationship between the word length and frequency.

    Input:      A List:     "tokens" which contains lemmatized words.
                A string:   "book_file_name" which is name of the book as stored on Hard disk.

    Returns:    Nothing
    """

    # count freq of each token
    freq = count_freq_of_each_token(tokens)

    # get relationship
    d_relation_word_len_freq.start(freq, book_file_name)


def do_pos_tag_and_get_dist_tags(tokens: list, book_file_name):
    """
    function:   Wrapper function to do POS_tagging and Get the distribution of various tags.

    Input:      A List: "tokens" which contains lemmatized words.
                A string:   "book_file_name" which is name of the book as stored on Hard disk.

    Returns:    A list: "tags", which contains a tuple as its elements. Each tuple is a word along with its tag
    """

    tags = e_pos_tag.start(tokens, book_file_name)

    return tags


def get_categories(tags, book_file_name):
    """
    function:   Wrapper function to get categories of nouns and verbs

    Input:      A list:     "tags", which contains a tuple as its elements. Each tuple is a word along with its tag.
                A string:   "book_file_name" which is name of the book as stored on Hard disk.

    Returns:    set_of_nouns: a set of unique nouns in the book
                set_of_verbs: a set of unique verbs in the book
                dict_of_noun_lexname: a dictionary of nouns and their corresponding lexame
                dict_of_verb_lexname: a dictionary of verbs and their corresponding lexame
    """

    set_of_nouns, set_of_verbs, dict_of_noun_lexname, dict_of_verb_lexname = f_get_lexname.get_nouns_verbs_lexname(
        tags, book_file_name)

    return set_of_nouns, set_of_verbs, dict_of_noun_lexname, dict_of_verb_lexname


def recognize_entity(new_book, book_file_name):
    """
    function:   Wrapper function to recognise all entity Types in book.
                (1) First recognise all the entity and then
                (2) recognise all entity types.

    Input:      A string: "new_book" of the pre-processed book
                A string: "book_file_name" which is name of the book as stored on Hard disk.

    Returns:    Nothing
    """

    g_get_entity_labels.start(new_book, book_file_name)


def get_relations(new_book, book_file_name):
    """
    function:   Wrapper function to Extract the relation between the entities in the book.

    Input:      A string: "new_book" of the pre-processed book
                A string: "book_file_name" which is name of the book as stored on Hard disk.

    Returns:   Nothing
    """

    h_get_entity_relations.start(new_book, book_file_name)


if __name__ == '__main__':
    """This function runs first."""

    # name of the files of book1 and book2 as stored on our hard drive
    book_file_name_list = [
        '0_alice.book',
        '0_shelock.book'
    ]

    for book_file_name in book_file_name_list:
        # importing book and storing its lines in list called "book"
        book = import_book(book_file_name)
        print("\n-------------------------------------\n\nImporting " + book_file_name + ", Done")

        # generate tokens and do pre-processing & lemmatization of the book.
        # "new_book" is a string, "tokens" is a List
        # "tokens" is A List,  which contains lemmatized words.
        new_book, tokens = pre_processing_book(book)
        print("Pre-processing " + book_file_name + ", Done")
        print("\nPlease close any graph shown on your screen to proceed...\n"
              "Don't Worry, these graphs will be savod on disk\n")

        # analyze frequency distribution of tokens and plot it
        analyze_freq_distribution_of_tokens(tokens, book_file_name)
        print("Analyzing frequency distribution of tokens of " + book_file_name + " and plotting it, Done")

        # generating word cloud of books
        generate_word_cloud(new_book, book_file_name)
        print("Generating Word cloud of " + book_file_name + ", Done")

        # get relationship between the word length and frequency
        get_relationship_between_the_word_length_and_frequency(tokens, book_file_name)
        print("Getting relation between word length and frequency for " + book_file_name + ", Done")
        print("\nPlease close any graph shown on your screen to proceed...\n"
              "Don't Worry, these graphs will be savod on disk\n")

        """ 
        Do POS_tagging and Get the distribution of various tags.
        We will be using PennTreebank as tagset which comes by default in NLTK.
        'tags' is a list which contains a tuple as its elements. Each tuple is a word along with its tag
        """
        tags = do_pos_tag_and_get_dist_tags(tokens, book_file_name)
        print("Pos Tagging for " + book_file_name + ", Done")

        # Round 2: "First Part"
        set_of_nouns, set_of_verbs, dict_of_noun_lexname, dict_of_verb_lexname = get_categories(tags,
                                                                                                book_file_name)
        print("Recognizing categories of nouns and verbs for " + book_file_name + ", Done")

        # Round 2: "Second Part"
        recognize_entity(new_book, book_file_name)
        print("Recognizing entity types for " + book_file_name + ", Done")

        # Round 2: "Third Part"
        get_relations(new_book, book_file_name)
        print("Getting relations between entities for " + book_file_name + ", Done")

    print("\n--------------------------------------------------\nAll Done...")
    print("Please see the root folder of project, there will be many graphs and text files generated.")
    print("These files will be starting with letters like 'a_' or 'b_' (and so on) followed by what that file is about")
