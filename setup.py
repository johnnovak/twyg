#!/usr/bin/env python

from setuptools import setup

setup(name='twyg',
      version='0.1',
      description='Generative tree visualiser for Python',
      long_description=open('README.md').read(),

      classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',

        'Environment :: Console',
        'Environment :: Other Environment',

        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',

        'Topic :: Artistic Software',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Software Development :: Libraries :: Python Modules'
      ],

      keywords='tree graph visualisation generative graphics layout
      nodebox cairo pdf png postscript svg',
      url='http://www.johnnovak.net/twyg/',
      author='John Novak',
      author_email='john@johnnovak.net',
      license='MIT',

      packages=['twyg'],
      include_package_data=True,

      install_requires=['cairo'],

      entry_points = {
        'console_scripts': ['twyg=twyg.cmdline:main']
      },

      zip_safe=False
)

