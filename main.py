#!/usr/bin/python3

import os
import threading
import time
from pathlib import Path
from typing import Union, Set, List

# Define a semaphore with a limit of 10 threads
max_threads = 10
thread_semaphore = threading.Semaphore(max_threads)

def extract_domain(email: str, domains: Union[Set[str], List[str]]) -> bool:
    ''' Simple function to determine if an email belongs to the desired domains '''

    try:
        match = email.split("@", 1)[1] # Split the email on the first @ symbol to extract the domain
        return match in domains # Using set lookup, check if it exists previously
    except IndexError:
        return False

def process_file(file_path: str, domains: Union[Set[str], List[str]], matching_lines: set) -> None:
    ''' Extract all of the relevant emails in the file with the desired domains'''

    count = 0 # Tracks number of lines found in each file
    try:
        file_name = file_path.split('\\')[-1]
    except ValueError:
        print("File name retrieval failed.")

    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                email = line.split(":")[0]

                if extract_domain(email, domains): # If the email belongs to one of the domains
                    count += 1
                    matching_lines.add(line) # Add the credentials to the unique lines set

        # Log any errors when handling the file (generally char conversion issues)
        except Exception as e:
            print(f"Issue with {file_path}: {e}" + "\n")
            errorsFile = open("errors.txt", "a+")
            errorsFile.write(file_path + "\n")
            errorsFile.close()
            try:
                print(len(lines))
            except:
                pass

    # Release the semaphore to work on the next file if any
    thread_semaphore.release()

    try:
        print(f"Found {count} lines in file: {file_name}\n")
    except ValueError:
        print("Lines not handled due to previous exception")
    

def traverse_directory(directory: Path, domains: set) -> set:
    ''' Walk through the directory, uncover all text files and start a worker for each of them '''
    matching_lines = set()

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)

                # Acquire a semaphore before starting a thread to work on the file
                thread_semaphore.acquire()

                # Start the thread with a lamda function to simply extend the final contents of the set
                thread = threading.Thread(target=lambda: process_file(file_path, domains, matching_lines))
                thread.start()
                thread.join()

    return matching_lines

if __name__ == '__main__':
    start = time.time()

    # Variable arguments (can also be handled as sys args)

    old_file = 'remove.txt' # File that contains previously found emails in the domains

    domains_add = {"sky.com", "sky.co.uk"} # Add domains to extract e.g. sky.com, btinternet.com, hotmail.com

    getDir = input("Enter directory to work on: \n")
    path = Path(getDir)

    with open(old_file, "a+") as oldFile:

        old_lines = {line.strip().lower().split(":")[0] for line in oldFile} # Retrieve all old emails

    matching_lines = traverse_directory(path, domains_add)

    # Write matching lines to the output file
    if matching_lines:
        print(f"\nAttempting to add {len(matching_lines)} lines to the output file...")

        final_count = 0
        # Output the final count that has never been found
        with open("output.txt", "w+", encoding="utf-8") as f:
            for line in matching_lines:
                
                email = line.split(":")[0]
                if email.lower() in old_lines:
                    pass
                else:
                    f.write(line + "\n")
                    old_lines.add(email)
                    final_count += 1
    
    if old_lines:
        with open("remove.txt", "w+") as f:
            for line in old_lines:
                f.write(line + "\n")

    print(f"Successfully appended {final_count} emails to the file.")
    print(f"Whole process took {time.time() - start} seconds")