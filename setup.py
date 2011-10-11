from setuptools import setup

package = 'csv-diff'
version = '0.1'

setup_requires = []

try:
    import argparse
except ImportError:
    setup_requires.append('argparse')

setup(name=package, version=version,
      description="show differences between csv files",
      setup_requires=setup_requires,
      install_requires=setup_requires,
      test_suite="test",
      scripts=['csv_diff.py'],
      author='Andrea Crotti', author_email='andrea.crotti.0@gmail.com',
      url='url'
)
