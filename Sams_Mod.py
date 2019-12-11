__author__ = 'Sam Van Otterloo'


def main(

):
    import time
    import pandas as pd
    from Prediction_Schema import classify_dataframe, validate_classifier
    from Mind_Web import MindManager

    start = time.time()
    brain = MindManager()
    use_case_context = "Optane DC EU Dashboard"
    data_source = f"WW50 {use_case_context}.xlsx"

    print(f"Beginning to read from: {data_source} . . .")
    raw_data = pd.read_excel(
        data_source,
        sheet_name="Raw Data "
    )
    print(f"Finished reading in data.")

    good_data = validate_classifier(
        raw_data,
        "Vendor Group"
    )

    input("Do you want to export this data?")

    for table in good_data.tables:
        brain.export_memory(f"WW {use_case_context}", data_source, good_data.tables[table])


    end = time.time()
    duration = end - start
    print(f"This took: {round(duration, 3)} seconds.")


if __name__ == "__main__":
    main()
