from setuptools import setup, find_packages

VERSION = '0.0.1'

setup_info = dict(
    name='tim_smpplib',
    version=VERSION,
    url='https://github.com/timconnect/tim_smpplib',
    description='SMPP library for Python3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Communications :: Telephony',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Telecommunications Industry',
    ],
    packages=find_packages(),
    zip_safe=True,
)

setup(**setup_info)
