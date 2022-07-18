#!/usr/bin/env python

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='telerivet',
      version='1.6.1',
      description='Python client library for Telerivet REST API',
      author='Telerivet, Inc.',
      author_email='support@telerivet.com',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='http://telerivet.com/',
      packages=['telerivet'],
      python_requires='>=2.6',
      install_requires=[
        "requests >= 2.4.0",
      ],
      classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
      ]
     )
