#!/usr/bin/python3

import os
import threading
from dupes import removeDupes
from pathlib import Path

# Define a semaphore with a limit of 10 threads
max_threads = 10
thread_semaphore = threading.Semaphore(max_threads)

def extract_domain(email, x):
    try:
        match = email.split("@", 1)[1]
        if match in x:
            return True
    except:
        pass
    return False

def process_file(file_path, x):
    matching_lines = []

    try:
        file_name = file_path.split('\\')[-1]
    except:
        print("File name retrieval failed.")

    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                email = line.split(":")[0]

                if extract_domain(email, x):
                    matching_lines.append(line)

        except Exception as e:
            print(f"Issue with {file_path}: {e}" + "\n")
            errorsFile = open("errors.txt", "a+")
            errorsFile.write(file_path + "\n")
            errorsFile.close()
            try:
                print(len(lines))
            except:
                pass

    # Release the semaphore
    thread_semaphore.release()

    try:
        print(f"Found {len(matching_lines)} lines in file: {file_name}\n")
    except:
        pass
    
    return matching_lines

def traverse_directory(directory, x):
    matching_lines = []

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)

                # Acquire a semaphore before starting a thread
                thread_semaphore.acquire()

                thread = threading.Thread(target=lambda: matching_lines.extend(process_file(file_path, x)))
                thread.start()
                thread.join()

    return matching_lines

if __name__ == '__main__':
    output_file = 'output.txt'
    x = ["talktalk.net", "talktalk.com", "talktalk.co.uk", "tiscali.co.uk", "tiscali.com"]
    #x = ["btinternet.com", "bt.com", "ntlworld.com", "blueyonder.co.uk", "ntlworld.co.uk", "virginmedia.com", "blueyonder.com"]
    matching_lines = []

    getDir = input("Enter directory to work on: \n")
    path = Path(getDir)

    matching_lines.extend(traverse_directory(path, x))

    # Write matching lines to the output file
    if matching_lines:
        print(f"\nAttempting to add {len(matching_lines)} lines to the output file...")

        removeDupes(matching_lines)
