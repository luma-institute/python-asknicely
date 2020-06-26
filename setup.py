
import setuptools
from setuptools import find_packages

setuptools.setup(
     name='asknicely',  
     version='1.0',
     author="Max Gelman",
     author_email="max@luma-institute.com",
     description="Simple SDK for AskNicely",
     url="https://github.com/luma-institute/python-asknicely",
     packages=find_packages(exclude=['tests*']),
     install_requires=[
          'requests',
     ],
     classifiers=[
         "Programming Language :: Python :: 3",
         "Operating System :: OS Independent",
     ],

 )
