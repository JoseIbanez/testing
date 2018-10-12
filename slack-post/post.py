#!/usr/bin/env python

import os
from slackclient import SlackClient

slack_token = os.environ["SLACK_API_TOKEN"]
sc = SlackClient(slack_token)

#print sc.api_call(
#    "channels.list",
#    exclude_archived=1
#)

sc.api_call(
    "chat.postMessage",
    channel="varios",
    text="Hello from Python! :tada:",
    attachments=[{"pretext": "hi" ,
                  "text": "long *text* here\n line 2\n line3"}]

)

