#!/usr/bin/python


from setuptools import setup

from jindo.__init__ import __version__ as VERSION



setup(name="jindo",
    license = "GPL-2",
    version=VERSION,
    description="Command-line tool and library for (mt) API",
    long_description=open("README", "r").read(),
    maintainer="Rob Cakebread",
    author="Rob Cakebread",
    author_email="rcakebread at mediatemple.net",
    url="http://localhost/jindo/",
    keywords="API mt",
    classifiers=["Development Status :: 3 - Alpha",
                 "Intended Audience :: Developers",
                 "License :: OSI Approved :: GNU General Public License (GPL)",
                 "Programming Language :: Python",
                 "Topic :: Software Development :: Libraries :: Python Modules",
                 ],
    install_requires=["setuptools"],
    tests_require=["nose"],
    packages=['jindo'],
    package_dir={'jindo':'jindo'},
    entry_points={'console_scripts': ['jindo = jindo.cli:main',]},
    test_suite = 'nose.collector',
)

