from distutils.core import setup

with open('Readme.md') as f:
      long_description = ''.join(f.readlines())

setup(name='Schrodinger',
      version='0.1',
      description='Solution to the Schrodinger Equation',
      author='Heta Gandhi',
      author_email='hgandhi@ur.rochester.edu',
      packages=['SEq'],
      entry_points = 
      {
            'console_scripts': ['solve=SEq.seq:main']
      }
      )
     