from setuptools import setup, find_packages

VERSION = '1.0.1a' 
DESCRIPTION = 'An API wrapper for ShinyDB'
LONG_DESCRIPTION = 'Just an API wrapper for ShinyDB server. So cool!'
requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()
# Setting up
setup(
        name="ShinyPy", 
        version=VERSION,
        author="RyZeDZ",
        author_email="<cuzimkamel@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=requirements,
        keywords=['python'],
        classifiers= [
            "Programming Language :: Python :: 3",
        ]
)