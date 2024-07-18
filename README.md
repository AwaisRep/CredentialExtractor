# Credential Extractor

## Description

A short python script that uses multi-threading in order to extract all emails from leaked credentials with the desired domains

## Features

- **Feature 1**: Gathers all email:pass credentials found in a given directory, for specific domains
- **Feature 2**: Disgregards all duplicates and old values
- **Feature 3**: Uses multi-threading (10 threads) to simultaneously work on extracting credentials from files

## Installation

- Download the folder from the github repo

### Prerequisites

- Install Python 3

### Example Usage

1. Extract the contents of the folder
2. Modify the script to ensure you have your desired domains selected (see line 88 in main.py)
3. Run the script as done below
4. Examine the output file for your desired contents


```console
foo@bar:~$ main.py
Enter directory to work on: 
c://somePath

Found 6 lines in file: some_file.txt

Attempting to add 6 lines to the output file...
Succesfully appended 3 lines to the file.
Whole process 2.443 seconds
foo@bar:~$
```

NOTE: Any errors in file handling will be written to errors.txt in the directory of where main.py is ran