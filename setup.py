import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-emailuser',
    version='0.1',
    packages=['emailuser'],
    include_package_data=True,
    license='BSD License',  # example license
    description='Djano email-based users.',
    long_description=README,
    url='https://github.com/rpkilby/django-emailuser/',
    author='Ryan P Kilby',
    author_email='rpkilby@ncsu.edu',
    keywords="django emailuser email-based user",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
