import os
import sys
from setuptools import setup

tests_require = ["unittest2"]

base_dir = os.path.dirname(os.path.abspath(__file__))

version = "0.2.0"

setup(
    name = "app",
    version = version,
    description = "A python flask app for Imperial Genomics Facility",
    url = "https://github.com/imperial-genomics-facility/Metadata_validation",
    author = "Avik Datta",
    author_email = "reach4avik@yahoo.com",
    maintainer = "Avik Datta",
    maintainer_email = "reach4avik@yahoo.com",
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing',
    ],
    packages = ["app"],
    zip_safe = False,
    tests_require = tests_require,
    test_suite = "test.get_tests",
)
