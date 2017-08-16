from setuptools import setup, find_packages

from test_generator import (
    __title__ as title,
    __version__ as version,
    __author__ as author,
    __license__ as license
)

description = 'A set of mixins to automatically generate test for generic Django views and DRF Viewsets.'
email = 'jklar@aip.de'
url = 'https://github.com/aipescience/django-test-generator'

requirements = [
    'Django>=1.8'
]

keywords = [
    'testing',
    'django'
]

classifiers = []

setup(
    name=title,
    version=version,
    description=description,
    url=url,
    author=author,
    author_email=email,
    maintainer=author,
    maintainer_email=email,
    license=license,
    packages=find_packages(),
    install_requires=requirements,
    keywords=keywords,
    classifiers=classifiers
)
