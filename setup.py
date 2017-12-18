from distutils.core import setup
from setuptools import setup, find_packages

with open('Readme.md') as f:
      long_description = ''.join(f.readlines())

setup(name='Schrodinger',
      version='0.0.1',
      description='Solution to the Schrodinger Equation',
      author='Heta Gandhi',
      author_email='hgandhi@ur.rochester.edu',
      packages=find_packages(),
      entry_points = 
      {
            'console_scripts': ['solver=SEq.seq:main']
      }
      )