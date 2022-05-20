from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read()

setup(
    name="yasca",
    version='0.0.1',
    description="Yet Another SCA tool",
    author="Javier Dominguez",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'yasca-cli=yasca.main:run_cli',
        ],
    },
    install_requires=requirements,
)
