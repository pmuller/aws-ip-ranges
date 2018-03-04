from os.path import join, dirname

from setuptools import setup, find_packages


def read(filename):
    with open(join(dirname(__file__), filename)) as fileobj:
        return fileobj.read()


def get_version(package):
    return [
        line for line in read('{}/__init__.py'.format(package)).splitlines()
        if line.startswith('__version__ = ')][0].split("'")[1]


PROJECT_NAME = 'aws-ip-ranges'
VERSION = get_version('aws_ip_ranges')


setup(
    name=PROJECT_NAME,
    version=VERSION,
    description='Retrieves and processes AWS IP ranges data.',
    author='Philippe Muller',
    author_email='philippe.muller@gmail.com',
    url='https://github.com/pmuller/aws-ip-ranges',
    packages=find_packages(exclude=['tests']),
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, <4',
    install_requires=[
        'netaddr >=0.7.19',
        'PyYAML >=3.12',
        'requests >=2.18.4',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: System :: Networking',
        'Intended Audience :: System Administrators',
    ],
    entry_points="""
        [console_scripts]
        aws-ip-ranges = aws_ip_ranges.cli:main
    """,
    license='Apache License 2.0',
)
