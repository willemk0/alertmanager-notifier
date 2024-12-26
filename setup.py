from setuptools import setup, find_packages


#setup(
#    name="alertmanager-notify",
#    version="0.1",
#    packages=find_packages(),
#)
#
#_import__("setuptools").setup()

import setuptools

setup(
    name="alertmanager-notify",
    version='0.1.2',
    description="Alertmanager notification",
    url="https://github.com/willemk0/alertmanager-notify",
    author="Willem Kalandrijn",
    packages=find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],    
	keywords=['Alertmanager'],
    package_dir={"": "src"},
    install_requires=[
        'requests',
        'notify-py'
    ],
    scripts=['src/alertmanager-notify.py'],
    package_data={
        'alertmanager-notify': ['icons/alertmanager.svg'],
    },
)
