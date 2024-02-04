# File: AddurlDataObject.py

import os
import hashlib
import json
from datetime import datetime
from urllib.parse import urlparse

class AddurlDataObject:
    def __init__(self, downloads_directory):
        self.downloads_directory = downloads_directory

    def get_domain_name(self, url):
        parsed_url = urlparse(url)
        return parsed_url.netloc

    def strip_anchor_from_url(self, url):
        parsed_url = urlparse(url)
        stripped_url = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path
        return stripped_url

    def generate_sha512_hash(self, url):
        return hashlib.sha512(url.encode()).hexdigest()

    def add_url(self, url):
        domain_name = self.get_domain_name(url)
        stripped_url = self.strip_anchor_from_url(url)
        sha512_hash = self.generate_sha512_hash(stripped_url)

        data_directory = os.path.join(self.downloads_directory, domain_name, sha512_hash)
        os.makedirs(data_directory, exist_ok=True)

        json_file_path = os.path.join(data_directory, 'kv_data.json')

        # Check if kv_data.json already exists
        if not os.path.isfile(json_file_path):
            json_data = {
                "$id": "CSAwebContentMirror",
                "$schema": "",
                "$schemaVersion": "1.0.0",
                "urlData": {
                    "timestamp": datetime.now().isoformat(),
                    "originalURL": url,
                    "addedTime": datetime.now().isoformat()
                }
            }

            with open(json_file_path, 'w') as json_file:
                json.dump(json_data, json_file, indent=4)
        else:
            print(f"'kv_data.json' already exists in {data_directory}. Skipping file creation.")

# Example usage:
# processor = AddurlDataObject('/path/to/downloads')
# processor.add_url('https://example.com/page')
