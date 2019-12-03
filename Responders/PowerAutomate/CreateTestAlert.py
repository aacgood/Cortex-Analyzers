#!/usr/bin/env python
# encoding: utf-8

import uuid
import json
import requests

uid = str(uuid.uuid4())
theHiveURL = '<YOUR HIVE API ENDPOINT>/api/alert'

headers = {
    'Authorization': 'Bearer <API KEY>',
    'Content-Type': 'application/json'
}

data = {
    "title": "test alert - Phishing email",
    "description": "generic alert description in here",
    "type": "Python generated",
    "source" : "email",
    "tags" : ["test1"],
    "artifacts": [
        { "dataType": "other", "data": "Phishing Email", "message": "use_case" },
        { "dataType": "mail_subject", "data": "Sample email subject!", "message": "email_subject" },
        { "dataType": "other", "data": "adrian@agood.cloud", "message": "dst" },
        { "dataType": "other", "data": "themalicious1@somel33tr4nd0mhaxx0rdomain.com", "message": "src" }
    ],
    "sourceRef": uid
}

r = requests.post(theHiveURL, data=json.dumps(data), headers=headers)

print(r.status_code)
print(r.content)
