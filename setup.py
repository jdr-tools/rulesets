import io, sys

from setuptools import find_packages, setup

with io.open('README.rst', 'rt', encoding='utf8') as f:
  readme = f.read()

setup(
  name='virtuatable-rulesets',
  version='0.1.0',
  url='http://flask.pocoo.org/docs/tutorial/',
  license='BSD',
  maintainer='Vincent Courtois',
  maintainer_email='courtois.vincent@outlook.com',
  description='The service to create, update, get or delete rule sets for any tabletop RPG',
  long_description=readme,
  packages=find_packages(),
  include_package_data=True,
  zip_safe=False,
  install_requires=[
    'flask',
  ],
  extras_require={
    'test': [
      'pytest',
      'coverage',
    ],
  },
)