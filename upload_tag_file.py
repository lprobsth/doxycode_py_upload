#!/usr/bin/env python3

import sys
from optparse import OptionParser
import os

def upload_using_json_api(url, token, filename, file_content):
    print("Using JSON RPC API")

    import requests
    import json

    json_payload = {
        "jsonrpc": "2.0",
        "id": "uploadTagFile",
        "method": "plugin.doxycode.uploadTagFile",
        "params": [filename, file_content.decode('utf-8')]  # Assuming file_content is utf-8 encoded text
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    response = requests.post(url, headers=headers, data=json.dumps(json_payload))

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

def upload_using_xml_rpc(url, user, password, filename, file_content):
    print("Using XML RPC API")

    from dokuwikixmlrpc import DokuWikiClient
    import xmlrpc.client as xmlrpclib

    dw = DokuWikiClient(url, user, password)

    try:
        response = dw._xmlrpc.plugin.doxycode.uploadTagFile(filename, xmlrpclib.Binary(file_content))

        if response:
            print("Upload successful.")
            sys.exit(0)
        else:
            print("Upload failed.")
            sys.exit(2)

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(3)

def main():
    parser = OptionParser(usage="usage: %prog filename")
    parser.add_option("-u", "--url", dest="url", help="DokuWiki URL or API URL", default=os.environ.get('DOKUWIKI_DOMAIN'))
    parser.add_option("-t", "--token", dest="token", help="Authorization token for JSON RPC API", default=os.environ.get('DOKUWIKI_API_TOKEN'))
    parser.add_option("-p", "--password", dest="password", help="DokuWiki password for XML RPC API", default=os.environ.get('DOKUWIKI_PASSWORD'))
    parser.add_option("-n", "--username", dest="username", help="DokuWiki username for XML RPC API", default=os.environ.get('DOKUWIKI_USER'))

    (options, args) = parser.parse_args()

    # Check if filename is provided
    if len(args) != 1:
        parser.error("Filename must be provided")
    filename = args[0]

    # Read the file to be uploaded
    try:
        with open(filename, "rb") as in_file:
            file_content = in_file.read()
    except IOError as e:
        sys.exit(f"Error reading file: {e}")

    # Determine which API to use based on provided environment variables
    if options.token and options.url:
        # Use JSON RPC API
        if 'jsonrpc.php' not in options.url:
            if not options.url.endswith('/'):
                options.url += '/'
            options.url += 'lib/exe/jsonrpc.php'
        upload_using_json_api(options.url, options.token, filename, file_content)
    elif options.url and options.username and options.password:
        # Fall back to XML RPC API
        if 'xmlrpc.php' not in options.url:
            if not options.url.endswith('/'):
                options.url += '/'
            options.url += 'lib/exe/xmlrpc.php'
        upload_using_xml_rpc(options.url, options.username, options.password, filename, file_content)
    else:
        sys.exit("Error: Insufficient credentials provided for either JSON RPC or XML RPC API.")


if __name__ == "__main__":
    main()