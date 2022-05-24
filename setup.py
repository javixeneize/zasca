from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read()

__version__ = "1.0.0"

setup(
    name="yasca",
    version=__version__,
    description="Yet Another SCA tool",
    author="Javier Dominguez",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'yasca=yasca.main:run_cli',
        ],
    },
    install_requires=requirements,
)
