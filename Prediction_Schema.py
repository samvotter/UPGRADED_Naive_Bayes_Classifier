__author__ = "Sam Van Otterloo"

'''
The purpose of this module is to wrap together the many steps required to build a set of bayesian tables,
instantiate the Engine
make predictions on a dataset
return the altered data
'''

from pandas import DataFrame
from Bayesian_Engine import BayesianEngine
from Bayesian_Tables import BayesianTable
from numpy import nan


def classify_dataframe(
        df: DataFrame,
        focus: str,
        confidence_threshold: float = 0.0,
        verbose: bool = False
) -> DataFrame:
    print(f"Locating {focus} . . .")
    column_values: set = column_set(df, focus)
    print(f"Found: {column_values}")

    engine = instantiate_engine(df, column_values, focus)

    print(f"Making predictions for {engine.predicting} on the original data: ")
    altered_data = engine.predict_from_pandas(df, confidence_threshold, verbose)
    return altered_data


def validate_classifier(
        df: DataFrame,
        focus: str,
) -> DataFrame:
    print(f"Locating {focus} . . .")
    column_values: set = column_set(df, focus)
    print(f"Found: {column_values}")

    engine = instantiate_engine(df, column_values, focus)

    print(f"Making predictions for {engine.predicting} on the original data: ")
    engine.pandas_validation(df[df[focus].notnull()])


def column_set(
        df: DataFrame,
        focus: str
) -> set:
    return set(df[focus].tolist())


def instantiate_engine(
        df:DataFrame,
        focus_set: set,
        focus: str
) -> BayesianEngine:
    print(f"Building Bayesian data tables and subsets . . .")
    buckets = {}
    subsets = {}
    for group in focus_set:
        if group is not nan:
            buckets[group] = BayesianTable(group)
            subsets[group] = df[df[focus] == group]
    print(f"Finished making tables and subsets.")

    print(f"Calculating frequency table values for . . .")
    for group in subsets:
        print(f"\t{group} . . .")
        index = 0
        for row in subsets[group].iterrows():
            if index and index % 100 == 0:
                print(f"\t\tProcessed {index} rows . . .")
            index += 1
            for column in row[1]:
                buckets[group].add_string(column)
        print(f"\t\tThere were {index} rows.")
    print(f"Finished building frequency tables.")

    print(f"Instantiating the Bayesian Engine . . .")
    engine = BayesianEngine(
        focus,
        list(buckets.values())
    )
    print(f"Finished instantiating the Bayesian Engine.")

    print(f"Calculating proportional values for each bucket . . .")
    engine.account_for_unknowns()
    print(f"Finished calculating proportions.")
    return engine
