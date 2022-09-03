from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read()

__version__ = "2.0.0"

setup(
    name="zasca",
    version=__version__,
    description="Yet Another SCA tool, but with Z",
    author="Javier Dominguez",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'zasca=zasca.main:run_cli',
        ],
    },
    install_requires=requirements,
)
