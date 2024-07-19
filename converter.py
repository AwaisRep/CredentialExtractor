import os
from pathlib import Path
import chardet
import threading

# Semaphore to limit the number of concurrent threads
semaphore = threading.Semaphore(10)

def convert_to_utf8(file_path):
    try:
        with open(file_path, 'rb') as file:
            content = file.read()
            encoding_result = chardet.detect(content)
            detected_encoding = encoding_result['encoding']

            if detected_encoding != 'utf-8':
                print(f"Converting {file_path} from {detected_encoding} to UTF-8...")
                content = content.decode(detected_encoding)
                with open(file_path, 'w', encoding='utf-8') as output:
                    output.write(content)
                    print(f"Converted {file_path} to UTF-8.")
            else:
                print(f"{file_path} is already UTF-8 encoded.")

    except Exception as e:
        print(f"Error converting {file_path}: {e}")

    finally:
        # Release the semaphore when the thread is done
        semaphore.release()

def convert_files_in_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)

                # Acquire the semaphore to limit concurrent threads
                semaphore.acquire()

                # Start a new thread to convert the file
                thread = threading.Thread(target=convert_to_utf8, args=(file_path,))
                thread.start()

if __name__ == '__main__':
    getDir = input("Enter directory: \n")
    path = Path(getDir)

    print(f"Converting text files to UTF-8 in directory: {path} \n")

    # Create a separate thread to start the conversion process
    start_thread = threading.Thread(target=convert_files_in_directory, args=(path,))
    start_thread.start()

    print("Conversion started. \n")

    # Wait for the starting thread to finish
    start_thread.join()

    # Wait for all threads to finish
    main_thread = threading.current_thread()
    for thread in threading.enumerate():
        if thread is not main_thread:
            thread.join()

    print("\nConversion complete.")
