from setuptools import setup

setup(name='soda-python',
      version='0.1',
      description='Wittkuhn & Schuck (2021) implementation to detect fast sequences in fMRI',
      long_description_content_type="text/markdown",
      url='http://github.com/skjerns/SODA-Python',
      author='skjerns',
      author_email='nomail@nomail.com',
      license='GPLv4',
      packages=['soda'],
      zip_safe=False,
      classifiers=[
          "Programming Language :: Python :: 3",
          "Operating System :: OS Independent",
      ],)
