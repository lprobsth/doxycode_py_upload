#!/usr/bin/env python3

import sys
import os
from optparse import OptionParser
from dokuwikixmlrpc import DokuWikiClient
import xmlrpc.client as xmlrpclib

def main():
    parser = OptionParser(usage="usage: %prog filename")
    parser.add_option("-d", "--domain", dest="domain", help="DokuWiki domain URL", default=os.environ.get('DOKUWIKI_DOMAIN'))
    parser.add_option("-u", "--user", dest="user", help="DokuWiki username", default=os.environ.get('DOKUWIKI_USER'))
    parser.add_option("-p", "--password", dest="password", help="DokuWiki password", default=os.environ.get('DOKUWIKI_PASSWORD'))

    (options, args) = parser.parse_args()

    # Check if filename is provided
    if len(args) != 1:
        parser.error("Filename must be provided")

    filename = args[0]

    # Check if all environment variables are set
    if not options.domain or not options.user or not options.password:
        sys.exit("Error: DokuWiki domain, user, or password not set. Please set environment variables.")

    # Initialize the DokuWiki client
    dw = DokuWikiClient(options.domain, options.user, options.password)

    try:
        # Open the file
        with open(filename, "rb") as in_file:
            data = in_file.read()

        # Upload file
        response = dw._xmlrpc.doxycode.uploadTagFile(filename, xmlrpclib.Binary(data))

        # Check response and exit accordingly
        if response[0]:
            print("Upload successful.")
            sys.exit(0)
        else:
            print("Upload failed.")
            sys.exit(2)

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(3)

if __name__ == "__main__":
    main()
