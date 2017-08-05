Python client library for Telerivet REST API

http://telerivet.com/api

Overview:
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

All API methods are fully documented at http://telerivet.com/api/rest/python ,
as well as in the comments of the Python source files.

To learn what functionality is available, start with telerivet/__init__.py, 
telerivet/project.py, and telerivet/apicursor.py .

System Requirements:
--------------------
Python 2.6 or higher (including Python 3)
Python Requests module - <http://docs.python-requests.org/en/latest/>

Installation:
-------------

Make sure the Requests module is installed:
http://docs.python-requests.org/en/latest/user/install/#install

You can either embed the 'telerivet' directory directly in your Python package, 
or install the library into your site-packages by running:

python setup.py install

Example Usage:
--------------

```python
from __future__ import print_function # python 2/3 compatibility for example code

import telerivet
   
API_KEY = 'YOUR_API_KEY'  # from https://telerivet.com/api/keys
PROJECT_ID = 'YOUR_PROJECT_ID'

tr = telerivet.API(API_KEY)

project = tr.initProjectById(PROJECT_ID)
```

# Send a SMS message

```python
project.sendMessage(
    to_number = '555-0001',
    content = 'Hello world!'
)
```

# Query contacts

```python
name_prefix = 'John';
cursor = project.queryContacts(
    name = {'prefix': name_prefix},
    sort = 'name'
).limit(20)

print("%d contacts matching %s:\n" % (cursor.count(), name_prefix))

for contact in cursor:
    print(contact.name, contact.phone_number, contact.vars.birthdate)
```

# Import a contact

```python
contact = project.getOrCreateContact(
    name = 'John Smith',
    phone_number = '555-0001',
    vars = {
        'birthdate': '1981-03-04',
        'network': 'Vodacom'
    }
)
```

# Add a contact to a group    

```python
group = project.getOrCreateGroup('Subscribers')
contact.addToGroup(group)
```