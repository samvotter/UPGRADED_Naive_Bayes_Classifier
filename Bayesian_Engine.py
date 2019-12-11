__author__ = 'Sam Van Otterloo'

from Bayesian_Tables import BayesianTable
from math import log
from typing import List, Dict, Tuple
from statistics import mean, stdev
from collections import Counter
from Math_Functions import squash
from copy import deepcopy
from pandas import DataFrame

# Performs the math and comparisons needed to make a classification prediction
# To instantiate:
#   name the element you intend to predict
#       if using pandas predict, it should be the column name
#   pass in a List of FrequencyTable objects
#       These FrequencyTables are the segmentation buckets the classifier will sort new FrequencyTables into
class BayesianEngine:

    def __init__(
            self,
            predicting: str,
            tables: List[BayesianTable]
    ) -> None:
        self.predicting = predicting
        self.tables: Dict = {}
        for table in tables:
            self.tables[table.name] = table
        self.combined: set = set()

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
    def format_tables(
            self
    ) -> None:
        # make sure tables have valid totals
        for table in self.tables:
            if not self.tables[table].total:
                for token in self.tables[table].frequencies:
                    self.tables[table].total += self.tables[table].frequencies[token]

        # combine the sets
        for table in self.tables:
            for word in self.tables[table].frequencies:
                self.combined.add(word)

        for table in self.tables:
            print(f"\tBeginning table transform on: {table} . . .")
            for word in self.tables[table].frequencies:
                self.tables[table].proportions[word] = \
                    (self.tables[table].frequencies[word] + 1/self.tables[table].total)/(self.tables[table].total+1)
            self.tables[table].proportions["__UNKNOWN__"] = (1/self.tables[table].total)/(self.tables[table].total+1)
            print(f"\t\tFinished transforms on: {table}.")

    # Given a FrequencyTable object, compare it against the initial segmentation buckets to make a classification
    def make_prediction(
            self,
            unknown_string_table: BayesianTable,
            verbose: bool = False
    ) -> Tuple[str, float, float]:
        guesses: Dict = {}
        for table in self.tables:
            guesses[table] = self.tables[table].total / len(self.combined)
        for word in unknown_string_table.frequencies:
            for table in self.tables:
                if word in self.tables[table].frequencies:
                    guesses[table] += log(self.tables[table].proportions[word]) * unknown_string_table.frequencies[
                            word]
                else:
                    guesses[table] += log(self.tables[table].proportions["__UNKNOWN__"]) * \
                                      unknown_string_table.frequencies[
                                          word]
        # rate and report the guess
        scores = guesses.values()
        maximum_key = max(guesses, key=guesses.get)
        maximum_val = max(scores)
        avg = mean(scores)
        std = stdev(scores)
        diff = maximum_val - avg
        confidence = diff/std
        confidence = squash(confidence)
        top_2 = Counter(guesses).most_common(2)
        not_diff = top_2[0][1] - top_2[1][1]
        not_confidence = not_diff/std
        not_confidence = squash(not_confidence)
        confidence = round(confidence, 3) * 100
        not_confidence = round(not_confidence, 3) * 100
        if verbose:
            print(f"Full Guess table: ")
            for guess in guesses:
                print(f"\t{guess}: {guesses[guess]}")
            print(f"Average: {avg}")
            print(f"Stds from avg: {diff/std}")
            print(f"Stds from closest: {not_diff/std}")
        return maximum_key, confidence, not_confidence

    # given a Pandas Dataframe object, iterate over it and make predictions
    def predict_from_pandas(
            self,
            df: DataFrame,
            confidence_threshold: float = 0.0,
            verbose: bool = False,
            null_is: str = None
    ) -> DataFrame:
        confidence_1 = 0
        confidence_2 = 0
        total = 0
        altered_data = deepcopy(df)
        iterover = df[df[self.predicting].isnull() & (df[self.predicting] == null_is)]
        guess_distribution = {}
        for index, row in iterover.iterrows():
            row_guess = BayesianTable(index)
            for column in row:
                row_guess.add_string(column)
            guess = self.make_prediction(row_guess, verbose)
            confidence_1 += guess[1]
            confidence_2 += guess[2]
            if guess[1] >= confidence_threshold:
                altered_data.at[index, self.predicting] = guess[0]
                if guess[0] in guess_distribution:
                    guess_distribution[guess[0]] += 1
                    total += 1
                else:
                    guess_distribution[guess[0]] = 1
                    total += 1
            print(f"\t{row_guess.name}: True Value: {row[self.predicting]} ", end="")
            print(f"Predicted: {guess}")
        print(f"\tGuess Distributions:")
        for guess in guess_distribution:
            print(f"\t\t{guess}: {guess_distribution[guess]}")
        print(f"Average General Confidence: {round(confidence_1 / total, 3)}")
        print(f"Average Specific Confidence: {round(confidence_2 / total, 3)}")
        return altered_data

    def pandas_validation(
            self,
            df: DataFrame
    ) -> None:
        total = 0
        correct = 0
        confidence_1 = 0
        confidence_2 = 0
        for index, row in df.iterrows():
            if row[self.predicting]:
                row_guess = BayesianTable(index)
                for column in row:
                    row_guess.add_string(column)
                guess = self.make_prediction(row_guess)
                confidence_1 += guess[1]
                confidence_2 += guess[2]
                print(f"\t{row_guess.name}: True Value: {row[self.predicting]} ", end="")
                print(f"Predicted: {guess}")
                if row[self.predicting] == guess[0]:
                    correct += 1
                    total += 1
                else:
                    total += 1
        print(f"This classification attempt was {(round(correct / total, 2) * 100)}% successful")
        print(f"Average General Confidence: {round(confidence_1 / total, 3)}")
        print(f"Average Specific Confidence: {round(confidence_2 / total, 3)}")
