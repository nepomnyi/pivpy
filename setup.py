import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "PIVPy",
    version = "0.0.002",
    author = "Ron Shnapp, Tomer Ast, Alex Liberzon",
    author_email = "ronshnapp@gmail.com",
    description = ("Post processing of PIV vector files "
                                   " eventually going into OpenPIV "),
    license = "BSD",
    keywords = "example documentation tutorial",
    url = "http://packages.python.org/pivpy",
    packages=['pivpy', 'tests'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
