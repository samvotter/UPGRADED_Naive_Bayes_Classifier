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
from Mind_Web import MindManager


def classify_dataframe(
        df: DataFrame,
        focus: str,
        eng_load: bool = False,
        use_case_context: str = None,
        confidence_threshold: float = 0.0,
        verbose: bool = False,
        null_is: str = None
) -> DataFrame:
    print(f"Locating {focus} . . .")
    column_values: set = column_set(df, focus)
    if nan not in column_values and null_is not in column_values:
        print(f"ERROR! There are no NULL values to classify!")
        return df
    else:
        print(f"Found: {column_values}")

        if eng_load and use_case_context:
            data = MindManager(
                use_case_context
            ).import_memory()

            buckets = [
                BayesianTable(
                    bucket_name,
                    data[bucket_name]
                )
                for bucket_name in data.keys()
            ]
            engine = BayesianEngine(focus, buckets)
            engine.format_tables()
        else:
            engine = instantiate_engine(df, column_values, focus, null_is=null_is)

        if verbose:
            engine.print_combined()

        print(f"Making predictions for {engine.predicting} on the original data: ")
        return engine.predict_from_pandas(df, confidence_threshold, verbose, null_is=null_is)


def validate_classifier(
        df: DataFrame,
        focus: str,
        eng_load: bool = False,
        use_case_context: str = None,
        null_is: str = None
) -> BayesianEngine:
    print(f"Locating {focus} . . .")
    column_values: set = column_set(df, focus)
    print(f"Found: {column_values}")

    if eng_load and use_case_context:
        data = MindManager(
            use_case_context
        ).import_memory()

        buckets = [
            BayesianTable(
                bucket_name,
                data[bucket_name]
            )
            for bucket_name in column_values if bucket_name is not nan and bucket_name != null_is
        ]
        engine = BayesianEngine(focus, buckets)
        engine.format_tables()
    else:
        engine = instantiate_engine(df, column_values, focus, null_is=null_is)

    print(f"Making predictions for {engine.predicting} on the original data: ")
    engine.pandas_validation(df[df[focus].notnull() & (df[focus] != null_is)])
    return engine


def column_set(
        df: DataFrame,
        focus: str
) -> set:
    df = df[df[focus].notnull()]
    return set(df[focus].tolist())


def instantiate_engine(
        df: DataFrame,
        focus_set: set,
        focus: str,
        null_is: str = None
) -> BayesianEngine:
    print(f"Building Bayesian data tables and subsets . . .")
    buckets = {}
    subsets = {}
    for group in focus_set:
        if null_is:
            if group is not nan and group != null_is:
                buckets[group] = BayesianTable(group)
                subsets[group] = df[df[focus] == group]
        else:
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
    engine.format_tables()
    print(f"Finished calculating proportions.")
    return engine

