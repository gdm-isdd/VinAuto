from setuptools import setup, find_packages

setup(
    name='VinAuto',
    version='1.0',
    description='A Python tool for virtual screening using VINA',
    author='Gabriele De Marco',
    author_email='gabriele.demarco.isdd@gmail.com',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'rdkit', 
        'wheel',
        'setuptools',
        'openpyxl'
        # Or the appropriate RDKit package name
        # Add dependencies for file conversion and external process handling
    ],
    entry_points={
        'console_scripts': [
            'vinauto=virtual_screening.clip:main',
        ],
    },
)
