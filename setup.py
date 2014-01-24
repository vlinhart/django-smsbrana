#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup, find_packages
except ImportError:
    import ez_setup
    ez_setup.use_setuptools()
    from setuptools import setup, find_packages
    
import os

setup(
    name = "django-smsbrana",
    version = "0.2",
    url = 'https://github.com/vlinhart/django-smsbrana',
    download_url = 'https://github.com/vlinhart/django-smsbrana/downloads',
    license = 'BSD',
    description = "Django app to ease smsbrana.cz smsconnect integration.",
    author = 'Vladimir Linhart',
    author_email = 'vladimir.linhart@gmail.com',
    packages = find_packages(),
    include_package_data = True,
    zip_safe = False,
    install_requires = ['requests',],
    classifiers = [
        'Development Status :: Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
