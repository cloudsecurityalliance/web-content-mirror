#!/usr/bin/env python3

import sys
import os
from AddContentFileObject import AddContentFileObject

def read_urls_from_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def process_url(url, download_directory):
    content_file_object = AddContentFileObject(url, download_directory)
    content_file_object.download_content()

def main():
    if len(sys.argv) != 3:
        print("Usage: python main_script.py <URL or path to URL file> <Download Directory>")
        sys.exit(1)

    input_arg = sys.argv[1]
    download_directory = sys.argv[2]

    # Check if the input is a file or a single URL
    if os.path.isfile(input_arg):
        urls = read_urls_from_file(input_arg)
    else:
        urls = [input_arg]

    for url in urls:
        process_url(url, download_directory)

if __name__ == "__main__":
    main()
