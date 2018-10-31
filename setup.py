from setuptools import setup

setup(
    name='BirthdayBot',
    version='0.1.0',
    packages=['birthday'],
    entry_points={
        'console_scripts': [
            'BirthdayBot=birthday.main:main'
        ]
    }
)
