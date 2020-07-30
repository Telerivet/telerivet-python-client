## Python client library for Telerivet REST API

https://telerivet.com/api

Overview
---------
This library makes it easy to integrate your Python application with Telerivet.
You can use it to:

- send SMS messages via an Android phone or SMS gateway service
- update contact information in Telerivet (e.g. from a signup form on your own website)
- add or remove contacts from groups
- export your message/contact data from Telerivet into your own systems
- schedule messages to be sent at a later time
- control automated services
- much more

All API methods are fully documented at https://telerivet.com/api/rest/python ,
as well as in the comments of the Python source files.

To learn what functionality is available, start with `telerivet/__init__.py`,
`telerivet/project.py`, and `telerivet/apicursor.py`.

System Requirements
--------------------
Python 2.6 or higher (including Python 3)

Installation
-------------

Telerivet's Python client library is distributed via `pip` (https://pypi.org/project/telerivet/). If you have `pip`, run:

`pip install telerivet`

Alternatively, if you don't have `pip`, you can install the install the library into your site-packages by downloading the code and running:

`python setup.py install`

The installation process will also install the `requests` module if it is not already installed (https://requests.readthedocs.io/).

Example Usage
--------------
```
from __future__ import print_function # python 2/3 compatibility for example code

import telerivet

API_KEY = 'YOUR_API_KEY'  # from https://telerivet.com/api/keys
PROJECT_ID = 'YOUR_PROJECT_ID'

tr = telerivet.API(API_KEY)

project = tr.initProjectById(PROJECT_ID)

# Send a SMS message
project.sendMessage(
    to_number = '555-0001',
    content = 'Hello world!'
)

# Query contacts
name_prefix = 'John';
cursor = project.queryContacts(
    name = {'prefix': name_prefix},
    sort = 'name'
).limit(20)

print("%d contacts matching %s:\n" % (cursor.count(), name_prefix))

for contact in cursor:
    print(contact.name, contact.phone_number, contact.vars.birthdate)

# Import a contact
contact = project.getOrCreateContact(
    name = 'John Smith',
    phone_number = '555-0001',
    vars = {
        'birthdate': '1981-03-04',
        'network': 'Vodacom'
    }
)

# Add a contact to a group
group = project.getOrCreateGroup('Subscribers')
contact.addToGroup(group)
```