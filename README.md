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

- Python 3
- The program by default expects UTF-8 encoded text files, it will attempt to read any that aren't, but please note this can significantly reduce performance time

### Installation

1. Download/Clone from github
2. Install the requirements using pip as such:

    ```console
    pip install -r requirements.txt
    ```
   Only chardet is required to run this program, so alternatively, you may run this command:

    ```console
    pip install chardet
    ```

### Example Usage

1. Modify the script to ensure you have your desired domains selected (see line 106 in main.py)
2. Run the script as shown below
3. Examine the output file for your desired contents


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

### NOTE
- Any errors in file handling will be written to errors.txt in the directory of where main.py is ran
