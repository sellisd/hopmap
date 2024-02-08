from setuptools import setup, find_packages

setup(
    name='hopmap',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'click',
        'cartopy',
        'scapy',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'hopmap=hopmap.hopmap:plot',
        ],
    },
)