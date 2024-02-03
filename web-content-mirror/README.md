# Web Content Mirror

This S3 bucket contains directories in the form /domain-name/SHA512 of URL/content for that URL.

with anything past a # anchor removed from the URL prior to SHA512'ing it

kv_data: kv_data.json
files: semi unique names with a timestamp, referenced from kv_data.json
