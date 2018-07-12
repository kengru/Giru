import io
import os

from setuptools import find_packages, setup

# Package meta-data.
NAME = 'giru'
DESCRIPTION = 'An only Spanish talking telegram bot.'
URL = 'https://github.com/kengru/Giru'
EMAIL = ''
AUTHOR = 'kengru'
REQUIRES_PYTHON = '==3.5'
VERSION = '1.0.0'
LICENSE = 'MIT'

here = os.path.abspath(os.path.dirname(__file__))

# What packages are required for this module to be executed?
REQUIRED = []
try:
    with io.open(os.path.join(here, 'requirements.txt'), encoding='utf-8') as f:
        REQUIRED.extend(f.readlines())
except FileNotFoundError:
    pass

# What packages are optional?
EXTRAS = {
    'testing': ['nose', 'coverage', 'python-coveralls'],
}

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    with open(os.path.join(here, NAME, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION

# Where the magic happens:
setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    # long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    # python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=('tests',)),
    package_data={'giru': ['res/*']},
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython'
    ],
)
