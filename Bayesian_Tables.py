__author__ = 'Sam Van Otterloo'

from nltk.corpus import stopwords
'''
stopwords may need to be downloaded: 
    nltk.setproxy()
    nltk.download('stopwords')
'''


# organizes string data into a frequency table
#   This class is used either:
#       1. as a segmentation bucket for the BayesEngine
#       OR
#       2. A corpus of string data for the BayesEngine to classify
# name is the unique identifier associated with a the data source
class BayesianTable:

    # name is the identity associated with the frequency table
    name: str

    def __init__(
            self,
            name: str
    ):
        self.name = name
        self.frequencies = {}
        self.proportions = {}
        self.total = 0

    # mostly for testing purposes to check under the hood at what items are being stored in the table
    def print_dict(
            self,
            **kwargs
    ) -> None:
        options = {
            "table": None,
            "frequencies": self.frequencies,
            "proportions": self.proportions
        }
        for opt in kwargs:
            if opt in options:
                options[opt] = kwargs[opt]

        print(f"Printing {self.name}'s {options['table']}: ")
        for item in options[options['table']]:
            print(f"\t{item}: {options[options['table']][item]}")

    # turns the table from:
    #   [word]: #_of_occurences
    #   to:
    #   [word]: #_of_occurences / total
    def turn_into_proportions(
            self
    ) -> None:
        for item in self.frequencies:
            self.proportions[item] = self.frequencies[item] / self.total

    # adds an entire string into the frequency table and not just a single word
    def add_string(
            self,
            string_to_be_added: str
    ) -> None:
        if isinstance(string_to_be_added, str):
            broken_into_words = string_to_be_added.split()
        else:
            return
        for word in broken_into_words:
            self.add_word(word)

    # adds an individual string token into the frequency table
    #   new words are thoroughly cleaned before they enter the table
    def add_word(
            self,
            word: str
    ) -> None:
        # attempt to clean word as much as possible
        #       remove punctuation / whitespace
        #       standardize case
        #       eliminate stopwords
        if isinstance(word, str):
            word = self.clean_input(word)
            if len(word):
                if word in stopwords.words("english"):
                    return
                else:
                    if word in self.frequencies:
                        self.frequencies[word] += 1
                        self.total += 1
                    else:
                        self.frequencies[word] = 1
                        self.total += 1
            else:
                return

    # Does the actual cleaning
    def clean_input(
            self,
            word: str
    ) -> str:
        word = word.lower().strip()
        while not word[-1].isalnum():
            word = word[:-1]
            if not word:
                return ""
        while not word[0].isalnum():
            word = word[1:]
            if not word:
                return ""
        if word[-2:] == "'s":
            word = word[:-2]
        return word


