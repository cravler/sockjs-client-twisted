# -*- coding: utf-8 -*-
"""
SockJS-Client-Twisted
-------------

SockJS client for Twisted-Python
"""
from setuptools import setup

setup(
    name='txsockjs_client',
    version='0.1.0',
    url='http://github.com/cravler/sockjs-client-twisted/',
    license='MIT',
    author='Sergei Vizel',
    author_email='sergei.vizel@gmail.com',
    description='SockJS client for Twisted-Python',
    long_description=__doc__,
    py_modules=['txsockjs_client'],
    packages=['txsockjs_client'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Twisted', 'autobahn[twisted]==0.10.2'
    ],
    classifiers=[
        "Framework :: Twisted",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet",
    ]
)