#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Django>=1.11,<2.1',
    'djangorestframework>=3.6,<4',
    'djangorestframework-jsonapi>=2.4,<3',
    'attrs>=17.2.0',
    'coreapi>=2.3',
    'Markdown>=2.6',
    'Pygments>=2.2',
]

setup_requirements = ['pytest-runner', ]

test_requirements = [
    'pytest',
    'pytest-django',
]

setup(
    author="Thorgate",
    author_email='code@thorgate.eu',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    description="Opinionated API framework on top of Django REST framework",
    install_requires=requirements,
    license="ISC license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='tg-apicore django djangorestframework',
    name='tg-apicore',
    packages=find_packages(include=['tg_apicore']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/thorgate/tg-apicore',
    version='0.3.0',
    zip_safe=False,
)
