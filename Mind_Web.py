import os
import json
from re import findall
from Bayesian_Tables import BayesianTable

'''
Memory is organized in this format:
/working_directory/use_case_context/bucket.json

it is possible that bucket exist in multiple use_case_contexts, however, it seems more reasonable to segment them
by use case. Identifying tokens relevant in one context might be confounding in another. 
'''


class MindManager:

    def __init__(
            self,
            use_case_context: str
    ):
        self.use_case_context = use_case_context
        # Determine the current state of the Mind directory
        dir_name = os.getcwd()
        dir_name = os.path.join(dir_name, "Mind")
        print(f"Checking if {dir_name} exists . . .")
        if os.path.isdir(dir_name):
            print(f"\tFound the mind path.")
            self.mind_path = dir_name
        else:
            print(f"\tDirectory not found. Attempting to create {dir_name}")
            try:
                os.mkdir(dir_name)
            except OSError:
                print(f"\t\tERROR! Could not create the directory {dir_name}")
            else:
                print(f"\t\t{dir_name} directory successfully created!")
            self.mind_path = dir_name

    # memory imports are expected to be in json format
    def import_memory(
            self
    ) -> json.load:
        full_path = os.path.join(self.mind_path, self.use_case_context)
        print(f"Looking for {self.use_case_context} . . .")
        if os.path.isdir(full_path):
            print(f"\tFound {self.use_case_context}.")
            full_path = os.path.join(full_path, f"{self.use_case_context}.json")
            print(f"\t\tLooking for {self.use_case_context}.json . . .")
            if os.path.exists(full_path):
                print(f"\t\t\tFound {self.use_case_context}.json.")
                print(f"Importing {self.use_case_context}.json data.")
                with open(full_path, "r") as read_file:
                    return json.load(read_file)
            else:
                print(f"\t\t\tERROR! Could not find {full_path}.")
                return
        else:
            print(f"\tERROR! Could not find {full_path}.")
            return

    # assumes that you wish to create a wholly new use_case_context element
    def export_memory(
            self,
            data_source: str,
            bucket: BayesianTable
    ):
        export_path = os.path.join(self.mind_path, self.use_case_context)
        # determine if the use_case_context already exists
        print(f"Checking if {export_path} exists . . .")
        if os.path.isdir(export_path):
            print(f"\tSuccess!")
            # determine if this data_source has already been exported
            memory_path = os.path.join(export_path, "Memory_Log.json")
            export_path = os.path.join(export_path, f"{self.use_case_context}.json")
            print(f"\t\tChecking if {data_source} : {bucket.name} has already been exported . . .")
            if os.path.exists(memory_path):
                # a Memory_Log already exists, check if the source is contained in that memory
                with open(memory_path, 'r') as read_file:
                    mem = json.load(read_file)
                # was data from this data source already exported?
                if data_source in mem.keys():
                    # with this group?
                    if bucket.name in mem[data_source]:
                        print(
                            f"\t\t\tERROR! {data_source} : {bucket.name} has already been exported. Export refused.")
                        return
                    else:
                        # adding the bucket.name to data_source, then export data
                        print(f"\t\t\tCreating memory record for {data_source} : {bucket.name} . . .")
                        mem[data_source].append(bucket.name)
                        with open(memory_path, 'w') as outfile:
                            json.dump(mem, outfile, indent=4)
                        print(f"\t\t\t\tSuccess!")
                        # does the use case already exist (it should)?
                        if os.path.exists(export_path):
                            print(f"\t\t\t\t\tMerging new data with old data . . .")
                            with open(export_path, 'r') as old_data:
                                old = json.load(old_data)
                            # merge the data with old?
                            if bucket.name in old.keys():
                                for token in bucket.frequencies:
                                    if token in old[bucket.name].keys():
                                        old[bucket.name][token] += bucket.frequencies[token]
                                    else:
                                        old[bucket.name][token] = 1
                            # there is no old data, create new entry
                            else:
                                old[bucket.name] = bucket.frequencies
                            with open(export_path, 'w') as out_file:
                                json.dump(old, out_file, indent=4)
                            print(f"\t\t\t\t\t\tSuccess!")
                        # use_case_context.json does not exist for some reason
                        else:
                            print(f"\t\t\t\t\tExporting {bucket.name} data . . .")
                            with open(export_path, 'w') as out_file:
                                json.dump({bucket.name: bucket.frequencies}, out_file, indent=4)
                            print(f"\t\t\t\t\t\tSuccess!")
                else:
                    # Create data source entry, then export data
                    print(f"\t\t\tCreating memory record for {data_source} : {bucket.name} . . .")
                    mem[data_source] = [bucket.name]
                    with open(memory_path, 'w') as outfile:
                        json.dump(mem, outfile, indent=4)
                    print(f"\t\t\t\tSuccess!")
                    # data is ready to be exported
                    if os.path.exists(export_path):
                        print(f"\t\t\t\t\tMerging new data with old data . . .")
                        with open(export_path, 'r') as old_data:
                            old = json.load(old_data)
                            # merge the data with old?
                            if bucket.name in old.keys():
                                for token in bucket.frequencies:
                                    if token in old[bucket.name].keys():
                                        old[bucket.name][token] += bucket.frequencies[token]
                                    else:
                                        old[bucket.name][token] = 1
                            # there is no old data, create new entry
                            else:
                                old[bucket.name] = bucket.frequencies
                        with open(export_path, 'w') as out_file:
                            json.dump(old, out_file, indent=4)
                        print(f"\t\t\t\t\t\tSuccess!")
                    else:
                        with open(export_path, 'w') as out_file:
                            json.dump({bucket.name: bucket.frequencies}, out_file, indent=4)
            else:
                # Create a memory log and export data
                print(f"\t\t\tAdding {data_source} : {bucket.name} to the web.")
                mem = {data_source: [bucket.name]}
                with open(memory_path, 'w') as out_file:
                    json.dump(mem, out_file, indent=4)
                print(f"\t\t\t\tSuccess!")
                # data is ready to be exported
                if os.path.exists(export_path):
                    with open(export_path, 'r') as old_data:
                        old = json.load(old_data)
                        # merge the data with old?
                        if bucket.name in old.keys():
                            for token in bucket.frequencies:
                                if token in old[bucket.name].keys():
                                    old[bucket.name][token] += bucket.frequencies[token]
                                else:
                                    old[bucket.name][token] = 1
                        # there is no old data, create new entry
                        else:
                            old[bucket.name] = bucket.frequencies
                    with open(export_path, 'w') as out_file:
                        json.dump(old, out_file, indent=4)
                else:
                    with open(export_path, 'w') as out_file:
                        json.dump({bucket.name: bucket.frequencies}, out_file, indent=4)
        else:
            # Create a new directory, memory log, and data export
            print(f"\t{self.use_case_context} does not exist. Creating directory . . .")
            os.mkdir(export_path)
            memory_path = os.path.join(export_path, "Memory_Log.json")
            export_path = os.path.join(export_path, f"{self.use_case_context}.json")
            print(f"\t\tWriting new Memory_Log . . .")
            mem = {data_source: [bucket.name]}
            with open(memory_path, 'w') as out_file:
                json.dump(mem, out_file, indent=4)
            print(f"\t\t\tWriting to {export_path} . . .")
            with open(export_path, 'w') as out_file:
                json.dump({bucket.name: bucket.frequencies}, out_file, indent=4)
            print("\t\t\t\tSuccess!")
