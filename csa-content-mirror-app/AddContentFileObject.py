import json
import os
import hashlib
import subprocess
from urllib.parse import urlparse
from datetime import datetime

class AddContentFileObject:
    def __init__(self, url, download_directory):
        self.url = self.strip_anchor_from_url(url)
        self.download_directory = download_directory
        self.domain = urlparse(self.url).netloc
        self.file_path = self.generate_file_path()
        print("self.file_path:")
        print(self.file_path)
        self.json_data = self.load_json_file()

    def strip_anchor_from_url(self, url):
        parsed_url = urlparse(url)
        stripped_url = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path
        return stripped_url

    def generate_file_path(self):
        hash_object = hashlib.sha512(self.url.encode())
        hashed_url = hash_object.hexdigest()
        domain_path = os.path.join(self.download_directory, self.domain)
        if not os.path.exists(domain_path):
            os.makedirs(domain_path)
        return os.path.join(domain_path, hashed_url)

    def load_json_file(self):
        json_file_path = os.path.join(self.file_path, 'kv_data.json')
        try:
            with open(json_file_path, 'r') as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading JSON file: {e}")
            return None

    def get_file_extension(self, url):
        path = urlparse(url).path
        extension = os.path.splitext(path)[1].lower()
        if extension in ['.pdf', '.html', '.json', '.md']:
            return extension[1:]  # Remove the dot
        else:
            return 'html'  # Default to html
        
    def update_json_file(self, timestamp, command_used, http_status_code, extension, directory, filename):
        content_file_object = {
            "timestamp": timestamp,
            "retrievedTime": timestamp,
            "retrievedCommand": command_used,
            "contentHTTPStatusCode": http_status_code,
            "contentMimeType": extension,
            "contentSize": str(os.path.getsize(os.path.join(directory, f"{filename}.{extension}"))),
            "contentFileName": f"{filename}.{extension}",
        }
        if "contentFile" not in self.json_data:
            self.json_data["contentFile"] = []
        self.json_data["contentFile"].append(content_file_object)

        json_file_path = os.path.join(self.file_path, 'kv_data.json')
        with open(json_file_path, 'w') as file:
            json.dump(self.json_data, file, indent=4)

    def download_content(self):
        url = self.json_data['urlData']['originalURL']
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        extension = self.get_file_extension(url)
        print("self.file_path")
        print(self.file_path)
        #directory = os.path.dirname(self.file_path)
        directory = self.file_path
        print("directory:")
        print(directory)
        filename = f"content-{timestamp}"

        if extension == 'html':
            command_used, http_status_code = self.download_html(url, directory, filename)
        else:
            command_used, http_status_code = self.download_other(url, directory, filename, extension)

        self.update_json_file(timestamp, command_used, http_status_code, extension, directory, filename)

    def download_html(self, url, directory, filename, timeout_duration=30):
        print("Downloading HTML...")
        print(directory)
        command = ["google-chrome", "--no-sandbox", "--crash-dumps-dir=/tmp/www",
                   "--disable-crash-reporter", "--headless", "--disable-gpu",
                   "--enable-javascript", "--dump-dom", url]

        try:
            with open(os.path.join(directory, f"{filename}.html"), "w") as file:
                subprocess.run(command, stdout=file, timeout=timeout_duration)
            return ' '.join(command), "200"  # Assuming successful download, replace with actual status code logic as needed
        except subprocess.TimeoutExpired:
            print(f"Timeout expired: Command took longer than {timeout_duration} seconds.")
            return ' '.join(command), "Timeout"


    def download_other(self, url, directory, filename, extension):
        print("Downloading Other...")
        print(directory)
        output_path = os.path.join(directory, f"{filename}.{extension}")
        command = ["curl", "-o", output_path, "-w", "%{http_code}", url]
        result = subprocess.run(command, capture_output=True, text=True)
        http_status_code = result.stdout.strip()
        return ' '.join(command), http_status_code



# Example Usage
if __name__ == "__main__":
    url = "https://example.com/some-content#anchor"
    download_directory = "/path/to/download"
    # Create an instance of AddContentFileObject
    content_file_object = AddContentFileObject(url, download_directory)
    # Assuming there's a method to trigger download (e.g., download_content)
    # You would need to ensure that the JSON structure matches your needs
    content_file_object.download_content()
