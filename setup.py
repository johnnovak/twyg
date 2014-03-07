from setuptools import setup

setup(name='twyg',
      version='0.1',
      description='Scriptable tree visualisatino for Python',
      long_description=open('README.rst').read(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Graphics :: Visualisation'
      ],
      keywords='tree graph visualisation layout nodebox',
      url='http://www.johnnovak.net/twyg/',
      author='John Novak',
      author_email='john@johnnovak.net',
      license='BSD',
      packages=['twyg'],
      install_requires=[],
      include_package_data=True,
      entry_points = {
        'console_scripts': ['twyg=twyg.cmdline:main']
      },
      zip_safe=False)
