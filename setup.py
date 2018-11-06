import re

from setuptools import setup, find_packages

with open('test_generator/__init__.py') as f:
    metadata = dict(re.findall(r'__(.*)__ = [\']([^\']*)[\']', f.read()))

setup(
    name=metadata['title'],
    version=metadata['version'],
    author=metadata['author'],
    author_email=metadata['email'],
    maintainer=metadata['author'],
    maintainer_email=metadata['email'],
    license=metadata['license'],
    url='https://github.com/aipescience/django-test-generator',
    description=u'A set of mixins to automatically generate test for generic Django views and DRF Viewsets.',
    long_description=open('README.md').read(),
    packages=find_packages(),
    install_requires=[
        'Django>=1.11'
    ],
    keywords=[
        'testing',
        'django'
    ],
    classifiers=[]
)
