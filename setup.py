from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='dih',
    version='0.0.1.1',
    packages=['src'],
    python_requires='>=3.8',
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'dih = src.main:main',
        ],
    },
)