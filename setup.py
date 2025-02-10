from setuptools import setup, find_packages


setup(
    name='xmlbind',
    description='A xml decorator package.',
    version='0.0.4',
    install_requires=[
        'lxml==5.3.0'
    ],
    packages=find_packages(),
    # package_dir={'spherical_functions': '.'},
    # data_files=[('lenexdb', ['FINA_Points_Table_Base_Times.xlsx'])]
)
