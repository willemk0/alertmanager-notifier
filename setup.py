import os
import sys

from setuptools import setup, find_packages
import sysconfig

full_path = sysconfig.get_paths()["purelib"]
relative_path = sysconfig.get_paths()["data"]
icon_path =  os.path.relpath(full_path, relative_path)

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="alertmanager_notify",
    version='0.2.0',
    description="Alertmanager notification",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/willemk0/alertmanager-notify",
    author="Willem Kalandrijn",
    packages=['alertmanager_notify'],
    install_requires=[
        'requests',
        'notify-py',
        'pyxdg>=0.22'
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],    
	keywords=['Alertmanager'],
    entry_points={"console_scripts": ["alertmanager-notify = alertmanager_notify.alertmanager_notify:main"]},
    include_package_data=True,
    package_dir={"alertmanager_notify": "src"},
    data_files=[
        (icon_path + "/alertmanager_notify/icons", [
            'icons/alertmanager.ico',
            'icons/prometheus_logo_grey.png',
            'icons/prometheus_logo_grey.svg'
            ]
        )
    ]
)
