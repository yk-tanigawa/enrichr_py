# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='enrichr_py',
    version='0.0.1',
    description='A simple package for Enrichr Python API',
    long_description=readme,
    author='Yosuke Tanigawa',
    author_email='info@yosuketanigawa.com',
    install_requires=['numpy', 'requests'],
    url='https://yosuketanigawa/software/enrichr_py',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

