from setuptools import setup, find_packages

setup(
    name='nasa_neows_assignment',
    version='0.1.0',
    author='MENGYI MERYL FANG',
    author_email='mfang@wellesley.edu',
    description='nasa neows assignment',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Meryl-Fang/nasa-neows-assignment',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'pyyaml',
        'matplotlib'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11.0',
)
