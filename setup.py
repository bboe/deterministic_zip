"""deterministic_zip setup.py."""
import re
from codecs import open
from os import path
from setuptools import setup


PACKAGE_NAME = 'deterministic_zip'
HERE = path.abspath(path.dirname(__file__))
with open(path.join(HERE, 'README.md'), encoding='utf-8') as fp:
    README = fp.read()
with open(path.join(HERE, PACKAGE_NAME, '__init__.py'),
          encoding='utf-8') as fp:
    VERSION = re.search("__version__ = '([^']+)'", fp.read()).group(1)


setup(name=PACKAGE_NAME,
      author='Bryce Boe',
      author_email='bbzbryce@gmail.com',
      classifiers=[
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python :: 3.7'],
      description='A program to create deterministic zip files.',
      entry_points={'console_scripts': ['{0} = {0}:main'
                                        .format(PACKAGE_NAME)]},
      keywords='aws lambda zip',
      license='Simplified BSD License',
      long_description=README,
      long_description_content_type='text/markdown',
      packages=[PACKAGE_NAME],
      url='https://github.com/bboe/deterministic_zip',
      version=VERSION)
