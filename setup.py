from distutils.core import setup

version = '0.1.0'

setup(
    name='django-test-generator',
    version=version,
    description='A set of mixins to automatically generate test for generic Django views and DRF Viewsets.',
    url='https://github.com/aipescience/django-test-generator',
    author='Jochen Klar',
    author_email='jklar@aip.de',
    maintainer=u'AIP E-Science',
    maintainer_email=u'escience@aip.de',
    license=u'Apache License (2.0)',
    packages=['test_generator'],
    download_url='https://github.com/aipescience/django-test-generator/archive/%s.tar.gz' % version,
    keywords=['testing', 'django'],
    classifiers=[],
)
