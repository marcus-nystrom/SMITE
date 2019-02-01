from setuptools import setup

setup(
    name='SMITE',
    url='https://github.com/marcus-nystrom/SMITE',
    author='Marcus Nystrom',
    author_email='marcus.nystrom@humlab.lu.se',
    packages=['smite'],
    install_requires=['psychopy', 'tobii-research'],
    version='0.1',
    license='Creative Commons Attribution 4.0 (CC BY 4.0)',
    description='SMITE is a toolbox for using eye trackers from SMI GmbH with Python, specifically offering integration with PsychoPy',
    long_description=open('README.md').read(),
)