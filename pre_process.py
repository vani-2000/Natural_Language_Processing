import re


# remove numbers and punctuation
def remove_numbers_and_punctuation(line):
    result = re.sub(r'\d+', '', line)
    result = re.sub(r'[,.;:]', ' ', result)
    result = re.sub(r'[\'\"\“\”\’\-\_]', '', result)
    return result


# remove whitespace
def remove_whitespace(line):
    return " ".join(line.split())


# function to pre-process text, this will call various other functions
# that will perform tasks on text like removing numbers, whitespaces etc
# returns a string
def start(book: list):
    # we will remove first 30 lines of book since they contain contents and running section
    # we will still use chapter name for our corpus
    book = book[30:]

    # we will append the strings to this list after making all changes
    new_book = ''

    for line in book:
        line = remove_numbers_and_punctuation(line)
        line = remove_whitespace(line)
        new_book += ' ' + line

    return new_book
