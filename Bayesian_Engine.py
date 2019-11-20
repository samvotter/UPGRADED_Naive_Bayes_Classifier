from Bayesian_Tables import FrequencyTable
from math import log
from typing import List, Dict


# Performs the math and comparisons needed to make a classification prediction
# To instantiate, pass in a List of FrequencyTable objects
#   These FrequencyTables are the segmentation buckets the classifier will sort new FrequencyTables into
class BayesianEngine:

    def __init__(
            self,
            tables: List[FrequencyTable]
    ) -> None:
        self.tables: Dict = {}
        for table in tables:
            self.tables[table.name] = table
        self.combined: set = set()
        for table in tables:
            for word in table.frequencies:
                self.combined.add(word)
        for word in self.combined:
            for table in self.tables:
                if word not in self.tables[table].frequencies:
                    self.tables[table].frequencies[word] = 0

    # Mostly for testing purposes. Displays to the console the combined set of values from all tables
    def print_combined(
            self
    ) -> None:
        print(f"Combined Dictionary: ")
        for word in self.combined:
            print(f"\t{word}")
        for table in self.tables:
            print(f"Length of {table}: {len(self.tables[table].frequencies.keys())}")

    # add <UNKNOWN> into each table dictionary and adjust the frequency values
    # so that the algorithm is capable of interpreting what to do with unknown values
    def account_for_unknowns(
            self
    ) -> None:
        for word in self.combined:
            for table in self.tables:
                self.tables[table].frequencies[word] = \
                    (self.tables[table].frequencies[word] + 1/self.tables[table].total)/(self.tables[table].total+1)
        for table in self.tables:
            self.tables[table].frequencies["<UNKNOWN>"] = (1/self.tables[table].total)/(self.tables[table].total+1)

    # Given a FrequencyTable object, compare it against the initial segmentation buckets to make a classification
    def make_prediction(
            self,
            unknown_string_table: FrequencyTable
    ) -> str:
        guesses: Dict = {}
        for table in self.tables:
            guesses[table] = self.tables[table].total / len(self.combined)
        for word in unknown_string_table.frequencies:
            for table in self.tables:
                if word in self.tables[table].frequencies:
                    guesses[table] += log(self.tables[table].frequencies[word])*unknown_string_table.frequencies[word]
        maximum = max(guesses, key=guesses.get)
        return maximum
