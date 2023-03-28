#!/usr/bin/env python
import setuptools
from acelink_server._version import __version__

with open('./requirements.txt') as f:
    install_requires = f.read().strip().split('\n')

with open("./README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='acelink_server',
    version=__version__,
    description='Manages acestream connections',
    url='http://',
    author='ibanez.j@gmail.com',
    author_email='ibanez.j@gmail.com',
    license="MIT License",
    long_description= long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'get_netconf = netconf_gatherer.netconf_controller:main'
            ],
    }
)
