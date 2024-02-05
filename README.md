# web content mirror

The directory /web-content-mirror/ contains root files that get synchronized into the S3 bucket.

In the S3 bucket it also contains data directories in the /data/ directory in the form /domain-name/base64.urlsafe_b64encode(url.encode('utf-8'))/ of URL/content for that URL. Please note any anchor tag is removed from the URL first.

Please note that URLs can be retrieved multiple times (e.g. Hacker News threads with more comments), processed to text/csv/json/md multiple times (e.g. as we get better PDF extraction tools) and processed by AI multiuple times (e.g. as we have better text input, better prompts, better models, etc.).

Every object is in a list so they all get a timestamp so we can easily order them oldest to newest.

General process is:

* AddURLDataObject()
  * Add URL (write basic kv_data.json to data/domain/base64/kv_data.json with urlData object)
* StoreURLContentFileObject()
  * Retrieve URL and update data/domain/base64/kv_data.json with a contentFile object and file
  * Given a URL and a file update data/domain/base64/kv_data.json with a contentFile object and file for manual uploads
  * When loading the URLs from a text file remove the anchor and deduplicate the list for downloads and analysis
* StoreFileObject()
  * Given a filename/path generate an entry based on the filename (so be unique), use domain "file", update data/domain/base64/kv_data.json with a contentFile object and file for manual uploads
* ScanContentFileObject()
  * AV scan the content and update avScan fields and make sure it isn't some sort of hostile binary
* ExtractTextFromContentFile()
  * Get the context text and update the contentText object and file, this can be done multiple times e.g. as we get better PDF extraction tools or decide to structure the format in md instead of just text for example
* SendAIPromptWithText()
  * Depending on prompt/capabilities send a prompt and content file or contentText file to AI and get result, add contentAIProcessing object and file

# Dealing with files

If we get a file with no origin URL we simply use the filename for the base64 and otherwise treat it like a URL. This means we'll want to rename files to be unique.

# Adding and updating data in the S3 bucket

The S3 bucket does NOT have versioning enabled. This is intentional, as we do not want to rely upon it.

Files either get read, updated and written (e.g. kv_data.json) or created with a timestamp and other semi unique properties to ensure they don't overwrite any other files.

Longer term we'll need a file locking or queue mechanism to ensure kv_data.json doesn't get mangled, the solution for now is to run the work in single batches sequentially (especially for AI processing where we are rate limited for API access in most cases).

To sync the root files (README.md, kv_data.json, etc.):

```
aws s3 sync ./web-content-mirror/ s3://web-content-mirror
```

# TODO:

* Write a Python library and tools to add and update data in the S3 bucket
* Write a Python library that given a URL retrieves the content, AI summaries, etc.
* Write a front end for people to add URLs and get the results
