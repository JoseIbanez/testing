#!/usr/bin/env python

"""
	Upload a photo to Twitter
	-----------------------------------------------------------------
	
	Run this command line script with any Twitter endpoint.  The json-formatted
	response is printed to the console.  The script works with both Streaming API and
	REST API endpoints.

	IMPORTANT: Before using this script, you must enter your Twitter application's OAuth
	credentials in TwitterAPI/credentials.txt.  Log into http://dev.twitter.com to create
	your application.
	
	Examples:

	::
	
		python cli -endpoint search/tweets -parameters q=zzz
		python cli -endpoint statuses/filter -parameters track=zzz
		
	These examples print the raw json response.  You can also print one or more fields
	from the response, for instance the tweet 'text' field, like this:
	
	::
	
		python cli -endpoint statuses/filter -parameters track=zzz -fields text
		
	Documentation for all Twitter endpoints is located at:
		 https://dev.twitter.com/docs/api/1.1
"""


__author__ = "ibanez.j@gmail.com"
__date__ = "July 4, 2017"
__license__ = "MIT"


from TwitterAPI import TwitterAPI, __version__
#from TwitterAPI import TwitterAPI
from TwitterAPI.TwitterOAuth import TwitterOAuth
import argparse
#import codecs
#import json
#import sys
from os.path import expanduser



if __name__ == '__main__':
    print('TwitterAPI %s by geduldig' % __version__)

    parser = argparse.ArgumentParser(
        description='Request any Twitter Streaming or REST API endpoint')
    parser.add_argument(
        '-oauth',
        metavar='FILENAME',
        type=str,
        help='file containing OAuth credentials',
        default=expanduser("~/.secrets/twitter"))
    parser.add_argument(
        '-file',
        metavar='FILENAME',
        type=str,
        help='image to upload',
        required=True)
    parser.add_argument(
        '-text',
        metavar='NAME_VALUE',
        type=str,
        help='text to send',
        default='My picture')
    args = parser.parse_args()

    try:
        oauth = TwitterOAuth.read_file(args.oauth)

        file = open(args.file, 'rb')
        data = file.read()
        file.close()

        api = TwitterAPI(oauth.consumer_key,
                         oauth.consumer_secret,
                         oauth.access_token_key,
                         oauth.access_token_secret)

        r = api.request('statuses/update_with_media', {'status':args.text}, {'media[]':data})
        print(r.status_code)


    except KeyboardInterrupt:
        print('Terminated by user')

    except Exception as e:
        print('STOPPED: %s' % e)




