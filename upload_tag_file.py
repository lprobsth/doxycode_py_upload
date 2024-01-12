#!/usr/bin/env python3

import sys
import os
import json
import requests
from optparse import OptionParser

def main():
    parser = OptionParser(usage="usage: %prog filename")
    parser.add_option("-u", "--url", dest="url", help="DokuWiki JSON API URL", default=os.environ.get('DOKUWIKI_API_URL'))
    parser.add_option("-t", "--token", dest="token", help="Authorization token", default=os.environ.get('DOKUWIKI_API_TOKEN'))

    (options, args) = parser.parse_args()

    # Check if filename is provided
    if len(args) != 1:
        parser.error("Filename must be provided")

    filename = args[0]

    # Check if API URL and token are set
    if not options.url or not options.token:
        sys.exit("Error: DokuWiki API URL or token not set. Please set environment variables.")

    # Read the file to be uploaded
    try:
        with open(filename, "rb") as in_file:
            file_content = in_file.read()
    except IOError as e:
        sys.exit(f"Error reading file: {e}")

    # Prepare the JSON payload for the API request
    json_payload = {
        "jsonrpc": "2.0",
        "id": "uploadTagFile",
        "method": "plugin.doxycode.uploadTagFile",
        "params": [filename, file_content.decode('utf-8')]  # Assuming file_content is utf-8 encoded text
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {options.token}'
    }

    # Make the API request
    try:
        response = requests.post(options.url, headers=headers, data=json.dumps(json_payload))

        if response.status_code == 200:
            response_data = response.json()
            if 'result' in response_data and response_data['result']:
                print("Upload successful.")
                sys.exit(0)
            else:
                print("Upload failed with response:", response_data)
                sys.exit(2)
        else:
            print("HTTP error:", response.status_code)
            sys.exit(3)

    except requests.RequestException as e:
        print(f"Request error: {e}")
        sys.exit(4)

if __name__ == "__main__":
    main()