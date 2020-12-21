import random

import nltk
from openie import StanfordOpenIE


def is_relation_good(triple):
    """
    function:   check if the relation is between two noun entities or between a noun and a vert.

    Input:      A dict:   "triple", contains a subject, relation and object as its elements.

    Returns:    True, if the given "triple" contains good relation.
                False otherwise
    """

    split_nouns = str(triple['subject']).split(" ")
    split_verbs = str(triple['object']).split(" ")

    noun_tags = nltk.pos_tag(split_nouns)
    verb_tags = nltk.pos_tag(str(triple['object']).split(" "))

    all_words = split_nouns + split_verbs
    all_tags = noun_tags + verb_tags


    tag_dict = {}
    for tag in all_tags:
        tag_dict[tag[0]] = tag[1]

    is_it_good_sub = False
    is_it_good_obj = False

    sub = str(triple['subject']).split(" ")
    obj = str(triple['object']).split(" ")

    # if they both subject and verb are "NN", then its a good relation
    for each_sub in sub:
        if "NN" in tag_dict[each_sub] and len(str(sub).split(" ")) < 4:
            is_it_good_sub = True
            break

    #  or if subject is "NN" and obj is "VB", then its a good relation
    if is_it_good_sub:
        for each_obj in obj:
            if ("NN" in tag_dict[each_obj] and len(str(obj).split(" ")) < 4) or ("VB" in tag_dict[each_obj]):
                is_it_good_obj = True
                break

    if is_it_good_obj and is_it_good_sub:
        return True
    else:
        return False


def start(new_book: str, book_file_name: str):
    """
    function:   Extract the relation between the entities in the book.
                we will use Python3 wrapper for Stanford OpenIE for this job.

    Input:      A string:   "new_book" of the pre-processed book
                A string:   "book_file_name" which is name of the book as stored on Hard disk.

    Returns:    Nothing, it generates the graph and saves it as image. It also outputs the relations in a text file
    """

    # We will take only first 40,000 letters for getting relationships in the books
    # We will then store block of 10,000 letters in each element of a list to make processing easy.

    TEXT = []
    for x in range(0, 40000, 10000):
        TEXT.append(new_book[x:x + 10000])

    relation_file = open("h_entity_relation_list_" + book_file_name + '.txt', 'w+')
    relation_file.write("This File contains Entity relations (of nouns) extracted"
                        " from first 8,000 words from the book " + book_file_name + "\n")
    relation_file.write("\n--------------------------------------------------\n\n\n")

    # passing text to StanfordOpenIE to process
    with StanfordOpenIE() as client:
        for text in TEXT:
            # print('\nText: \n%s.' % text)
            for triple in client.annotate(text):
                # Below lines check if the relation is between two noun entities or between noun and verb.
                try:
                    if is_relation_good(triple):
                        relation_file.write("|- " + str(triple) + '\n')
                except KeyError:
                    pass
            graph_image = 'h_entity_relation_graph_' + book_file_name + '_' + str(random.randint(0, 100000)) + '_.png'
            client.generate_graphviz_graph(text, graph_image)
