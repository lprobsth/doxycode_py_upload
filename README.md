# Python Script for Uploading Doxygen Tag Files from CI/CD Pipelines to The Dokuwiki Doxygen Plugin

The doxycode dokuwiki plugin lets users create code snippets in dokuwiki that are cross referenced to external doxygen documentations (see http://www.dokuwiki.org/plugin:doxycode).

The keywords in the code snippets are matched using doxygen tag files that can be genererated when building a doxygen documentation (see https://www.doxygen.nl/manual/external.html).

This script can be used for uploading these tag files from a CI/CD pipeline that builds the doxygen documentation.
This is especially useful when the resulting doxygen documentation (and therefore also the tag file) is not publicly available.

## Technical Background

Doxycode implements a remote component with a method for uploading files to the tag file directory.
It can be used through the dokuwiki remote APIs:
- XML RPC API (all dokuwiki versions; after Jack Jackrum the lagacy API is used)
- JSON RPC API (dokuwiki version > Jack Jackrum)

Newer dokuwiki versions can use both the XML RPC API and the JSON RPC API.
The user of this script decides which API will be used by either providing credentials for token authentication (JSON RPC API only) or username/password authentication (XML RPC API only).


## Usage

`./doxycode_py_upload/upload_tag_file.py docs/tagname.xml`

The credentials can be either passed through environment variables (default) or command line arguments.
Using environment variables is encouraged since this decreases the probability of accidentally leaking the authentication secrets in the CI/CD pipeline.

| Environment Variable | Argument        | Description                                                       | API      |
|----------------------|-----------------|-------------------------------------------------------------------|----------|
| DOKUWIKI_DOMAIN      | -u / --url      | URL to the Dokuwiki instance (e.g. 'https://wiki.your-domain.com/ |          |
| DOKUWIKI_API_TOKEN   | -t / --token    | Dokuwiki API token.                                               | JSON RPC |
| DOKUWIKI_USER        | -n / --username | Dokuwiki username of the remote user.                             | XML RPC  |
| DOKUWIKI_PASSWORD    | -p / --password | Password of the Dokuwiki user.                                    | XML RPC  |
