from setuptools import setup


install_requires = [
    'requests==2.9.1',
    'schematics==1.1.1',
]

setup(
    name='python-stockfighter',
    version='0.0.2',
    packages=['stockfighter'],
    install_requires=install_requires,
    include_package_data=True,
    author='github.com/akshaynanavati',
    author_email='akshay.nanavati1@gmail.com',
    license='Apache License 2.0',
    description='A stockfighter Python API',
    long_description='',
    url='https://github.com/akshaynanavati/python-stockfighter',
    scripts=['bin/sfrepl.py'],
)
