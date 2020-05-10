"""
Based on https://github.com/pypa/sampleproject/blob/master/setup.py

Created 9 May 2020

@author: patricktoche
"""

# Get path
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='GDLC',  # Required
    version='0.0.1',  # Required
    description='Python module to edit mobi source files for the GDLC (Kindle edition).',  # Optional
    # long_description=long_description,  # Optional
    # long_description_content_type='text/markdown',  # Optional 
    url='https://github.com/ptoche/GDLC',  # Optional
    author='Patrick Toche',  # Optional
    author_email='ptoche@gmail.com',  # Optional
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Catalan readers who own a Kindle Paperwhite and the GDLC Kindle ebook',
        'Topic :: Kindle Lookup Dictionary for Catalan Language',

        # Specify the project license
        'License :: OSI Approved :: BSD 3',

        # Specify the Python versions you support 
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',

        # Specify the Operating systems you support
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
    ],

    # This field adds keywords for your project 
    keywords='kindle dictionary mobi azw calibre kindleunpack kindlegen',  # Optional

    # When your source code is in a subdirectory under the project root, e.g.
    # `src/`, it is necessary to specify the `package_dir` argument.
    # package_dir={'': 'src'},  # Optional

    # You can just specify package directories manually here
    packages=find_packages(where='.', exclude=()),  # Required

    # Specify which Python versions you support. 
    python_requires='>=3.5, <4',  # Required

    # This field lists other packages that your project depends on to run.
    install_requires=['os', 're', 'BeautifulSoup >= 4.9.0'],  # Optional

    # List additional groups of dependencies here.
    # extras_require={},  # Optional

    # List data files included in your packages.
    # package_data={},  # Optional

    # To provide executable scripts, use entry points. 
    # entry_points={  # Optional
    #     'console_scripts': [
    #         'sample=sample:main',
    #     ],
    # },

    # List additional URLs that are relevant to your project as a dict.
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/ptoche/GDLC',
    #    'Funding': 'https://donate.pypi.org',
    #    'Say Thanks!': 'http://saythanks.io/to/example',
        'Source': 'https://github.com/ptoche/GDLC',
    },
)
