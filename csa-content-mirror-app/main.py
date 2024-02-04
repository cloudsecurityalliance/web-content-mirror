#!/usr/bin/env python3

import sys
import os
from urllib.parse import urlparse
import AddurlDataObject

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def process_url(processor, url):
    if is_valid_url(url):
        processor.add_url(url)
    else:
        print(f"Error: '{url}' is not a valid URL.")

def main():
    if len(sys.argv) != 2:
        print("Usage: script.py <URL or path to text file>")
        sys.exit(1)

    argument = sys.argv[1]

    # Specify your downloads directory
    downloads_directory = "web-content-mirror/data"

    # Create an instance of the class
    processor = AddurlDataObject.AddurlDataObject(downloads_directory)

    if os.path.isfile(argument):
        with open(argument, 'r') as file:
            for line in file:
                url = line.strip()
                if url:
                    process_url(processor, url)
    elif is_valid_url(argument):
        process_url(processor, argument)
    else:
        print(f"Error: '{argument}' is neither a valid file nor a URL.")

if __name__ == "__main__":
    main()
